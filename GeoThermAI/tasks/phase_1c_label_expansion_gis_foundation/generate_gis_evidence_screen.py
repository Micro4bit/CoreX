#!/usr/bin/env python3
"""Generate a descriptive northern-Thailand GIS evidence screen.

The output intentionally shows evidence coverage, source-derived manifestations,
coordinate-quality flags, geology and active-fault context. It does not compute
or display geothermal prospectivity, occurrence probability, resource capacity,
or a model result.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import shapefile
from pyproj import Transformer


TASK_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TASK_DIR.parents[1]
DEFAULT_REGISTRY = TASK_DIR / "geothermal_label_master_registry.csv"
DEFAULT_ROCK = TASK_DIR / "rock_unit_250k_northern_esrijson.json"
DEFAULT_ACTIVE_FAULTS = PROJECT_DIR / "tasks/phase_1_data_acquisition_label_validation/N_ZONE_ACTIVEFAULT_20230419_091427.shp"
DEFAULT_TILES = ("N17E099.hgt.gz", "N18E099.hgt.gz", "N19E099.hgt.gz", "N20E099.hgt.gz")
MAP_BOUNDS = (99.0, 100.0, 17.8, 20.3)  # longitude min/max, latitude min/max


def read_hgt(path: Path, step: int = 20) -> np.ndarray:
    """Read an SRTM HGT tile and downsample it for a regional evidence display."""
    with gzip.open(path, "rb") as handle:
        raw = handle.read()
    values = np.frombuffer(raw, dtype=">i2")
    dimension = int(np.sqrt(values.size))
    if dimension * dimension != values.size:
        raise ValueError(f"Unexpected HGT sample count in {path.name}: {values.size}")
    array = values.reshape((dimension, dimension)).astype(float)
    array[array == -32768] = np.nan
    return array[::step, ::step]


def hillshade(elevation: np.ndarray) -> np.ndarray:
    """Return a display-only hillshade; it is not a terrain predictor product."""
    filled = np.where(np.isnan(elevation), np.nanmedian(elevation), elevation)
    gy, gx = np.gradient(filled)
    slope = np.pi / 2 - np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    azimuth, altitude = np.deg2rad(315), np.deg2rad(45)
    shaded = np.sin(altitude) * np.sin(slope) + np.cos(altitude) * np.cos(slope) * np.cos(azimuth - aspect)
    return (shaded - shaded.min()) / (shaded.max() - shaded.min())


def load_northern_hillshade(tile_directory: Path) -> np.ndarray:
    # HGT rows run north-to-south. Stack N20 through N17 to cover 17-21 N.
    arrays = [read_hgt(tile_directory / tile) for tile in reversed(DEFAULT_TILES)]
    return hillshade(np.vstack(arrays))


def terrain_summary(tile_directory: Path, output: Path) -> list[dict[str, str]]:
    """Derive per-tile terrain summaries from actual one-arc-second HGT pixels."""
    rows: list[dict[str, str]] = []
    for tile in DEFAULT_TILES:
        elevation = read_hgt(tile_directory / tile, step=1)
        latitude_center = int(tile[1:3]) + 0.5
        meters_per_lat_pixel = 111_320 / 3600
        meters_per_lon_pixel = meters_per_lat_pixel * np.cos(np.deg2rad(latitude_center))
        dz_dy, dz_dx = np.gradient(elevation)
        slope_degrees = np.degrees(np.arctan(np.hypot(dz_dx / meters_per_lon_pixel, dz_dy / meters_per_lat_pixel)))
        valid_elevation = elevation[~np.isnan(elevation)]
        valid_slope = slope_degrees[~np.isnan(slope_degrees)]
        rows.append({
            "tile": tile, "source_resolution_arc_second": "1", "elevation_min_m": f"{np.min(valid_elevation):.0f}",
            "elevation_max_m": f"{np.max(valid_elevation):.0f}", "elevation_mean_m": f"{np.mean(valid_elevation):.2f}",
            "slope_mean_degrees": f"{np.mean(valid_slope):.2f}", "slope_p95_degrees": f"{np.percentile(valid_slope, 95):.2f}",
            "no_data_pixels": str(int(np.isnan(elevation).sum())),
            "method_note": "Horn-style local gradient approximation on 1-arc-second HGT pixels; summary only, not a model feature set.",
        })
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows


def draw_rock_units(ax: plt.Axes, path: Path, transformer: Transformer) -> int:
    dataset = json.loads(path.read_text(encoding="utf-8"))
    count = 0
    for feature in dataset.get("features", []):
        geometry = feature.get("geometry") or {}
        for ring in geometry.get("rings", []):
            if len(ring) < 3:
                continue
            east, north = zip(*ring)
            lon, lat = transformer.transform(east, north)
            ax.plot(lon, lat, color="#886f4c", linewidth=0.18, alpha=0.42, zorder=2)
        count += 1
    return count


def draw_active_faults(ax: plt.Axes, path: Path, transformer: Transformer) -> int:
    reader = shapefile.Reader(str(path))
    count = 0
    for shape in reader.shapes():
        points = shape.points
        if not points:
            continue
        part_starts = list(shape.parts) + [len(points)]
        for start, end in zip(part_starts[:-1], part_starts[1:]):
            east, north = zip(*points[start:end])
            lon, lat = transformer.transform(east, north)
            ax.plot(lon, lat, color="#b2182b", linewidth=0.55, alpha=0.7, zorder=3)
        count += 1
    return count


def draw_manifestations(ax: plt.Axes, path: Path) -> tuple[int, int]:
    rows = [r for r in csv.DictReader(path.open(encoding="utf-8")) if r["source_region"] == "Northern Thailand"]
    consistent = 0
    review = 0
    for row in rows:
        lon, lat = float(row["derived_longitude_wgs84"]), float(row["derived_latitude_wgs84"])
        is_consistent = row["coordinate_validation_status"] == "CRS_AND_DMS_CONSISTENT"
        marker, color = ("o", "#2166ac") if is_consistent else ("^", "#d73027")
        ax.scatter(lon, lat, s=34, marker=marker, color=color, edgecolor="white", linewidth=0.55, zorder=5)
        ax.annotate(row["source_record_code"], (lon, lat), xytext=(3, 3), textcoords="offset points", fontsize=6.8, color="#111111", zorder=6)
        if is_consistent:
            consistent += 1
        else:
            review += 1
    return consistent, review


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--rock-units", type=Path, default=DEFAULT_ROCK)
    parser.add_argument("--active-faults", type=Path, default=DEFAULT_ACTIVE_FAULTS)
    parser.add_argument("--tile-directory", type=Path, default=TASK_DIR)
    parser.add_argument("--output", type=Path, default=TASK_DIR / "gis_evidence_screen.png")
    parser.add_argument("--summary", type=Path, default=TASK_DIR / "gis_evidence_screen_generation_summary.json")
    parser.add_argument("--terrain-summary", type=Path, default=TASK_DIR / "northern_terrain_variable_summary.csv")
    args = parser.parse_args()

    required = [args.registry, args.rock_units, args.active_faults, *(args.tile_directory / tile for tile in DEFAULT_TILES)]
    absent = [str(path) for path in required if not path.exists()]
    if absent:
        raise FileNotFoundError("Missing input(s): " + ", ".join(absent))

    transformer = Transformer.from_crs(32647, 4326, always_xy=True)
    fig, ax = plt.subplots(figsize=(9.5, 11))
    fig.subplots_adjust(left=0.13, right=0.98, top=0.92, bottom=0.14)
    shade = load_northern_hillshade(args.tile_directory)
    terrain_rows = terrain_summary(args.tile_directory, args.terrain_summary)
    ax.imshow(shade, cmap="Greys", extent=(99, 100, 17, 21), origin="upper", alpha=0.72, zorder=0)
    rock_count = draw_rock_units(ax, args.rock_units, transformer)
    fault_count = draw_active_faults(ax, args.active_faults, transformer)
    consistent, review = draw_manifestations(ax, args.registry)
    min_lon, max_lon, min_lat, max_lat = MAP_BOUNDS
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.set_xlabel("Longitude (WGS 84, derived display coordinates)")
    ax.set_ylabel("Latitude (WGS 84, derived display coordinates)")
    ax.set_title("Northern Thailand GIS Evidence Screen\nDescriptive source coverage only - not a geothermal prediction map", fontsize=13, weight="bold")
    ax.grid(color="white", linewidth=0.4, alpha=0.5)
    legend = [
        Line2D([0], [0], marker="o", color="w", label=f"Table 1 manifestation: internally consistent coordinate ({consistent})", markerfacecolor="#2166ac", markeredgecolor="white", markersize=7),
        Line2D([0], [0], marker="^", color="w", label=f"Table 1 manifestation: coordinate review required ({review})", markerfacecolor="#d73027", markeredgecolor="white", markersize=7),
        Line2D([0], [0], color="#b2182b", linewidth=1.2, label="DMR active-fault line context (reuse conditions unresolved)"),
        Line2D([0], [0], color="#886f4c", linewidth=0.8, label="DMR 1:250,000 rock-unit boundaries"),
    ]
    ax.legend(handles=legend, loc="lower left", fontsize=7.3, framealpha=0.92)
    fig.text(0.5, 0.035, "Terrain background: four SRTM HGT tiles, downsampled for display. Coordinate flags include CR_02 mismatch and CM_16 missing DMS.\nUnlabeled locations are not negative observations. DMR structural-line geometry was unavailable and is not plotted.", ha="center", fontsize=7.2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=220, bbox_inches="tight")
    plt.close(fig)
    summary = {
        "screen_type": "descriptive_gis_evidence_screen_not_prediction",
        "map_bounds_wgs84": {"min_longitude": min_lon, "max_longitude": max_lon, "min_latitude": min_lat, "max_latitude": max_lat},
        "northern_manifestations_plotted": consistent + review,
        "coordinate_consistent_points": consistent,
        "coordinate_review_points": review,
        "rock_unit_features_drawn": rock_count,
        "active_fault_features_drawn": fault_count,
        "dem_tiles": list(DEFAULT_TILES),
        "terrain_summary_rows": len(terrain_rows),
        "known_omission": "DMR GEOL_STR_250K attributes were accessed but geometry was unavailable from the service query; not plotted.",
    }
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
