# GeoThermAI / CoreX — Phase 2E Prediction-First Research Plan

**As of:** 2026-10-26 (Asia/Bangkok)
**Basis:** four uploaded Phase 2D reports, the two existing research PDFs, and the externally sourced publications in `RESEARCH_EVIDENCE_MATRIX.md`.
**Status:** RESEARCH DESIGN IN PROGRESS; **PREDICTIVE ML IS STILL NO-GO**.

## 1. Revised mission (claim discipline)

**Target:** produce an auditable *relative geothermal exploration favorability* ranking for a specifically defined Thai pilot area once independent labels, permitted predictors, and spatial-validation conditions pass review.

**NOT the target:** reservoir existence confirmation, calibrated discovery probability, drilling success, installed MW, LCOE, or quantified cost savings. No such estimate was made in Phase 2D or in this research package.

**Proposed contribution to test, not a proven innovation:** whether quality-aware, source-traceable geological evidence integration improves geographically held-out prospectivity rankings over a conventional GIS/geology-only reference in an under-sampled Thai setting.

## 2. Frozen Phase 2D baseline — do not reinterpret as model-ready

- Manifestation registry: **47 source rows**; only **14 internally consistent map points**; **31 southern provisional coordinates**; **CR_02 and CM_16 withheld**. The **18 co-withholding units are *not* expert-validated independent geothermal systems**. No verified negative sites.
- DMR northern geology: **1,266 polygons / 42 symbol descriptions** with context at approximately 1:250,000; partial geographical coverage and redistribution uncertainty.
- DMR structures: **0 returned geometry**. Active faults: **630 local line features blocked pending permissions**; do not export, train on, or enable them.
- SRTM: **5 QC-passed HGT tiles**, coverage incomplete; no national terrain inference.
- IHFC workbook: **91,182 rows globally**, **154 Thai records at 111 coordinates**. Descriptive observed-point use only; neither interpolation nor predictive ML is approved.
- Landsat surface-temperature: **zero valid GeoTIFF / QA pairs**. LST must not be conflated with subsurface temperature.
- Phase 2D unit, immutability, and UI tests passed; no ML model was fitted or validated.

## 3. Research question and hypotheses

RQ: *Can a reproducible, quality-aware multi-source approach predict **relative favorability for further geothermal exploration** in a Thai pilot region more reliably than a simple geology-only baseline under honest group/spatial holdout?*

- H1 (performance): given adequate, independent reference labels, integrated predictors improve pre-registered spatial/group-held-out ranking criteria versus geology-only baseline.
- H2 (ablation): improvements remain informative when individually removing each feature family; improvements cannot be attributed to target leakage or background sampling bias.
- H3 (reliability): model disagreement and poor data coverage are flagged; rankings on poorly supported areas remain suppressed or explicitly provisional.

**Null possibility:** no improvement / insufficient data. This is a valid research outcome.

## 4. Reference model to replicate and adapt

- **Scientific frame:** geothermal Play Fairway Analysis and explicit evidence/knowledge matrices (DeAngelo et al., 2024); maintain the physical interpretations of heat source, permeability and fluids; do not equate all proxies.
- **First baseline:** geology-only *descriptive* screen, formalized after licensing/coverage are cleared; if labels/conditions allow, regularized logistic regression as statistical comparator.
- **First non-linear alternative:** one modest tree model, e.g. shallow XGBoost/Random Forest, with fixed folds matching the baseline. Do **not** start with a complex neural network.
- **Rationale:** Mordensky et al. (2023, 2025) show why training-site strategy, improved evidence layers and uncertainty matter more than algorithm size.
- **New local evidence:** Phiranram et al. (2026) gives a methodological research lead for southern Thailand gravity/THD lineaments. Treat these as a distinct uncertain proxy, **not confirmed fault traces or directly available reusable features**.

## 5. Prioritized feature catalogue (candidate status only)

| Feature family | Candidate feature and native unit | Transformation / preprocessing | Evidence constraint | Current Phase 2D status |
|---|---|---|---|---|
| Geology | rock unit categorical, age in Ma if actually sourced | source legend mapping, categorical encoding *within training folds* | provenance, categorical unknown retained | contextual northern-only; model use conditional |
| Structure | distance to verified active fault [m], geological lineaments [m] | projected CRS; uncertainty-aware distance | requires lawful geometry & geological review; gravity lineaments separate | BLOCKED |
| Terrain | elevation [m], local relative elevation [m], slope [degree] | valid raster extent, regional/local separation only if tested | no extrapolating beyond 5 verified tiles | PARTIAL |
| Heat | measured terrestrial heat flow [mW/m²] | keep depth/method/uncertainty, repeated observations distinct | never silently interpolate 154 records | OBSERVATION ONLY |
| Hydrothermal manifestations | hot spring position [lat/lon], water temp [°C] if sourced | grouped positives after expert review; site uncertainty | NEVER use validation manifestations as predictor pixels in holdout | LABELS NOT READY |
| Remote sensing | surface temp [K or °C], QA, observation date | sensor-specific QA masking and time filtering | surface temperature is not reservoir temperature | NO USABLE RASTERS |
| Gravity (research lead) | Bouguer gravity [mGal], THD lineament proxy | geophysical interpretation and source-specific QA | ambiguous anomalies; NOT a mapped fault; check data rights | NOT ACQUIRED FOR PIPELINE |
| Geochemistry (research lead) | Na/K etc [mg/L], EC [µS/cm], pH [none] | units + chemistry validity checks, no invented values | requires sampling provenance and applicability of geothermometers | NOT VERIFIED |

