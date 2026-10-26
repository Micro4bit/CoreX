# Execution Log — Phase 1B Coordinate & Label Integrity

Run date: 2026-10-23  
Task status: **EXECUTED**. No predictive model was trained.

## Objective

Audit coordinate integrity and label dependence for the 16 Table 1 records in Wood & Singharajwarapan (2014), preserve source values, and determine whether the registry can support defensible predictive-model validation.

## Inputs actually reviewed

### Current project reference files

- `../../docs/project_context/01_GEOTHERMAI_MASTER.md`
- `../../docs/project_context/02_GEOTHERMAI_RESEARCH.md`
- `../../docs/project_context/03_GEOTHERMAI_AI_CONTEXT.md`
- `../../../01_GEOTHERMAI_MASTER.md`
- `../../../02_GEOTHERMAI_RESEARCH.md`
- `../../../03_GEOTHERMAI_AI_CONTEXT.md`

The current `docs/project_context/` versions are labelled v0.2; their locked distinction between surface manifestations and commercial resources governed this work. The root-level v0.1 files were also read as available reference material.

### Phase 1 evidence and outputs

- `../phase_1_data_acquisition_label_validation/wood_singharajwarapan_2014_northern_thailand.pdf`
- `../phase_1_data_acquisition_label_validation/northern_geothermal_table-02.png`
- `../phase_1_data_acquisition_label_validation/northern_hot_spring_label_registry_wood2014.csv`
- `../phase_1_data_acquisition_label_validation/data_feasibility_audit.md`
- `../phase_1_data_acquisition_label_validation/geothermal_label_audit.md`
- `../phase_1_data_acquisition_label_validation/pilot_area_comparison.md`
- `../phase_1_data_acquisition_label_validation/data_acquisition_log.md`
- `../phase_1_data_acquisition_label_validation/next_phase_readiness.md`

### Master Review availability

`rg --files /Users/knight/Development/CoreX | rg -i 'master.*review|review.*master'` produced no matching file. Therefore a standalone Master Review was **NOT AVAILABLE** in this workspace and was not represented as reviewed.

## Original-paper inspection

- The original local Wood & Singharajwarapan PDF opened successfully: 10 pages; PDF metadata identifies 2014.
- Page 608/Table 1 was rendered to PNG and visually inspected. It has 16 rows, labels the coordinate columns `WGS84 UTM East`/`WGS84 UTM North`, gives 15 DMS pairs, and leaves DMS blank for `CM_16`.
- Text extraction was performed with `pypdf` using the supplied runtime. Pages 612–614 were used only to document source-supported system/fault relationships in `geothermal_site_groups.csv`.
- Source text on p. 612 calls the Kok River areas (including `CR_02`) 73°C maximum, while Table 1 reports `CR_02=85°C`. This was recorded as `TABLE_TEXT_INTERNAL_CONFLICT`; the Table 1 value was not changed.

## Coordinate execution

The supplied runtime had `pypdf` but not `pyproj`. A temporary dependency directory was created with `mktemp -d`; `pyproj==3.7.2` was installed there for the run. No dependency vendor directory was added to the project. `requirements.txt` records the reproducible dependency.

Executed command (paths shown relative to the GeoThermAI root):

```sh
PYTHONPATH="$TASK_DEPS" python3.12 tasks/phase_1b_coordinate_label_integrity/coordinate_validation.py \
  --input tasks/phase_1_data_acquisition_label_validation/northern_hot_spring_label_registry_wood2014.csv \
  --output tasks/phase_1b_coordinate_label_integrity/validated_hot_spring_registry.csv \
  --summary-json tasks/phase_1b_coordinate_label_integrity/coordinate_validation_run_summary.json
```

Actual result:

- Input/output rows: 16.
- Library: `pyproj 3.7.2`; PROJ `9.5.1`.
- Selected CRS: `EPSG:32647` — WGS 84 / UTM zone 47N.
- Adjacent-zone medians: EPSG:32646 = 628,062.674 m; EPSG:32647 = 0.372 m; EPSG:32648 = 628,063.029 m (15 DMS-comparable rows).
- `CR_02`: 1,872.76 m discrepancy.
- `CR_05`: 29.21 m discrepancy.
- `CM_16`: no DMS comparison available.

## Verification performed

1. `py_compile coordinate_validation.py` completed successfully.
2. Automated CSV assertions passed:
   - source/derived registry row counts are each 16;
   - every source field in the derived registry exactly equals its input value;
   - focus-record discrepancies are `CR_02=1872.76`, `CR_05=29.21`, `CM_16=blank`;
   - `CR_02` is labelled `TABLE_TEXT_INTERNAL_CONFLICT` for its 85°C Table 1 versus 73°C prose conflict;
   - group table has 13 candidate `site_group_id` values and 9 conservative `validation_cluster_id` values.
3. Re-executed the script from this task folder using the documented sibling input path. The reproduced output was byte-identical to `validated_hot_spring_registry.csv`.

## Deliverables generated in this one task folder

- `validated_hot_spring_registry.csv`
- `coordinate_qc_report.md`
- `geothermal_site_groups.csv`
- `spatial_validation_feasibility.md`
- `coordinate_validation.py`
- `requirements.txt`
- `coordinate_validation_run_summary.json`
- this `execution_log.md`

## Security scan status

**NOT RUN — no scannable web target.** After the script change, HawkScan preflight found no `hawk` CLI on PATH, no `HAWK_API_KEY`, no `stackhawk.yml`, and no HTTP/local web target in this offline CSV/Python task. DAST cannot be run honestly without an initialized scanner and target. The script was nevertheless syntax-compiled and its deterministic CSV output was verified as above.

## Unresolved blockers / next evidence

1. `CR_02` requires an erratum, original field source, author confirmation, or authoritative registry before either coordinate representation is preferred.
2. `CM_16` requires a DMS/source-coordinate record before it can be independently cross-checked.
3. Candidate group membership—especially `CR_09`, `CM_16`, and fault-corridor relationships—needs hydrogeologic/source review.
4. An authoritative Thai occurrence inventory and an independent geographic registry are still absent. The current data do not support predictive-model performance claims; see `spatial_validation_feasibility.md`.
