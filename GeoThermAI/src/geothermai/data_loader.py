"""Local-file ingestion for the GeoThermAI evidence explorer."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from pyproj import Transformer

from .data_validation import ValidationResult, validate_observations


@dataclass(frozen=True)
class LayerLoadResult:
    layer_id: str
    available: bool
    usable: bool
    message: str
    data: dict[str, Any] | None = None


def require_file(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(f"Required local input is unavailable: {path}")
    return path


def load_observations(path: Path) -> tuple[pd.DataFrame, ValidationResult]:
    frame = pd.read_csv(require_file(path), dtype="string", keep_default_na=False)
    # These are derived display fields. Source columns are retained unchanged in the frame.
    for column in ("derived_longitude_wgs84", "derived_latitude_wgs84", "surface_temperature_c"):
        if column in frame:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame, validate_observations(frame)


def load_csv_inventory(path: Path) -> pd.DataFrame:
    return pd.read_csv(require_file(path), dtype="string", keep_default_na=False)


def inspect_optional_file(path: Path, label: str) -> LayerLoadResult:
    if not path.is_file():
        return LayerLoadResult(label, False, False, f"Local file is unavailable: {path.name}")
    return LayerLoadResult(label, True, True, f"Local file is available: {path.name}")


def load_vector_layer(path: Path, layer_id: str) -> LayerLoadResult:
    """Open GeoJSON, GeoPackage, or shapefile defensively and report CRS/geometry readiness."""

    if not path.is_file():
        return LayerLoadResult(layer_id, False, False, f"Vector file is unavailable: {path.name}")
    try:
        import geopandas as gpd

        layer = gpd.read_file(path)
        if layer.crs is None:
            return LayerLoadResult(layer_id, True, False, "Vector file has no CRS information.")
        invalid = int((~layer.geometry.is_valid).sum())
        if invalid:
            return LayerLoadResult(
                layer_id, True, False, f"Vector file has {invalid} invalid geometries."
            )
        return LayerLoadResult(
            layer_id,
            True,
            True,
            f"Loaded {len(layer)} valid geometries with CRS {layer.crs.to_string()}.",
            {"feature_count": len(layer), "crs": layer.crs.to_string()},
        )
    except Exception as exc:  # GeoPandas exposes driver-specific exception types.
        return LayerLoadResult(layer_id, True, False, f"Vector layer could not be read: {exc}")


def load_raster_metadata(path: Path, layer_id: str) -> LayerLoadResult:
    """Inspect raster metadata only; no raster values are invented or resampled here."""

    if not path.is_file():
        return LayerLoadResult(layer_id, False, False, f"Raster file is unavailable: {path.name}")
    try:
        import rasterio

        with rasterio.open(path) as dataset:
            if dataset.crs is None:
                return LayerLoadResult(layer_id, True, False, "Raster file has no CRS information.")
            return LayerLoadResult(
                layer_id,
                True,
                True,
                f"Raster metadata read: {dataset.width}×{dataset.height}, CRS {dataset.crs}.",
                {
                    "width": dataset.width,
                    "height": dataset.height,
                    "crs": str(dataset.crs),
                    "bounds": tuple(dataset.bounds),
                    "nodata": dataset.nodata,
                },
            )
    except Exception as exc:
        return LayerLoadResult(layer_id, True, False, f"Raster metadata could not be read: {exc}")


def _transform_esri_geometry(value: Any, transformer: Transformer) -> Any:
    if isinstance(value, list):
        if len(value) >= 2 and all(isinstance(v, (int, float)) for v in value[:2]):
            lon, lat = transformer.transform(value[0], value[1])
            return [lon, lat, *value[2:]]
        return [_transform_esri_geometry(item, transformer) for item in value]
    return value


def load_rock_units_geojson(path: Path) -> LayerLoadResult:
    """Convert the verified local ESRI JSON layer from EPSG:32647 for visual context only."""

    if not path.is_file():
        return LayerLoadResult(
            "DMR_ROCK_UNIT_250K_NORTH", False, False, "Rock-unit geometry file is unavailable."
        )
    try:
        source = json.loads(path.read_text(encoding="utf-8"))
        transformer = Transformer.from_crs("EPSG:32647", "EPSG:4326", always_xy=True)
        features = []
        for item in source.get("features", []):
            geometry = item.get("geometry", {})
            rings = geometry.get("rings")
            if not rings:
                continue
            features.append(
                {
                    "type": "Feature",
                    "properties": {
                        "source_layer": "DMR_ROCK_UNIT_250K_NORTH",
                        "symbol": item.get("attributes", {}).get("TEXT_SYM", "Not supplied"),
                        "year": item.get("attributes", {}).get("YEAR_COMPI", "Not supplied"),
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": _transform_esri_geometry(rings, transformer),
                    },
                }
            )
        if not features:
            return LayerLoadResult(
                "DMR_ROCK_UNIT_250K_NORTH", True, False, "No valid polygon geometries were found."
            )
        return LayerLoadResult(
            "DMR_ROCK_UNIT_250K_NORTH",
            True,
            True,
            f"Loaded {len(features)} rock-unit polygons as descriptive map context.",
            {"type": "FeatureCollection", "features": features},
        )
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        return LayerLoadResult(
            "DMR_ROCK_UNIT_250K_NORTH", True, False, f"Rock-unit layer could not be read: {exc}"
        )
