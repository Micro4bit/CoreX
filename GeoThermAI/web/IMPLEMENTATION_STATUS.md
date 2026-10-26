# GeoThermAI Web Evidence Explorer — Current Implementation Status

Date: 2026-10-24  
UI direction: **Option 2 — Light Dashboard / Map-Centric Research Workspace**

## Implemented and verified

| Requirement | Actual result |
| --- | --- |
| Evidence workspace | React 19, TypeScript, Vite and MapLibre; local runtime and production build verified. |
| Scientific boundary | 47 published surface manifestations remain observations, not reservoirs. Predictive AI, potential scoring and density heatmaps remain disabled. |
| Coordinate safety | 14 consistent records map by default. The 31 southern working coordinates require explicit opt-in in every view and remain warned. CR_02/CM_16 are excluded from authoritative points. |
| Navigation safety | Southern opt-in persists between Dashboard, Evidence Map, Data Quality and Research Status during the active app session; a full reload safely resets it off. |
| GIS registry | Typed availability, permission, coverage, transformation, geometry-count, acquisition and UI-eligibility metadata for DMR, SRTM, IHFC, Kapong and Landsat candidates. |
| Geology | Real 1,266-feature DMR rock-unit source is preprocessed from EPSG:32647 to EPSG:4326, simplified in source metres, lazy-loaded and displayed only as context. |
| Coverage/quality overlays | Five exact local HGT filename footprints plus non-authoritative CR_02/CM_16 review geometry. No interpolation or density surface. |
| Spatial tools | Location inspection with provenance, geodesic path distance, spherical area and disabled mapped-fault distance with exact reason. |
| Export | Selected, filtered and location JSON exports are permission-gated. Current observation and DMR-derived exports remain disabled because reuse is unresolved. |
| Accessibility | Native keyboard controls, text warnings in addition to color, responsive 390 × 844 flow and bilingual English/Thai labels. |

## Verified checks

| Check | Result |
| --- | --- |
| `npm run typecheck` | PASS |
| `npm test` | PASS — 7 files, 24 tests |
| `PYTHONPATH=. .venv/bin/pytest -q` | PASS — 16 tests |
| `npm run build` | PASS — 1,610 modules; 393.79 kB app shell plus 1,081.54 kB lazy EvidenceMap chunk |
| `npm audit --json` | PASS — 0 vulnerabilities |
| `npm run test:e2e` | PASS — 4 Chromium flows in 10.5 s |
| HawkScan DAST | `NOT_RUN` unless the current preflight recorded in `PHASE2C_TEST_LOG.md` succeeds. |

## Blocked by external evidence or permission

- Fault rendering/export/distance: local geometry is valid, but DMR reuse terms conflict.
- DMR structures: service responses contain attributes but no usable geometry.
- Terrain/hillshade: SRTM coverage and QA are incomplete and reuse terms remain unverified.
- Heat flow: no validated Thailand boundary clip, duplicate/offshore review or reuse clearance.
- Landsat ST: no usable raster, therefore no cloud/QA/data-gap processing.
- Observation exports: publication reuse permission is not assessed.
- CR_02, CM_16, southern inferred CRS and the 31-row/30-sample conflict remain unresolved.
- Historical before-change browser timings, FPS and heap were not captured with the final methodology; they remain `NOT MEASURED` rather than reconstructed.

## Completion decision

**Phase 2C overall: PARTIAL.** All independently implementable descriptive tools and safety fixes in the current local evidence set are implemented and tested. Items that require new licensed data, external permission, domain resolution or a historical performance baseline remain explicitly blocked or `NOT MEASURED`.
