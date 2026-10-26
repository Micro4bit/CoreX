# Spatial Validation Feasibility — Phase 1B

Date: 2026-10-23  
Status: **EXECUTED grouping/geometry count; PROPOSED validation designs; no model trained.**

## Label unit being evaluated

The available table is a registry of published, georeferenced **surface hot-spring/thermal-manifestation observations**. It is not a register of confirmed commercial reservoirs, proven MW capacity, or true negative locations. Accordingly, any later analysis must be positive-unlabeled/background-based and must not use distance to this same registry as a predictor.

## Grouping outcome

`geothermal_site_groups.csv` makes two deliberate levels explicit:

1. **Candidate site groups: 13.** The only direct multi-row consolidation supported by the inspected paper is `KOK_RIVER_GEOTHERMAL_AREAS` (CR_01, CR_02, CR_03, CR_08; Wood & Singharajwarapan 2014, p. 612). The other 12 candidate groups are named manifestations/systems; they are not thereby proven independent hydrothermal reservoirs.
2. **Conservative validation clusters: 9.** To avoid a held-out observation from the same named area or related active-fault corridor being predicted from its neighbours, the groups were co-withheld as follows:

| Conservative validation cluster | Source records | Basis / uncertainty |
|---|---|---|
| KOK_RIVER_GEOTHERMAL_AREAS | CR_01, CR_02, CR_03, CR_08 | Direct multi-row grouping in the paper. |
| MAE_CHAN_FAULT_CORRIDOR | CR_04, CR_09, CM_16, CR_WNL | The paper describes multiple springs along the active Mae Chan fault and explicitly relates Wiang Nong Lom to it. It does **not** prove all four are one reservoir; CR_09 and CM_16 membership remain unresolved. |
| MAE_THA_FAULT_CORRIDOR | CM_01, CM_02 | Paper treats San Kamphaeng and Doi Saket as distinct named systems but relates both to the Mae Tha fault. Co-withholding is a leakage safeguard, not a merger claim. |
| PONG_PHU_FUANG_MAE_SUAI | CR_05 | One Table 1 named manifestation. |
| SOP_PONG_WIANG_PA_PAO | CR_06 | One Table 1 named manifestation. |
| HUAI_SAI_KHAO_PHAN | PR_07 | One Table 1 named manifestation. |
| FANG | CM_03 | One Table 1 named manifestation. |
| BAN_PONG_NAM_RON | LPa_04 | One Table 1 named manifestation. |
| MAE_JOK_PHRAE | PR_02 | One Table 1 named manifestation. |

**Result:** The defensible, conservative maximum for a group-held-out exercise is **9 validation units**, not 16 independent labels. This is an upper bound on usable independent systems because several singleton designations and the two fault-corridor memberships need further source review.

## Spatial-block sensitivity count

Using the reported UTM coordinates under EPSG:32647, each conservative cluster was assigned a centroid (mean easting/northing of its member rows). A north/east-aligned grid anchored at projected coordinate (0,0) was used only to count occupied cells; it is not a final geological blocking design.

| Candidate grid cell width | Occupied cells containing conservative-cluster centroids | Consequence |
|---:|---:|---|
| 25 km | 9 | One cluster per occupied cell in this particular alignment; leave-one-cell-out is numerically the same as leave-one-cluster-out and does not create an independent external test. |
| 50 km | 7 | Two cells contain two clusters each; at most seven spatial test folds. |
| 75 km | 6 | Multiple geological contexts are merged; at most six spatial test folds. |

Grid origin, orientation and block width affect the count. These counts are a feasibility diagnostic, not an optimized design. Before any authorized experiment, report sensitivity across offset grids and set an exclusion buffer based on measured spatial correlation and positional uncertainty; do not choose a size because it gives a favorable score.

## Proposed validation designs

### A. Leave-one-conservative-cluster-out (LOGO)

- Nine outer folds: hold out all records and all sampled background inside one `validation_cluster_id` per fold.
- Preprocessing, background construction, feature selection, thresholding and any tuning occur using that fold’s training region only.
- `CR_02` must be assessed in two prespecified variants: source UTM representation included versus its whole Kok River cluster excluded. `CM_16` must be excluded or marked low-confidence in a sensitivity variant.
- Report each fold separately. A pooled mean is descriptive only; it is not a stable estimate of Thailand-wide performance.

### B. Spatial-block-held-out sensitivity

- Run leave-one-occupied-cell-out at 50 km and 75 km grids, with multiple offsets/orientations and whole validation clusters assigned atomically.
- Use a buffer around held-out cells/groups before background sampling and any spatial feature construction. Buffer distance is **TBD**; no empirical variogram or predictor correlation range has been measured in this task.
- Do not let samples from one named/fault-correlated cluster appear in both train and test even if a grid boundary cuts through it.

## Is predictive validation feasible now?

**No, not rigorously.** Nine conservative units (and only six to seven coarse spatial blocks) can support data-ingestion checks and perhaps a clearly labelled exploratory descriptive baseline after the pending gates. They are insufficient for reliable model selection, hyperparameter tuning, uncertainty calibration, regional transfer claims, or a credible estimate of predictive performance. There is no independently curated external-region occurrence registry, and background cells are not verified negatives.

The available temperature label also has an unresolved internal source conflict for `CR_02` (Table 1: 85°C; p. 612 Kok River prose: group maximum 73°C). Therefore temperature thresholding must not be used as a target definition until source precedence is resolved.

## Decision: NO-GO FOR PREDICTIVE MODELING

This decision applies to predictive-model training/performance claims from the current 16-row registry. It is driven by the 9-unit conservative ceiling, unresolved `CR_02`/`CM_16` integrity issues, uncertain group memberships, lack of true negatives, and lack of an external held-out registry—not by a lack of interest in the research question.

The permitted alternative is an **evidence-ranking GIS product**, not a predictive model: provenance-tiered surface-manifestation coverage; fault/geology/DEM overlays; explicit coordinate-confidence markers; and sensitivity maps that state assumptions. It must not be marketed as validated geothermal prospectivity, a probability of occurrence, or evidence of commercial viability.

## Required gates to reconsider the decision

1. Resolve or formally document the `CR_02` coordinate conflict and obtain authoritative provenance for `CM_16`.
2. Acquire and audit an authoritative Thai occurrence inventory with unique identifiers, dates, coordinate metadata and reuse terms.
3. Review system membership with hydrogeologic/geologic evidence and define the target before sampling.
4. Acquire a geographically independent, audited registry (for example a southern region) before any transfer claim.
5. Pre-register group/block and background protocol before fitting a model.
