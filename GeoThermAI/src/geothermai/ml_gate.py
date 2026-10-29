"""Fail-closed ML readiness checker for GeoThermAI.

Enforces the 9 prerequisite scientific, legal, and data validation conditions
before any predictive model training, interpolation, or prospectivity mapping.
Supports both Phase 2E ('conditions') and Phase 2F ('review_requirements') schemas.
"""

from __future__ import annotations

import datetime
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Phase 2E condition names
EXPECTED_CONDITIONS: tuple[str, ...] = (
    "authoritative_label_review",
    "independent_system_group_review",
    "locked_pilot_region",
    "licensed_predictor_coverage",
    "pu_background_protocol",
    "preregistered_spatial_group_validation",
    "sufficient_independent_groups",
    "external_geographic_holdout",
    "rights_and_output_review",
)

# Phase 2F review requirement names
EXPECTED_PHASE2F_REQUIREMENTS: tuple[str, ...] = (
    "labels_verified",
    "independent_groups_verified",
    "study_area_locked",
    "predictors_licensed_and_covered",
    "pu_background_protocol_approved",
    "spatial_validation_preregistered",
    "independent_validation_feasible",
    "external_test_plan_approved",
    "output_release_approved",
)

DEFAULT_GATE_INPUT_PATH = (
    Path(__file__).resolve().parents[2]
    / "tasks"
    / "phase_2e_prediction_first"
    / "phase2e_gate_input.json"
)

DEFAULT_PHASE2F_GATE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tasks"
    / "phase_2f_scientific_validation"
    / "phase2f_gate_snapshot.json"
)


class MLGateBlockedError(RuntimeError):
    """Raised when an operation requiring ML approval is attempted while the gate is blocked."""

    def __init__(self, message: str, blocked_conditions: list[dict[str, str]] | None = None) -> None:
        super().__init__(message)
        self.blocked_conditions = blocked_conditions or []


@dataclass(frozen=True)
class GateCondition:
    name: str
    approved: bool
    evidence: str


@dataclass(frozen=True)
class GateReport:
    project: str
    snapshot_date: str | None
    decision: str
    blocked_count: int
    blocked_conditions: tuple[dict[str, str], ...]
    warning: str
    phase: str = "2E"

    @property
    def is_approved(self) -> bool:
        return self.blocked_count == 0 and self.decision in (
            "GO_FOR_REVIEWED_EXPERIMENT_PROTOCOL_ONLY",
            "GO_FOR_REVIEW_ONLY",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "project": self.project,
            "phase": self.phase,
            "snapshot_date": self.snapshot_date,
            "decision": self.decision,
            "blocked_count": self.blocked_count,
            "blocked_conditions": list(self.blocked_conditions),
            "warning": self.warning,
        }


