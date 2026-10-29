"""Automated test for Phase 2G ML Gate Evaluation and Fail-Closed Governance."""

from pathlib import Path
import pytest

from geothermai.ml_gate import evaluate_gate_file

PHASE2G_DIR = Path(__file__).resolve().parents[1] / "tasks" / "phase_2g_thailand_readiness_and_decision_support"
GATE_REPORT_JSON = PHASE2G_DIR / "PHASE2G_ML_GATE_REPORT.json"


def test_phase2g_gate_is_strictly_fail_closed():
    assert GATE_REPORT_JSON.is_file(), f"Phase 2G gate report not found at {GATE_REPORT_JSON}"
    report = evaluate_gate_file(GATE_REPORT_JSON)
    assert not report.is_approved
    assert report.decision == "NO_GO_FOR_PREDICTIVE_ML"
    assert report.blocked_count == 9
    assert report.phase == "2G"
    
    # Verify blocking reasons exist for all 9 requirements
    blocked_conditions = {b["condition"] for b in report.blocked_conditions}
    assert "labels_verified" in blocked_conditions
    assert "independent_groups_verified" in blocked_conditions
    assert "study_area_locked" in blocked_conditions
    assert "predictors_licensed_and_covered" in blocked_conditions
    assert "pu_background_protocol_approved" in blocked_conditions
    assert "spatial_validation_preregistered" in blocked_conditions
    assert "independent_validation_feasible" in blocked_conditions
    assert "external_test_plan_approved" in blocked_conditions
    assert "output_release_approved" in blocked_conditions
