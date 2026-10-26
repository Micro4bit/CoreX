# GeoThermAI — RESEARCH & TECHNICAL BLUEPRINT

**Version:** 0.1  
**Status:** Proposed methodology; not validated results.

## 1. Scientific Scope

GeoThermAI targets **geothermal exploration prospectivity screening**, not confirmation of commercial geothermal reserves.

All outputs must distinguish:

- Geological indicators
    
- Statistical prospectivity estimates
    
- Predictive uncertainty
    
- Data availability and quality
    
- Exploration suitability
    
- Commercial feasibility
    

These are related but not interchangeable concepts.

## 2. Research Design

Use a staged research design.

### Stage A — Data Feasibility

Identify, inspect, and document accessible geospatial datasets.

Candidate sources include:

- Department of Mineral Resources geological maps
    
- Fault and structural geology information
    
- Hot spring inventories
    
- Digital elevation models
    
- Landsat-derived surface temperature
    
- Relevant geophysical datasets
    
- Borehole temperature or heat-flow data, if accessible
    
- Grid infrastructure and access information for supporting analyses
    

These are candidate sources, not a verified complete dataset inventory.

For every dataset record:

- Publisher
    
- Original source URL
    
- Access date
    
- Spatial coverage
    
- Temporal coverage
    
- Resolution
    
- Coordinate reference system
    
- Units
    
- License
    
- Missing-data patterns
    
- Measurement uncertainty
    
- Processing history
    
- Potential target leakage
    

### Stage B — Pilot Study Selection

Choose a study area based on:

- Sufficient positive observations
    
- Adequate spatial coverage
    
- Meaningful geological variation
    
- Availability of independent validation evidence
    
- Manageable data processing requirements
    

Northern Thailand is a candidate, not a finalized study area.

### Stage C — Modeling

Start with interpretable methods.

Candidate models:

- Transparent rule-based or geological screening baseline
    
- Logistic Regression
    
- Random Forest or Gradient Boosting
    
- XGBoost, where justified
    

More complex models are optional and require demonstrated value.

### Stage D — Data Fusion Experiment

Compare, at minimum:

**Model A:** Selected baseline geological predictors.

**Model B:** Model A plus suitable satellite-derived predictors.

**Model C:** A justified alternative modeling strategy or uncertainty-aware decision layer.

Keep training splits, evaluation areas, and other experimental conditions comparable.

### Stage E — Spatial Validation

Use spatially separated validation where scientifically appropriate.

Avoid relying exclusively on random train/test splits because neighboring geospatial samples may be highly correlated.

Document:

- Spatial blocking design
    
- Block size and rationale
    
- Geographic distribution of samples
    
- Class imbalance
    
- Hyperparameter tuning procedure
    
- Independent test-set handling
    
- Sensitivity to validation design
    

### Stage F — Uncertainty

Evaluate feasible methods such as:

- Bootstrap variation
    
- Model ensembles
    
- Sensitivity to input features
    
- Variation across spatial folds
    
- Out-of-distribution or insufficient-data flags
    

Do not label a raw model score as a calibrated probability unless calibration has been evaluated.

## 3. Critical Labeling Risks

### Positive Observations

Known hot springs or geothermal occurrences may provide partial positive evidence, but do not automatically indicate economically viable power-generation resources.

### Negative Observations

Areas without recorded geothermal occurrences are not necessarily confirmed negatives.

Consider:

- Positive-unlabeled learning
    
- Carefully justified background sampling
    
- Sensitivity analysis for alternative negative/background strategies
    

### Data Leakage

If known hot spring coordinates define the prediction target, using distances to those same hot springs as predictors may leak target information.

Also inspect:

- Spatial duplicates
    
- Neighboring pixels from the same observation
    
- Survey-derived features that encode labels
    
- Preprocessing conducted before cross-validation
    

## 4. Satellite Data Caveat

Satellite land surface temperature is affected by weather, land cover, elevation, time of observation, and surface conditions.

**It is not direct evidence of deep geothermal reservoir temperature.**

The research must test whether satellite-derived features contribute meaningful independent information.

If they do not, report the negative finding.

## 5. Proposed Evaluation

Candidate metrics, selected according to the labeling design:

- PR-AUC or ROC-AUC where valid labels permit
    
- Recall of withheld known occurrences
    
- Precision or enrichment in top-ranked screening areas
    
- Performance variation across spatial folds
    
- Ranking stability
    
- Calibration metrics if probability estimates are defensible
    
- Coverage of known occurrences versus fraction of land screened
    

Do not interpret background samples as verified negatives without justification.

Report confidence intervals or uncertainty where feasible.

## 6. Decision-Support Evaluation

