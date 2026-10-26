# GeoThermAI Phase 2C Implementation Report

Date: 2026-10-24  
Overall status: **PARTIAL — all independently implementable local features complete; permission/data/history blockers remain**

## A. Actually implemented

- Typed GIS registry with all requested states plus explicit acquisition record, CRS, scale/resolution, coverage, transformation method, loaded-geometry count, source-record count, display/coverage/export eligibility and UI eligibility (`src/gisRegistry.ts`, `src/types.ts`). Landsat ST is now an explicit `NOT_LOADED` candidate rather than an implicit absence.
- Reproducible geology preprocessing from immutable EPSG:32647 EsriJSON to EPSG:4326 full and simplified GeoJSON (`../scripts/preprocess_geology.py`). The manifest records source hash, feature/vertex/byte counts, bounds, timing, Hausdorff deviation, orphan holes and topology repairs.
- Reproducible DMR structure response-shape audit (`../scripts/audit_dmr_structure.py`) covering `returnGeometry=true`, WGS84/UTM output CRS, offsets, ObjectID batches, JSON and EsriJSON without saving or approximating missing geometry.
- Map-safe coordinate handling: 14 consistent records display by default; 31 southern coordinates remain hidden until opt-in in Map, List, Split and Site Insights. Opt-in persists across in-app navigation and safely resets on reload. CR_02 and CM_16 never enter authoritative map points.
- Real coverage/quality overlays (`src/coverageOverlays.ts`): five filename-derived local SRTM HGT footprints, the unresolved CR_02 UTM↔DMS separation, and the CM_16 working representation. Quality geometry is visibly non-authoritative and off by default.
- Location inspector now reports WGS84 plus rendered intersections with publisher/source, URL, license, scale/resolution, method and scientific warning.
- User-drawn haversine path distance and spherical area with units, EPSG:4326 and limitations (`src/spatialAnalysis.ts`).
- Mapped-fault distance remains visibly disabled because permission-eligible fault geometry is unavailable.
- Selected, filtered and location JSON export paths are implemented and permission-gated (`src/evidenceExport.ts`). Current source/detail exports remain disabled because redistribution permission was not assessed.
- EvidenceMap/MapLibre and geology assets are independently lazy-loaded; stale geology fetches are cancelled. Performance instrumentation distinguishes load/add time from MapLibre visible-ready `idle` time.
- English/Thai copy, keyboard-native controls, non-color warnings and responsive controls remain in the locked Option 2 layout.
- Predictive heatmap, probability, prospectivity, drilling, MW, LCOE and claimed savings remain absent.

## B. Data and GIS sources genuinely opened

- `rock_unit_250k_northern_esrijson.json`: 7,743,929 bytes, EPSG:32647, 1,266 polygon features; SHA-256 remains `c3d8807d6dc700c1d0acde90da657499e0bbf512db3554fc4068702330bd63e1`.
- Geometry audit: 1 invalid derived polygon part (`OBJECTID 14319`) repaired by recorded `buffer(0)` method; zero orphan holes; 1,266 input and output features.
- `geol_str_250k_northern_esrijson.json`: 2,000 attribute records, zero geometry. The 2026-10-24 reproducible live DMR audit recorded 12,741 ObjectIDs, 25 attribute features but zero geometry from both `outSR=4326` and `32647`, zero features from the tested ObjectID batch, and HTTP 400 for unsupported `f=esriJSON`. Exact response-shape evidence is in `../derived/phase2c/dmr-structure-query-audit.json`.
- Active-fault SHP re-opened locally: 630 valid/non-empty lines in EPSG:32647 (616 LineString, 14 MultiLineString). It is not rendered or analysed because permission terms conflict.
- Five local SRTM HGT gzip files are present. Four Phase 1C tiles have recorded raster QA; `N19E098` is represented only as a file-presence footprint.
- IHFC workbook was opened directly as a 30,728,338-byte OOXML workbook. Sheet `data release2024` declares `A1:BV91188`; row 6 exposes `q`, uncertainty, latitude/longitude, elevation, environment, QC, method and depth fields, and sampled rows explicitly identify offshore environments. The existing Phase 1 profile records 91,181 data rows. No Thailand boundary clip or permission clearance was produced.
- Phase 1/1B/1C registries, inventories, acquisition/execution logs, README, known limitations and Phase 2B report were inspected.

## C. Exact final checks

| Check | Result |
| --- | --- |
| `npm run preprocess:geology` | PASS — 1,266 features; 1 recorded repair; 0 orphan holes |
| `npm run typecheck` | PASS |
| `npm test -- --run` | PASS — 7 files, 24 tests |
| `PYTHONPATH=. .venv/bin/pytest -q` | PASS — 16 tests |
| `npm run build` | PASS — 1,610 modules; 1.84 s Vite |
| `npm audit --json` | PASS — 0 vulnerabilities |
| `npm run test:e2e` | PASS — 4 Chromium flows in 10.5 s |
| Desktop browser | PASS — opt-in/navigation, layer on/off, exact unavailable reasons, inspector provenance, export gate |
| 390 × 844 browser | PASS — keyboard Space toggled coverage control; spatial toolbar visible |
| HawkScan DAST | See the current preflight result in `PHASE2C_TEST_LOG.md`; no pass is claimed unless a scan ID and quality gate exist. |

