"""Coordinate-display rules that preserve uncertainty rather than correcting sources."""

from __future__ import annotations

import pandas as pd

from config.settings import COORDINATE_REVIEW_STATUSES, PROVISIONAL_STATUSES


def coordinate_category(status: str) -> str:
    if status in COORDINATE_REVIEW_STATUSES:
        return "review_required"
    if status in PROVISIONAL_STATUSES:
        return "provisional"
    if status == "CRS_AND_DMS_CONSISTENT":
        return "consistent"
    return "unknown"


def displayable_observations(
    observations: pd.DataFrame, include_provisional: bool = False
) -> pd.DataFrame:
    """Return valid map points; review-required locations are never plotted as certain."""

    result = observations.copy()
    result["longitude"] = pd.to_numeric(result["derived_longitude_wgs84"], errors="coerce")
    result["latitude"] = pd.to_numeric(result["derived_latitude_wgs84"], errors="coerce")
    result["coordinate_category"] = result["coordinate_validation_status"].map(
        coordinate_category
    )
    usable = result["longitude"].between(-180, 180) & result["latitude"].between(-90, 90)
    usable &= result["coordinate_category"].ne("review_required")
    if not include_provisional:
        usable &= result["coordinate_category"].eq("consistent")
    return result.loc[usable].copy()


def map_color(category: str) -> list[int]:
    return {
        "consistent": [30, 136, 229, 220],
        "provisional": [245, 158, 11, 220],
        "review_required": [220, 38, 38, 220],
    }.get(category, [100, 116, 139, 200])
