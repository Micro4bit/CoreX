# Spatial Validation & Buffer Sensitivity Audit — Phase 2F.1
**GeoThermAI Methodological Integrity Review**  
*Date: 28 October 2026 | Topic: Spatial Autocorrelation, Buffer Sensitivity, and Small-Sample Gating*

---

## 1. The Challenge of Spatial Autocorrelation in Geoscience AI

In geospatial datasets, neighboring locations exhibit high spatial autocorrelation (Tobler's First Law of Geography: *"Everything is related to everything else, but near things are more related than distant things"*).
- When a model is evaluated using standard random K-Fold cross-validation, points from the test fold fall within hundreds of meters of training points.
- This creates **Spatial Data Leakage**: the model merely memorizes the coordinates and local terrain of nearby training occurrences, resulting in artificially inflated test accuracy ($>95\%$) that collapses when applied to a genuinely new exploration basin.

---

## 2. Buffer Sensitivity Testing Schedule (5 to 30 km)

In Phase 2E, a 20 km exclusion buffer was proposed as an initial hypothesis.

### Critical Methodological Audit:
**A 20 km buffer is a provisional hypothesis, NOT an immutable physical law.**

To scientifically determine the optimal spatial exclusion distance, GeoThermAI Phase 2F.1 preregisters a 5-step **Buffer Sensitivity Testing Schedule**:

| Candidate Buffer Radius | Geological & Hydrological Hypothesis | Spatial Impact on Background Sampling | Trade-off / Risk |
|---|---|---|---|
| **5 km** | Local hydrothermal discharge plume boundary; covers immediate shallow outflow apron | Minimal background exclusion; preserves maximum training area | High risk of spatial autocorrelation leakage from deeper fracture conduits |
| **10 km** | Typical strike length of active segment in Mae Chan / Mae Tha fault zones | Moderate exclusion of surrounding valley sediments | Balances local structure isolation with background availability |
| **15 km** | Regional convective cell diameter in Basin-and-Range style extensional geothermal systems | Substantial exclusion around major thermal clusters (e.g. Fang, San Kamphaeng) | May eliminate prospective fault steps between neighboring sub-basins |
| **20 km** | Phase 2E default hypothesis; deep crustal recharge-to-discharge circulation radius | Broad exclusion zone around each northern hot spring cluster | Substantially reduces valid background grid cells in narrow intermontane valleys |
| **30 km** | Deep regional tectonic stress domain; eliminates all regional crustal correlation | Severe exclusion; multiple northern clusters merge into single exclusion masks | High risk of severe data starvation in Northern Thailand ($102,028.5\text{ km}^2$) |

### Preregistered Sensitivity Procedure:
When training is unlocked, models will be trained and evaluated under each of the 5 buffer radii (5, 10, 15, 20, 30 km). If performance drops drastically between 5 km and 20 km, it confirms that smaller buffers suffered from spatial leakage.

---

## 3. Independent System Grouping & Small-Sample Gating

### The Clustering Reality in Northern Thailand:
- Surface manifestation points in published catalogs (e.g. Wood & Singharajwarapan, 2014) report individual hot spring discharge orifices.
- For example, multiple thermal vents along the Kok River or in the San Kamphaeng basin share a single underlying convective heat engine and deep fracture network.
- As audited in [`PHASE2F_LABEL_REVIEW.csv`](file:///Users/knight/Development/CoreX/GeoThermAI/tasks/phase_2f_scientific_validation/PHASE2F_LABEL_REVIEW.csv), there are **only 6 to 10 genuinely independent hydrothermal systems** in the candidate Northern pilot area.

### Truthful Non-Estimability Rule:
```
IF confirmed_independent_systems < 5:
    evaluation_status = "EVALUATION_NOT_ESTIMABLE"
    message = "Statistical sample size of independent positive clusters is insufficient "
              "to compute statistically meaningful cross-validation metrics. "
              "Reporting F1 or AUC on <5 independent clusters is scientifically misleading."
```

Under no circumstances will GeoThermAI publish cross-validation metrics if the effective sample size is below this statistical threshold.

---

## 4. Status of Expert Adjudication Fields

In [`PHASE2F_LABEL_REVIEW.csv`](file:///Users/knight/Development/CoreX/GeoThermAI/tasks/phase_2f_scientific_validation/PHASE2F_LABEL_REVIEW.csv):
- `expert_reviewer`: **STRICTLY BLANK**
- `review_date`: **STRICTLY BLANK**
- `review_evidence_uri`: **STRICTLY BLANK**
- `system_decision`: **PENDING_EXPERT_HYDROLOGIC_REVIEW**

These fields will remain unapproved until qualified external hydrogeologists review primary well logs and geochemical isotope data and provide signed documentary evidence.
