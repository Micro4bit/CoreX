# GeoThermAI Web Evidence Explorer

React/TypeScript/Vite implementation of the locked **Option 2 — Light Dashboard / Map-Centric Research Workspace**, visually aligned to the Owner-supplied reference. It replaces neither the existing research artifacts nor the legacy Streamlit MVP; it is a separate, local web client for evidence exploration.

## Scientific boundary

This app is a **Geospatial Evidence Explorer**. It presents published surface thermal-manifestation observations, provenance, coordinate-quality limitations, and the availability of inspected GIS context.

It does **not** implement, imply, or visualize:

- a geothermal-potential prediction or heatmap;
- a validated AI/ML model, probability, or confidence score;
- ROC-AUC, F1, or other performance metrics;
- commercial reservoir, resource, drilling, generation, or MW claims.

Coordinate-review records are not placed on the map. Southern display coordinates require an explicit opt-in and stay labelled as a working, unverified CRS representation.

## Features

- Dashboard with runtime-computed registry, source, quality-flag, and validation-unit counts.
- URL routes for Dashboard, Evidence Map, Data Quality, and Research Status.
- Map-centric Evidence Map with all eligible observations shown individually, region filters, site inspection, source provenance, map legend, locate and zoom controls.
- Optional descriptive DMR northern rock-unit overlay, preprocessed from locally inspected EPSG:32647 geometry to WGS84 GeoJSON outside the UI main thread.
- Route-level lazy loading keeps MapLibre/EvidenceMap out of the Data Quality and Research Status entry bundle.
- WGS84 location inspection plus descriptive distance and area measurement with explicit CRS/method caveats and per-intersection publisher, URL, license, scale and warning.
- Toggleable SRTM file-availability footprints and non-authoritative CR_02/CM_16 coordinate-review geometry. These are coverage/quality overlays, never a density or potential surface.
- Typed GIS availability/permission states with acquisition, CRS, scale/resolution, coverage, transformation, geometry-count and UI-eligibility metadata.
- License-gated selected-record, filtered-record and location-inspection JSON export behavior.
- Explicit disabled states for unavailable Hot Springs Catalog, Fault Lines, Heat Flow, and unauthorized Geothermal Potential layers.
- Data Quality page for coordinate state, missing temperature, known source conflicts, and GIS-layer restrictions.
- Research Status page exposing the Phase 1C conditional evidence go / predictive ML no-go decision.
- Collapsible provenance, coverage, analysis-boundary, and permission-gated filtered JSON download panel.
- Responsive three-column desktop workspace with tablet/mobile fallbacks.

## Data read by the app

The web app imports these existing, read-only project inputs at build time; it does not alter them.

| Project file | Use |
| --- | --- |
| `../tasks/phase_1c_label_expansion_gis_foundation/geothermal_label_master_registry.csv` | Registry, KPI counts, observation markers, site insights, filtered download |
| `../tasks/phase_1c_label_expansion_gis_foundation/expanded_geothermal_source_inventory.csv` | Source provenance and limitation text |
| `../tasks/phase_1c_label_expansion_gis_foundation/verified_gis_layer_inventory.csv` | Layer availability and restriction states |
| `../tasks/phase_1c_label_expansion_gis_foundation/rock_unit_250k_northern_esrijson.json` | Immutable preprocessing input for the optional descriptive northern geology overlay |

The default basemap uses OpenStreetMap tiles and therefore needs network access in the browser. All project evidence remains local.

## Run locally

From this directory:

```sh
npm install
npm run preprocess:geology
npm run dev
```

Open the local URL Vite reports (normally `http://localhost:5173`).

## Verify production build

```sh
npm run typecheck
npm test
npm run test:e2e
npm run build
npm audit --json
npm run preview
```

## Structure

```text
web/
├── public/favicon.svg
├── src/
│   ├── App.tsx              # dashboard, map explorer, quality and status views
│   ├── EvidenceMap.tsx      # MapLibre map, safe GIS overlay and spatial tools
│   ├── coverageOverlays.ts  # HGT availability and coordinate-review geometry
│   ├── data.ts              # typed local CSV loaders
│   ├── gisRegistry.ts       # layer availability, permission and eligibility states
│   ├── spatialAnalysis.ts   # descriptive distance/area calculations
│   ├── evidenceExport.ts    # evidence reuse/export gate
│   ├── workspaceLogic.ts    # reusable filtering and metric rules
│   ├── workspaceLogic.test.ts
│   ├── types.ts             # source-data interfaces
│   ├── styles.css           # responsive locked Option 2 presentation
│   └── main.tsx
├── package.json
├── playwright.config.ts
├── e2e/phase2c.spec.ts
├── vite.config.ts
└── IMPLEMENTATION_STATUS.md
```

## Known limits

- Satellite and terrain basemaps are intentionally disabled: no configured/licensed imagery or terrain source is available in this MVP.
- Active-fault geometry is not rendered because its local response lacks usable geometry and its reuse conditions remain unresolved.
- Heat flow is not rendered: the inspected global workbook has not completed a Thailand clip/provenance review.
- The DMR rock-unit overlay is descriptive only; there is no lithologic legend or verified site-level intersection result.
- The immutable geology source is approximately 7.74 MB. The browser lazy-fetches a 4.59 MB prebuilt GeoJSON; transformation and simplification run through `../scripts/preprocess_geology.py` rather than in the UI thread.
- Southern working coordinates remain hidden in Site Insights until explicit opt-in, including when the record is selected through List/Split view. The opt-in persists across in-app routes but intentionally resets on a full reload.
- See `GIS_LAYER_PROVENANCE.md`, `GIS_ANALYSIS_METHODS.md`, and `PHASE2C_IMPLEMENTATION_REPORT.md` for exact evidence, permission, method and performance limits.
