# Preregistered Validation Design — DRAFT (NO TRAINING)

## Model target
Relative prospectivity for geothermal exploration. Not calibrated probability of occurrence, not drilling success, not electricity-grade MW.

## Label/background policy
- Positive training examples only from independent, domain-verified geothermal systems matched to valid features. Duplicate manifestations in one system are one group.
- Unobserved/background locations remain `UNLABELED` rather than asserted negative. Candidate PU / case-control design requires rationale, sampling-bias sensitivity and geologist review.
- Do not derive target-lookup predictors such as `distance_known_manifestation_m` or `manifestation_density` from the same label set.

## Fold design
1. Freeze study region, data versions, feature families, site IDs and folds **before** model selection.
2. Separate all observations belonging to the same `system_group_id`; test at least a true geographic held-out area if independent labels permit.
3. Phase 2E named a 20-km buffer as initial protocol, but this is **a proposed parameter**, not a scientifically validated constant. Test spatial autocorrelation and assess buffer sensitivity (e.g. 5, 10, 20, 30 km) only where the geography allows, without picking the buffer that inflates scores.
4. Apply background sampling, categorical encoding, imputation and scaling *within training folds* only. No full-dataset data transformation that leaks test information.
5. If valid group count too small for meaningful blocking or external test, stop; emit `EVALUATION_NOT_ESTIMABLE`, report data needs, no headline accuracy.

## First models if gate later passes
A) legally permitted scientifically grounded PFA/geology baseline; B) regularized Logistic Regression; C) one small XGBoost/Random Forest model under same folds. Limited features with rationale; test one feature family at a time (ablation).

## Reporting
- Data support masks and group counts, out-of-region generalization limits, confidence intervals only when estimable.
- Precision/Recall/AUC computed **only** when assumptions regarding true labels and background are explicitly valid; report presence-background ranking / recall-at-area metric with clear denominator and survey bias when applicable.
- Never convert a normal-score-transformed favorability score into an occurrence probability.
- Cross validation is not a substitute for truly external geographic evidence.

Scientific methodological references:
- Mordensky et al. 2023 https://doi.org/10.1016/j.geothermics.2023.102662
- Roberts et al. 2017 https://doi.org/10.1111/ecog.02881
- Valavi et al. 2019 https://doi.org/10.1111/2041-210X.13107
- Mordensky et al. 2025 https://doi.org/10.1016/j.geothermics.2025.103450
