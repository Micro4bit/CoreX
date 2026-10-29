import json
import unittest
from copy import deepcopy
from pathlib import Path

from ml_gate_check import EXPECTED, evaluate_gate


class GateTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((Path(__file__).parent / "phase2e_gate_input.json").read_text(encoding="utf-8"))

    def test_phase2d_snapshot_is_no_go(self):
        result = evaluate_gate(self.fixture)
        self.assertEqual(result["decision"], "NO_GO_FOR_PREDICTIVE_ML")
        self.assertEqual(result["blocked_count"], len(EXPECTED))

    def test_single_unresolved_flag_blocks_gate(self):
        example = deepcopy(self.fixture)
        for entry in example["conditions"].values():
            entry["approved"] = True  # synthetic logical fixture, NOT actual evidence approval
        example["conditions"]["licensed_predictor_coverage"]["approved"] = False
        self.assertEqual(evaluate_gate(example)["blocked_count"], 1)

    def test_missing_condition_fails_closed(self):
        example = deepcopy(self.fixture)
        del example["conditions"]["authoritative_label_review"]
        with self.assertRaises(ValueError):
            evaluate_gate(example)

    def test_no_blank_evidence_even_if_flag_true(self):
        example = deepcopy(self.fixture)
        example["conditions"]["locked_pilot_region"] = {"approved": True, "evidence": ""}
        with self.assertRaises(ValueError):
            evaluate_gate(example)


if __name__ == "__main__":
    unittest.main()
