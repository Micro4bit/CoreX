#!/usr/bin/env python3
"""Validate local SRTM HGT tiles and create georeferenced GeoTIFF derivatives."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any

import numpy as np
import rasterio
from rasterio.transform import from_origin


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "tasks/phase_2d_data_readiness/derived/terrain"
TILES = [
    ROOT / "tasks/phase_1_data_acquisition_label_validation/N19E098.hgt.gz",
    ROOT / "tasks/phase_1c_label_expansion_gis_foundation/N17E099.hgt.gz",
    ROOT / "tasks/phase_1c_label_expansion_gis_foundation/N18E099.hgt.gz",
    ROOT / "tasks/phase_1c_label_expansion_gis_foundation/N19E099.hgt.gz",
    ROOT / "tasks/phase_1c_label_expansion_gis_foundation/N20E099.hgt.gz",
]
NAME = re.compile(r"([NS])(\d{2})([EW])(\d{3})\.hgt\.gz$")
NODATA = -32768


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_label(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def tile_origin(path: Path) -> tuple[int, int]:
    match = NAME.match(path.name)
    if not match:
        raise ValueError(f"Unsupported HGT name: {path.name}")
    latitude = int(match.group(2)) * (1 if match.group(1) == "N" else -1)
    longitude = int(match.group(4)) * (1 if match.group(3) == "E" else -1)
    return longitude, latitude


def read_hgt(path: Path) -> np.ndarray:
    with gzip.open(path, "rb") as handle:
        raw = handle.read()
    sample_count = len(raw) // 2
    dimension = int(sample_count**0.5)
    if len(raw) % 2 or dimension * dimension != sample_count:
        raise ValueError(f"{path.name} is not a square big-endian int16 HGT raster")
    return np.frombuffer(raw, dtype=">i2").reshape((dimension, dimension))


def build(output_dir: Path, tiles: list[Path] = TILES) -> dict[str, Any]:
    started = time.perf_counter()
    output_dir.mkdir(parents=True, exist_ok=True)
    arrays: dict[str, np.ndarray] = {}
    records: list[dict[str, Any]] = []
    for path in tiles:
        array = read_hgt(path)
        if array.shape != (3601, 3601):
            raise ValueError(f"Expected 3601 x 3601 for {path.name}, received {array.shape}")
        longitude, latitude = tile_origin(path)
        valid = array[array != NODATA]
        if not valid.size:
            raise ValueError(f"{path.name} contains no valid elevations")
        tile_name = path.name.removesuffix(".hgt.gz")
        arrays[tile_name] = array
        resolution = 1 / 3600
        transform = from_origin(longitude - resolution / 2, latitude + 1 + resolution / 2, resolution, resolution)
        output_path = output_dir / f"{tile_name}.tif"
        with rasterio.open(
            output_path, "w", driver="GTiff", width=3601, height=3601, count=1,
            dtype="int16", crs="EPSG:4326", transform=transform, nodata=NODATA,
            compress="DEFLATE", predictor=2, tiled=True, blockxsize=256, blockysize=256,
        ) as dataset:
            dataset.write(array.astype("int16"), 1)
            dataset.update_tags(
                source_file=path.name,
                source_sha256=source_hash(path),
                processing="Big-endian SRTM HGT point posts written without elevation resampling",
                attribution="SRTM data courtesy of the U.S. Geological Survey",
                scientific_use="Terrain variable only; not evidence of a geothermal reservoir",
            )
        with rasterio.open(output_path) as dataset:
            check = dataset.read(1)
            if dataset.crs.to_epsg() != 4326 or check.shape != array.shape or not np.array_equal(check, array.astype("int16")):
                raise ValueError(f"GeoTIFF round-trip failed for {tile_name}")
            bounds = [dataset.bounds.left, dataset.bounds.bottom, dataset.bounds.right, dataset.bounds.top]
        records.append({
            "tile": tile_name,
            "sourcePath": path_label(path),
            "sourceSha256": source_hash(path),
            "compressedBytes": path.stat().st_size,
            "dimensions": [3601, 3601],
            "sampleSpacingArcSeconds": 1,
            "coordinateConvention": "Filename gives southwest 1-degree tile; 3601 x 3601 point posts include shared edges; rows north-to-south.",
            "coverageBoundsWgs84": [longitude, latitude, longitude + 1, latitude + 1],
            "geotiffPixelBoundsWgs84": bounds,
            "validSampleCount": int(valid.size),
            "noDataCount": int(np.count_nonzero(array == NODATA)),
            "minimumElevationM": int(valid.min()),
            "maximumElevationM": int(valid.max()),
            "geotiffPath": path_label(output_path),
            "geotiffBytes": output_path.stat().st_size,
        })

    seams: list[dict[str, Any]] = []
    for southern, northern in [("N17E099", "N18E099"), ("N18E099", "N19E099"), ("N19E099", "N20E099")]:
        differences = np.abs(arrays[southern][0].astype("int32") - arrays[northern][-1].astype("int32"))
        seams.append({"tiles": [southern, northern], "edge": "north-south shared point posts", "maximumAbsoluteDifferenceM": int(differences.max()), "nonMatchingPostCount": int(np.count_nonzero(differences))})
    west, east = arrays["N19E098"], arrays["N19E099"]
    differences = np.abs(west[:, -1].astype("int32") - east[:, 0].astype("int32"))
    seams.append({"tiles": ["N19E098", "N19E099"], "edge": "east-west shared point posts", "maximumAbsoluteDifferenceM": int(differences.max()), "nonMatchingPostCount": int(np.count_nonzero(differences))})

    summary = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "Mapzen Terrain Tiles AWS distribution; Thailand tiles contain SRTM elevations",
        "sourceUrl": "https://registry.opendata.aws/terrain-tiles/",
        "licenseAndAttribution": "SRTM public-domain status documented by distribution attribution; credit requested: SRTM data courtesy of the U.S. Geological Survey.",
        "tileCount": len(records),
        "tiles": records,
        "seamChecks": seams,
        "missingCoverage": "Only five one-degree tiles are present. This is not a complete northern-Thailand or national terrain mosaic; missing tiles are not extrapolated.",
        "derivedProduct": "GeoTIFF copies preserve source elevations and add EPSG:4326 georeferencing; no slope/hillshade generated because spatial coverage remains incomplete.",
        "scientificUse": "Elevation is a terrain variable, not proof of subsurface geothermal resources.",
        "processingSeconds": time.perf_counter() - started,
    }
    (output_dir / "terrain_qc_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(build(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
