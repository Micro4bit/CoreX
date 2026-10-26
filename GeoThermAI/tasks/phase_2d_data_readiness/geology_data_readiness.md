# Geological-unit data readiness — 2026-10-26

## Verified input and processing

- Immutable source: `tasks/phase_1c_label_expansion_gis_foundation/rock_unit_250k_northern_esrijson.json`; SHA-256 `c3d8807d6dc700c1d0acde90da657499e0bbf512db3554fc4068702330bd63e1`.
- Source CRS is EPSG:32647. The 1,266 polygon features carry `OBJECTID`, `TEXT_SYM`, `YEAR_COMPI`, area and length attributes.
- `scripts/preprocess_geology.py` transforms with `pyproj` (`always_xy=True`) to EPSG:4326 and simplifies in the source CRS with a 25 m topology-preserving tolerance. It never rewrites the EsriJSON.
- All 1,266 outputs are non-empty. One invalid derived polygon, OBJECTID 14319, required `buffer(0)` repair; no orphan holes remained.
- Vertices changed from 188,846 to 113,355. Maximum/mean Hausdorff deviation are 39.871 m/22.671 m. Output bounds are 98.262788–100.485114 E and 16.939605–20.491914 N.
- Source size is 7,743,929 bytes; simplified GeoJSON is 4,697,868 bytes. The manifest records hashes, method, timing and deviation.

## Classification and scientific use

The official ArcGIS layer metadata contains 94 renderer legend entries. All 42 `TEXT_SYM` values present in the extract match an entry; the app now exposes the matching legend label. This is an authoritative service legend mapping, not permission to infer unrecorded lithology, age, or site geology. Scale remains nominal 1:250,000 and coverage is northern/partial, not national.

Decision: **CONDITIONAL GO** for contextual map display and future categorical-feature research. Predictor use remains **NO-GO** until reuse terms, study-area completeness, category semantics and spatial-resolution suitability are approved.

