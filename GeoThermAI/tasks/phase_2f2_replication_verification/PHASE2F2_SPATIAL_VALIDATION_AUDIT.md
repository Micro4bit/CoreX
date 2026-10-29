# Ground Truth & Spatial Validation Audit — Phase 2F.2
**Small-Sample Gating, System Grouping & Buffer Sensitivity Protocol**  
*Date: 28 October 2026 | Topic: Spatial Leakage Controls & Non-Estimability Criteria*

---

## 1. Ground Truth Reality: Manifestations vs. Independent Systems

A critical flaw in early geothermal machine learning applications is treating every reported hot spring coordinate as an independent training observation.

### Comprehensive Audit of the Master Registry:
Across the master registry ([`geothermal_label_master_registry.csv`](file:///Users/knight/Development/CoreX/GeoThermAI/tasks/phase_1c_label_expansion_gis_foundation/geothermal_label_master_registry.csv), SHA-256: `93d3bf9c...`):
- **Total Published Rows:** Exactly **47 manifestation records**.
- **Northern Thailand Candidate Area (16 records):**
  - **14 Internally Consistent (`CRS_AND_DMS_CONSISTENT`):** Reported UTM Zone 47N coordinates agree with published Degrees-Minutes-Seconds within $<100\text{ m}$.
  - **1 Withheld for Discrepancy (`CR_02`):** UTM vs. DMS coordinates deviate by $>1,100\text{ m}$. Strictly withheld from training inputs.
  - **1 Withheld for Missing Data (`CM_16`):** Published table omits DMS verification coordinates. Strictly withheld from training inputs.
- **Southern Thailand Subset (31 records):**
  - All 31 southern records have unresolved UTM Zone 47N vs. Zone 48N coordinate ambiguities. Strictly flagged `PROVISIONAL_PENDING_UTM_ZONE_VERIFICATION` and excluded from model inputs.

### Effective Sample Size in Northern Thailand:
- Geologically, multiple surface thermal manifestations originate from single hydrothermal convective plumes along major regional faults.
- In Northern Thailand, the estimated number of genuinely independent hydrothermal systems is only **6 to 10 systems** (e.g. Fang, San Kamphaeng, Mae Chan, Wiang Pa Pao, Pong Nam Ron).
- **Scientific Impact:** An effective sample size of $N_{\text{pos}} \in [6, 10]$ is an **extreme small-sample regime**.

---

## 2. Preregistered Group-Preserving Spatial Validation

To prevent spatial autocorrelation leakage, GeoThermAI preregisters the following spatial validation architecture:

```
[ GROUP-PRESERVING SPATIAL K-FOLD ]
  Rule 1: All manifestation points belonging to the same candidate hydrothermal system 
          MUST be placed in the EXACT SAME validation fold.
  Rule 2: No system may ever have points split across the training partition and test partition.
  Rule 3: Fold boundaries must be separated by an exclusion buffer to prevent boundary autocorrelation.
```

---

## 3. Buffer Sensitivity Schedule (5 to 30 km)

In Phase 2E, an arbitrary 20 km buffer was suggested.

### Scientific Correction:
**A 20 km buffer is a provisional hypothesis, NOT an established geological constant.**

To evaluate spatial autocorrelation objectively, GeoThermAI establishes a 5-step sensitivity schedule:

| Candidate Radius | Hydrological & Structural Basis | Spatial Impact on Pilot AOI ($102,125.39\text{ km}^2$) | Autocorrelation Risk |
|---|---|---|---|
| **5 km** | Surface outflow apron & shallow gravel fan boundary | Minimal background exclusion; preserves maximum training area | High risk of spatial correlation through connected fractures |
| **10 km** | Average active segment length of Mae Chan / Mae Tha faults | Moderate background exclusion around valleys | Balances structural isolation with background availability |
| **15 km** | Convective cell diameter in Basin-and-Range style systems | Substantial exclusion around major clusters (Fang, San Kamphaeng) | May eliminate prospective fault steps between sub-basins |
| **20 km** | Deep crustal meteoric recharge-to-discharge circulation radius | Broad exclusion zone around each northern cluster | Substantially reduces valid background cells in intermontane basins |
| **30 km** | Regional crustal stress domain; eliminates all regional correlation | Severe exclusion; northern thermal clusters merge into single exclusion masks | High risk of severe data starvation across Northern Thailand |

### Preregistered Protocol:
When training is unlocked, the model will be evaluated across all 5 buffer distances. The variation in PR-AUC will quantify the magnitude of spatial autocorrelation in the feature set.

---

## 4. Truthful Small-Sample Non-Estimability Criteria

```
IF expert_confirmed_independent_systems < 5:
    evaluation_status = "EVALUATION_NOT_ESTIMABLE"
    justification = "The statistical sample size of independent positive clusters is "
                    "insufficient to compute statistically valid cross-validation metrics. "
                    "Reporting F1 or AUC on <5 clusters is scientifically indefensible."
```

Under this rule, GeoThermAI will explicitly refuse to publish cross-validation accuracy if the effective independent sample size drops below 5 confirmed systems.

---

## 5. Status of Expert Adjudication Fields

In [`PHASE2F_LABEL_REVIEW.csv`](file:///Users/knight/Development/CoreX/GeoThermAI/tasks/phase_2f_scientific_validation/PHASE2F_LABEL_REVIEW.csv):
- `expert_reviewer`: **STRICTLY BLANK**
- `review_date`: **STRICTLY BLANK**
- `review_evidence_uri`: **STRICTLY BLANK**
- `system_decision`: **PENDING_EXPERT_HYDROLOGIC_REVIEW**

These fields will remain unapproved until qualified external hydrogeologists review primary isotope, geochemical, and well data and provide formal documentary evidence.
