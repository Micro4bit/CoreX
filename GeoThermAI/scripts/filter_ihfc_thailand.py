#!/usr/bin/env python3
"""Create a provenance-preserving Thailand IHFC audit extract.

The source workbook is read directly from OOXML so the pipeline does not
rewrite it. Points are classified with a documented Natural Earth polygon;
duplicate coordinates remain separate measurement rows.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterator
from xml.etree.ElementTree import iterparse
from zipfile import ZipFile

import geopandas as gpd
from shapely import prepare
from shapely.geometry import Point, mapping


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKBOOK = ROOT / "tasks/phase_1_data_acquisition_label_validation/IHFC_2024_GHFDB.xlsx"
DEFAULT_BOUNDARY = ROOT / "tasks/phase_2d_data_readiness/source/ne_10m_admin_0_countries.zip"
DEFAULT_OUTPUT = ROOT / "tasks/phase_2d_data_readiness/derived/ihfc_thailand_qc.csv"
DEFAULT_SUMMARY = ROOT / "tasks/phase_2d_data_readiness/derived/ihfc_thailand_qc_summary.json"
DEFAULT_BOUNDARY_OUTPUT = ROOT / "tasks/phase_2d_data_readiness/derived/thailand_boundary_ne10m.geojson"
DEFAULT_MAP_OUTPUT = ROOT / "web/public/data/ihfc-thailand-points.geojson"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REGIONAL_BOUNDS = (97.0, 5.0, 106.0, 21.0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_label(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def column_index(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference)
    if not letters:
        raise ValueError(f"Invalid cell reference {reference!r}")
    value = 0
    for character in letters.group():
        value = value * 26 + ord(character) - 64
    return value - 1


def shared_strings(archive: ZipFile) -> list[str]:
    values: list[str] = []
    for _, element in iterparse(archive.open("xl/sharedStrings.xml"), events=("end",)):
        if element.tag == NS + "si":
            values.append("".join(node.text or "" for node in element.iter(NS + "t")))
            element.clear()
    return values


def iter_workbook_rows(path: Path) -> Iterator[tuple[int, dict[str, str]]]:
    with ZipFile(path) as archive:
        strings = shared_strings(archive)
        headers: list[str] = []
        for _, row in iterparse(archive.open("xl/worksheets/sheet1.xml"), events=("end",)):
            if row.tag != NS + "row":
                continue
            row_number = int(row.attrib["r"])
            cells: dict[int, str] = {}
            for cell in row.findall(NS + "c"):
                index = column_index(cell.attrib["r"])
                value_node = cell.find(NS + "v")
                value = "" if value_node is None else value_node.text or ""
                if cell.attrib.get("t") == "s" and value:
                    value = strings[int(value)]
                cells[index] = value
            if row_number == 6:
                headers = [cells.get(index, "") for index in range(max(cells) + 1)]
            elif row_number > 6 and headers:
                yield row_number, {header: cells.get(index, "") for index, header in enumerate(headers)}
            row.clear()


def load_thailand_boundary(path: Path):
    frame = gpd.read_file(f"zip://{path}")
    if frame.crs is None or frame.crs.to_epsg() != 4326:
        raise ValueError(f"Expected Natural Earth EPSG:4326, received {frame.crs}")
    matches = frame.loc[frame["ADMIN"] == "Thailand"]
    if len(matches) != 1:
        raise ValueError(f"Expected one Thailand polygon, received {len(matches)}")
    geometry = matches.geometry.iloc[0]
    if geometry.is_empty or not geometry.is_valid:
        raise ValueError("Thailand boundary is empty or invalid")
    return geometry


OUTPUT_FIELDS = [
    "source_row", "ID", "ID_parent", "name", "lat_NS", "long_EW", "spatial_class",
    "coordinate_review_required", "coordinate_review_reason", "duplicate_coordinate_count",
    "q", "q_uncertainty", "q_method", "total_depth_MD", "total_depth_TVD", "elevation",
    "environment", "Domain", "Country", "Region", "publication_reference", "data_reference",
    "q_date", "Review_status", "Quality_Code", "qc", "qc_uncertainty", "water_temperature",
]


def build(
    workbook: Path,
    boundary_path: Path,
    output: Path,
    summary_path: Path,
    boundary_output: Path,
    map_output: Path | None = None,
) -> dict[str, Any]:
    started = time.perf_counter()
    thailand = load_thailand_boundary(boundary_path)
    prepare(thailand)
    rows: list[dict[str, str]] = []
    workbook_row_count = 0
    invalid_coordinate_count = 0

    west, south, east, north = REGIONAL_BOUNDS
    for source_row, record in iter_workbook_rows(workbook):
        workbook_row_count += 1
        try:
            latitude = float(record["lat_NS"])
            longitude = float(record["long_EW"])
        except (KeyError, TypeError, ValueError):
            invalid_coordinate_count += 1
            continue
        if not (west <= longitude <= east and south <= latitude <= north):
            continue
        point = Point(longitude, latitude)
        inside = thailand.covers(point)
        offshore = "offshore" in record.get("environment", "").lower() or record.get("Domain", "").lower() == "marine"
        country = record.get("Country", "").strip()
        if inside:
            spatial_class = "INSIDE_THAILAND_BOUNDARY"
        elif offshore:
            spatial_class = "OFFSHORE_REGIONAL_CONTEXT"
        elif country and country.casefold() != "thailand":
            spatial_class = "NEIGHBORING_COUNTRY"
        else:
            spatial_class = "OUTSIDE_BOUNDARY_REVIEW"
        reasons: list[str] = []
        if inside and country and country.casefold() != "thailand":
            reasons.append("boundary_country_disagreement")
        if not inside and country.casefold() == "thailand":
            reasons.append("country_field_outside_boundary")
        rows.append({
            **{field: record.get(field, "") for field in OUTPUT_FIELDS if field not in {"source_row", "spatial_class", "coordinate_review_required", "coordinate_review_reason", "duplicate_coordinate_count"}},
            "source_row": str(source_row),
            "spatial_class": spatial_class,
            "coordinate_review_required": "true" if reasons else "false",
            "coordinate_review_reason": ";".join(reasons),
        })

    coordinate_counts = Counter((row["lat_NS"], row["long_EW"]) for row in rows)
    for row in rows:
        row["duplicate_coordinate_count"] = str(coordinate_counts[(row["lat_NS"], row["long_EW"])])

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    boundary_output.write_text(json.dumps({
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "properties": {"name": "Thailand", "source": "Natural Earth 1:10m Admin-0 Countries", "license": "Public domain"}, "geometry": mapping(thailand)}],
    }, separators=(",", ":")), encoding="utf-8")

    if map_output is not None:
        map_output.parent.mkdir(parents=True, exist_ok=True)
        map_features = []
        for row in rows:
            if row["spatial_class"] != "INSIDE_THAILAND_BOUNDARY":
                continue
            map_features.append({
                "type": "Feature",
                "id": f"ihfc-source-row-{row['source_row']}",
                "properties": {
                    "sourceRow": int(row["source_row"]),
                    "recordId": row["ID"],
                    "parentId": row["ID_parent"],
                    "name": row["name"],
                    "heatFlowMilliwattsPerSquareMetre": float(row["q"]),
                    "heatFlowUncertainty": row["q_uncertainty"] or None,
                    "heatFlowMethod": row["q_method"] or None,
                    "qualityCode": row["Quality_Code"] or None,
                    "reviewStatus": row["Review_status"] or None,
                    "duplicateCoordinateCount": int(row["duplicate_coordinate_count"]),
                    "publicationReference": row["publication_reference"] or None,
                    "dataReference": row["data_reference"] or None,
                    "totalDepthMd": row["total_depth_MD"] or None,
                    "environment": row["environment"] or None,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(row["long_EW"]), float(row["lat_NS"])],
                },
            })
        map_output.write_text(json.dumps({
            "type": "FeatureCollection",
            "name": "IHFC Thailand descriptive heat-flow observations",
            "provenance": {
                "source": "IHFC Global Heat Flow Database 2024",
                "doi": "https://doi.org/10.5880/fidgeo.2024.014",
                "license": "CC BY 4.0",
                "boundary": "Natural Earth 1:10m Admin-0 Countries (public domain)",
                "method": "Point-in-polygon covers predicate in EPSG:4326; repeated coordinates retained.",
                "warning": "Heat-flow observations are descriptive evidence, not reservoir temperatures, labels, or an interpolated prospectivity surface.",
            },
            "features": map_features,
        }, separators=(",", ":")), encoding="utf-8")

    classes = Counter(row["spatial_class"] for row in rows)
    thailand_rows = [row for row in rows if row["spatial_class"] == "INSIDE_THAILAND_BOUNDARY"]
    thailand_coordinates = Counter((row["lat_NS"], row["long_EW"]) for row in thailand_rows)
    summary = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "workbookPath": path_label(workbook),
        "workbookSha256": sha256(workbook),
        "workbookDataRowCount": workbook_row_count,
        "invalidCoordinateCount": invalid_coordinate_count,
        "regionalEnvelopeWgs84": list(REGIONAL_BOUNDS),
        "regionalRowCount": len(rows),
        "spatialClassCounts": dict(sorted(classes.items())),
        "insideThailandRowCount": len(thailand_rows),
        "insideThailandDistinctCoordinateCount": len(thailand_coordinates),
        "insideThailandDuplicateCoordinateGroupCount": sum(count > 1 for count in thailand_coordinates.values()),
        "insideThailandRepeatedRowsBeyondFirst": sum(count - 1 for count in thailand_coordinates.values() if count > 1),
        "insideThailandCoordinateReviewCount": sum(row["coordinate_review_required"] == "true" for row in thailand_rows),
        "insideThailandCompletedReviewCount": sum(row["Review_status"].casefold() == "completed" for row in thailand_rows),
        "insideThailandOpenReviewCount": sum(row["Review_status"].casefold() != "completed" for row in thailand_rows),
        "insideThailandMissingHeatFlowCount": sum(not row["q"].strip() for row in thailand_rows),
        "boundaryPath": path_label(boundary_path),
        "boundarySha256": sha256(boundary_path),
        "boundaryCrs": "EPSG:4326",
        "boundaryScale": "1:10,000,000",
        "boundaryLicense": "Natural Earth public domain",
        "datasetLicense": "CC BY 4.0 (GFZ Data Services metadata for DOI 10.5880/fidgeo.2024.014)",
        "duplicatePolicy": "Repeated coordinates are retained as separate measurements and annotated, never silently deleted.",
        "scientificUse": "Descriptive heat-flow observations; not geothermal occurrence labels or an interpolated prospectivity surface.",
        "mapOutputPath": path_label(map_output) if map_output is not None else None,
        "mapFeatureCount": len(thailand_rows) if map_output is not None else 0,
        "processingSeconds": time.perf_counter() - started,
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, default=DEFAULT_WORKBOOK)
    parser.add_argument("--boundary", type=Path, default=DEFAULT_BOUNDARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--boundary-output", type=Path, default=DEFAULT_BOUNDARY_OUTPUT)
    parser.add_argument("--map-output", type=Path, default=DEFAULT_MAP_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(build(args.workbook, args.boundary, args.output, args.summary, args.boundary_output, args.map_output), indent=2))


if __name__ == "__main__":
    main()
