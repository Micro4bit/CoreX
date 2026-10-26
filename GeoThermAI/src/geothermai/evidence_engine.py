"""Descriptive evidence availability; deliberately no scoring or prediction logic."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class EvidenceAvailability:
    record_uid: str
    coordinate_status: str
    available_layer_ids: tuple[str, ...]
    unavailable_or_restricted_layer_ids: tuple[str, ...]
    interpretation_notice: str


def describe_evidence_availability(
    record: pd.Series, layers: pd.DataFrame
) -> EvidenceAvailability:
    """Report available context without weights, scores, or geothermal inference."""

    status = layers["access_status"].fillna("")
    usable_mask = status.str.startswith("VERIFIED") & ~status.str.contains(
        "UNAVAILABLE", case=False
    )
    available = layers.loc[usable_mask, "layer_id"].tolist()
    restricted = layers.loc[~usable_mask, "layer_id"].tolist()
    return EvidenceAvailability(
        record_uid=str(record["record_uid"]),
        coordinate_status=str(record["coordinate_validation_status"]),
        available_layer_ids=tuple(available),
        unavailable_or_restricted_layer_ids=tuple(restricted),
        interpretation_notice=(
            "Evidence availability is descriptive only; no geothermal-potential score or "
            "prediction is calculated."
        ),
    )
