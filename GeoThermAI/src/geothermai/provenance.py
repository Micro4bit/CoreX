"""Traceability helpers for source records and downloadable evidence summaries."""

from __future__ import annotations

from datetime import date

import pandas as pd


PROVENANCE_FIELDS = [
    "record_uid",
    "source_id",
    "source_region",
    "source_record_code",
    "source_site_name",
    "source_easting_m",
    "source_northing_m",
    "reported_coordinate_reference",
    "working_coordinate_reference",
    "derived_longitude_wgs84",
    "derived_latitude_wgs84",
    "coordinate_validation_status",
    "coordinate_quality_note",
    "license_or_reuse_status",
    "source_location",
    "source_url",
]


def record_provenance(record: pd.Series) -> pd.DataFrame:
    fields = [field for field in PROVENANCE_FIELDS if field in record.index]
    return pd.DataFrame({"field": fields, "value": [record[field] for field in fields]})


def evidence_summary_markdown(record: pd.Series, gis_layers: pd.DataFrame) -> str:
    """Generate a descriptive record summary; intentionally contains no potential score."""

    lines = [
        "# GeoThermAI evidence summary",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Scientific scope",
        "This is a source-traceability and evidence-availability summary. It is not a geothermal potential score, resource estimate, or prediction.",
        "",
        "## Published observation",
    ]
    for label, field in [
        ("Record", "record_uid"),
        ("Source", "source_id"),
        ("Region", "source_region"),
        ("Reported coordinates", "reported_coordinate_reference"),
        ("Working CRS", "working_coordinate_reference"),
        ("Coordinate status", "coordinate_validation_status"),
        ("Coordinate note", "coordinate_quality_note"),
        ("Reuse status", "license_or_reuse_status"),
        ("Source URL", "source_url"),
    ]:
        value = record.get(field, "Not available")
        lines.append(f"- {label}: {value or 'Not available'}")
    lines.extend(["", "## GIS context availability"])
    for _, layer in gis_layers.iterrows():
        lines.append(
            f"- {layer['layer_id']}: {layer['access_status']}; "
            f"reuse: {layer['license_or_permission_status'] or 'not stated'}"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "Layer availability or overlap is descriptive context only. It must not be interpreted as evidence of a commercial reservoir or probability of discovery.",
        ]
    )
    return "\n".join(lines) + "\n"
