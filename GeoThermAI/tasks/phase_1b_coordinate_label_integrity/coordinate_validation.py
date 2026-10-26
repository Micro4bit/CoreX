#!/usr/bin/env python3
"""Reproduce coordinate checks for Wood & Singharajwarapan (2014), Table 1.

The program deliberately preserves every source coordinate string.  It appends
derived WGS 84 longitude/latitude, geodesic discrepancies, and a transparent
validation status; it never replaces reported UTM or DMS values.

Install the documented dependency before use:
    python -m pip install -r requirements.txt

Example (from this directory):
    python coordinate_validation.py \
      --input ../phase_1_data_acquisition_label_validation/northern_hot_spring_label_registry_wood2014.csv \
      --output validated_hot_spring_registry.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

try:
    import pyproj
    from pyproj import CRS, Geod, Transformer
except ImportError as exc:  # pragma: no cover - direct user-facing setup error
    raise SystemExit(
        "Missing dependency 'pyproj'. Install it with: python -m pip install -r requirements.txt"
    ) from exc


SELECTED_EPSG = 32647  # WGS 84 / UTM zone 47N; inference tested against Table 1 DMS.
CANDIDATE_EPSGS = (32646, 32647, 32648)
SOURCE_FIELDS = (
    "source_code",
    "site_name",
    "utm_easting_m_wgs84",
    "utm_northing_m_wgs84",
    "longitude_dms",
    "latitude_dms",
    "surface_temperature_c",
    "flow_rate_l_s",
    "observation_class",
    "source_citation",
    "source_location",
    "coordinate_note",
)
DERIVED_FIELDS = (
    "selected_utm_crs",
    "crs_selection_basis",
    "transformed_longitude_decimal_wgs84",
    "transformed_latitude_decimal_wgs84",
    "reported_longitude_decimal_wgs84",
    "reported_latitude_decimal_wgs84",
    "utm_to_dms_discrepancy_m",
    "coordinate_comparison_status",
    "coordinate_confidence",
    "coordinate_validation_status",
    "coordinate_qc_note",
    "surface_temperature_qc_status",
    "surface_temperature_qc_note",
)


def parse_dms(value: str, kind: str) -> float | None:
    """Parse the Table 1 `ddd mm s.ss E`/`dd mm s.ss N` strings without altering them."""
    if not value or not value.strip():
        return None
    match = re.fullmatch(
        r"\s*(\d{1,3})\s+(\d{1,2})\s+(\d{1,2}(?:\.\d+)?)\s*([NSEW])\s*",
        value,
    )
    if not match:
        raise ValueError(f"Unparseable {kind} DMS value: {value!r}")
    degrees, minutes, seconds, hemisphere = match.groups()
    decimal = int(degrees) + int(minutes) / 60 + float(seconds) / 3600
    if int(minutes) >= 60 or float(seconds) >= 60:
        raise ValueError(f"Out-of-range {kind} DMS value: {value!r}")
    if kind == "longitude" and hemisphere not in {"E", "W"}:
        raise ValueError(f"Longitude has invalid hemisphere: {value!r}")
    if kind == "latitude" and hemisphere not in {"N", "S"}:
        raise ValueError(f"Latitude has invalid hemisphere: {value!r}")
    return -decimal if hemisphere in {"S", "W"} else decimal


def status_for_discrepancy(discrepancy_m: float | None) -> tuple[str, str, str, str]:
    """Return comparison, confidence, validation status, and a conservative explanation."""
    if discrepancy_m is None:
        return (
            "NOT_COMPARABLE_DMS_MISSING",
            "LOW",
            "CRS_INFERRED_DMS_MISSING",
            "Table 1 supplies UTM values but no DMS pair; positional agreement cannot be measured.",
        )
    if discrepancy_m <= 50:
        return (
            "MATCH_WITHIN_50_M",
            "HIGH",
            "CRS_AND_DMS_CONSISTENT",
            "UTM transform and independently parsed DMS position agree within 50 m.",
        )
    if discrepancy_m <= 250:
        return (
            "MATCH_50_TO_250_M",
            "MEDIUM",
            "CRS_AND_DMS_REASONABLY_CONSISTENT",
            "UTM transform and DMS differ by 50–250 m; retain both source values and review if precision matters.",
        )
    if discrepancy_m <= 1000:
        return (
            "REVIEW_250_M_TO_1_KM",
            "LOW",
            "CRS_INFERRED_DMS_MISMATCH_UNRESOLVED",
            "Difference exceeds 250 m. This does not identify which source representation is wrong.",
        )
    return (
        "MISMATCH_OVER_1_KM",
        "LOW",
        "CRS_INFERRED_DMS_MISMATCH_UNRESOLVED",
        "Difference exceeds 1 km. Do not substitute one coordinate representation for the other without source-author confirmation.",
    )


def temperature_qc(source_code: str, surface_temperature: str) -> tuple[str, str]:
    """Flag observed source-text conflicts without changing Table 1 temperature values."""
    if source_code == "CR_02":
        return (
            "TABLE_TEXT_INTERNAL_CONFLICT",
            "Table 1 reports 85 C; p. 612 describes the Kok River areas (including CR_02) as having a 73 C maximum. Both are retained; no correction is verified.",
        )
    if not surface_temperature.strip():
        return (
            "TABLE_VALUE_MISSING",
            "No surface-temperature value is printed for this row in Table 1; no value was imputed.",
        )
    return (
        "TABLE_VALUE_RETAINED_NOT_INDEPENDENTLY_VERIFIED",
        "Surface-temperature value is retained exactly from Table 1; this run did not independently verify the measurement.",
    )


def transform_rows(rows: list[dict[str, str]], epsg: int) -> list[dict[str, Any]]:
    """Transform Table 1 UTM positions and compare to Table 1 DMS positions."""
    transformer = Transformer.from_crs(CRS.from_epsg(epsg), CRS.from_epsg(4326), always_xy=True)
    geod = Geod(ellps="WGS84")
    transformed: list[dict[str, Any]] = []
    for row in rows:
        easting = float(row["utm_easting_m_wgs84"])
        northing = float(row["utm_northing_m_wgs84"])
        transformed_lon, transformed_lat = transformer.transform(easting, northing)
        dms_lon = parse_dms(row["longitude_dms"], "longitude")
        dms_lat = parse_dms(row["latitude_dms"], "latitude")
        if (dms_lon is None) != (dms_lat is None):
            raise ValueError(f"{row['source_code']} has only one DMS component")
        discrepancy_m: float | None = None
        if dms_lon is not None and dms_lat is not None:
            _, _, discrepancy_m = geod.inv(transformed_lon, transformed_lat, dms_lon, dms_lat)
        comparison, confidence, validation, note = status_for_discrepancy(discrepancy_m)
        temperature_status, temperature_note = temperature_qc(row["source_code"], row["surface_temperature_c"])
        transformed.append(
            {
                **row,
                "_lon": transformed_lon,
                "_lat": transformed_lat,
                "_dms_lon": dms_lon,
                "_dms_lat": dms_lat,
                "_discrepancy_m": discrepancy_m,
                "_comparison": comparison,
                "_confidence": confidence,
                "_validation": validation,
                "_note": note,
                "_temperature_status": temperature_status,
                "_temperature_note": temperature_note,
            }
        )
    return transformed


def candidate_summary(rows: list[dict[str, str]]) -> dict[str, dict[str, float | int | None]]:
    """Quantify zone choice from source UTM/DMS agreement, rather than assume the zone."""
    summary: dict[str, dict[str, float | int | None]] = {}
    for epsg in CANDIDATE_EPSGS:
        discrepancies = [r["_discrepancy_m"] for r in transform_rows(rows, epsg) if r["_discrepancy_m"] is not None]
        summary[f"EPSG:{epsg}"] = {
            "records_with_dms": len(discrepancies),
            "median_discrepancy_m": round(statistics.median(discrepancies), 3) if discrepancies else None,
            "minimum_discrepancy_m": round(min(discrepancies), 3) if discrepancies else None,
            "maximum_discrepancy_m": round(max(discrepancies), 3) if discrepancies else None,
        }
    return summary


def write_registry(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=[*SOURCE_FIELDS, *DERIVED_FIELDS])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: row.get(field, "") for field in SOURCE_FIELDS
                }
                | {
                    "selected_utm_crs": f"EPSG:{SELECTED_EPSG} (WGS 84 / UTM zone 47N)",
                    "crs_selection_basis": (
                        "Table 1 labels WGS84 UTM without a zone; 99°E lies in UTM zone 47N and EPSG:32647 "
                        "minimizes UTM-to-DMS discrepancies among tested adjacent northern zones."
                    ),
                    "transformed_longitude_decimal_wgs84": f"{row['_lon']:.8f}",
                    "transformed_latitude_decimal_wgs84": f"{row['_lat']:.8f}",
                    "reported_longitude_decimal_wgs84": "" if row["_dms_lon"] is None else f"{row['_dms_lon']:.8f}",
                    "reported_latitude_decimal_wgs84": "" if row["_dms_lat"] is None else f"{row['_dms_lat']:.8f}",
                    "utm_to_dms_discrepancy_m": "" if row["_discrepancy_m"] is None else f"{row['_discrepancy_m']:.2f}",
                    "coordinate_comparison_status": row["_comparison"],
                    "coordinate_confidence": row["_confidence"],
                    "coordinate_validation_status": row["_validation"],
                    "coordinate_qc_note": row["_note"],
                    "surface_temperature_qc_status": row["_temperature_status"],
                    "surface_temperature_qc_note": row["_temperature_note"],
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Source-preserving Table 1 registry CSV")
    parser.add_argument("--output", type=Path, required=True, help="Derived validated registry CSV")
    parser.add_argument("--summary-json", type=Path, help="Optional machine-readable run summary")
    args = parser.parse_args()

    with args.input.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 16:
        raise ValueError(f"Expected 16 Table 1 records, found {len(rows)}")
    missing = [field for field in SOURCE_FIELDS if field not in rows[0]]
    if missing:
        raise ValueError(f"Input registry is missing required source fields: {missing}")

    candidate_crs = candidate_summary(rows)
    selected_rows = transform_rows(rows, SELECTED_EPSG)
    write_registry(selected_rows, args.output)
    result = {
        "input": str(args.input),
        "output": str(args.output),
        "record_count": len(selected_rows),
        "selected_crs": f"EPSG:{SELECTED_EPSG}",
        "pyproj_version": pyproj.__version__,
        "proj_version": pyproj.proj_version_str,
        "candidate_crs_discrepancy_summary": candidate_crs,
        "records_without_dms": [r["source_code"] for r in selected_rows if r["_discrepancy_m"] is None],
        "records_over_1km_discrepancy": [
            r["source_code"] for r in selected_rows if r["_discrepancy_m"] is not None and r["_discrepancy_m"] > 1000
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.summary_json:
        args.summary_json.parent.mkdir(parents=True, exist_ok=True)
        args.summary_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, csv.Error) as exc:
        print(f"coordinate validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
