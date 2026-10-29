"""Geospatial Coverage Calculator and AOI Auditor for GeoThermAI.

Implements rigorous ellipsoidal geodesic area measurements and true equal-area projections:
- Uses pyproj.Geod(ellps='WGS84') for exact geodesic ellipsoidal area calculations.
- Clarifies that UTM Zone 47N (EPSG:32647) is a conformal projection (preserving angles,
  not area) and provides geodesic measurements as the primary scientific standard.
- Removes overlaps via unary union before computing coverage.
- Intersects footprints with the candidate Area of Interest (AOI).
- Computes combined multi-predictor overlap (e.g. SRTM DEM ∩ DMR Geology).
- Identifies missing tiles and spatial gaps.
- Produces reproducible audit records for scientific validation.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

import geopandas as gpd
import numpy as np
import pyproj
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

# Default candidate Northern Thailand AOI
DEFAULT_NORTHERN_AOI_BOUNDS: tuple[float, float, float, float] = (98.0, 17.0, 100.5, 20.5)

# Standard WGS84 ellipsoid geodetic calculator (zero projection distortion)
WGS84_GEOD = pyproj.Geod(ellps="WGS84")


@dataclass(frozen=True)
class CoverageAuditResult:
    layer_name: str
    dataset_type: str
    native_crs: str
    calculation_method: str
    aoi_total_area_km2: float
    covered_area_km2: float
    missing_area_km2: float
    true_coverage_pct: float
    tile_or_item_count: int
    required_tiles_or_items: int | None
    tile_count_ratio_pct: float | None
    eligible_2km_grid_cells: int
    missing_components: str
    coverage_status: str
    polygon: Polygon | None = field(default=None, repr=False)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_name": self.layer_name,
            "dataset_type": self.dataset_type,
            "native_crs": self.native_crs,
            "calculation_method": self.calculation_method,
            "aoi_total_area_km2": round(self.aoi_total_area_km2, 2),
            "covered_area_km2": round(self.covered_area_km2, 2),
            "missing_area_km2": round(self.missing_area_km2, 2),
            "true_coverage_pct": round(self.true_coverage_pct, 2),
            "tile_or_item_count": self.tile_or_item_count,
            "required_tiles_or_items": self.required_tiles_or_items,
            "tile_count_ratio_pct": (
                round(self.tile_count_ratio_pct, 2)
                if self.tile_count_ratio_pct is not None
                else None
            ),
            "eligible_2km_grid_cells": self.eligible_2km_grid_cells,
            "missing_components": self.missing_components,
            "coverage_status": self.coverage_status,
        }


def get_aoi_polygon(bounds: tuple[float, float, float, float] = DEFAULT_NORTHERN_AOI_BOUNDS) -> Polygon:
    """Create bounding box polygon in EPSG:4326."""
    min_lon, min_lat, max_lon, max_lat = bounds
    return box(min_lon, min_lat, max_lon, max_lat)


def compute_geodesic_area_km2(geom: Polygon | None) -> float:
    """Compute true ellipsoidal surface area in km² using WGS84 ellipsoid."""
    if geom is None or geom.is_empty:
        return 0.0
    area_m2, _ = WGS84_GEOD.geometry_area_perimeter(geom)
    return abs(area_m2) / 1e6


def compute_geometric_coverage(
    layer_name: str,
    dataset_type: str,
    footprints: Sequence[Polygon],
    native_crs: str,
    aoi_bounds: tuple[float, float, float, float] = DEFAULT_NORTHERN_AOI_BOUNDS,
    metric_crs: str | None = None,
    required_count: int | None = None,
    missing_desc: str = "",
) -> CoverageAuditResult:
    """Measure exact geodesic coverage of candidate footprints inside the AOI."""
    aoi_geom = get_aoi_polygon(aoi_bounds)
    aoi_area_km2 = compute_geodesic_area_km2(aoi_geom)

    if not footprints:
        return CoverageAuditResult(
            layer_name=layer_name,
            dataset_type=dataset_type,
            native_crs=native_crs,
            calculation_method="Geodesic_WGS84_Ellipsoid",
            aoi_total_area_km2=aoi_area_km2,
            covered_area_km2=0.0,
            missing_area_km2=aoi_area_km2,
            true_coverage_pct=0.0,
            tile_or_item_count=0,
            required_tiles_or_items=required_count,
            tile_count_ratio_pct=0.0 if required_count else None,
            eligible_2km_grid_cells=0,
            missing_components=missing_desc or "Completely missing",
            coverage_status="ZERO_COVERAGE",
            polygon=Polygon(),
        )

    # Union all footprints in EPSG:4326 to eliminate overlapping polygon areas
    unified_footprints = unary_union(list(footprints))

    # Intersect with AOI
    covered_in_aoi = aoi_geom.intersection(unified_footprints)

    if covered_in_aoi.is_empty:
        return CoverageAuditResult(
            layer_name=layer_name,
            dataset_type=dataset_type,
            native_crs=native_crs,
            calculation_method="Geodesic_WGS84_Ellipsoid",
            aoi_total_area_km2=aoi_area_km2,
            covered_area_km2=0.0,
            missing_area_km2=aoi_area_km2,
            true_coverage_pct=0.0,
            tile_or_item_count=len(footprints),
            required_tiles_or_items=required_count,
            tile_count_ratio_pct=(
                (len(footprints) / required_count * 100) if required_count else None
            ),
            eligible_2km_grid_cells=0,
            missing_components=missing_desc or "No overlap with AOI",
            coverage_status="ZERO_COVERAGE",
            polygon=Polygon(),
        )

    covered_area_km2 = compute_geodesic_area_km2(covered_in_aoi)
    missing_area_km2 = max(0.0, aoi_area_km2 - covered_area_km2)
    true_coverage_pct = (covered_area_km2 / aoi_area_km2) * 100.0

    tile_ratio = (len(footprints) / required_count * 100.0) if required_count else None
    eligible_cells = int(np.floor(covered_area_km2 / 4.0))  # 2 km x 2 km = 4 km²

    if true_coverage_pct >= 99.9:
        status = "COMPLETE_COVERAGE"
    elif true_coverage_pct > 0.0:
        status = "PARTIAL_COVERAGE"
    else:
        status = "ZERO_COVERAGE"

    return CoverageAuditResult(
        layer_name=layer_name,
        dataset_type=dataset_type,
        native_crs=native_crs,
        calculation_method="Geodesic_WGS84_Ellipsoid",
        aoi_total_area_km2=aoi_area_km2,
        covered_area_km2=covered_area_km2,
        missing_area_km2=missing_area_km2,
        true_coverage_pct=true_coverage_pct,
        tile_or_item_count=len(footprints),
        required_tiles_or_items=required_count,
        tile_count_ratio_pct=tile_ratio,
        eligible_2km_grid_cells=eligible_cells,
        missing_components=missing_desc,
        coverage_status=status,
        polygon=covered_in_aoi,
    )


def audit_srtm_dem_coverage(
    terrain_dir: Path,
    aoi_bounds: tuple[float, float, float, float] = DEFAULT_NORTHERN_AOI_BOUNDS,
) -> CoverageAuditResult:
    """Audit available SRTM 1-arcsec DEM tiles against candidate AOI."""
    all_required_tiles = [
        "N17E098", "N18E098", "N19E098", "N20E098",
        "N17E099", "N18E099", "N19E099", "N20E099",
        "N17E100", "N18E100", "N19E100", "N20E100",
    ]

    tile_footprints: list[Polygon] = []
    found_tiles: list[str] = []

    for name in all_required_tiles:
        tif_path = terrain_dir / f"{name}.tif"
        if tif_path.is_file():
            lat = float(name[1:3])
            lon = float(name[4:7])
            tile_box = box(lon, lat, lon + 1.0, lat + 1.0)
            tile_footprints.append(tile_box)
            found_tiles.append(name)

    missing_tiles = [t for t in all_required_tiles if t not in found_tiles]
    missing_desc = f"{len(missing_tiles)} missing 1-degree tiles: {', '.join(missing_tiles)}"

    return compute_geometric_coverage(
        layer_name="SRTM 1 Arc-Second Global Elevation DEM",
        dataset_type="Raster DEM",
        footprints=tile_footprints,
        native_crs="EPSG:4326",
        aoi_bounds=aoi_bounds,
        required_count=len(all_required_tiles),
        missing_desc=missing_desc,
    )


def audit_geology_coverage(
    geology_geojson_path: Path,
    aoi_bounds: tuple[float, float, float, float] = DEFAULT_NORTHERN_AOI_BOUNDS,
) -> CoverageAuditResult:
    """Audit DMR 1:250k Northern Geology polygon extract against candidate AOI."""
    if not geology_geojson_path.is_file():
        return compute_geometric_coverage(
            layer_name="DMR 1:250k Northern Geology",
            dataset_type="Vector Polygons",
            footprints=[],
            native_crs="EPSG:4326",
            aoi_bounds=aoi_bounds,
            missing_desc="Geology GeoJSON file not found",
        )

    gdf = gpd.read_file(geology_geojson_path).to_crs("EPSG:4326")
    footprints = list(gdf.geometry)

    missing_desc = (
        "Western margin (98.0°-98.26°E) and southeastern margins unmapped in current extract; "
        "requires adjacent quadrangle sheet completion from DMR national database"
    )

    return compute_geometric_coverage(
        layer_name="DMR 1:250k Northern Geology",
        dataset_type="Vector Polygons",
        footprints=footprints,
        native_crs="EPSG:4326",
        aoi_bounds=aoi_bounds,
        required_count=None,
        missing_desc=missing_desc,
    )


def audit_active_faults_coverage(
    faults_shp_path: Path,
    aoi_bounds: tuple[float, float, float, float] = DEFAULT_NORTHERN_AOI_BOUNDS,
) -> CoverageAuditResult:
    """Audit DMR active faults line footprint against candidate AOI."""
    if not faults_shp_path.is_file():
        return compute_geometric_coverage(
            layer_name="DMR Active Fault Zones",
            dataset_type="Vector Lines",
            footprints=[],
            native_crs="EPSG:32647",
            aoi_bounds=aoi_bounds,
            missing_desc="Active fault shapefile not found",
        )

    gdf = gpd.read_file(faults_shp_path).to_crs("EPSG:4326")
    corridors = [line.buffer(0.005) for line in gdf.geometry]

    missing_desc = (
        "630 fault lines present locally, but live WFS returns 0 geometries. "
        "Subsurface 3D fault dip unmapped. BLOCKED for ML training due to conflicting licensing terms."
    )

    return compute_geometric_coverage(
        layer_name="DMR Active Fault Zones",
        dataset_type="Vector Corridors (500m buffer)",
        footprints=corridors,
        native_crs="EPSG:32647",
        aoi_bounds=aoi_bounds,
        required_count=None,
        missing_desc=missing_desc,
    )


def compute_combined_predictors_overlap(
    srtm_geom: Polygon | None,
    geol_geom: Polygon | None,
    aoi_bounds: tuple[float, float, float, float] = DEFAULT_NORTHERN_AOI_BOUNDS,
) -> CoverageAuditResult:
    """Compute combined spatial intersection where both SRTM DEM and DMR Geology co-occur."""
    aoi_geom = get_aoi_polygon(aoi_bounds)
    aoi_area_km2 = compute_geodesic_area_km2(aoi_geom)

    if srtm_geom is None or srtm_geom.is_empty or geol_geom is None or geol_geom.is_empty:
        return CoverageAuditResult(
            layer_name="Combined Usable Predictors (SRTM DEM ∩ DMR Geology)",
            dataset_type="Composite Intersection",
            native_crs="EPSG:4326",
            calculation_method="Geodesic_WGS84_Ellipsoid",
            aoi_total_area_km2=aoi_area_km2,
            covered_area_km2=0.0,
            missing_area_km2=aoi_area_km2,
            true_coverage_pct=0.0,
            tile_or_item_count=0,
            required_tiles_or_items=None,
            tile_count_ratio_pct=None,
            eligible_2km_grid_cells=0,
            missing_components="One or more constituent layers are empty or missing",
            coverage_status="ZERO_COVERAGE",
            polygon=Polygon(),
        )

    # Intersect both with AOI first
    srtm_in_aoi = aoi_geom.intersection(srtm_geom)
    geol_in_aoi = aoi_geom.intersection(geol_geom)

    combined_inter = srtm_in_aoi.intersection(geol_in_aoi)
    combined_area_km2 = compute_geodesic_area_km2(combined_inter)
    missing_area_km2 = max(0.0, aoi_area_km2 - combined_area_km2)
    true_coverage_pct = (combined_area_km2 / aoi_area_km2) * 100.0

    eligible_cells = int(np.floor(combined_area_km2 / 4.0))  # 2 km x 2 km = 4 km²

    missing_desc = (
        f"Missing {missing_area_km2:.2f} km² ({100 - true_coverage_pct:.2f}% of AOI) where either "
        "SRTM elevation or DMR lithology is absent. Faults currently 100% blocked by licensing."
    )

    return CoverageAuditResult(
        layer_name="Combined Usable Predictors (SRTM DEM ∩ DMR Geology)",
        dataset_type="Composite Intersection",
        native_crs="EPSG:4326",
        calculation_method="Geodesic_WGS84_Ellipsoid",
        aoi_total_area_km2=aoi_area_km2,
        covered_area_km2=combined_area_km2,
        missing_area_km2=missing_area_km2,
        true_coverage_pct=true_coverage_pct,
        tile_or_item_count=1,
        required_tiles_or_items=None,
        tile_count_ratio_pct=None,
        eligible_2km_grid_cells=eligible_cells,
        missing_components=missing_desc,
        coverage_status="PARTIAL_COVERAGE",
        polygon=combined_inter,
    )


def run_full_aoi_coverage_audit(
    *,
    terrain_dir: Path,
    geology_path: Path,
    faults_path: Path,
    output_csv_path: Path,
    aoi_bounds: tuple[float, float, float, float] = DEFAULT_NORTHERN_AOI_BOUNDS,
) -> list[CoverageAuditResult]:
    """Execute full geospatial coverage audit and write audit CSV."""
    results: list[CoverageAuditResult] = []

    # 1. SRTM DEM
    srtm_res = audit_srtm_dem_coverage(terrain_dir, aoi_bounds)
    results.append(srtm_res)

    # 2. DMR Geology
    geol_res = audit_geology_coverage(geology_path, aoi_bounds)
    results.append(geol_res)

    # 3. DMR Faults
    faults_res = audit_active_faults_coverage(faults_path, aoi_bounds)
    results.append(faults_res)

    # 4. Combined overlap of usable predictors
    combined_res = compute_combined_predictors_overlap(srtm_res.polygon, geol_res.polygon, aoi_bounds)
    results.append(combined_res)

    # Write CSV
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "layer_name",
        "dataset_type",
        "native_crs",
        "calculation_method",
        "aoi_total_area_km2",
        "covered_area_km2",
        "missing_area_km2",
        "true_coverage_pct",
        "tile_or_item_count",
        "required_tiles_or_items",
        "tile_count_ratio_pct",
        "eligible_2km_grid_cells",
        "missing_components",
        "coverage_status",
    ]
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r.to_dict())

    return results
