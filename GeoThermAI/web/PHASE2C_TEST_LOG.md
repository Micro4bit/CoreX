# Phase 2C Test Log

Run date: 2026-10-24 (Asia/Bangkok)

## Original baseline before Phase 2C edits

```text
npm run typecheck: PASS
npm test: PASS — 10 tests
npm run build: PASS — 54.36 s Vite
  index JS: 1,581.35 kB (450.63 kB gzip)
  geology JS chunk: 7,300.92 kB (2,483.02 kB gzip)
npm audit --json: PASS — 0 vulnerabilities
```

Browser load, geology-visible readiness, heap, pan FPS and filter latency were not captured with the final methodology before the original change and remain `NOT MEASURED`.

## Final source and GIS checks

```text
npm run preprocess:geology: PASS
  source SHA-256: c3d8807d6dc700c1d0acde90da657499e0bbf512db3554fc4068702330bd63e1
  source CRS: EPSG:32647
  output CRS: EPSG:4326
  input/output features: 1,266 / 1,266
  empty geometries: 0
  topology repairs: 1 — OBJECTID 14319, recorded Shapely buffer(0)
  orphan holes: 0 — unassigned holes now fail the build
  source bytes: 7,743,929
  simplified bytes: 4,593,713
  vertices: 188,846 -> 113,355
  max / mean measured Hausdorff deviation: 39.8706 / 22.6708 m

npm run typecheck: PASS
npm test -- --run: PASS — 7 files, 24 tests
PYTHONPATH=. .venv/bin/pytest -q: PASS — 16 tests
npm run build: PASS — 1,610 modules; 1.84 s Vite
  app-shell JS: 393.79 kB (115.87 kB gzip)
  lazy EvidenceMap/MapLibre JS: 1,081.54 kB (297.50 kB gzip)
  geology JS chunk: absent
  public geology GeoJSON: 4,593,713 bytes
npm audit --json: PASS — 0 vulnerabilities
```

The suites cover GIS eligibility and enriched metadata, non-mutation of source inventory fields, synthetic EPSG:32647 transformation, unexpected-CRS rejection, fail-closed orphan holes, topology audit fields, CR_02/CM_16 authoritative-map exclusion, southern working-coordinate withholding and route persistence, HGT coverage footprints, coordinate-review geometry, geodesic distance/area and units, evidence/location export licensing and absence of prospectivity output.

## Playwright browser flows

Checked-in configuration: `playwright.config.ts`  
Checked-in flows: `e2e/phase2c.spec.ts`

```text
npm run test:e2e: PASS — 4 Chromium tests in 10.5 s
  provisional coordinates hidden without opt-in: PASS
  provisional opt-in survives in-app navigation: PASS
  geology on/off state: PASS
  SRTM coverage and coordinate-review layer state/legends: PASS
  active-fault exact disabled reason: PASS
  current evidence export gate: PASS
  location inspector provenance and restricted export: PASS
  390 x 844 keyboard Space toggle and spatial toolbar: PASS
  screenshot capture: PASS
  performance artifact capture: PASS
```

The first run after adding `@playwright/test` failed before executing any flow because the matching Chromium executable was not installed. `npx playwright install chromium` installed Playwright Chromium 1248, after which the suite ran. During test development, one inspector assertion was too broad because the clicked tile boundary returned three provenance labels; the locator was narrowed and the full suite passed. These setup/development failures are not represented as application passes.

## Final local browser performance sample

Artifact: `test-results/phase2c-performance.json`

```text
Environment: Playwright Chromium, Vite development server, single local run
DOM interactive: 7.2 ms
load event: 110.2 ms
transferred development script bytes: 462,768
geology fetch/JSON/source/layer add: 22.8 ms
geology visible-ready through MapLibre idle: 1,114.0 ms
JS heap before/after: 13,400,000 / 13,400,000 bytes (coarse value; no zero-allocation claim)
provisional filter to visible 45-record count: 31.1 ms
pan sample: 49 frames over 1.2 s; approx. 40.0 FPS; max gap 33.4 ms
```

These values are diagnostic, single-run, local-development results. OSM/network cache, hardware, the automation driver and development mode affect them. They are not cross-browser or production benchmarks. The old 32.1 ms geology mark ended at `addLayer()` and is not compared with the new visible-ready metric.

## Local source verification

```text
Active-fault SHP: 630 rows; EPSG:32647
  616 LineString + 14 MultiLineString
  630 valid; 0 empty
IHFC workbook: opened directly as OOXML; 30,728,338 bytes
  sheet: data release2024; declared dimension A1:BV91188
  header row 6 includes q, q_uncertainty, lat_NS, long_EW, elevation, environment, qc, qc_uncertainty, method and depth fields
SRTM: five local HGT gzip files physically present
```

The reproducible DMR service audit (`../scripts/audit_dmr_structure.py`) wrote
`../derived/phase2c/dmr-structure-query-audit.json` on 2026-10-24. Its
response-shape summary records:

```text
Structure returnIdsOnly: 12,741 ObjectIDs
Structure f=esriJSON: HTTP 400, output format not supported
Structure f=json + returnGeometry=true + outSR=4326/32647 + offsets/ObjectIDs: attributes returned, geometry count 0
```

The audit is intentionally limited to response shape and counts. It does not
save or substitute restricted/missing geometry. Synthetic unit tests cover the
JSON, HTML-error and malformed-response summaries.

## Security gates

```text
npm audit --json: PASS — 0 vulnerabilities
hawk version: NOT_RUN — command not found
hawk config --help: unavailable
hawk skills status: unavailable
HAWK_API_KEY: absent
stackhawk.yml: absent
HawkScan DAST: NOT_RUN
```

The HawkScan v6+ prerequisite failed, so no configuration, scan, scan ID, finding, rescan or DAST quality-gate result exists. No HawkScan pass/certification is claimed.
