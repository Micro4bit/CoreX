# Phase 2E — Research-to-Methodology Evidence Matrix

**Retrieved / verified:** 2026-10-26. Distinguish a publication's observed results in its own region from *new hypotheses* for GeoThermAI. No foreign performance statistics can be claimed as performance in Thailand.

## Source-led selection — twelve additional publications (on top of the two user PDFs and the prior eight candidates)

| # | Paper / scholarly record | Source (publisher/USGS) | What the paper supports | Suggested transfer to GeoThermAI | Limitation / non-claim |
|---|---|---|---|---|---|
| R01 | **Mordensky et al. (2025)**, *Favorability mapping for hydrothermal power resource assessments of the Great Basin, USA* | https://doi.org/10.1016/j.geothermics.2025.103450 ; USGS https://pubs.usgs.gov/publication/70270953 | Modern favorability assessment uses improved evidence layers, more labeled wells, ordinal hydrothermal signals, simple nonlinear ML and repeated-validation uncertainty | **Primary replication design**, conditional on independent Thai labels & permission | Not an off-the-shelf trained Thai model; well-validated labels lacking locally |
| R02 | **DeAngelo et al. (2024)**, *Geothermal Play Fairway Analysis, Part 2: GIS methodology* | https://doi.org/10.1016/j.geothermics.2023.102882 ; USGS https://pubs.usgs.gov/publication/70250631 | PFA integrates critical elements, risk matrices reflecting success/knowledge, and code-based processing | **Scientific baseline** and separate uncertainty/evidence layers | Expert weighting and geothermal play differ between U.S. and Thailand |
| R03 | **Shervais et al. (2024)**, *Geothermal play fairway analysis, part 1: Example from the Snake River Plain, Idaho* | https://doi.org/10.1016/j.geothermics.2023.102865 ; USGS https://pubs.usgs.gov/publication/70250630 | Worked geological application of PFA in a specific geothermal setting | Compare conceptual system components / geological interpretation in a fixed pilot | Volcanic Snake River Plain assumptions cannot automatically generalize to Thai non-volcanic settings |
| R04 | **Smith et al. (2023)**, *Exploratory analysis of machine learning techniques in the Nevada geothermal play fairway analysis* | https://doi.org/10.1016/j.geothermics.2023.102693 ; USGS https://pubs.usgs.gov/publication/70241433 | Bayesian/probabilistic neural networks and PCA+k-means can expose alternative geothermal favorability signatures | Reference alternative algorithms **only after baseline** | Training examples and validation conditions are specific to Nevada |
| R05 | **Caraccioli et al. (2023)**, *Don't Let Negatives Hold You Back...* | USGS https://www.usgs.gov/publications/dont-let-negatives-hold-you-back-accounting-underlying-physics-and-natural | Comparing expert-selected vs sampled negative strategies changes model bias and favorability | **High priority: design PU/background protocol**; preserve Unknown ≠ Negative | Random background is not proof of true geothermal absence |
| R06 | **Mordensky et al. (2023)**, *Cursed? Why one does not simply add new data sets to supervised geothermal machine learning models* | USGS https://pubs.usgs.gov/publication/70251029 ; published text https://publications.mygeoenergynow.org/grc/1034860.pdf | Adding partially correlated features does not necessarily raise predictive skill; dimensionality and spatial support matter | **Require ablation and sample-size-aware feature selection** | More input channels are not intrinsically better |
| R07 | **Caraccioli Salinas et al. (2024)**, *Separating signals in elevation data improves supervised machine learning predictions for hydrothermal favorability* | USGS https://pubs.usgs.gov/publication/70264692 ; text https://publications.mygeoenergynow.org/grc/1035032.pdf | Decomposes elevation into regional vs local relative elevation signal, tests feature relevance | **Terrain feature engineering candidate** inside five HGT tile overlap, if physically warranted | Terrain extent and transferability constrained; synthetic or unmeasured coverage forbidden |
| R08 | **Phiranram et al. (2026)**, *Geophysical Investigation of Geothermal Potential in Southern Thailand: Insights From GGMplus Gravity* | https://doi.org/10.1029/2025EA004686 | Gravity THD lineaments correlate with some Thai faults and thermal springs but gravity interpretations are non-unique | **Priority Thai geology context**; assess separately a *gravity-structural-proxy* evidence layer | THD cannot be silently treated as mapped/verified faults or groundwater permeability; inspect license & raw data |
| R09 | **Feng et al. (2025)**, *Geothermal detection study using remote sensing data by combining machine learning and deep learning: A case study of Huanggang City* | https://doi.org/10.1016/j.geothermics.2025.103338 | Coarse RF/ML + fine MUnet pipeline tested in one Chinese city; integrates LST, anomalies, lithology, fault proximity | **Future second-stage research** after QA-cleared satellite data and reliable supervised labels | Their reported F1 in China is not Thai accuracy; zero acceptable Landsat ST rasters locally |
| R10 | **He et al. (2026)**, *A physics-guided clustered GBRT ensemble model for geothermal heat flow prediction and its application in China* | https://doi.org/10.1186/s40517-026-00389-2 | Physics-derived features and clustered boosting improve heat-flow model in China | **Longer-term heat-flow modeling** after sufficient reliable local point observations | Current 154 records / 111 coordinates not approved for interpolation/ML; no imported R² claims |
| R11 | **Uncertainty quantification using clustering-based quantile regression forests... (2026)**, *Geophysical Journal International* | https://doi.org/10.1093/gji/ggag113 ; code/data https://doi.org/10.5281/zenodo.16291112 | QRF plus clustering quantifies prediction intervals and diagnostic reliability in a heat-flow example | **Later uncertainty reference** and reproducibility example | Quantiles for heat flow do not automatically calibrate prospectivity probability |
| R12 | **Aliyu et al. (2026)**, *Review on geothermal prospectivity mapping: Global trends, challenges, and future directions* | https://doi.org/10.1016/j.rser.2026.117164 | Review of ~100 GPM studies: MCDA, ML, quality, spatial validation, uncertainty and reproducibility | **Recent literature-review structure** and research-gap justification | Review is not a new deployable predictive model or algorithm benchmark for Thailand |

