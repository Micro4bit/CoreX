# GeoThermAI — Geospatial Evidence Explorer

GeoThermAI Phase 2A is a local Streamlit application for inspecting published Thai surface thermal-manifestation observations, their provenance, coordinate-quality flags, and the availability of locally inspected GIS context.

It is **not** a geothermal-resource predictor. It does not estimate commercial reservoirs, resource potential, MW, LCOE, drilling success, or model performance. The predictive-model panel is explicitly disabled pending authorized, scientifically valid research.

## What is implemented

- Local CSV ingestion with required-column, duplicate-ID, CRS, malformed-coordinate, and missing-temperature checks.
- A GIS explorer using the local Phase 1C registry. Coordinate-consistent observations appear by default; provisional southern display coordinates require an explicit opt-in; records requiring coordinate review are not plotted as authoritative locations.
- An optional descriptive rendering of the locally saved northern DMR rock-unit geometry. Active-fault geometry is not displayed because its reuse conditions remain unresolved. Terrain is represented only through the existing local terrain summary, not a potential layer.
- Data Quality, Source Registry, provenance inspection, and downloadable record-level evidence summaries.
- A future-model software contract with no model implementation or fabricated outputs.

## Local inputs currently used

The application reads existing files in `tasks/` directly and never rewrites them:

| Input | Runtime use |
| --- | --- |
| `tasks/phase_1c_label_expansion_gis_foundation/geothermal_label_master_registry.csv` | Published observation registry |
| `tasks/phase_1c_label_expansion_gis_foundation/expanded_geothermal_source_inventory.csv` | Source provenance registry |
| `tasks/phase_1c_label_expansion_gis_foundation/verified_gis_layer_inventory.csv` | GIS availability, quality, and licensing status |
| `tasks/phase_1c_label_expansion_gis_foundation/rock_unit_250k_northern_esrijson.json` | Optional descriptive northern geological context |
| `tasks/phase_1c_label_expansion_gis_foundation/northern_terrain_variable_summary.csv` | Optional descriptive terrain summary |

The current registry physically contains 47 published observation rows (16 northern and 31 southern). Those are observations, not independently confirmed geothermal systems or commercial reservoirs. The app computes displayed metrics from the loaded CSV at runtime; it does not hardcode these counts.

## Run locally

Python 3.11+ is required. From this directory:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Or with `uv`:

```sh
uv venv .venv --python python3.13
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/streamlit run app.py
```

Open the localhost address printed by Streamlit. The app uses only local data files; it does not download or alter scientific inputs.

## Tests

```sh
.venv/bin/pytest -q
```

The tests use small synthetic DataFrames for validation behavior and one read-only assertion against the genuine registry. See `docs/DEVELOPMENT_STATUS.md` for the actual execution record and remaining security-scanner limitation.

## Project layout

```text
GeoThermAI/
├── app.py
├── config/settings.py
├── src/geothermai/
│   ├── coordinate_utils.py
│   ├── data_loader.py
│   ├── data_validation.py
│   ├── evidence_engine.py
│   ├── model_interface.py
│   └── provenance.py
├── tests/
├── docs/DEVELOPMENT_STATUS.md
├── requirements.txt
└── tasks/                         # pre-existing research inputs; not modified by the app
```

## Scientific limits and next steps

- `CR_02` and `CM_16` remain unresolved in the source record; the app does not silently correct either.
- Southern coordinates are explicitly provisional because the published UTM zone lacks an independent comparator. The source-table 31-row count also conflicts with prose stating 30 samples.
- Structural geometry, authoritative occurrence inventory, complete licensing clearance, and a defensible independent evaluation protocol remain incomplete.
- Do not enable predictive research until those gates are resolved and the project owner authorizes it.