A practical test is to compare alternative exploration ranking policies under the same assumed survey budget.

Example policy types:

- Geological baseline ranking
    
- AI ranking
    
- Uncertainty-aware ranking
    

Measure:

- Number or proportion of withheld known occurrences captured
    
- Area requiring follow-up
    
- Stability of rankings
    
- Sensitivity to survey cost assumptions
    

These are retrospective or simulated screening outcomes, not measured real-world drilling savings.

## 7. Economic Feasibility Module

**Purpose:** Illustrate decision tradeoffs, not certify bankability.

Potential inputs:

- Assumed survey cost
    
- Access and infrastructure proxies
    
- Distance to grid
    
- Exploration stage
    
- Scenario-specific drilling costs
    
- Uncertainty assumptions
    

Suggested scenarios:

- Low-cost case
    
- Central case
    
- High-cost case
    

Report all assumptions, units, currency year, and sources.

Do not calculate a site-specific LCOE unless adequate resource, drilling, production, operating, financing, and plant-performance assumptions are explicitly justified.

Do not convert prospectivity scores directly into MW.

## 8. Energy Scenario Module

Potential questions:

- Under what hypothetical conditions could geothermal contribute to clean firm energy?
    
- How would dispatchable geothermal generation differ conceptually from variable renewable generation?
    
- What constraints would govern integration into electricity supply?
    

PDP2026 references require verification against official, current documents.

Data-center scenarios must not assume that all data centers reject fossil-generated electricity.

Energy-system scenarios must remain explicitly hypothetical unless backed by verified generation and resource data.

## 9. Suggested Technology Stack

Candidates, subject to team capability:

- Python
    
- GeoPandas
    
- Rasterio / GDAL
    
- Scikit-learn
    
- XGBoost
    
- SHAP where appropriate
    
- QGIS
    
- Streamlit or a lightweight web GIS
    
- Git for version control
    

Technology selection should follow research needs rather than drive the research question.

## 10. Reproducibility

Maintain:

- Data provenance register
    
- Processing scripts
    
- Fixed random seeds where applicable
    
- Environment specification
    
- Model configurations
    
- Validation split definitions
    
- Experiment logs
    
- Generated output metadata
    
- Citation register
    

Avoid uploading restricted datasets or exposing sensitive infrastructure data without permission.

## 11. Reference Literature

**Methodological reference**

"When less is more: How increasing the complexity of machine learning strategies for geothermal energy assessments may not lead toward better estimates."

_Geothermics_ (2023).

DOI: [https://doi.org/10.1016/j.geothermics.2023.102662](https://doi.org/10.1016/j.geothermics.2023.102662)

Use as motivation to compare model complexity. Specific methods, findings, and quantitative results must be verified from the original paper before citation.

**User-provided reference files**

- `Energy.pdf`
    
- `1-s2.0-S0375650523000160-main.pdf`
    

These files are research inputs. Their specific findings, figures, equations, and economic parameters are **not yet incorporated as verified evidence** in this blueprint.

AI agents must inspect the actual documents before making document-specific claims.

## 12. Research Gates

**Gate 1 — Data Readiness**

Pass only if the pilot area has accessible, legally usable datasets and a defensible evaluation design.

**Gate 2 — Baseline Validity**

Pass only if the baseline can be reproduced and evaluated without obvious leakage.

**Gate 3 — Data Fusion Value**

Determine whether satellite features improve results, worsen them, or show no reliable difference.

**Gate 4 — Decision Utility**

Evaluate whether rankings and uncertainty information provide useful decision support under transparent assumptions.

**Gate 5 — Competition Readiness**

Require a coherent scientific story, demonstrable outputs, reproducible evidence, and clear limitations.

## 13. Main Risks

|Risk|Mitigation|
|---|---|
|Insufficient geothermal labels|Limit scope; explore suitable learning designs|
|Geographic data leakage|Spatial validation and feature audits|
|Misleading satellite signals|Ablation and sensitivity tests|
|Unsupported economic assumptions|Explicit scenarios and ranges|
|Overextended project scope|Prioritize research MVP|
|Overclaiming electricity potential|Separate screening from resource confirmation|
|Limited novelty|Compare against existing methods and demonstrate decision value|

## 14. Suggested 12-Week Development Sequence

**Weeks 1–3:** Dataset audit, pilot selection, baseline setup.

**Weeks 4–6:** Model development, spatial validation, data fusion experiments.

**Weeks 7–9:** Uncertainty analysis, ranking evaluation, preliminary economic scenarios.

**Weeks 10–12:** Dashboard, research documentation, presentation, independent review.

This is a proposed schedule, not a confirmed competition calendar.