def evaluate_phase2e_gate(payload: dict[str, Any]) -> dict[str, Any]:
    """Evaluate Phase 2E schema with 'conditions' object."""
    conditions = payload.get("conditions")
    if not isinstance(conditions, dict) or set(conditions) != set(EXPECTED_CONDITIONS):
        raise ValueError("Missing/unrecognized explicit conditions: expected exact schema")

    blocked: list[dict[str, str]] = []
    for name in EXPECTED_CONDITIONS:
        entry = conditions[name]
        if not isinstance(entry, dict) or not isinstance(entry.get("approved"), bool):
            raise ValueError(f"Invalid boolean approved flag: {name}")
        evidence = entry.get("evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError(f"Evidence field required for condition: {name}")
        if not entry["approved"]:
            blocked.append({"condition": name, "reason": evidence})

    decision = (
        "GO_FOR_REVIEWED_EXPERIMENT_PROTOCOL_ONLY"
        if not blocked
        else "NO_GO_FOR_PREDICTIVE_ML"
    )

    return {
        "project": payload.get("project", "GeoThermAI"),
        "phase": "2E",
        "snapshot_date": payload.get("snapshot_date"),
        "decision": decision,
        "blocked_count": len(blocked),
        "blocked_conditions": blocked,
        "warning": (
            "Passing a metadata gate is not model validity, training authorization, "
            "data-license clearance, or accuracy evidence. Independent review is mandatory."
        ),
    }


def evaluate_phase2f_gate(payload: dict[str, Any]) -> dict[str, Any]:
    """Evaluate Phase 2F schema with 'review_requirements' object."""
    statuses = payload.get("review_requirements")
    if not isinstance(statuses, dict):
        raise ValueError("Missing review_requirements object")

    blocked: list[dict[str, str]] = []
    for name in EXPECTED_PHASE2F_REQUIREMENTS:
        record = statuses.get(name)
        if not isinstance(record, dict):
            blocked.append({"condition": name, "reason": "Missing requirement or review record"})
            continue
        if record.get("approved") is not True:
            reason = record.get("why_blocked") or "Not approved"
            blocked.append({"condition": name, "reason": reason})
            continue
        if not all(
            isinstance(record.get(f), str) and record.get(f, "").strip()
            for f in ("reviewer", "evidence_uri", "approved_on")
        ):
            blocked.append({"condition": name, "reason": "Approved flag without evidence, reviewer, or date"})
            continue
        try:
            approved_on = datetime.date.fromisoformat(record["approved_on"])
        except (ValueError, TypeError):
            blocked.append({"condition": name, "reason": "Approval date must be ISO YYYY-MM-DD"})
            continue
        if approved_on > datetime.datetime.now(datetime.timezone.utc).date():
            blocked.append({"condition": name, "reason": "Approval date is in the future"})
            continue

    decision = "GO_FOR_REVIEW_ONLY" if not blocked else "NO_GO_FOR_PREDICTIVE_ML"

    return {
        "project": payload.get("project", "GeoThermAI"),
        "phase": payload.get("phase", "2F"),
        "snapshot_date": payload.get("snapshot_date"),
        "decision": decision,
        "blocked_count": len(blocked),
        "blocked_conditions": blocked,
        "warning": (
            "GO_FOR_REVIEW_ONLY is NOT authorization to train; confirm the repository gate "
            "and independent approvals."
        ),
    }


def evaluate_gate(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate schema and compute fail-closed gate decision across Phase 2E or 2F.

    Raises:
        ValueError: If payload structure, condition keys, or evidence strings are invalid.
    """
    if not isinstance(payload, dict):
        raise ValueError("Gate payload must be a JSON object dictionary")

    if "review_requirements" in payload:
        return evaluate_phase2f_gate(payload)
    elif "conditions" in payload:
        return evaluate_phase2e_gate(payload)
    else:
        raise ValueError("Missing/unrecognized explicit conditions: expected exact schema")


def evaluate_gate_file(path: Path | str) -> GateReport:
    """Read a JSON gate file and return a GateReport dataclass."""
    gate_path = Path(path)
    if not gate_path.is_file():
        raise FileNotFoundError(f"Gate input file not found: {gate_path}")

    payload = json.loads(gate_path.read_text(encoding="utf-8"))
    raw_report = evaluate_gate(payload)
    return GateReport(
        project=raw_report["project"],
        phase=raw_report.get("phase", "2E"),
        snapshot_date=raw_report["snapshot_date"],
        decision=raw_report["decision"],
        blocked_count=raw_report["blocked_count"],
        blocked_conditions=tuple(raw_report["blocked_conditions"]),
        warning=raw_report["warning"],
    )


def enforce_ml_gate(gate_input_path: Path | str | None = None) -> GateReport:
    """Check readiness gate and fail closed if blocked.

    Raises:
        MLGateBlockedError: If one or more gate conditions are unapproved.
    """
    path = Path(gate_input_path) if gate_input_path is not None else DEFAULT_GATE_INPUT_PATH
    report = evaluate_gate_file(path)
    if not report.is_approved:
        reasons = "; ".join(f"{b['condition']}: {b['reason']}" for b in report.blocked_conditions)
        raise MLGateBlockedError(
            f"Predictive ML gate is NO-GO ({report.blocked_count} blocking conditions): {reasons}",
            blocked_conditions=list(report.blocked_conditions),
        )
    return report


def main(argv: list[str]) -> int:
    """CLI entrypoint compatible with Phase 2E and Phase 2F specifications."""
    if len(argv) != 2:
        print("Usage: python -m geothermai.ml_gate <gate_input.json>", file=sys.stderr)
        return 1
    try:
        report = evaluate_gate_file(argv[1])
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
        return 0 if report.is_approved else 2
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"INVALID_GATE_INPUT: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
