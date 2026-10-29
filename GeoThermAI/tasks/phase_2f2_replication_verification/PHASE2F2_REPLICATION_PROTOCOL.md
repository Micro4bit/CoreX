# Methodological Replication Protocol — Phase 2F.2
**USGS Mordensky et al. (2023) Replication & Adaptation Specification**  
*Date: 28 October 2026 | Benchmark: Geothermics 110:102662 | Tag: `USGS_REPLICATION_ONLY`*

---

## 1. Scientific Framework & Classification

To maintain uncompromising scientific honesty, all replication activities in GeoThermAI must be explicitly classified according to the following 5-tier taxonomy:

```
[ EXPERIMENTAL OUTCOME TAXONOMY ]
  1. EXACT_REPLICATION        : Raw authentic USGS data, exact features, exact splits, identical loss/hyperparameters.
  2. PARTIAL_REPLICATION      : Authentic USGS data with minor software-framework differences (e.g. Scikit-Learn vs R).
  3. METHOD_ADAPTATION        : Methodological variation (e.g. 10:1 background undersampling or alternative PU formulation).
  4. SYNTHETIC_SOFTWARE_TEST  : Deterministic synthetic mock dataset used to verify pipeline execution and numerical stability.
  5. NOT_REPRODUCED           : Execution failed, data missing, or empirical results contradict published claims.
```

### Protocol Status for Phase 2F.2:
- **Sandbox Execution Status:** `SYNTHETIC_SOFTWARE_TEST` (Harness run using mock Western US distribution).
- **Undersampling Experiment Status:** `METHOD_ADAPTATION` (10:1 background-to-positive ratio on train fold).
- **Authentic Data Status:** `NOT_REPRODUCED` (Pending manual browser acquisition due to ScienceBase Cloudflare challenge).

---

## 2. Benchmark Population & Ground Truth

- **Spatial Resolution:** $2\text{ km} \times 2\text{ km}$ equal-area cells across Western United States.
- **Total Population ($N$):** $725,442$ cells.
- **Positive Hydrothermal Systems ($P$):** $278$ cells containing confirmed conventional hydrothermal systems (Williams et al., 2008).
- **Unlabeled Background ($U$):** $725,164$ cells.
- **Class Prevalence ($\pi$):** $\frac{278}{725,442} \approx 0.0003832$ ($1 : 2,609$).
- **Features Evaluated (5):**
  1. `heat_flow_mw_m2`: Terrestrial heat flow ($\text{mW/m}^2$)
  2. `dist_quaternary_fault_km`: Proximity to mapped Quaternary faults ($\text{km}$)
  3. `dist_quaternary_magma_km`: Proximity to Quaternary volcanic centers ($\text{km}$)
  4. `seismic_event_density_per_km2`: $M \ge 3$ earthquakes within $4\text{ km}$ radius
  5. `max_horizontal_stress_direction_deg`: $S_{Hmax}$ azimuth orientation ($0\text{--}180^\circ$)

---

## 3. Train/Test Partitioning & Preprocessing Protocol

### Partitioning:
- **Ratio:** 80% Training ($N_{\text{train}} \approx 580,353$ cells; $P_{\text{train}} \approx 222$ positives) / 20% Testing ($N_{\text{test}} \approx 145,089$ cells; $P_{\text{test}} \approx 56$ positives).
- **Stratification:** Stratified by positive label presence to guarantee identical positive prevalence across splits.
- **Replication Iterations:** 10 repeated randomized splits (`random_seed` $\in [42, 51]$) to quantify statistical variance.

### Strict Leakage Prevention:
1. **Scaler Fitting:** `StandardScaler.fit()` is computed **strictly on the training fold**.
2. **Test Transformation:** The test fold is transformed using training mean ($\mu_{\text{train}}$) and standard deviation ($\sigma_{\text{train}}$).
3. **No Target Leakage:** Spatial coordinates and target indices are stripped from feature arrays prior to model fitting.

---

## 4. Class Imbalance & Adaptation Justification

In Mordensky et al. (2023), the paper evaluates how machine learning models perform under extreme class imbalance ($278$ positives vs. $725,164$ background):
- Full population training with extreme imbalance requires heavily weighted loss functions or probability calibration.
- In GeoThermAI's benchmark sandbox, an adaptation using **10:1 background-to-positive undersampling** on the training fold is implemented to stabilize gradient updates and prevent numerical underflow in tree splits.
- **Scientific Caveat:** Because 10:1 undersampling changes the empirical class balance from $1:2,609$ to $1:10$, raw predicted probabilities reflect the artificial training prior ($P(\text{positive}) \approx 0.09$) rather than the true regional prevalence ($0.00038$).
- This is classified as a **`METHOD_ADAPTATION`**, NOT an exact replication of full-population loss minimization.

---

## 5. Output Transformation: Normal-Score Mapping

To compare favorability surfaces across distinct algorithms (Logistic Regression vs. XGBoost vs. WoE), outputs are transformed using **Normal-Score Transformation**:
- **Formula:** $z_i = \Phi^{-1}\left( \frac{\text{rank}(\hat{y}_i) - 0.5}{N_{\text{test}}} \right)$
- **Target Distribution:** Standard Gaussian $\mathcal{N}(0, 1)$.
- **CRITICAL RESTRICTION:** Normal-score outputs represent **relative favorability ranking**, NOT physical probability of geothermal discovery or commercial power capacity.
