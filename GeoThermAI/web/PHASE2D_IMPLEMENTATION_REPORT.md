# Phase 2D implementation report

Date: 2026-10-26 (Asia/Bangkok)  
Scope: research data readiness and GIS-layer completion; predictive ML remained disabled.

## Implemented

1. **DMR geology:** `scripts/preprocess_geology.py` now joins the authoritative service renderer metadata to all 42 symbols present in 1,266 polygons, while retaining immutable source hashes and measured simplification error. The inspector shows legend text with a 1:250,000 context warning.
2. **DMR structures/faults:** `scripts/audit_dmr_structure.py` now records layer metadata plus JSON/GeoJSON, offset, ObjectID, CRS and geometry-enabled variants. The service still returns zero geometry. The 630 valid local active-fault features remain disabled because catalog license statements conflict.
3. **Terrain:** `scripts/qc_terrain.py` validates five 3,601 × 3,601 HGT files, exact shared seams, georeferencing and lossless value round-trip into EPSG:4326 GeoTIFFs. Coverage footprints remain the only UI representation because coverage is incomplete.
4. **Heat flow:** `scripts/filter_ihfc_thailand.py` reads the real 91,182-row IHFC workbook, clips with a validated Natural Earth polygon, keeps repeated measurements, writes a provenance-rich QC CSV and creates the 154-feature browser GeoJSON.
5. **Landsat:** `scripts/audit_landsat_assets.py` rejects authentication HTML by content/type/signature. Eight candidate requests yielded zero usable rasters; the layer remains disabled.
6. **Application:** `web/src/gisRegistry.ts`, `App.tsx`, `EvidenceMap.tsx` and `i18n.ts` add an opt-in IHFC observed-point layer, descriptive location inspection, bilingual uncertainty text and Phase 2D status without changing Option 2 layout. Predictive heatmap controls remain gated.
7. **Tests:** synthetic pipeline tests cover duplicate retention, polygon filtering, HGT seams/round-trip and HTML rejection. Existing CRS, immutability, restriction, export, provisional-coordinate and no-prediction tests remain active.

## Data acquired or verified

- Natural Earth 1:10m Admin-0 archive stored at `tasks/phase_2d_data_readiness/source/ne_10m_admin_0_countries.zip`; public-domain terms and SHA-256 recorded.
- No newer IHFC workbook or Landsat raster was acquired. The attempted current IHFC archive transfer produced no file; Landsat endpoints required authenticated/requester-pays access.
- No new geothermal label was added. The registry remains 47 surface manifestations.

## Current runtime evidence

Playwright Chromium passed four flows, including opt-in persistence, GIS controls, export restrictions, small-screen keyboard use and local performance capture. Screenshot: `screenshots/phase2d-ihfc-layer-2026-10-26.png`.

Current single-run local diagnostics (not a cross-device benchmark): DOM interactive 4.3 ms, load event 94.9 ms, transferred script resources 537,182 bytes, geology load/add 156.6 ms, geology visible/idle 847.6 ms, 47-record provisional filter 40.3 ms, pan sample about 45.2 FPS with 33.4 ms maximum frame gap. No comparable Phase 2D pre-change run was captured, so improvement is **NOT MEASURED**.

## Remaining blockers

- DMR structure geometry missing; active-fault reuse/derivative permission unresolved.
- Geology and terrain coverage are partial; geology redistribution permission remains unresolved.
- CR_02, CM_16, southern UTM and 31/30 conflicts remain unresolved; independent-system grouping lacks expert validation.
- IHFC spatial support and missing uncertainties/depths do not justify interpolation or ML use.
- Landsat ST rasters and QA bands were not acquired.
- HawkScan DAST: **NOT_RUN / BLOCKED** because `hawk`, `HAWK_API_KEY`, `stackhawk.yml` and a responsive Docker runtime were unavailable.

## Final decisions

| Area | Decision | Basis |
|---|---|---|
| A. GIS Data Integration | CONDITIONAL GO | Real geology, terrain QC and heat-flow points work; structural geometry/permissions and nationwide coverage do not. |
| B. Geothermal Label Readiness | NO-GO | Conflicts, provisional coordinates and unvalidated independent groups remain. |
| C. Satellite Data Readiness | NO-GO | Zero usable ST rasters. |
| D. Heat-Flow Data Readiness | CONDITIONAL GO | GO for descriptive points; NO-GO for interpolation/ML. |
| E. Predictive ML Research Readiness | NO-GO | Labels, groups, predictor coverage and validation design are insufficient. |
| F. Application Integration | GO | Verified point layer, provenance, restrictions and regression flows pass locally. |

Overall Phase 2D: **PARTIAL / CONDITIONAL GO for evidence-platform continuation; predictive research remains NO-GO.**

