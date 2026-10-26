# GeoThermAI — Research Blueprint & Data Feasibility Audit 01

Version: 0.2 | Date: 2026-10-23 | Audit type: desk review of official catalogs, documented data products, and relevant literature; **not** a downloaded-and-profiled geospatial dataset audit.

## Executive verdict
**CONDITIONAL GO.** The data supply for geology, structure, satellite LST and DEM is plausible and source-traceable. The central open question is whether Thailand has enough *usable, independent, georeferenced observations* to train and evaluate geothermal potential rigorously. A national positive-unlabeled screening prototype may be feasible; reliable commercial prospectivity prediction is not established.

## Evidence tags
- CATALOG_CONFIRMED: official publisher/catalog or actual service page inspected.
- DOCUMENT_ONLY: map or article found; structured records not validated.
- GLOBAL_PRODUCT: documented global product; coverage/access still must be profiled for pilot AOI.
- NOT_VERIFIED: availability, machine readability, licensing, quantity or suitability needs direct testing.
- RESEARCH_INFERENCE: recommendation/risk from study design, not an observed empirical outcome.

## Dataset register (audit 01)

| ID | Candidate and authority | Audit status | Planned use | Blocking checks |
|---|---|---|---|---|
| TH-GEO-01 | DMR Rock Units 1:250,000; https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/ROCK_UNIT_250K/MapServer | CATALOG_CONFIRMED; ArcGIS MapServer displays a rock-unit layer and JSON/GeoJSON query support at service level | lithology, unit age/rock classes | verify feature-layer query count, export, attributes, nationwide coverage, license, CRS and geometry quality |
| TH-STR-01 | DMR Geological structural lines 1:250,000; https://data.go.th/en/dataset/gdpublish-geol-str-250k | CATALOG_CONFIRMED | distance/density of mapped structures | check fault types; structures are not automatically all faults or active faults; access and geometry quality |
| TH-FAULT-01 | DMR active-fault groups; https://data.go.th/dataset/activefault | CATALOG_CONFIRMED; catalog advertises shapefile resource | separate structural predictor | confirm downloadable file, coordinates, recency, completeness and scientific meaning |
| TH-SPR-01 | DMR Thailand hot-spring map; https://www.dmr.go.th/น้ำพุร้อน-แผนที่แหล่งน้ำพุร้อนในประเทศไทย/ | DOCUMENT_ONLY; map PDF offered, **structured point layer not confirmed** | candidate positive observations; retrospective comparison | obtain source inventory as CSV/GIS with unique ID, surveyed coordinates, temperatures, provenance and dates; permission/license |
| SAT-LST-01 | USGS Landsat 8/9 Collection 2 Level-2 ST; https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature ; https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2 | GLOBAL_PRODUCT | satellite ablation, LST anomaly candidate | cloud mask, missing pixels/ASTER GED dependency, season/time, surface confounding; resampling scale |
| DEM-01 | NASA/USGS SRTM Global 1 arc-second (~30m); https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003 | GLOBAL_PRODUCT | elevation/slope/topography | vertical units, CRS, voids, derived-covariate relevance |
| HF-01 | IHFC Global Heat Flow Database release 2024; https://www.ihfc-iugg.org/products/global-heat-flow-database/data | CATALOG_CONFIRMED, Thai sample count NOT_VERIFIED | optional independent physical evidence | filter Thailand and pilot AOI; evaluate number, geolocation, QC status and selection bias |
| SUBSURF-01 | Field wells, downhole temperatures, geophysical surveys (Fang/Mae Chan etc.) | Literature records exist; systematic usable datasets NOT_VERIFIED | independent resource-related evaluation, if licensed/accessible | public accessibility, data licensing, measured depth/temp/flow, geographic bias |
| GRID-01 | Electricity grid access, road access, cost | NOT_VERIFIED for usable nationally licensed layers | optional economics and site constraints | official data, licensing, capacity constraints, scale |

**IMPORTANT:** Presence of an official catalog is not proof a GIS export was successfully obtained. Nothing in this audit demonstrates complete training data, fitted models, or achieved predictive accuracy.

## Prior Thai evidence and novelty check
1. Sainarmtip, Wetchayont & Chenrai, *Development of Geothermal Potential Resources Map using Land Surface Temperature from MODIS in Northern Thailand*, RMUTI Journal, published 2020, vol 14(1), pp. 68–82: used MODIS LST, rocks and faults via weighted overlay. Abstract reports 53.3% agreement/accuracy under its own methodology; **do not compare that number directly with modern out-of-area ML accuracy**. https://ph01.tci-thaijo.org/index.php/rmutijo/article/view/241847
2. *Geologic framework of the Fang Hot Springs area ...*, Geothermal Energy (2017): detailed Fang hydrogeological context; notes substantial private subsurface material may be unavailable publicly. https://link.springer.com/article/10.1186/s40517-017-0087-7
3. *Geophysical Investigation of Geothermal Potential in Southern Thailand: Insights From GGMplus Gravity*, Earth and Space Science (first published 2026-07-06), DOI:10.1029/2025EA004686. Shows alternative gravity/structural evidence, relevant as an alternate-region context. https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025EA004686
4. *When less is more: How increasing the complexity of machine learning strategies for geothermal energy assessments may not lead toward better estimates*, Geothermics 110 (2023), 102662, DOI:10.1016/j.geothermics.2023.102662. User-provided PDF: `1-s2.0-S0375650523000160-main.pdf`. Methodological reference; study used US data, positive/unlabeled challenge and severe imbalance; **published random splitting is not a substitute for testing geographic transferability in Thailand**.
5. `Energy.pdf` user-provided background on technology/cost benchmarks. International $/kW plant CAPEX cannot be treated as Thai exploration costs or empirically achieved savings. The economics annex must use source-dated scenarios and no invented point estimates.

