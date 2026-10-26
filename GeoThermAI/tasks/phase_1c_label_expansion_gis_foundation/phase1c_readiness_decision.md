# Phase 1C Readiness Decision

Date: 2026-10-23  
Scope: evidence and GIS readiness only. **No ML training, tuning, score calculation or performance result was produced.**

## Evidence reviewed

- Three v0.2 GeoThermAI master-reference files in `../../docs/project_context/` and the available v0.1 root-level reference files.
- All available Phase 1 / Phase 1B reports, registries, source PDFs and acquisition records.
- A downloaded and opened 2021 southern Thailand peer-reviewed table with 31 coordinate rows.
- DMR geological unit and structure service metadata/query results; active-fault source metadata and existing shapefile; four newly downloaded northern SRTM HGT tiles; Kapong Mendeley metadata/appendix.

`GeoThermAI_Master_Review_Phase1B.md` was searched for under `/Users/knight/Development` and was not accessible. This decision relies on the current instruction and available Phase 1/1B artifacts; it does not claim to have reviewed the missing file.

## A. GIS evidence screening readiness — CONDITIONAL GO

**Supported now:** A reproducible, descriptive northern evidence screen has executed successfully. It contains 16 cited northern manifestations (14 coordinate-consistent and 2 coordinate-review flags), 1,266 DMR rock-unit polygons, 630 active-fault polylines and terrain context from four inspected one-arc-second HGT tiles. It explicitly identifies missing structure geometry and does not infer a score or probability.

**Conditions:**

1. Keep all outputs labelled as evidence coverage / uncertainty, not geothermal potential.
2. Preserve `CR_02` and `CM_16` quality flags and do not imply a correction.
3. Retain DMR active-fault use as context only until conflicting reuse conditions are clarified.
4. Do not substitute the unavailable DMR structural geometry with approximate/digitized linework.

## B. Predictive machine-learning readiness — NO-GO

**Reason:** Current evidence has 47 observations but only 18 provisional co-withholding units across two source regions. That number is not a verified independent-system count. Key uncertainties remain: northern `CR_02` / `CM_16`; southern Table 1’s 31-row versus 30-sample conflict; southern UTM zone not printed; unreviewed province-to-system membership; no authoritative national point inventory; incomplete structural geometry; unresolved active-fault reuse terms; and no confirmed negative observations.

The master decision prohibiting predictive training remains in force. A row count is not a validation design. Do not fit/tune a predictive model, interpret an evidence overlay as model performance, or call a score a calibrated probability.

## C. Geographic external-validation readiness — CONDITIONAL GO, NOT YET AUTHORIZED TO RUN

**Positive change:** An independently acquired southern peer-reviewed Table 1 now exists. Its records are geographically separated from the northern registry and retain source coordinates/temperatures. This is a real candidate for future out-of-region validation, unlike the prior metadata-only southern evidence.

**Why it is not ready to execute:** Southern UTM zone needs independent confirmation; the 31-row/prose-30 inconsistency must be resolved or explicitly included in a preregistered policy; nine province-level co-withholding units are not verified independent systems; and every covariate must be available with comparable CRS, scale, licensing and coverage across both regions. No target, background policy or leakage audit has been preregistered.

## Required gate to revisit B and C

1. Obtain DMR or another authoritative coordinate-level Thai occurrence inventory with provenance and permission terms.
2. Resolve/record source precedence for `CR_02`, `CM_16`, southern UTM zone and the 31/30 southern discrepancy.
3. Have a domain geologist review group membership and identify defensible independent systems.
4. Reproducibly acquire structural geometry and verify permissions for all predictor layers.
5. Pre-register positive-unlabeled/background sampling, north-only group/block validation and a true geographic external holdout before any model code runs.

Until then, the recommended product is the reproducible evidence-ranking GIS alternative in `gis_evidence_screen.png`, with explicit provenance and missing-data statements.
