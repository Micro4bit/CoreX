# GeoThermAI Phase 2A — Development Status

Date: 2026-10-23  
Status: **PARTIAL — functional MVP implementation, automated tests, and browser verification completed; HawkScan DAST is blocked because its CLI and credentials are absent.**

## Objective

Deliver the smallest scientifically bounded GeoThermAI MVP: a local Streamlit geospatial evidence explorer for the existing Thailand thermal-manifestation registry. The scope excludes predictive geothermal AI, prospectivity scoring, simulated maps, and resource/economic claims.

## Inputs actually inspected

### Project references

- `docs/project_context/01_GEOTHERMAI_MASTER.md`
- `docs/project_context/02_GEOTHERMAI_RESEARCH.md`
- `docs/project_context/03_GEOTHERMAI_AI_CONTEXT.md`
- Available Phase 1, 1B, and 1C reports under `tasks/`.

No file matching a Master Review or Development Authorization was found under `GeoThermAI/`; it was not represented as reviewed.

### Runtime data inputs

| File | Actual local condition | App use |
| --- | --- | --- |
| `geothermal_label_master_registry.csv` | 47 records: 16 Northern Thailand and 31 Southern Thailand; 47 unique IDs | Observation/source-coordinate registry |
| `expanded_geothermal_source_inventory.csv` | 5 source-attempt/provenance rows | Source Registry |
| `verified_gis_layer_inventory.csv` | 6 GIS/context inventory rows | Availability, quality, license, and restrictions display |
| `rock_unit_250k_northern_esrijson.json` | local ESRI JSON for a verified northern rock-unit context layer | Optional descriptive GeoJSON rendering after EPSG:32647 → EPSG:4326 display transform |
| `northern_terrain_variable_summary.csv` | local derived terrain summary | Optional descriptive terrain table |

The source registry records published surface hot springs / thermal manifestations. It does not establish independent systems, reservoirs, resource MW, or economic viability.

## Coordinate and data-quality handling

- The map defaults to `CRS_AND_DMS_CONSISTENT` observations only.
- Records marked `CRS_INFERRED_DMS_MISMATCH_UNRESOLVED` or `CRS_INFERRED_DMS_MISSING` are deliberately not plotted as authoritative locations.
- Southern `CRS_INFERRED_NO_DMS_COMPARATOR` observations are shown only after the user explicitly selects the provisional-coordinate option.
- Original easting/northing, coordinate reference, source URL, and quality note remain in the loaded table; derived display values are not written back to research data.
- Local active-fault geometry is recorded in the inventory but not mapped by this MVP because licensing/reuse status is unresolved. The GIS inventory retains the restriction.

## Implemented files

| Path | Purpose |
| --- | --- |
| `app.py` | Streamlit UI: Overview, GIS Explorer, Data Quality, Source Registry, Evidence Explorer, Research Status, and disabled AI Module |
| `config/settings.py` | Project-local paths and scientific display rules |
| `src/geothermai/data_loader.py` | CSV, vector, raster-metadata, optional-file, and local rock-unit ingestion interfaces |
| `src/geothermai/data_validation.py` | Schema, duplicate-ID, CRS, coordinate, and temperature validation |
| `src/geothermai/coordinate_utils.py` | Coordinate-category and conservative map-display logic |
| `src/geothermai/provenance.py` | Record-level provenance table and Markdown evidence-summary export |
| `src/geothermai/evidence_engine.py` | Descriptive evidence availability without weights or potential scores |
| `src/geothermai/model_interface.py` | Disabled future predictive-model contract |
| `tests/` | Unit tests using synthetic fixtures plus a read-only registry preservation test |
| `requirements.txt` | MVP dependencies |

## Commands executed

Executed from `GeoThermAI/`:

```sh
uv venv .venv --python /opt/anaconda3/bin/python3.13
.venv/bin/python -m py_compile app.py config/settings.py src/geothermai/*.py tests/*.py
```

The syntax compilation command completed without compiler output, which is a successful `py_compile` result.

The first non-verbose dependency installation attempt stalled. A single verbose retry completed successfully with:

```sh
UV_NO_PROGRESS=1 uv pip install -v --python .venv/bin/python -r requirements.txt
```

The retry installed 46 packages, including Streamlit, Pandas, GeoPandas, PyProj, Shapely, Rasterio, PyDeck, and Pytest, into `.venv`.

## Verification status

| Check | Result |
| --- | --- |
| Static Python syntax compilation | PASS |
| Automated tests | PASS — `11 passed in 0.39s` with `.venv/bin/pytest -q` |
| Streamlit launch | PASS — `.venv/bin/streamlit run app.py --server.headless true --server.port 8501` served `http://127.0.0.1:8501/` |
| Interactive browser workflow | PASS — inspected Overview, GIS Explorer (including provisional-coordinate and geology toggles), Data Quality, Evidence Explorer, and disabled AI Module |
| HawkScan DAST preflight/scan | BLOCKED — `hawk` CLI absent, `HAWK_API_KEY` absent, no `stackhawk.yml`, and thus no initialized scanner despite a running local target |

The data-driven UI and tests are verified, but this is not a DAST security result.

## Reproduction once dependencies are available

```sh
cd /Users/knight/Development/CoreX/GeoThermAI
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/pytest -q
.venv/bin/streamlit run app.py
```

## Known blockers and limitations

1. HawkScan DAST cannot be run until the `hawk` CLI is installed and initialized with authorized credentials/configuration.
2. A standalone Master Review and Development Authorization are absent from the repository.
3. Northern `CR_02` has an unresolved coordinate discrepancy and a retained temperature text/table conflict; northern `CM_16` has no independent DMS comparator.
4. The southern source has an unverified UTM-zone interpretation and a 31-row table/prose-30 discrepancy.
5. DMR structural geometry is unavailable locally in a usable form. Active-fault reuse terms are unresolved.
6. The local DEM/terrain evidence is northern-only and descriptive. It is not a predictive feature set.
7. ML training, model metrics, prospectivity scoring, and AI heatmaps are not implemented or authorized.

## Next recommendations

1. Install and initialize the HawkScan CLI with the project’s authorized configuration, then scan the local running app before release.
2. Obtain owner authorization and source evidence before resolving coordinate ambiguities or changing the scientific registry.
3. Obtain an authoritative coordinate-level occurrence inventory, confirmed GIS licensing/coverage, and a spatially defensible evaluation protocol before proposing model work.
4. If future model work is approved, extend the disabled model contract only after preregistered leakage controls and validation gates are satisfied.
