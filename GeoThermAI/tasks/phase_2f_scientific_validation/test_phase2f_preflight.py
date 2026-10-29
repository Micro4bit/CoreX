import copy
import json
import unittest
from pathlib import Path
from phase2f_preflight import inspect_gate, REQUIRED, cli

BASE=json.loads(Path(__file__).with_name('phase2f_gate_snapshot.json').read_text(encoding='utf-8'))
class TestPreflight(unittest.TestCase):
    def test_frozen_phase2f_no_go(self):
        report=inspect_gate(BASE)
        self.assertEqual(report['decision'],'NO_GO_FOR_PREDICTIVE_ML')
        self.assertEqual(report['conditions_blocked'],9)
    def test_cli_exit_code_2(self):
        self.assertEqual(cli(['--gate',str(Path(__file__).with_name('phase2f_gate_snapshot.json'))]),2)
    def test_missing_keys_fail_closed(self):
        candidate=copy.deepcopy(BASE)
        del candidate['review_requirements']['labels_verified']
        self.assertIn('labels_verified',inspect_gate(candidate)['blockers'])
    def test_true_bool_without_evidence_still_blocked(self):
        candidate=copy.deepcopy(BASE)
        for key in REQUIRED: candidate['review_requirements'][key]['approved']=True
        self.assertEqual(inspect_gate(candidate)['conditions_blocked'],9)
    def test_only_complete_review_records_clear_preflight(self):
        candidate=copy.deepcopy(BASE)
        for key in REQUIRED:
            x=candidate['review_requirements'][key]
            x.update(approved=True,evidence_uri='internal://review/evidence/'+key,reviewer='domain-qualified reviewer',approved_on='2026-10-27')
        self.assertEqual(inspect_gate(candidate)['decision'],'GO_FOR_REVIEW_ONLY')
    def test_future_dated_review_blocked(self):
        candidate=copy.deepcopy(BASE)
        for key in REQUIRED:
            x=candidate['review_requirements'][key]
            x.update(approved=True,evidence_uri='internal://review/evidence',reviewer='reviewer',approved_on='2999-10-27')
        self.assertEqual(inspect_gate(candidate)['conditions_blocked'],9)
    def test_invalid_schema(self):
        with self.assertRaises(ValueError):inspect_gate({})
if __name__=='__main__':unittest.main()