The automated suites cover registry states and immutable inputs, synthetic EPSG:32647 transformation, topology audit/fail-closed holes, CR_02/CM_16 exclusion, provisional coordinate withholding and route persistence, MapLibre-facing layer toggles, unavailable feedback, distance/area and units, export licensing, no prospectivity output, responsive keyboard control and performance capture.

## D. Performance

| Metric | Original Phase 2C baseline | Final | Interpretation |
| --- | ---: | ---: | --- |
| Source geology bytes | 7,743,929 | unchanged | Immutable source retained. |
| Browser geology asset | 7,300.92 kB JS geology chunk | 4,593,713-byte lazy GeoJSON | Geometry no longer parsed/transformed in the React main bundle. |
| Geology vertices | 188,846 | 113,355 | 39.98% reduction; maximum measured Hausdorff deviation 39.871 m. |
| Application entry JS | 1,581.35 kB / 450.63 kB gzip | 393.79 kB / 115.87 kB gzip | MapLibre is removed from non-workspace route entry via lazy import. |
| Lazy EvidenceMap chunk | Included in original entry | 1,081.54 kB / 297.50 kB gzip | Loaded only by Dashboard/Evidence Map routes; Vite warning remains. |
| DOM interactive / load event | `NOT MEASURED` | 7.2 / 110.2 ms | Single local Chromium/Vite run; not a production benchmark. |
| Geology fetch/parse/add | `NOT MEASURED` | 22.8 ms | Ends after source/layer creation. |
| Geology visible-ready | `NOT MEASURED` | 1,114.0 ms | Ends on MapLibre `idle`; not comparable to the earlier 32.1 ms add-layer-only mark. |
| JS heap delta after geology | `NOT MEASURED` | 0 bytes reported | Chromium returned the same coarse 13.4 MB value; do not interpret as zero allocation. |
| Provisional filter render | `NOT MEASURED` | 31.1 ms | Checkbox action through visible 45-record count. |
| Pan frame sample | `NOT MEASURED` | approx. 40.0 FPS; max gap 33.4 ms | One 1.2 s automated local drag, 49 samples; diagnostic only. |

`test-results/phase2c-performance.json` is generated by the checked-in Playwright performance flow. Historical browser baselines cannot be reconstructed and remain `NOT MEASURED`; no unsupported timing improvement is claimed.

## E. Scientific, legal and technical blockers

- DMR active-fault permission conflict requires written clarification. Fault rendering, export and nearest-distance remain blocked.
- DMR structure service still exposes no usable geometry.
- DMR rock-unit reuse terms are unverified. Only local contextual display is enabled; geometry/intersection export is blocked.
- SRTM terrain/hillshade remains blocked by incomplete QA/coverage and unverified reuse; only filename coverage metadata is displayed.
- IHFC lacks a validated Thailand boundary, duplicate/offshore review and reuse audit; heat flow remains metadata-only.
- Landsat ST raster is absent; cloud, QA and data-gap processing cannot run.
- Observation-source redistribution permission is not assessed, so current evidence exports are blocked even though the allowed code path is tested synthetically.
- CR_02, CM_16, southern inferred CRS and the 31-row/30-sample conflict require domain/source resolution.
- No Git metadata exists in this folder, so an isolated branch could not be created.
- A comparable historical browser baseline was not captured before the original implementation.

## F. Runtime evidence

- `screenshots/phase2c-coverage-quality-2026-10-24.png` — real coverage/quality overlays and provenance inspector.
- `screenshots/phase2c-mobile-complete-2026-10-24.png` — 390 × 844 keyboard-tested view.
- `test-results/phase2c-performance.json` — reproducible single-run local browser profile.
- `public/data/dmr-rock-units-north.manifest.json` — preprocessing integrity/performance manifest.
- `../derived/phase2c/dmr-structure-query-audit.json` — live DMR response-shape audit with request parameters and counts.

## G. Acceptance status

| Deliverable | Status |
| --- | --- |
| A — GIS layer access and provenance | **PARTIAL** — current candidates and real geology are registered/integrated; permission- or geometry-blocked layers cannot legally/technically be activated. |
| B — descriptive GIS tools | **COMPLETE for available inputs** — inspector, user measurement, coverage/quality overlays and permission-gated export work; mapped-fault distance is correctly blocked. |
| C — performance | **PARTIAL** — preprocessing, lazy/cancelled loading and final browser profiling are complete; comparable historical browser baseline remains `NOT MEASURED`. |
| Accessibility / UX integrity | **COMPLETE for implemented scope** — Option 2, Thai, keyboard/small screen, non-color warnings and persistent opt-in verified. |
| Automated / browser verification | **COMPLETE except external DAST gate** — unit, GIS, build, audit and checked-in Playwright flows pass. |
| Phase 2C overall | **PARTIAL** — external permission/data/domain decisions and historical baseline prevent full phase closure. |

## Unresolved owner / DMR decisions and next actions

1. Obtain written DMR clarification for active-fault, rock-unit and structure display, derived-analysis and export rights.
2. Approve a validated Thailand administrative boundary and reuse terms before IHFC clipping.
3. Resolve CR_02, CM_16, southern UTM-zone inference and the 31/30 source-count conflict with domain/source review.
4. Acquire actual Landsat Collection 2 Level-2 ST assets before any thermal UI work.
5. Capture a fixed-hardware/network, cold-cache production baseline if comparable browser improvement claims are required.
6. Complete HawkScan only when the CLI, authentication, application/environment and quality gate are available; do not treat `npm audit` as DAST.
