# IHFC heat-flow data audit — 2026-10-26

## Source and method

The actual OOXML workbook `IHFC_2024_GHFDB.xlsx` contains 91,182 data rows (rows 7–91,188), not 91,181. SHA-256 is `9f5e4595b5362ec9888656c76fbea91da2751fe995d9cea024c0727edcf5bf8b`. Fields inspected include coordinates, heat flow `q`, uncertainty, method, measured depths, elevation, environment/domain, country/region, references, review status, quality code and identifiers.

`scripts/filter_ihfc_thailand.py` streams the original workbook without rewriting it and classifies points with the official Natural Earth 1:10m Admin-0 Thailand polygon in EPSG:4326. Boundary archive SHA-256 is `ce1ac7036499a0edd641fbc093cd209a98f96a49d2eca8480aaacad35138a7f6`; Natural Earth data are public domain. The IHFC dataset is recorded as CC BY 4.0.

## Results

- Regional envelope: 460 rows: 154 inside Thailand, 291 offshore, 15 neighboring countries.
- Thailand: 154 measurement rows at 111 distinct coordinates; 28 duplicate-coordinate groups and 43 repeated rows beyond the first. Nothing was silently deduplicated.
- All 154 have heat-flow values and completed review status. All 154 lack `q_uncertainty`; 147 lack total measured depth and all lack total vertical depth.
- `q` ranges 12–779.34 mW/m² (median 56; mean 83.32). The maximum is an observation requiring source/domain review, not a reservoir claim.
- Heat-flow method: 130 “Interval”, 24 unspecified. Quality codes remain verbatim.

Outputs: `derived/ihfc_thailand_qc.csv`, summary JSON and `web/public/data/ihfc-thailand-points.geojson`. The browser layer is opt-in, point-only, provenance-labelled and explicitly non-interpolated.

Readiness: descriptive point display **GO**; exploratory statistics **CONDITIONAL GO** with repeated-measurement and missing-uncertainty controls; ML feature construction **NO-GO** pending spatial-support/missingness protocol; national interpolation **NO-GO** pending defensible variography, spatial cross-validation and uncertainty analysis.

