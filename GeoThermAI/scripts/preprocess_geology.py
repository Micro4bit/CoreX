#!/usr/bin/env python3
"""Build immutable-source-derived MapLibre geology assets for Phase 2C.

The source EsriJSON remains untouched. Geometry is simplified in its native
EPSG:32647 coordinate system before being transformed to EPSG:4326.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

from pyproj import Transformer
from shapely import transform
from shapely.geometry import MultiPolygon, Polygon, mapping


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "tasks/phase_1c_label_expansion_gis_foundation/rock_unit_250k_northern_esrijson.json"
DEFAULT_METADATA = ROOT / "tasks/phase_1c_label_expansion_gis_foundation/rock_unit_250k_metadata.json"
DEFAULT_OUTPUT = ROOT / "web/public/data"
DEFAULT_FULL_OUTPUT = ROOT / "derived/phase2c"


def signed_area(ring: list[list[float]]) -> float:
    return sum(
        ring[index][0] * ring[(index + 1) % len(ring)][1]
        - ring[(index + 1) % len(ring)][0] * ring[index][1]
        for index in range(len(ring))
    ) / 2


def esri_rings_to_geometry(
    rings: list[list[list[float]]],
    *,
    audit: dict[str, Any] | None = None,
    object_id: int | None = None,
) -> Polygon | MultiPolygon:
    cleaned = [ring for ring in rings if len(ring) >= 4]
    if not cleaned:
        return Polygon()

    # Esri polygon exteriors are clockwise. Assign counter-clockwise holes to
    # the smallest containing exterior; this also preserves multipart features.
    exteriors = [ring for ring in cleaned if signed_area(ring) < 0]
    holes = [ring for ring in cleaned if signed_area(ring) >= 0]
    if not exteriors:
        exteriors, holes = [cleaned[0]], cleaned[1:]

    exterior_polygons = [Polygon(ring) for ring in exteriors]
    assigned_holes: list[list[list[list[float]]]] = [[] for _ in exteriors]
    for hole in holes:
        representative = Polygon(hole).representative_point()
        containers = [
            (index, polygon.area)
            for index, polygon in enumerate(exterior_polygons)
            if polygon.contains(representative)
        ]
        if not containers:
            if audit is not None:
                audit["orphanHoleCount"] += 1
            raise ValueError(f"Unassigned Esri polygon hole in OBJECTID {object_id!r}; refusing to drop source geometry")
        assigned_holes[min(containers, key=lambda item: item[1])[0]].append(hole)

    polygons = [Polygon(exterior, assigned_holes[index]) for index, exterior in enumerate(exteriors)]
    valid = []
    for polygon in polygons:
        if polygon.is_empty:
            continue
        if polygon.is_valid:
            valid.append(polygon)
            continue
        if audit is not None:
            audit["topologyRepairCount"] += 1
            audit["topologyRepairObjectIds"].append(object_id)
        repaired = polygon.buffer(0)
        if repaired.is_empty or repaired.geom_type not in {"Polygon", "MultiPolygon"}:
            raise ValueError(f"Topology repair did not produce polygon geometry for OBJECTID {object_id!r}")
        valid.append(repaired)
    flattened: list[Polygon] = []
    for geometry in valid:
        if isinstance(geometry, Polygon):
            flattened.append(geometry)
        elif isinstance(geometry, MultiPolygon):
            flattened.extend(geometry.geoms)
    return flattened[0] if len(flattened) == 1 else MultiPolygon(flattened)


def count_vertices(geometry: Polygon | MultiPolygon) -> int:
    polygons = [geometry] if isinstance(geometry, Polygon) else list(geometry.geoms)
    return sum(len(polygon.exterior.coords) + sum(len(ring.coords) for ring in polygon.interiors) for polygon in polygons)


def load_authoritative_legend(metadata_path: Path | None) -> dict[str, str]:
    if metadata_path is None:
        return {}
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    infos = metadata.get("drawingInfo", {}).get("renderer", {}).get("uniqueValueInfos", [])
    legend: dict[str, str] = {}
    for info in infos:
        value = str(info.get("value", ""))
        symbol = value.split("-", 2)[-1] if value else ""
        label = str(info.get("label", "")).strip()
        if symbol and label:
            legend[symbol] = label
    return legend


def build(source: Path, output_dir: Path, tolerance_m: float, full_output_dir: Path | None = None, metadata_path: Path | None = None) -> dict[str, Any]:
    started = time.perf_counter()
    source_bytes = source.read_bytes()
    payload = json.loads(source_bytes)
    wkid = payload.get("spatialReference", {}).get("latestWkid") or payload.get("spatialReference", {}).get("wkid")
    if wkid != 32647:
        raise ValueError(f"Expected source EPSG:32647, received {wkid!r}")
    transformer = Transformer.from_crs(32647, 4326, always_xy=True)
    legend = load_authoritative_legend(metadata_path)

    full_features: list[dict[str, Any]] = []
    simplified_features: list[dict[str, Any]] = []
    deviations: list[float] = []
    original_vertices = 0
    simplified_vertices = 0
    geometry_audit: dict[str, Any] = {"orphanHoleCount": 0, "topologyRepairCount": 0, "topologyRepairObjectIds": []}
    empty_geometry_count = 0
    source_bounds = [float("inf"), float("inf"), float("-inf"), float("-inf")]
    output_bounds = [float("inf"), float("inf"), float("-inf"), float("-inf")]

    for source_feature in payload.get("features", []):
        rings = source_feature.get("geometry", {}).get("rings", [])
        object_id = source_feature.get("attributes", {}).get("OBJECTID")
        geometry = esri_rings_to_geometry(rings, audit=geometry_audit, object_id=object_id)
        if geometry.is_empty:
            empty_geometry_count += 1
            continue
        simplified = geometry.simplify(tolerance_m, preserve_topology=True)
        deviations.append(geometry.hausdorff_distance(simplified))
        original_vertices += count_vertices(geometry)
        simplified_vertices += count_vertices(simplified)
        attributes = source_feature.get("attributes", {})
        properties = {
            "objectId": attributes.get("OBJECTID"),
            "symbol": attributes.get("TEXT_SYM") or "Unclassified source symbol",
            "legendLabel": legend.get(attributes.get("TEXT_SYM")),
            "year": attributes.get("YEAR_COMPI"),
            "sourceLayerId": "DMR_ROCK_UNIT_250K_NORTH",
        }
        transformed = transform(geometry, transformer.transform, interleaved=False)
        transformed_simplified = transform(simplified, transformer.transform, interleaved=False)
        full_features.append({"type": "Feature", "properties": properties, "geometry": mapping(transformed)})
        simplified_features.append({"type": "Feature", "properties": properties, "geometry": mapping(transformed_simplified)})
        for bounds, aggregate in ((geometry.bounds, source_bounds), (transformed.bounds, output_bounds)):
            aggregate[0] = min(aggregate[0], bounds[0])
            aggregate[1] = min(aggregate[1], bounds[1])
            aggregate[2] = max(aggregate[2], bounds[2])
            aggregate[3] = max(aggregate[3], bounds[3])

    output_dir.mkdir(parents=True, exist_ok=True)
    full_output_dir = full_output_dir or output_dir
    full_output_dir.mkdir(parents=True, exist_ok=True)
    full_path = full_output_dir / "dmr-rock-units-north.full.geojson"
    simplified_path = output_dir / "dmr-rock-units-north.simplified.geojson"
    manifest_path = output_dir / "dmr-rock-units-north.manifest.json"
    full_path.write_text(json.dumps({"type": "FeatureCollection", "features": full_features}, separators=(",", ":")), encoding="utf-8")
    simplified_path.write_text(json.dumps({"type": "FeatureCollection", "features": simplified_features}, separators=(",", ":")), encoding="utf-8")
    elapsed = time.perf_counter() - started
    try:
        source_label = str(source.relative_to(ROOT))
    except ValueError:
        source_label = str(source)
    manifest = {
        "sourcePath": source_label,
        "sourceSha256": hashlib.sha256(source_bytes).hexdigest(),
        "metadataPath": str(metadata_path.relative_to(ROOT)) if metadata_path and metadata_path.is_relative_to(ROOT) else str(metadata_path) if metadata_path else None,
        "metadataSha256": hashlib.sha256(metadata_path.read_bytes()).hexdigest() if metadata_path else None,
        "sourceCrs": "EPSG:32647",
        "outputCrs": "EPSG:4326",
        "transformation": "pyproj Transformer EPSG:32647 to EPSG:4326, always_xy=True",
        "simplification": "Shapely simplify(preserve_topology=True) in source metres",
        "simplificationToleranceM": tolerance_m,
        "inputFeatureCount": len(payload.get("features", [])),
        "featureCount": len(simplified_features),
        "emptyGeometryCount": empty_geometry_count,
        "topologyRepairMethod": "Shapely buffer(0) applied only to invalid derived polygon parts before simplification",
        "topologyRepairCount": geometry_audit["topologyRepairCount"],
        "topologyRepairObjectIds": geometry_audit["topologyRepairObjectIds"],
        "orphanHoleCount": geometry_audit["orphanHoleCount"],
        "sourceSymbolCount": len({feature["properties"]["symbol"] for feature in simplified_features}),
        "legendEntryCount": len(legend),
        "matchedSourceSymbolCount": len({feature["properties"]["symbol"] for feature in simplified_features if feature["properties"]["legendLabel"]}),
        "unmatchedSourceSymbols": sorted({feature["properties"]["symbol"] for feature in simplified_features if not feature["properties"]["legendLabel"]}),
        "sourceBounds": source_bounds if full_features else None,
        "outputBoundsWgs84": output_bounds if full_features else None,
        "sourceBytes": len(source_bytes),
        "fullGeojsonBytes": full_path.stat().st_size,
        "simplifiedGeojsonBytes": simplified_path.stat().st_size,
        "originalVertexCount": original_vertices,
        "simplifiedVertexCount": simplified_vertices,
        "maxHausdorffDeviationM": max(deviations, default=0.0),
        "meanHausdorffDeviationM": sum(deviations) / len(deviations) if deviations else 0.0,
        "processingSeconds": elapsed,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scientificUse": "Descriptive 1:250,000 geological boundary context only; not site lithology or geothermal prospectivity.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--full-output-dir", type=Path, default=DEFAULT_FULL_OUTPUT)
    parser.add_argument("--tolerance-m", type=float, default=25.0)
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output_dir, args.tolerance_m, args.full_output_dir, args.metadata), indent=2))


if __name__ == "__main__":
    main()