## Existing anchors (not counted as new)

- **AlGaiar et al. (2024)**: *Applications of artificial intelligence in geothermal resource exploration: A review.* https://doi.org/10.1002/dug2.12122 — context on AI + data engineering, not a source-specific code implementation.
- **Mordensky et al. (2023)**: *When less is more: How increasing the complexity of machine learning strategies for geothermal energy assessments may not lead toward better estimates.* https://doi.org/10.1016/j.geothermics.2023.102662 — severe positive/unlabeled imbalance and limits of using complex AI with weak features.

## Decision log derived from papers + local reports

1. **Use R01 + R02 as implementation reference**, not R09's deep segmentation as initial MVP.
2. **Use R05 to define negative/background strategy**, never label all non-hot-spring cells as true negative.
3. **R06 + R07 drive ablation tests**, not a demand to include every obtainable layer.
4. **R08 supplies Thailand-specific scientific context**, not automatically data acquisition rights or geometries.
5. **R11 supports future uncertainty methodology** but do not promise calibrated probabilities in round 1.
6. **R12 establishes current literature context** but primary scientific claims should cite R01/R02/R05/R08 and user-verified sources.

## Research evidence still missing

- Site-by-site authoritative Thai reference labels and independent-system grouping approved by domain expert.
- Rights/authoritative geometries for structural lineaments and DMR datasets.
- A georeferenced, *permitted*, sufficiently overlapping independent pilot dataset; formal measurement units / dates / uncertainty / provenance.
- Within-Thai-region independent test, not only a random split of adjacent samples.
- Direct comparison against a data-leakage-controlled scientific baseline.

These are **requirements for future work**, not completed Phase 2E findings.
