# GeoThermAI — Phase 2F (27 October 2026)

## Objective
Prediction-first DATA & SCIENTIFIC VALIDATION READINESS. Continue Phase 2E, do not rebuild the application. The uploaded Phase 2E report describes working architecture and passing tests; the actual project source tree was **not provided in this conversation**, so these are portable review artifacts, not claimed repository commits.

## Current result
- **NO-GO for predictive ML** (9 outstanding approval conditions in the documented readiness gate).
- Expert review and license approval **have not** been obtained.
- Phase 2F produces a documented triage, draft templates, scientific validation design and safe, testable readiness preflight—not a prediction model, map, calibrated probability or drilling forecast.
- `GO_FOR_REVIEW_ONLY` from the portable preflight does **not** override the actual project's `geothermai.ml_gate`.

## Content
- `PHASE2F_SCIENTIFIC_TRIAGE_TH.md`: priority, evidence and concrete blockers.
- `PHASE2F_LABEL_ADJUDICATION_TH.md` + `expert_system_review_template.csv`: independent geothermal grouping decisions for geologists; no invented records.
- `PHASE2F_PILOT_AND_FEATURE_GATE_TH.md`: pilot location/coverage/license decision gates.
- `PHASE2F_SPATIAL_VALIDATION_TH.md`: PU handling, leakage, buffer sensitivity, holdouts, outputs.
- `PHASE2F_REFERENCE_UPDATE.md`: directly verified references and implications.
- `DMR_DATA_PERMISSION_REQUEST_TH.md`: a draft for requesting DMR clarification.
- `MASTER_PROMPT_PHASE2F.md`: Codex instruction to integrate with a real repository safely.
- `phase2f_gate_snapshot.json`, `phase2f_preflight.py`, `test_phase2f_preflight.py`: portable gate snapshot, checker and tests.
- `SOURCE_REPORT_HASHES.json`: checksums for user-provided reports only (NOT checksums for unseen original datasets).

## Reproduce the portable checks
```
python3 -m unittest -v test_phase2f_preflight.py
python3 phase2f_preflight.py --gate phase2f_gate_snapshot.json
```
Expected: tests PASS; checker exits 2 and says `NO_GO_FOR_PREDICTIVE_ML`.

## Source constraints
Fact source: uploaded PHASE2D_DATA_READINESS.md, PHASE2D_ML_GATE.md, PHASE2E_IMPLEMENTATION_REPORT.md. Supplemental citations are explicit URLs in the references file. Internal reports are secondary claims about the repo; a Codex agent must compare them against real source files and actual tests.
