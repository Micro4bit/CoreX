# GeoThermAI — Phase 2A MVP Implementation Report

Date: 2026-10-23  
Prepared by: Codex  
Decision: **PARTIAL**

## Executive summary

The GeoThermAI Geospatial Evidence Explorer MVP has been implemented as a local Streamlit application and verified with automated tests and browser inspection. It reads the existing local research artifacts without modifying them, makes coordinate uncertainty visible, preserves observation provenance, and deliberately does not produce geothermal-potential scores or predictive-AI outputs.

The implementation is functionally ready for local research use. The Phase 2A decision remains **PARTIAL**, rather than COMPLETE, because HawkScan DAST could not be performed: the environment has no `hawk` CLI, no `HAWK_API_KEY`, and no initialized `stackhawk.yml` configuration.

## A. Implemented features

| Feature | Actual implementation | Validation status |
| --- | --- | --- |
| Local observation ingestion | Loads the Phase 1C master registry from local CSV and validates schema, duplicate IDs, CRS fields, numeric coordinate values, and missing temperatures. | Automated test coverage; real registry loaded in UI. |
| Conservative coordinate display | Shows internally consistent coordinates by default; hides coordinate-review records from the map; requires explicit opt-in before showing provisional southern coordinates. | Automated test and browser-checked. |
| GIS Explorer | Provides source/region filters, coordinate-quality legend, optional northern rock-unit context, terrain-summary availability, and source identification. | Browser-checked. |
| Data Quality dashboard | Calculates totals, source/region counts, coordinate-status counts, missing display coordinates, provisional records, and GIS inventory status from local files. | Browser-checked. |
| Source Registry and provenance | Supports text filtering, record-level provenance inspection, and source-level registry display. | Implemented; data sources loaded from local CSV. |
| Evidence Explorer | Shows descriptive layer availability/restrictions and downloads a documented Markdown evidence summary. No weights or potential score are calculated. | Automated test and browser-checked. |
| Future AI contract | Provides a disabled future-model interface with explicit required inputs, outputs, uncertainty, and provenance requirements. | Automated test and browser-checked. |

## B. Files created or modified

### Application and configuration

- `app.py`
- `config/settings.py`
- `src/geothermai/data_loader.py`
- `src/geothermai/data_validation.py`
- `src/geothermai/coordinate_utils.py`
- `src/geothermai/evidence_engine.py`
- `src/geothermai/provenance.py`
- `src/geothermai/model_interface.py`
- `requirements.txt`

### Automated tests

- `tests/conftest.py`
- `tests/test_data_validation.py`
- `tests/test_coordinates.py`
- `tests/test_provenance.py`
- `tests/test_evidence_engine.py`

### Documentation

- `README.md`
- `docs/DEVELOPMENT_STATUS.md`
- `docs/[2026-10-23][Phase_2A_MVP_Implementation_Report].md`

Existing research datasets and Phase 1/1B/1C scripts were not modified.

## C. Data sources actually loaded

| Local source | Actual use | Important boundary |
| --- | --- | --- |
| `tasks/phase_1c_label_expansion_gis_foundation/geothermal_label_master_registry.csv` | Observation registry for map, quality dashboard, source registry, and evidence explorer. | 47 published surface thermal-manifestation observations; not commercial reservoirs or independently confirmed systems. |
| `tasks/phase_1c_label_expansion_gis_foundation/expanded_geothermal_source_inventory.csv` | Source provenance display. | Source/reuse limitations are preserved. |
| `tasks/phase_1c_label_expansion_gis_foundation/verified_gis_layer_inventory.csv` | GIS availability, quality, access, and licensing display. | Locally present does not imply unrestricted reuse or scientific suitability. |
| `tasks/phase_1c_label_expansion_gis_foundation/rock_unit_250k_northern_esrijson.json` | Optional descriptive northern rock-unit overlay. | Context only; not used to compute a score. |
| `tasks/phase_1c_label_expansion_gis_foundation/northern_terrain_variable_summary.csv` | Optional descriptive terrain summary. | Northern-only context; not a model feature layer. |

Runtime data-quality results are calculated from the loaded registry, including 47 rows, 16 northern rows, 31 southern rows, 2 coordinate-review records, 31 provisional-coordinate records, and 2 missing-temperature records.

## D. Test and verification results

### Commands executed

```sh
uv venv .venv --python /opt/anaconda3/bin/python3.13
UV_NO_PROGRESS=1 uv pip install -v --python .venv/bin/python -r requirements.txt
.venv/bin/python -m py_compile app.py config/settings.py src/geothermai/*.py tests/*.py
.venv/bin/pytest -q
.venv/bin/streamlit run app.py --server.headless true --server.port 8501
```

### Actual results

- Python syntax compilation: **PASS**.
- Automated tests: **PASS — 11 passed**.
- Streamlit launch: **PASS** at `http://127.0.0.1:8501/` during verification.
- Browser inspection: **PASS** for Overview, GIS Explorer, provisional-coordinate control, geological-overlay control, Data Quality, Evidence Explorer, and the disabled AI Module.
- Research data integrity: **PASS** for a read-only test that confirms source coordinate values remain preserved in the loaded registry.

## E. Unresolved problems and limitations

1. HawkScan DAST is blocked: `hawk` is not installed, `HAWK_API_KEY` is absent, and no `stackhawk.yml` exists. No security-scan result is claimed.
2. No standalone Master Review or Development Authorization was present in the repository.
3. Northern `CR_02` retains its unresolved coordinate discrepancy and source temperature conflict. Northern `CM_16` has no independent DMS comparator.
4. Southern observations retain an inferred working UTM CRS and the published 31-row table/prose-30 conflict.
5. Structural geometry is not available in a usable local form; active-fault reuse conditions remain unresolved, so the app does not map those fault lines.
6. The application contains no predictive model, performance metric, simulated result, potential score, resource estimate, MW estimate, or LCOE claim.

## F. Local run instructions

```sh
cd /Users/knight/Development/CoreX/GeoThermAI
uv venv .venv --python python3.13
UV_NO_PROGRESS=1 uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/pytest -q
.venv/bin/streamlit run app.py
```

Open the local URL printed by Streamlit. The application uses local research files and does not download, rewrite, or fabricate research data.

## G. Phase 2A readiness decision

**PARTIAL**

The intended scientific MVP is implemented, tests pass, and core UI workflows were verified. Completion is held at PARTIAL until the project can run an authorized HawkScan DAST scan against the local application and record its outcome. This decision does not authorize predictive-model development.

## Recommended next actions

1. Install and initialize HawkScan with the project’s authorized credentials/configuration; scan the local app before release.
2. Obtain or document the missing Master Review and Development Authorization.
3. Resolve scientific data gates before any predictive work: authoritative occurrence inventory, coordinate reconciliation, GIS licensing/coverage, and spatially valid evaluation protocol.
4. Keep the Evidence Explorer descriptive until the owner explicitly authorizes a scientifically valid predictive-research phase.
