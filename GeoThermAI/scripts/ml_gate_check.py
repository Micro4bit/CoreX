#!/usr/bin/env python3
"""Fail-closed ML readiness checker. DOES NOT train a model or read geospatial data.

Usage: python ml_gate_check.py phase2e_gate_input.json
Exit 0 only for an explicitly reviewed and evidence-bearing complete gate;
exit 2 if blocked; exit 1 for invalid/incomplete input.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add src to path if executed standalone from scripts or root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from geothermai.ml_gate import EXPECTED_CONDITIONS as EXPECTED, evaluate_gate, main
except ImportError:
    # Standalone fallback if package structure is unavailable
    import json

    EXPECTED = (
        "authoritative_label_review", "independent_system_group_review",
        "locked_pilot_region", "licensed_predictor_coverage",
        "pu_background_protocol", "preregistered_spatial_group_validation",
        "sufficient_independent_groups", "external_geographic_holdout",
        "rights_and_output_review",
    )

    def evaluate_gate(payload: dict) -> dict:
        conditions = payload.get("conditions")
        if not isinstance(conditions, dict) or set(conditions) != set(EXPECTED):
            raise ValueError("Missing/unrecognized explicit conditions: expected exact schema")
        blocked = []
        for name in EXPECTED:
            entry = conditions[name]
            if not isinstance(entry, dict) or not isinstance(entry.get("approved"), bool):
                raise ValueError(f"Invalid boolean approved flag: {name}")
            evidence = entry.get("evidence")
            if not isinstance(evidence, str) or not evidence.strip():
                raise ValueError(f"Evidence field required for condition: {name}")
            if not entry["approved"]:
                blocked.append({"condition": name, "reason": evidence})
        return {
            "project": payload.get("project", "Unknown"),
            "snapshot_date": payload.get("snapshot_date"),
            "decision": "GO_FOR_REVIEWED_EXPERIMENT_PROTOCOL_ONLY" if not blocked else "NO_GO_FOR_PREDICTIVE_ML",
            "blocked_count": len(blocked), "blocked_conditions": blocked,
            "warning": "Passing a metadata gate is not model validity, training authorization, data-license clearance, or accuracy evidence. Independent review is mandatory.",
        }

    def main(argv: list[str]) -> int:
        if len(argv) != 2:
            print("Usage: python ml_gate_check.py phase2e_gate_input.json", file=sys.stderr)
            return 1
        try:
            payload = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
            report = evaluate_gate(payload)
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            print(f"INVALID_GATE_INPUT: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["blocked_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