Unknown units, coordinates, measurement dates, and permissions **must remain unknown**; no silent substitution or imputation into model training.

## 6. Gate before actual predictive training

All the below require review and evidence and must be true **simultaneously**:
1. Positive locations and ambiguity/withholding have authoritative resolution.
2. Independent geothermal system groups validated by a qualified expert.
3. A single pilot study area locked with lawful, sufficient predictor coverage.
4. Positive–unlabeled/background selection and sampling biases documented and approved.
5. Spatial/group blocks, exclusion buffers and leakage checks preregistered.
6. Effective independent group count deemed sufficient for reporting meaningful held-out uncertainty.
7. External geographic holdout approved; no target-derived proxies enter predictor features or standardizer fitting on test sets.
8. Licensing and output export restrictions explicitly passed for the *intended* output.

Until then: **NO predictive fit; NO probability map; NO prospectivity heatmap advertised as validated**. Run `python ml_gate_check.py phase2e_gate_input.json` to see the frozen NO-GO status.

## 7. Pre-registered experiment blueprint (on gate approval only)

- Freeze dataset version, feature schema, label policy, geographic domain, baseline, target rank metric and held-out groups *before training*.
- Reserve spatially distant/geologically distinct validation blocks, grouped by validated geothermal system; prohibit adjacent/duplicate measurements across train/test; fit encoders and scalers on training folds only.
- Compare three options under **identical** folds: (A) geology-only reference, (B) regularized logistic regression using approved inputs, (C) a justified small tree model.
- If true negatives are unavailable, explicitly adopt an expert-approved positive–unlabeled evaluation protocol; **do not present ordinary classification accuracy or F1 as verified detection accuracy**.
- Preselect ranking-oriented indicators (e.g. spatially held-out known-site hit rate / precision-at-k interpreted only under approved reference design), map stability across resamples, and feature-family ablation. Report counts, confidence intervals and limitations, not just one score.
- Only add satellite / IHFC / gravity predictors by documented ablation once measured coverage, permissions and physical interpretation are supported.
- Distinguish uncalibrated relative ranking scores from true probabilities; map data coverage and uncertainty separately.

## 8. Practical pilot-region selection criterion

Do **not** name or rank a Thai pilot province on geothermal promise from a coverage map alone. Score candidate pilot regions by:

1. source evidence legality and reproducibility;
2. independent trustworthy positives/negative evidence;
3. permitted, spatially overlapping geology/terrain/structural proxies;
4. expert support for separate geothermal-system grouping;
5. achievable geographic holdout outside the immediate training neighborhood.

Either north or south may be chosen after verifying conditions. The latest southern gravity paper makes southern study *interesting*, not automatically feasible.

## 9. Proposal-first execution order (deadline-sensitive)

**26–27 Oct:** lock problem statement, copy/adapt attribution table, evidence matrix, source and label audit; obtain expert decisions on independent system groupings and withheld coordinates.

**27–29 Oct:** freeze a feasible single pilot candidate with predictor-permission/coverage matrix, preregistered PU/background and spatial-validation design. If gate remains blocked, produce a reproducible protocol and working *evidence-only* demonstration—do not fabricate prediction.

**29–31 Oct:** finish competition project proposal (maximum 10 A4 pages), video (maximum 5 minutes) and truthful demo of completed GIS. State that prospective predictive models are the funded investigation rather than achieved results. Confirm submission requirements and dates against the official portal if needed.

## 10. Definition of Done for Phase 2E

- [x] Prediction-first research question and hypothesis defined
- [x] Extended new-paper research matrix, each source tied to a workflow decision
- [x] Pre-ML gate codified with explicit blockers and an executable checker
- [x] Draft proposal claims and no-claim policy
- [ ] Primary project repository source files reviewed and patch landed (not supplied in this session)
- [ ] Expert label and system-group approval received
- [ ] Legal/coverage evaluation and locked pilot approved
- [ ] Actual predictive model trained, evaluated and calibrated (**NOT DONE**)

**External references**: `RESEARCH_EVIDENCE_MATRIX.md`; **Phase 2D internal sources:** uploaded `PHASE2D_IMPLEMENTATION_REPORT.md`, `PHASE2D_DATA_READINESS.md`, `PHASE2D_ML_GATE.md`, `PHASE2D_TEST_LOG.md`.
