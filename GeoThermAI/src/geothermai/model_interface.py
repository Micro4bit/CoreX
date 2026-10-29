"""Contract and interface for future authorized predictive research."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .ml_gate import (
    DEFAULT_GATE_INPUT_PATH,
    MLGateBlockedError,
    enforce_ml_gate,
    evaluate_gate_file,
)


@dataclass(frozen=True)
class FutureModelContract:
    enabled: bool = False
    status: str = "Predictive model not yet validated or enabled."
    gate_decision: str = "NO_GO_FOR_PREDICTIVE_ML"
    gate_status: str = "Predictive model not yet validated or enabled. ML Gate: NO_GO_FOR_PREDICTIVE_ML (9 blocking conditions)."
    blocked_condition_count: int = 9
    required_inputs: tuple[str, ...] = (
        "documented feature schema",
        "source-to-variable provenance",
        "spatially valid evaluation design",
        "uncertainty specification",
        "positive-unlabeled / background design",
        "independent-system label review",
        "contiguous licensed predictor coverage",
    )
    required_outputs: tuple[str, ...] = (
        "prediction schema",
        "uncertainty fields",
        "model and validation metadata",
        "provenance requirements",
        "feature attribution / explainability",
    )


def predictive_model_status(gate_path: Path | str | None = None) -> FutureModelContract:
    """Return the current research model contract based on fail-closed gate evaluation."""
    target_path = Path(gate_path) if gate_path is not None else DEFAULT_GATE_INPUT_PATH
    try:
        report = evaluate_gate_file(target_path)
        is_approved = report.is_approved
        decision = report.decision
        blocked_count = report.blocked_count
        status_msg = (
            "Ready for pre-registered experiment protocol only."
            if is_approved
            else "Predictive model not yet validated or enabled."
        )
        gate_status_msg = (
            "Ready for pre-registered experiment protocol only."
            if is_approved
            else f"Predictive model not yet validated or enabled. ML Gate: {decision} ({blocked_count} blocking conditions)."
        )
    except Exception as exc:
        is_approved = False
        decision = "GATE_EVALUATION_ERROR"
        blocked_count = 9
        status_msg = "Predictive model not yet validated or enabled."
        gate_status_msg = f"Predictive model disabled: failed to evaluate gate ({exc})."

    return FutureModelContract(
        enabled=is_approved,
        status=status_msg,
        gate_decision=decision,
        gate_status=gate_status_msg,
        blocked_condition_count=blocked_count,
    )


def assert_predictive_model_ready(gate_path: Path | str | None = None) -> None:
    """Enforce fail-closed gate before any predictive model instantiation or training.

    Raises:
        MLGateBlockedError: If one or more gate prerequisites remain unapproved.
    """
    enforce_ml_gate(gate_path)
