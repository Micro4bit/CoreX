# GeoThermAI Phase 2E — Portable Research & Gate Package

Created on 2026-10-26 from the four uploaded Phase 2D summary reports plus research verified via original publisher / USGS records. This is **not a Git commit or a merge to the previous development repository**; the original project tree and Phase 2D task directory were not present among the supplied files in this chat.

Files:

- `PHASE2E_PREDICTION_FIRST_PLAN.md` — revised scope, baseline facts, candidate features, hypotheses, gate and validation protocol.
- `RESEARCH_EVIDENCE_MATRIX.md` — 12 *additional* scholarly records, their evidence and cautions. New vs existing anchor PDFs are identified.
- `COMPETITION_PROPOSAL_CORE_TH.md` — usable Thai draft content based on new prediction-first scope (not the final form).
- `phase2e_gate_input.json` — frozen Phase 2D-derived NO-GO evidence flags.
- `ml_gate_check.py` — executable fail-closed readiness checker; never fits, interpolates or predicts.
- `test_ml_gate_check.py` — unit tests for gate logic, not model performance.

Run locally:

```bash
python -m unittest -v test_ml_gate_check.py
python ml_gate_check.py phase2e_gate_input.json
```

The second command **should return exit code 2** and list nine blocking conditions. Do not override `approved=false` without documented verification of the underlying evidence by appropriate experts / data owners.

**Handoff into source repository (not done):** place this package under a research task folder, reconcile its feature/gate values against the actual source files, add gate check to the research CI, and keep existing no-prediction UI gates until the domain review permits experimentation. If Phase 2D summaries and source disagree, inspect original datasets and maintain stricter control until resolved.
