"""Validation routines for source-preserving geothermal observation tables."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


REQUIRED_OBSERVATION_COLUMNS = {
    "record_uid",
    "source_id",
    "source_region",
    "source_record_code",
    "source_easting_m",
    "source_northing_m",
    "reported_coordinate_reference",
    "working_coordinate_reference",
    "derived_longitude_wgs84",
    "derived_latitude_wgs84",
    "coordinate_validation_status",
    "coordinate_quality_note",
    "license_or_reuse_status",
    "source_url",
}


@dataclass(frozen=True)
class ValidationResult:
    """Issues found without altering the source table."""

    missing_columns: tuple[str, ...]
    duplicate_record_ids: tuple[str, ...]
    invalid_coordinate_ids: tuple[str, ...]
    missing_crs_ids: tuple[str, ...]
    missing_temperature_ids: tuple[str, ...]

    @property
    def is_schema_valid(self) -> bool:
        return not self.missing_columns


def _nonempty(series: pd.Series) -> pd.Series:
    return series.notna() & series.astype(str).str.strip().ne("")


def validate_observations(frame: pd.DataFrame) -> ValidationResult:
    """Validate required fields and display coordinates without imputing any values."""

    missing_columns = tuple(sorted(REQUIRED_OBSERVATION_COLUMNS - set(frame.columns)))
    if missing_columns:
        return ValidationResult(missing_columns, (), (), (), ())

    record_ids = frame["record_uid"].astype(str)
    duplicate_ids = tuple(sorted(record_ids[record_ids.duplicated(keep=False)].unique()))
    longitudes = pd.to_numeric(frame["derived_longitude_wgs84"], errors="coerce")
    latitudes = pd.to_numeric(frame["derived_latitude_wgs84"], errors="coerce")
    longitude_supplied = _nonempty(frame["derived_longitude_wgs84"])
    latitude_supplied = _nonempty(frame["derived_latitude_wgs84"])
    invalid_mask = (
        (longitude_supplied & (longitudes.isna() | ~longitudes.between(-180, 180)))
        | (latitude_supplied & (latitudes.isna() | ~latitudes.between(-90, 90)))
    )
    invalid_ids = tuple(record_ids[invalid_mask].tolist())
    crs_mask = ~_nonempty(frame["reported_coordinate_reference"]) | ~_nonempty(
        frame["working_coordinate_reference"]
    )
    missing_crs_ids = tuple(record_ids[crs_mask].tolist())
    if "surface_temperature_c" not in frame.columns:
        missing_temperature_ids: tuple[str, ...] = tuple(record_ids.tolist())
    else:
        temperatures = pd.to_numeric(frame["surface_temperature_c"], errors="coerce")
        missing_temperature_ids = tuple(record_ids[temperatures.isna()].tolist())
    return ValidationResult(
        (), duplicate_ids, invalid_ids, missing_crs_ids, missing_temperature_ids
    )


def missing_required_columns(columns: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(REQUIRED_OBSERVATION_COLUMNS - set(columns)))
