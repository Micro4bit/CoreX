# Next-Phase Readiness

Date: 2026-10-23  
Phase reviewed: Data Acquisition and Label Validation.

## Research decision: CONDITIONAL GO

Proceed to **label curation and a small northern data-engineering feasibility pilot**. Do not proceed to a claim of validated Thailand-wide geothermal prospectivity AI, commercial-resource prediction, resource MW, or drilling success.

## What has passed

- A cited northern hot-spring registry was derived from a downloaded and visually inspected primary table: 16 records, with UTM coordinates for all records and reported surface temperature for 14.
- DMR rock-unit queries are real and return usable polygon geometry in Esri JSON.
- DMR active-fault vector data were downloaded, opened, and profiled.
- One SRTM-derived 1-arc-second tile was downloaded and inspected successfully.
- IHFC heat-flow observations were downloaded and their actual schema/duplicate pattern inspected.

## Blocking acceptance criteria

All items below are required before fitting any predictive experiment.

1. **Coordinates and labels**: Verify UTM zone/hemisphere for all northern registry rows; preserve raw values; assign a `site_group_id`; record coordinate confidence, evidence level, and source date.
2. **Target definition**: Formally lock the target as surface thermal manifestation, a thresholded temperature class, or another evidence tier. Do not silently convert it to reservoir/commercial potential.
3. **Independent units**: Report the number of distinct geothermal-system groups after deduplication. If there are too few groups for meaningful held-out testing, stop predictive modeling.
4. **Spatial validation**: Pre-register at least one group-held-out and one spatial-block-held-out split. Choose spatial block/exclusion distances from measured clustering and sensitivity analysis; do not use random split as the only test.
5. **Leakage register**: Prohibit all label-derived predictors and verify that preprocessing, background sampling, feature selection, and tuning occur inside training folds.
6. **Covariate coverage**: Obtain geometry for each intended geology/structure layer; record CRS, scale, date, license, and transformations. Acquire valid Landsat product files and perform QA/cloud/data-gap checks before proposing a satellite ablation.
7. **License clearance**: Resolve the active-fault resource's conflicting CC Attribution and noncommercial/no-legal-citation text. Confirm permissions for all downloadable and literature-derived data used in redistributed artifacts.
8. **External test**: Obtain and audit a separate southern or other-region georeferenced occurrence registry before claiming geographic transfer outside the northern pilot.

## Permitted work before all criteria pass

- Build a provenance-preserving label/feature catalog.
- Validate geometry and coordinate transformations.
- Create descriptive maps marked as evidence coverage, not prediction.
- Test data ingestion and calculate label clustering without reporting model skill.
- Design a transparent geological screening baseline only after its inputs are verified.

## Stop / re-scope conditions

Choose a nonpredictive evidence-ranking and uncertainty-mapping pilot if any of the following holds:

- the 16 records collapse into too few independent systems for spatial validation;
- DMR cannot provide/usefully expose structural geometry or permissions;
- no authoritative or auditable country-wide label inventory can be obtained;
- valid satellite products cannot be acquired with documented QA;
- an out-of-region registry remains unavailable.

In that fallback, clearly label output as a sensitivity-tested GIS evidence screen. It must not be presented as a validated AI prospectivity or commercial-resource map.
