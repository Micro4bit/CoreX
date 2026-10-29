# GeoThermAI — PHASE 2F MASTER PROMPT FOR CODEX

You are the Lead Geothermal Research Engineer, Geospatial Data Scientist, Research Data Steward and Senior Software Engineer.

## Mission
CONTINUE the existing GeoThermAI repository from Phase 2E. Do not rebuild the app. The new focus is **Prediction Data and Scientific Validation Readiness**. Prediction remains the research objective, but the current gate is **NO-GO**. Do not fit, save, or display predictive models unless the real repository's gate legitimately passes with auditable, independent scientific approvals.

## Start by inspecting real sources
1. Read the repository's Phase 2D and Phase 2E reports plus tests, source files, datasets and licenses. The portable Phase 2F package is supplementary, not proof that the repo has been modified.
2. Inspect `src/geothermai/ml_gate.py`, `prediction_architecture.py`, source datasets and test suites. Reconcile reported `41 pytest / 4 unittest / 25 web` with fresh executions; never report past test claims as newly run results.
3. Read `PHASE2F_SCIENTIFIC_TRIAGE_TH.md`, `PHASE2F_LABEL_ADJUDICATION_TH.md`, `PHASE2F_PILOT_AND_FEATURE_GATE_TH.md`, `PHASE2F_SPATIAL_VALIDATION_TH.md`, `PHASE2F_REFERENCE_UPDATE.md` and `phase2f_gate_snapshot.json`. Preserve Phase 2E work.

## Mandatory constraints from reports
- 47 manifestation records != 47 independent hydrothermal systems; 14 internally consistent, 31 southern provisional and 2 withheld (CR_02, CM_16).
- The ~6–10 northern independent groups are only **an unverified report estimate**, not expert-certified labels.
- DMR fault shapefile (630 valid lines) and DMR northern geology (1,266 polygons) are NOT automatically approved for ML or derivative publication. Respect current UI/export restrictions.
- Five SRTM tiles only, observed IHFC heat-flow locations only (154 records/111 positions), no approved heat-flow interpolation, zero verified usable Landsat ST rasters.
- Preserve immutable source hashes, CRS/geometry audits, opt-in behavior and label/provenance exclusion rules.
- No target-derived feature leakage, including distance to known manifestation or label-derived occurrence density.
- No invented negative class, no synthetic geological positives, no invented expert signatures/permissions.

## Execute the highest-value tasks (do not stop at a plan)
A. Create a source-by-source, row-ID aware expert label-adjudication worksheet from the *real* registry WITHOUT changing raw data. Include coordinate confidence, original source, provisional/withheld status, candidate grouping, geological evidence, decision state and review version. All unreviewed rows remain unapproved.
B. Create AOI candidacy audit from *actual* coverage footprints, measuring valid feature intersection, contiguous extent, usable CRS/resolution and number of genuinely independent validated positive systems. Document why a candidate is selected or rejected. Never treat dataset coverage as prospectivity.
C. Produce a written DMR permission/query packet for geology and active-fault training, transformation, display, redistribution, derivative maps, commercial potential and appropriate attribution. Do not mark permission granted until documentary evidence exists.
D. Identify missing SRTM tiles based only on the eventually approved AOI; use official USGS/NASA sources and verify real rasters/metadata if access permits. Do not bypass authentication or silently replace unavailable datasets.
E. Formalize PU/background selection and preregistered spatial/group separation. The Phase 2E 20-km buffer is an initial hypothesis, **not a fixed scientific law**: investigate spatial correlation, test sensitivity where valid and prevent selection bias. Group all records of one confirmed system in the same fold. Use train-only transforms and spatially independent evaluation.
F. Investigate a separate USGS 2023/2025 **replication sandbox** using openly accessible original features and labels. If data can be acquired and permission permits, replicate methodology on original US data and label results `USGS_REPLICATION_ONLY`. NEVER call these scores Thai geothermal model accuracy.
G. Extend the existing ML gate with auditable domain sign-off evidence and fail-closed checks. Use the attached `phase2f_preflight.py` only as a portable design reference, not as a substitute for original gate. Keep model training/inference/heatmap disabled when blocked.
H. Run real Python/UI/regression tests and report pass/fail command output. Add tests proving provisional labels remain excluded, group isolation, missing coverage masks, license gate, target leakage prevention, fail-closed behavior and no model output when blocked.

## Research foundations
- Mordensky et al. (2023) https://doi.org/10.1016/j.geothermics.2023.102662 — primary baseline methodology, PU challenge.
- Mordensky et al. (2025) https://doi.org/10.1016/j.geothermics.2025.103450 — improved data, ordinal well evidence, Monte Carlo uncertainty, not directly transferable labels.
- DeAngelo et al. (2024) https://doi.org/10.1016/j.geothermics.2023.102882 — PFA/GIS methodology.
- Roberts et al. (2017) https://doi.org/10.1111/ecog.02881 ; Valavi et al. (2019) https://doi.org/10.1111/2041-210X.13107 — spatial blocking.
- USGS 2023 public data https://doi.org/10.5066/P9V1Q9XM . Cite actual acquired data files rather than claiming download from a catalog page.

## Deliverables to implement in the repository
1. `PHASE2F_IMPLEMENTATION_REPORT.md` with exact source commits, file diffs, actual tests, unmet blockers and scientific/implementation status separation.
2. `PHASE2F_LABEL_REVIEW.csv` populated from actual records, with unverified fields blank/blocked and source hash references.
3. `PHASE2F_GROUP_ADJUDICATION_LOG.md` with expert-review pending questions and sign-off schema.
4. `PHASE2F_AOI_COVERAGE_AUDIT.csv`, AOI rationale, CRS and mask checks, plus GIS previews limited to permitted layers.
5. `PHASE2F_LICENSE_MATRIX.md` and ready-to-send DMR inquiry; no fictional approvals.
6. `PHASE2F_VALIDATION_PREREGISTRATION.md`, PU protocol, buffer sensitivity and truthful non-estimability criteria.
7. Gate implementation/tests and `PHASE2F_ML_GATE_REPORT.json` referencing actual evidence.
8. Updated competition methodology narrative: distinguish built GIS, gated predictive research and expected future outcomes.

## Verification / release criteria
Do not train if ANY required approval is missing. Keep `NO_GO_FOR_PREDICTIVE_ML` until the actual 9-condition gate is passed and expert, legal and validation decisions have authoritative documents. Even after gate passes, the portable preflight alone cannot authorize training: apply a separate human scientific review. Do not claim F1/accuracy, probability, MW, drilling success, LCOE, cost reduction or a prediction heatmap without verified out-of-sample evidence.

## Final response language
Respond in Thai. Show what was ACTUALLY changed/tested, what remains unverified, the precise next blocking action and file paths. If the repo is inaccessible, create a patch-ready bundle and identify the limitation. Start executing immediately; do not stop after planning.
