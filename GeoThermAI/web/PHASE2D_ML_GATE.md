# Phase 2D predictive ML gate

Decision: **NO-GO** on 2026-10-26.

No predictive model was fitted. No prospectivity surface, probability, drilling-success estimate, MW, LCOE or cost-saving claim was created.

The effective sample size is not the 47 published rows: two northern locations are withheld, 31 southern coordinates are provisional, and 18 co-withholding units are not domain-confirmed independent systems. There is no validated negative class. Predictor coverage is partial or restricted: northern-only geology, missing structure geometry, license-blocked active faults, five terrain tiles, sparse/repeated heat-flow measurements with no reported uncertainty, and zero usable Landsat ST rasters.

The gate can be reconsidered only after:

1. authoritative resolution/withholding policy and expert system-group review;
2. a locked study area with permitted predictor coverage;
3. an approved positive–unlabeled/background design;
4. preregistered group/spatial blocking, exclusion buffers, leakage control and external geographic testing;
5. sufficient effective independent groups to support honest uncertainty estimates.

If approved later, first compare a geology-only baseline, regularized logistic regression and one justified tree model under identical spatial/group folds. Satellite features must enter only as an ablation using real QA-cleared rasters. Full protocol: `tasks/phase_2d_data_readiness/spatial_validation_protocol.md`.

