# Positive-Unlabeled (PU) Learning & Class Imbalance Audit — Phase 2F.1
**GeoThermAI Methodological Evaluation**  
*Date: 28 October 2026 | Theoretical Framework: Positive-Unlabeled (PU) Exploration Modeling*

---

## 1. The Core Scientific Premise: Unknown != Negative

In geothermal exploration and mineral prospectivity mapping, data reality differs fundamentally from classic supervised machine learning:
1. **Known Positives ($P$):** Locations with documented, verified surface thermal manifestations (geysers, boiling hot springs) or drilled commercial production wells.
2. **Unlabeled Background ($U$):** Every other grid cell across the territory.
   - **Critical Principle:** The absence of a surface hot spring **DOES NOT** prove the absence of a geothermal reservoir.
   - Deep concealed or blind geothermal reservoirs (such as Desert Peak, Nevada, or fault-sealed hydrothermal traps in Thailand) exhibit no surface boiling discharge.
   - Treating $U$ as confirmed negatives ($y = 0$) introduces severe **label noise and negative contamination**, directly penalizing algorithms that correctly identify prospective blind systems.

---

## 2. Mordensky et al. (2023) Imbalance Benchmark vs. Thailand

### Western United States Assessment (Williams et al., 2008 / Mordensky et al., 2023):
- Total grid cells ($2\text{ km} \times 2\text{ km}$): $N = 725,442$
- Known positive cells: $P = 278$
- Unlabeled cells: $U = 725,164$
- Empirical class prevalence: $\pi = \frac{278}{725,442} \approx 0.0003832$ ($1 : 2,609$)

### Thailand Data Reality:
- Total candidate Northern pilot cells ($2\text{ km} \times 2\text{ km}$ over $102,028.5\text{ km}^2$): $\approx 25,507$ cells.
- Surface manifestation records: 47 published points (14 internally consistent in North, 2 withheld, 31 provisional in South).
- **Independent hydrothermal systems in North:** Only **6 to 10 systems** (e.g. Fang, San Kamphaeng, Mae Chan).
- **CRITICAL RESTRICTION:**
  The USGS class prevalence ($0.038\%$) is specific to the Western US tectonic regime (Basin and Range crustal extension and Walker Lane transform faulting). **It must NOT be copy-pasted or assumed as factual class prevalence for Thailand.**

---

## 3. Evaluation Metrics Limitations Under PU Conditions

Standard supervised classification metrics fail catastrophically under extreme PU imbalance:

| Metric | Mathematical Limitation Under PU Conditions | Recommendation for GeoThermAI |
|---|---|---|
| **Accuracy** | $\frac{TP + TN}{N}$. A degenerate dummy model predicting $0$ everywhere achieves **$99.96\%$ accuracy**, while failing entirely to discover any geothermal resource. | **FORBIDDEN** as an exploration quality metric |
| **F1-Score** | $2 \frac{P \cdot R}{P + R}$. Unlabeled cells that actually contain undiscovered blind geothermal systems are counted as "False Positives" ($FP$), artificially penalizing prospective predictions. | **NOT INFORMATIVE** without known class prior $c = P(s=1|y=1)$ |
| **ROC-AUC** | True Positive Rate vs. False Positive Rate ($FPR = \frac{FP}{FP + TN}$). Because $TN$ is massive ($>700,000$), $FPR$ stays near zero even with thousands of false alarms, creating misleadingly high ROC-AUC ($>0.85$). | **SECONDARY ONLY**; report with caution |
| **PR-AUC (Average Precision)** | Precision vs. Recall curve area. Highly sensitive to false alarms in the top ranks. Under PU conditions with Selected Completely At Random (SCAR), PR-AUC is proportional to true PR-AUC up to a constant scalar $c$. | **RECOMMENDED PRIMARY STATISTICAL METRIC** |
| **Recall @ Top X% Land Area** | $\frac{\text{Positives in Top } X\% \text{ Ranked Cells}}{\text{Total Known Positives}}$. Directly answers the exploration economic question: *"If we survey the top 10% most favorable land area, what percentage of geothermal systems do we capture?"* | **RECOMMENDED PRIMARY GEOLOGICAL & DECISION METRIC** |

---

## 4. Preregistered PU Training Strategies for Phase 3 Adaptation

When the Thai ML Gate is legitimately cleared, the following PU learning algorithms will be benchmarked:
1. **Biased PU Formulation (Elkan & Noto, 2008):**
   - Assumes known positives are Selected At Random (SAR) conditional on spatial features: $s = 1 \implies y = 1$, $P(s=1|y=0) = 0$.
2. **Two-Step Heuristic (Spy-based or Rocchio clustering):**
   - Identifies "Reliable Negatives" ($RN$) from the background that are statistically furthest from any thermal manifestation in feature space.
3. **Bagging PU / Ensemble Subsampling:**
   - Trains an ensemble of models, each pairing all known positives ($P$) with a distinct random subsample of unlabeled background ($U_b$), averaging predictions across 100 realizations.
