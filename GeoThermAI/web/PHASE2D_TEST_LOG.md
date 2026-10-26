# Phase 2D test log

Date: 2026-10-26  
Environment: macOS; Node v24.18.0; npm 11.16.0; Python 3.13.9; GeoPandas 1.2.0; Rasterio 1.5.2; Shapely 2.2.0; pyproj 3.8.0; Playwright 1.64.1.

## Executed checks

| Command | Genuine result |
|---|---|
| `.venv/bin/python -m compileall -q scripts src tests` | PASS; no syntax diagnostics |
| `.venv/bin/python -m pytest -q` | Initial run: 19 passed, 1 failed because a synthetic temp output was forced through `relative_to(ROOT)`. Fixed with the existing safe path-label helper. Final: **20 passed in 1.67s**. |
| `.venv/bin/python scripts/preprocess_geology.py` | PASS; 1,266 features; source hash unchanged; 1 recorded repair; 42/42 source symbols matched. |
| `.venv/bin/python scripts/qc_terrain.py` | PASS; five GeoTIFF round-trips and four exact seam checks. |
| `.venv/bin/python scripts/filter_ihfc_thailand.py` | PASS; 91,182 workbook rows; 154 Thailand features written. |
| `.venv/bin/python scripts/audit_dmr_structure.py --timeout 20` | Completed; HTTP response evidence recorded; JSON and GeoJSON geometry counts remain zero. |
| `npm run typecheck` | PASS |
| `npm test -- --run` | **7 files, 24 tests passed** |
| `npm run build` | PASS; Vite built 1,610 modules. Warning: EvidenceMap chunk 1,083.67 kB (298.06 kB gzip) exceeds 500 kB advisory threshold. |
| `npm audit --audit-level=high` | **0 vulnerabilities** |
| `npm run test:e2e` | **4/4 Chromium tests passed in 9.6s** |

## Browser evidence

- Desktop layer/inspection and export-restriction flow: PASS.
- Provisional southern coordinates remain off by default and survive navigation only after explicit opt-in: PASS.
- Keyboard operation at 390 × 844: PASS.
- Runtime screenshot: `web/screenshots/phase2d-ihfc-layer-2026-10-26.png` (502,866 bytes).
- Performance JSON: `web/test-results/phase2c-performance.json`; single local development-server run, not a production/cross-browser benchmark.

## Integrity and security

- Rock-unit source SHA-256 remained `c3d8807d6dc700c1d0acde90da657499e0bbf512db3554fc4068702330bd63e1`.
- IHFC source SHA-256 remained `9f5e4595b5362ec9888656c76fbea91da2751fe995d9cea024c0727edcf5bf8b`.
- Tests retain source-field immutability, EPSG:32647 synthetic transform, CR_02/CM_16 exclusion, southern opt-in, license/export gates and absence of predictive output.
- HawkScan DAST: **NOT_RUN / BLOCKED**. `hawk` was not found; `HAWK_API_KEY` and `stackhawk.yml` were absent; Docker did not report a server version. No scan result is claimed.

