import json
from copy import deepcopy
from pathlib import Path

import pytest

from geothermai.ml_gate import (
    DEFAULT_GATE_INPUT_PATH,
    EXPECTED_CONDITIONS,
    MLGateBlockedError,
    enforce_ml_gate,
    evaluate_gate,
    evaluate_gate_file,
    main,
)
from geothermai.model_interface import (
    assert_predictive_model_ready,
    predictive_model_status,
)


@pytest.fixture
def gate_payload():
    return json.loads(DEFAULT_GATE_INPUT_PATH.read_text(encoding="utf-8"))


def test_phase2e_snapshot_is_no_go(gate_payload):
    result = evaluate_gate(gate_payload)
    assert result["decision"] == "NO_GO_FOR_PREDICTIVE_ML"
    assert result["blocked_count"] == len(EXPECTED_CONDITIONS)
    assert result["blocked_count"] == 9
    assert len(result["blocked_conditions"]) == 9


def test_single_unapproved_condition_blocks_gate(gate_payload):
    synthetic = deepcopy(gate_payload)
    for entry in synthetic["conditions"].values():
        entry["approved"] = True  # synthetic fixture only

    synthetic["conditions"]["licensed_predictor_coverage"]["approved"] = False
    result = evaluate_gate(synthetic)
    assert result["decision"] == "NO_GO_FOR_PREDICTIVE_ML"
    assert result["blocked_count"] == 1
    assert result["blocked_conditions"][0]["condition"] == "licensed_predictor_coverage"


def test_all_approved_returns_reviewed_experiment_decision(gate_payload):
    synthetic = deepcopy(gate_payload)
    for entry in synthetic["conditions"].values():
        entry["approved"] = True  # synthetic fixture only

    result = evaluate_gate(synthetic)
    assert result["decision"] == "GO_FOR_REVIEWED_EXPERIMENT_PROTOCOL_ONLY"
    assert result["blocked_count"] == 0
    assert result["blocked_conditions"] == []


def test_missing_condition_fails_closed(gate_payload):
    synthetic = deepcopy(gate_payload)
    del synthetic["conditions"]["authoritative_label_review"]
    with pytest.raises(ValueError, match="Missing/unrecognized explicit conditions"):
        evaluate_gate(synthetic)


def test_blank_evidence_fails_closed(gate_payload):
    synthetic = deepcopy(gate_payload)
    synthetic["conditions"]["locked_pilot_region"] = {"approved": True, "evidence": "  "}
    with pytest.raises(ValueError, match="Evidence field required"):
        evaluate_gate(synthetic)


def test_invalid_approved_type_fails_closed(gate_payload):
    synthetic = deepcopy(gate_payload)
    synthetic["conditions"]["locked_pilot_region"] = {"approved": "yes", "evidence": "something"}
    with pytest.raises(ValueError, match="Invalid boolean approved flag"):
        evaluate_gate(synthetic)


def test_enforce_ml_gate_raises_blocked_error():
    with pytest.raises(MLGateBlockedError) as exc_info:
        enforce_ml_gate()
    assert len(exc_info.value.blocked_conditions) == 9
    assert "Predictive ML gate is NO-GO" in str(exc_info.value)


def test_model_interface_assert_predictive_model_ready_raises():
    with pytest.raises(MLGateBlockedError):
        assert_predictive_model_ready()


def test_predictive_model_status_reflects_gate():
    status = predictive_model_status()
    assert not status.enabled
    assert status.gate_decision == "NO_GO_FOR_PREDICTIVE_ML"
    assert status.blocked_condition_count == 9


def test_gate_cli_exit_code_on_blocked(tmp_path):
    gate_file = tmp_path / "gate.json"
    gate_file.write_text(DEFAULT_GATE_INPUT_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    exit_code = main(["ml_gate_check.py", str(gate_file)])
    assert exit_code == 2


def test_gate_cli_exit_code_on_invalid_input(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{}", encoding="utf-8")
    exit_code = main(["ml_gate_check.py", str(invalid_file)])
    assert exit_code == 1
