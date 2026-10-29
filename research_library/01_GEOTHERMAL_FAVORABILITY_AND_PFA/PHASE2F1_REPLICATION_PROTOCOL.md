# USGS Mordensky 2023 Replication Protocol — Phase 2F.1
**GeoThermAI Methodological Specification**  
*Date: 28 October 2026 | Status: Preregistered Experimental Protocol | Profile: MORDENSKY_2023_BASELINE_PROFILE*

---

## 1. Research Objective & Scope

This protocol defines the exact procedure to replicate the machine learning geothermal favorability workflow of **Mordensky et al. (2023)** (*Geothermics* 110, 102662) in an isolated sandbox. 

**Mandatory Guardrail:**
All models, parameters, logs, and outputs generated under this protocol are tagged `USGS_REPLICATION_ONLY`. Under no circumstances may any replication result be output or cited as geothermal prospectivity in Thailand.

---

## 2. Experimental Data Schema & Split Strategy

### Data Schema
- **Spatial Resolution:** $2\text{ km} \times 2\text{ km}$ equal-area cells across the Western United States.
- **Total Population:** $N = 725,442$ cells.
- **Positive Labels:** $P = 278$ cells containing confirmed hydrothermal systems.
- **Background:** $U = 725,164$ unlabeled cells.
- **Input Features (5):**
  1. `heat_flow_mw_m2`
  2. `dist_quaternary_fault_km`
  3. `dist_quaternary_magma_km`
  4. `seismic_event_density_per_km2`
  5. `max_horizontal_stress_mpa`

### Train/Test Splitting Protocol
1. **Partitioning:** Stratified 80/20 train/test split.
   - Training Set: $80\%$ of positives ($\approx 222$ cells) and $80\%$ of unlabeled background ($\approx 580,131$ cells).
   - Test Set: $20\%$ of positives ($\approx 56$ cells) and $20\%$ of unlabeled background ($\approx 145,033$ cells).
2. **Stratification Key:** Binary label indicator ($y \in \{0, 1\}$).
3. **Random Seed:** Fixed to `42` for baseline reproducibility, with 10 repeated randomized splits for variance estimation.

---

## 3. Preprocessing & Leakage Prevention Protocol

### Strict Fold Isolation Rule:
> **No preprocessing transformation that learns parameters from data (mean, standard deviation, quantiles, min, max) may be fitted on the combined dataset prior to splitting.**

### Step-by-Step Transformations:
1. **Physical Bounds Clipping:**
   - Distances $< 0\text{ km}$ clipped to $0$.
   - Heat flow bounded to physically viable crustal ranges ($10\text{--}350\text{ mW/m}^2$).
2. **Missing Value Handling:**
   - Median imputation fitted strictly on the training partition.
3. **Feature Standardization:**
   - $z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}}}$
   - `StandardScaler.fit()` is called exclusively on `X_train`. `X_test` is transformed using $\mu_{\text{train}}, \sigma_{\text{train}}$.

---

## 4. Class Imbalance & Positive-Unlabeled (PU) Strategy

Under the Positive-Unlabeled framework, background cells are not verified negatives ($P(s=1|y=0) = 0$).

### Imbalance Treatment:
1. **Undersampling of Unlabeled Background (Training Only):**
   - In the training set, unlabeled background is subsampled to a fixed ratio $r_{\text{unl}} = \frac{|U_{\text{train\_sample}}|}{|P_{\text{train}}|} \in \{5, 10, 20\}$.
   - Default baseline ratio: **$10 : 1$** (e.g. 222 positives : 2,220 sampled unlabeled cells).
2. **Full Population Evaluation:**
   - The test set retains the natural full class prevalence ($1 : 2,609$) to measure realistic ranking capability across the entire geographic region.

---

## 5. Machine Learning Algorithms

The replication focuses on two primary benchmark models:

### Model 1: Regularized Logistic Regression (LR)
- **Mathematical Form:** $P(y=1|\mathbf{x}) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$
- **Regularization:** L2 ridge penalty ($C = 1.0$), solver: `lbfgs`.
- **Purpose:** Serves as the transparent, convex baseline directly comparable to Williams and DeAngelo (2008).

### Model 2: Extreme Gradient Boosting (XGBoost)
- **Algorithm:** Tree-based ensemble minimizing binary cross-entropy loss with gradient boosting.
- **Hyperparameters:**
  - `n_estimators`: 100
  - `max_depth`: 4
  - `learning_rate`: 0.05
  - `subsample`: 0.8
  - `colsample_bytree`: 0.8
  - `eval_metric`: `logloss`
- **Purpose:** Replicates the nonlinear, feature-interacting model evaluated in Mordensky et al. (2023).

---

## 6. Output Transformation: Normal-Score Mapping

To compare favorability surfaces across distinct algorithms (LR vs. XGBoost vs. WoE), Mordensky et al. (2023) apply a **Normal-Score Transformation**:
- **Algorithm:** Rank-based quantile transformation mapping predictions to standard normal distribution $\mathcal{N}(0, 1)$.
- **Mathematical Form:** $z_{\text{favorability}} = \Phi^{-1}\left( \frac{\text{rank}(\hat{y}) - 0.5}{N_{\text{eval}}} \right)$
- **Interpretation:**
  - High positive $z$ ($z > +2.0$): Top $\approx 2.3\%$ highest favorability cells.
  - Near zero $z$ ($z \approx 0.0$): Median regional background favorability.
  - Large negative $z$ ($z < -2.0$): Bottom $\approx 2.3\%$ least prospective cells.
- **SCIENTIFIC WARNING:** Normal scores reflect **relative ranking only**, NOT physical probability of discovering a commercial geothermal reservoir.

---

## 7. Performance Evaluation Metrics

Due to severe class imbalance and unverified background, traditional accuracy is meaningless ($>99.96\%$ by simply predicting all zeros). Evaluation must use:
1. **PR-AUC (Precision-Recall Area Under Curve / Average Precision):** The gold standard for highly imbalanced positive-unlabeled ranking.
2. **ROC-AUC:** Measures discrimination capability across all thresholds.
3. **Brier Score:** Mean squared calibration error: $\frac{1}{N} \sum (\hat{y}_i - y_i)^2$.
4. **Recall at Top 10% Land Area:** Percentage of known positive systems captured within the top $10\%$ highest predicted favorability grid cells (exploration efficiency).
