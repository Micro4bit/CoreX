"""Contract placeholder for future authorized predictive research."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FutureModelContract:
    enabled: bool = False
    status: str = "Predictive model not yet validated or enabled."
    required_inputs: tuple[str, ...] = (
        "documented feature schema",
        "source-to-variable provenance",
        "spatially valid evaluation design",
        "uncertainty specification",
    )
    required_outputs: tuple[str, ...] = (
        "prediction schema",
        "uncertainty fields",
        "model and validation metadata",
        "provenance requirements",
    )


def predictive_model_status() -> FutureModelContract:
    return FutureModelContract()
