#!/usr/bin/env python3
"""Research-readiness preflight. DOES NOT train models or certify scientific validity.

Exit codes: 0 all nine documented approvals present; 2 blocked; 1 invalid file/usage.
The sign-offs supplied in JSON must be checked by real responsible reviewers.
"""
import argparse
import datetime
import json
from pathlib import Path
import sys

REQUIRED = (
    'labels_verified',
    'independent_groups_verified',
    'study_area_locked',
    'predictors_licensed_and_covered',
    'pu_background_protocol_approved',
    'spatial_validation_preregistered',
    'independent_validation_feasible',
    'external_test_plan_approved',
    'output_release_approved',
)


def inspect_gate(obj):
    if not isinstance(obj, dict) or not isinstance(obj.get('review_requirements'), dict):
        raise ValueError('Missing review_requirements object')
    statuses = obj['review_requirements']
    blocked = {}
    for name in REQUIRED:
        record = statuses.get(name)
        if not isinstance(record, dict):
            blocked[name] = 'Missing requirement or review record'
            continue
        if record.get('approved') is not True:
            blocked[name] = record.get('why_blocked') or 'Not approved'
            continue
        if not all(isinstance(record.get(f), str) and record.get(f).strip() for f in ('reviewer','evidence_uri','approved_on')):
            blocked[name] = 'Approved flag without evidence, reviewer, or date'
            continue
        try:
            approved_on = datetime.date.fromisoformat(record['approved_on'])
        except ValueError:
            blocked[name] = 'Approval date must be ISO YYYY-MM-DD'
            continue
        if approved_on > datetime.datetime.now(datetime.timezone.utc).date():
            blocked[name] = 'Approval date is in the future'
    # Unknown keys do not substitute for required conditions.
    return {'decision':'GO_FOR_REVIEW_ONLY' if not blocked else 'NO_GO_FOR_PREDICTIVE_ML',
            'requirements_total':len(REQUIRED),
            'conditions_blocked':len(blocked),
            'blockers':blocked,
            'warning':'GO_FOR_REVIEW_ONLY is NOT authorization to train; confirm the repository gate and independent approvals.'}


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gate',default=str(Path(__file__).with_name('phase2f_gate_snapshot.json')))
    parser.add_argument('--output',help='Optional machine-readable report file')
    args=parser.parse_args(argv)
    try:
        report=inspect_gate(json.loads(Path(args.gate).read_text(encoding='utf-8')))
        if args.output:
            Path(args.output).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 2 if report['conditions_blocked'] else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print('Invalid preflight input: '+str(exc),file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(cli())