**Novelty conclusion:** 'First satellite/geology geothermal potential map in Thailand' would be false. Defensible proposed novelty is spatially robust AI versus baselines, satellite ablation, transparent uncertainty, and utility of prioritization under limited information. Novelty remains to be reviewed against further ML studies.

## Essential labeling and evaluation protocol
1. Compile an inventory of unique Thai geothermal/spring sites with evidence level, geocoordinates, measurement date and independent study reference.
2. Distinguish warm springs, geothermal field measurements, production wells, and confirmed usable energy systems. Define target class precisely and conservatively.
3. Do not convert unlabeled pixels into ground-truth negatives. If background sampling is used, report as *background* and perform sensitivity tests.
4. Prevent target leakage: if spring locations create the label, distances to the same spring locations **must not** be predictors in that experiment; otherwise model merely rediscovers labels.
5. Partition by spatial block/site/group before feature selection, normalization, tuning, or sampling where appropriate. Respect spacing and geological context.
6. Compare transparent geology/rule baseline, Logistic Regression, optional XGBoost; keep folds consistent and tune inside training folds.
7. Perform ablations geology/structure vs + satellite vs optional additional inputs.
8. Report withholding geography, sample counts, enrichment/recall at fixed land-area budget, uncertainty across blocks; avoid unsupported 'true probability' calibration.
9. Reserve holdout sites where possible; a tiny number of independent sites may make performance claims unstable. Report that openly.

## Pilot geography recommendation
**First candidate: Northern Thailand / Chiang Mai–Chiang Rai geothermal study corridor, narrowed after label/data coverage audit.** Rationale: published Fang/Mae Chan studies, known hot-spring context, prior satellite-plus-geology map enabling comparison. This is not proof that labels are sufficient. Candidate **B**: Southern Thailand (Ranong–Phang Nga) with geoscientific literature, e.g. https://kb.psu.ac.th/items/21c5712b-b93c-402d-b9e2-ab58791a0a9d and new 2026 GGMplus study. Select by measurable label availability and independent spatial folds, not convenience or a predetermined outcome.

## First sprint: 10 acceptance tests
- [ ] AT01 Obtain actual DMR rock-unit vector or queryable records; save sample schema, CRS, license.
- [ ] AT02 Obtain structural/fault vector geometry and inspect feature classes and dates.
- [ ] AT03 Obtain raw hot-spring inventory with coordinates, unique IDs and dates; record unavailable items explicitly.
- [ ] AT04 Deduplicate known sites and assign occurrence evidence tiers.
- [ ] AT05 Filter IHFC heat-flow records in northern Thailand; record actual point counts and QC.
- [ ] AT06 Generate Landsat imagery for pilot AOI; record cloud/data-gap coverage and valid pixel ratio.
- [ ] AT07 Prepare SRTM and verify raster extents/NoData and compatible reprojection.
- [ ] AT08 Define target and an evaluation split with no feature/label leakage.
- [ ] AT09 Run a basic geological/rule baseline and a spatial holdout diagnostic; no claims until executed.
- [ ] AT10 Produce Go/No-Go memo for supervised/positive-unlabeled vs purely descriptive GIS alternative.

## Go / No-Go decision
**GO** to ingest, schema profiling, source quality review and spatial pilot feasibility tests. **STOP/RE-SCOPE** if georeferenced label data cannot be licensed/accessed or independent spatial evaluation is scientifically untenable. Safe fallback: evidence-tiered multi-criteria GIS ranking with sensitivity analysis (do not advertise as a validated AI predictive model).

## Source access log — inspected 2026-10-23
- DMR rock unit REST service: https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/ROCK_UNIT_250K/MapServer
- DMR structural lines catalog: https://data.go.th/en/dataset/gdpublish-geol-str-250k
- DMR active faults catalog: https://data.go.th/dataset/activefault
- DMR hot-spring map page: https://www.dmr.go.th/น้ำพุร้อน-แผนที่แหล่งน้ำพุร้อนในประเทศไทย/
- USGS Landsat ST documentation: https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature
- NASA SRTM Earth Engine catalog: https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003
- IHFC 2024 download: https://www.ihfc-iugg.org/products/global-heat-flow-database/data
- Thailand 2020 MODIS study: https://ph01.tci-thaijo.org/index.php/rmutijo/article/view/241847
- Fang research: https://link.springer.com/article/10.1186/s40517-017-0087-7
- 2026 Southern Thailand study: https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025EA004686

## Limitations
No actual spatial data downloaded/profiled, no verified Thailand spring CSV, no count of geographic validation sites, no trained model, no field confirmation, no computed cost savings. Source access, licensing, vintage and mapping resolution require verification before analytics.
