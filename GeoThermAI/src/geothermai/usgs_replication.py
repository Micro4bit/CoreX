"""USGS Methodology Replication Sandbox for GeoThermAI.

Provides an isolated sandbox to replicate and benchmark established geothermal
favorability methodologies from USGS publications, specifically:
- Canonical Baseline: Mordensky et al. (2023), "When less is more: How increasing the
  complexity of machine learning strategies for geothermal energy assessments may not lead
  toward better estimates", Geothermics, 110, 102662. DOI: 10.1016/j.geothermics.2023.102662.
  Accompanying USGS data release: DOI: 10.5066/P9V1Q9XM.
- Preserved Alternative Profile: Play Fairway Analysis (PFA) / Great Basin 2025 profile
  (DeAngelo et al. 2024 / Mordensky et al. 2025).

CRITICAL ARCHITECTURAL GUARDRAIL:
All models, benchmarks, evaluations, and artifacts produced in this module are
strictly tagged 'USGS_REPLICATION_ONLY'. Programmatic assertions strictly prohibit
foreign USGS benchmark models from being applied to Thailand or presented as
Thai geothermal prospectivity predictions.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Sequence

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import QuantileTransformer, StandardScaler

USGS_REPLICATION_TAG: str = "USGS_REPLICATION_ONLY"
MORDENSKY_2023_DOI: str = "10.1016/j.geothermics.2023.102662"
USGS_2023_DATA_DOI: str = "10.5066/P9V1Q9XM"
MORDENSKY_2025_DOI: str = "10.1016/j.geothermics.2025.103450"
DEANGELO_2024_DOI: str = "10.1016/j.geothermics.2023.102882"

# ---------------------------------------------------------------------------
# Feature Profile Definitions
# ---------------------------------------------------------------------------

# Profile Name Constants
MORDENSKY_2023_BASELINE_PROFILE: str = "MORDENSKY_2023_BASELINE_PROFILE"
USGS_PFA_DEANGELO_PROFILE: str = "USGS_PFA_DEANGELO_PROFILE"

ReplicationOutcome = Literal[
    "EXACT_REPLICATION",
    "PARTIAL_REPLICATION",
    "METHOD_ADAPTATION",
    "SYNTHETIC_SOFTWARE_TEST",
    "NOT_REPRODUCED",
]

# Canonical Mordensky et al. (2023) 5 input feature families (Section 2.1)
# Note on units:
# - heat_flow_mw_m2: mW/m²
# - dist_quaternary_fault_km: km
# - dist_quaternary_magma_km: km
# - seismic_event_density_per_km2: M>=3 earthquakes within 4 km search radius
# - max_horizontal_stress_direction_deg: azimuth degrees (0-180°) from North (NOT MPa)
MORDENSKY_2023_FEATURES: tuple[str, ...] = (
    "heat_flow_mw_m2",
    "dist_quaternary_fault_km",
    "dist_quaternary_magma_km",
    "seismic_event_density_per_km2",
    "max_horizontal_stress_mpa",  # Preserved as variable key; native units audited as azimuth / orientation
)

# Backward-compatibility alias
USGS_BENCHMARK_FEATURES: tuple[str, ...] = MORDENSKY_2023_FEATURES

# Preserved alternative profile: Play Fairway Analysis (DeAngelo et al. 2024 / Great Basin 2025)
USGS_PFA_DEANGELO_FEATURES: tuple[str, ...] = (
    "temp_3km_c",
    "fault_density_km_km2",
    "slip_dilation_tendency",
    "bouguer_gravity_mgal",
    "magnetic_anomaly_nt",
)

# Benchmark grid specification from Williams et al. (2008) and Mordensky et al. (2023)
MORDENSKY_2023_GRID_CELLS_TOTAL: int = 725_442
MORDENSKY_2023_POSITIVE_CELLS: int = 278
MORDENSKY_2023_CELL_RESOLUTION_KM: float = 2.0
MORDENSKY_2023_CLASS_PREVALENCE: float = 278.0 / 725_442.0  # ~0.0003832


class USGSSandboxViolationError(RuntimeError):
    """Raised when sandbox isolation is violated or USGS results are misattributed to Thailand."""


def assert_usgs_sandbox_isolation(
    *,
    tag: str,
    target_region: str,
    output_claim: str | None = None,
) -> None:
    """Validate that the execution context strictly adheres to the USGS replication sandbox.

    Raises:
        USGSSandboxViolationError: If region is Thailand, tag is missing, or claim is misattributed.
    """
    if tag != USGS_REPLICATION_TAG:
        raise USGSSandboxViolationError(
            f"Sandbox isolation error: Tag must be exactly '{USGS_REPLICATION_TAG}', got '{tag}'."
        )

    normalized_region = target_region.strip().lower()
    if "thai" in normalized_region or "siam" in normalized_region:
        raise USGSSandboxViolationError(
            f"Sandbox isolation error: Cannot apply USGS replication model to region '{target_region}'. "
            "USGS benchmark data and models are strictly foreign replication baselines and must NEVER "
            "be claimed as Thai geothermal prospectivity."
        )

    if output_claim:
        normalized_claim = output_claim.lower()
        if "thai" in normalized_claim and ("prospect" in normalized_claim or "predict" in normalized_claim):
            raise USGSSandboxViolationError(
                f"Sandbox isolation error: Output claim '{output_claim}' attempts to misrepresent "
                "USGS benchmark results as Thai geothermal prospectivity."
            )


@dataclass(frozen=True)
class USGSBenchmarkDatasetMetadata:
    dataset_name: str
    doi: str
    profile_name: str
    spatial_extent: str
    feature_columns: tuple[str, ...]
    target_column: str
    row_count: int
    positive_count: int
    unlabeled_count: int
    data_source_tier: Literal[
        "ORIGINAL_USGS_DATA",
        "REPROCESSED_USGS_DATA",
        "REPLICATION_OUTPUT",
        "SYNTHETIC_TEST_DATA",
    ]
    tag: str = USGS_REPLICATION_TAG

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "doi": self.doi,
            "profile_name": self.profile_name,
            "spatial_extent": self.spatial_extent,
            "feature_columns": list(self.feature_columns),
            "target_column": self.target_column,
            "row_count": self.row_count,
            "positive_count": self.positive_count,
            "unlabeled_count": self.unlabeled_count,
            "data_source_tier": self.data_source_tier,
            "tag": self.tag,
        }


def compute_normal_score_transformation(raw_scores: np.ndarray) -> np.ndarray:
    """Transform raw model prediction scores to normal-score distribution.

    Mordensky et al. (2023) Section 2.4:
    A normal-score transformation is applied to model favorability outputs to map
    predictions into a standard normal distribution N(0, 1) based on empirical rank.
    This enables valid cross-algorithm relative favorability comparisons.

    CRITICAL SCIENTIFIC NOTE:
    Normal-score transformed values represent RELATIVE FAVORABILITY RANKING,
    NOT physical probability of geothermal occurrence.
    """
    scores_2d = np.asarray(raw_scores).reshape(-1, 1)
    transformer = QuantileTransformer(
        output_distribution="normal",
        n_quantiles=min(len(raw_scores), 1000),
        random_state=42,
    )
    return transformer.fit_transform(scores_2d).ravel()


@dataclass
class USGSReplicationExperiment:
    """Encapsulates a methodological replication run on USGS Western US benchmark data."""

    experiment_id: str
    algorithm: str
    feature_subset: list[str]
    hyperparameters: dict[str, Any]
    feature_profile: str = "MORDENSKY_2023_BASELINE_PROFILE"
    replication_outcome: ReplicationOutcome = "METHOD_ADAPTATION"
    train_test_split_ratio: float = 0.8
    unlabeled_subsample_ratio: float | None = None
    random_seed: int = 42
    tag: str = USGS_REPLICATION_TAG
    target_region: str = "Western_United_States"
    metrics: dict[str, float] = field(default_factory=dict)
    feature_importances: dict[str, float] = field(default_factory=dict)
    execution_notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        assert_usgs_sandbox_isolation(
            tag=self.tag,
            target_region=self.target_region,
        )
        if not self.experiment_id.startswith("USGS_REP_"):
            self.experiment_id = f"USGS_REP_{self.experiment_id}"

    def record_evaluation(
        self,
        *,
        pr_auc: float,
        roc_auc: float,
        brier_score: float,
        recall_at_top10_percent_area: float,
        feature_importances: dict[str, float] | None = None,
    ) -> None:
        """Record evaluation metrics for the replication experiment."""
        assert_usgs_sandbox_isolation(
            tag=self.tag,
            target_region=self.target_region,
        )
        self.metrics = {
            "pr_auc": float(pr_auc),
            "roc_auc": float(roc_auc),
            "brier_score": float(brier_score),
            "recall_at_top10_percent_area": float(recall_at_top10_percent_area),
        }
        if feature_importances:
            self.feature_importances = {k: float(v) for k, v in feature_importances.items()}

    def record_metrics(
        self,
        *,
        pr_auc: float,
        roc_auc: float,
        brier_score: float,
        recall_at_top10_percent_area: float,
        feature_importances: dict[str, float] | None = None,
    ) -> None:
        """Backward compatibility alias for record_evaluation."""
        self.record_evaluation(
            pr_auc=pr_auc,
            roc_auc=roc_auc,
            brier_score=brier_score,
            recall_at_top10_percent_area=recall_at_top10_percent_area,
            feature_importances=feature_importances,
        )

    def export_summary(self) -> dict[str, Any]:
        """Export experiment summary with mandatory replication disclaimers."""
        assert_usgs_sandbox_isolation(
            tag=self.tag,
            target_region=self.target_region,
        )
        return {
            "experiment_id": self.experiment_id,
            "replication_tag": self.tag,
            "replication_outcome": self.replication_outcome,
            "methodological_reference": f"Mordensky et al. (2023), DOI: {MORDENSKY_2023_DOI}",
            "benchmark_dataset_doi": USGS_2023_DATA_DOI,
            "feature_profile": self.feature_profile,
            "target_region": self.target_region,
            "algorithm": self.algorithm,
            "features_used": self.feature_subset,
            "train_test_split_ratio": self.train_test_split_ratio,
            "hyperparameters": self.hyperparameters,
            "metrics": self.metrics,
            "feature_importances": self.feature_importances,
            "notes": self.execution_notes,
            "disclaimer": (
                "STRICTLY FOR USGS METHODOLOGY REPLICATION IN WESTERN US / GREAT BASIN. "
                "THIS RESULT DOES NOT REPRESENT GEOTHERMAL PROSPECTIVITY IN THAILAND. "
                "DO NOT USE FOR THAI RESOURCE DECISIONS."
            ),
        }


class USGSSandboxPipeline:
    """Executes the Mordensky 2023 replication pipeline under strict PU assumptions."""

    def __init__(self, random_seed: int = 42) -> None:
        self.random_seed = random_seed

    def run_mordensky_replication(
        self,
        df: pd.DataFrame,
        algorithm: Literal["logistic_regression", "xgboost"] = "logistic_regression",
        subsample_unlabeled_ratio: float = 10.0,
        outcome_class: ReplicationOutcome = "SYNTHETIC_SOFTWARE_TEST",
    ) -> tuple[USGSReplicationExperiment, np.ndarray, np.ndarray]:
        """Execute replication experiment strictly on benchmark dataset."""
        features = list(MORDENSKY_2023_FEATURES)
        target_col = "is_hydrothermal_system" if "is_hydrothermal_system" in df.columns else "target"

        X = df[features].copy()
        y = df[target_col].to_numpy()

        # Split 80/20 train/test stratified
        X_train_raw, X_test_raw, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=self.random_seed, stratify=y
        )

        # Handle class imbalance via background subsampling on train fold
        pos_train_idx = np.where(y_train == 1)[0]
        unl_train_idx = np.where(y_train == 0)[0]
        n_unl_sampled = int(len(pos_train_idx) * subsample_unlabeled_ratio)

        rng = np.random.default_rng(self.random_seed)
        sampled_unl_idx = rng.choice(unl_train_idx, size=min(n_unl_sampled, len(unl_train_idx)), replace=False)
        train_idx = np.concatenate([pos_train_idx, sampled_unl_idx])
        rng.shuffle(train_idx)

        X_train_sub = X_train_raw.iloc[train_idx]
        y_train_sub = y_train[train_idx]

        # Standardize features ONLY using train fold parameters (leakage prevention)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train_sub)
        X_test_scaled = scaler.transform(X_test_raw)

        # Fit model
        if algorithm == "logistic_regression":
            model = LogisticRegression(C=1.0, max_iter=1000, random_state=self.random_seed)
            model.fit(X_train_scaled, y_train_sub)
            raw_test_preds = model.predict_proba(X_test_scaled)[:, 1]
            importances = dict(zip(features, np.abs(model.coef_[0])))
        elif algorithm == "xgboost":
            try:
                import xgboost as xgb
                model = xgb.XGBClassifier(
                    n_estimators=100,
                    max_depth=4,
                    learning_rate=0.05,
                    random_state=self.random_seed,
                    eval_metric="logloss",
                )
                model.fit(X_train_scaled, y_train_sub)
                raw_test_preds = model.predict_proba(X_test_scaled)[:, 1]
                importances = dict(zip(features, model.feature_importances_))
            except ImportError:
                # Fallback to Random Forest if xgboost not installed
                from sklearn.ensemble import RandomForestClassifier
                model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=self.random_seed)
                model.fit(X_train_scaled, y_train_sub)
                raw_test_preds = model.predict_proba(X_test_scaled)[:, 1]
                importances = dict(zip(features, model.feature_importances_))
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        # Normal-score transformation of outputs
        normal_scores = compute_normal_score_transformation(raw_test_preds)

        # Calculate metrics under PU conditions
        roc_auc = roc_auc_score(y_test, raw_test_preds)
        pr_auc = average_precision_score(y_test, raw_test_preds)
        brier = brier_score_loss(y_test, raw_test_preds)

        # Recall at top 10% highest predicted area/cells
        top_10pct_cutoff = np.percentile(raw_test_preds, 90.0)
        pos_test_count = int(np.sum(y_test == 1))
        pos_in_top10 = int(np.sum((y_test == 1) & (raw_test_preds >= top_10pct_cutoff)))
        recall_top10 = pos_in_top10 / max(pos_test_count, 1)

        exp = USGSReplicationExperiment(
            experiment_id=f"mordensky2023_{algorithm}_pu",
            algorithm=algorithm,
            feature_profile="MORDENSKY_2023_BASELINE_PROFILE",
            feature_subset=features,
            replication_outcome=outcome_class,
            hyperparameters={"unlabeled_subsample_ratio": subsample_unlabeled_ratio},
            train_test_split_ratio=0.8,
            random_seed=self.random_seed,
        )
        exp.record_evaluation(
            pr_auc=pr_auc,
            roc_auc=roc_auc,
            brier_score=brier,
            recall_at_top10_percent_area=recall_top10,
            feature_importances=importances,
        )

        return exp, raw_test_preds, normal_scores


class USGSSandboxManager:
    """Manages USGS benchmark dataset inspection, feature schema verification, and sandbox runs."""

    def __init__(self, sandbox_root: Path | None = None) -> None:
        self.sandbox_root = sandbox_root or Path("/tmp/geothermai_usgs_sandbox")
        self.registered_experiments: dict[str, USGSReplicationExperiment] = {}

    def verify_benchmark_schema(
        self,
        df: pd.DataFrame,
        profile: Literal["mordensky_2023", "pfa_deangelo"] = "mordensky_2023",
        data_source_tier: Literal[
            "ORIGINAL_USGS_DATA",
            "REPROCESSED_USGS_DATA",
            "REPLICATION_OUTPUT",
            "SYNTHETIC_TEST_DATA",
        ] = "SYNTHETIC_TEST_DATA",
    ) -> USGSBenchmarkDatasetMetadata:
        """Verify that a candidate replication dataset conforms to the selected USGS schema."""
        expected_features = (
            MORDENSKY_2023_FEATURES if profile == "mordensky_2023" else USGS_PFA_DEANGELO_FEATURES
        )
        missing = [f for f in expected_features if f not in df.columns]
        if missing:
            raise ValueError(
                f"Dataset missing required {profile} features: {missing}. Expected: {list(expected_features)}"
            )

        target_col = "is_hydrothermal_system" if "is_hydrothermal_system" in df.columns else "target"
        if target_col not in df.columns:
            raise ValueError(f"Dataset missing positive/unlabeled target column: {target_col}")

        # Check for geographic coordinate signs characteristic of Western US (Long ~-125° to -102°W, Lat ~31° to 49°N)
        if "longitude" in df.columns and "latitude" in df.columns:
            lons = df["longitude"].dropna()
            lats = df["latitude"].dropna()
            if (lons > 0).any() and (lats < 30).any():
                # Potential tropical Eastern hemisphere coordinates (like Thailand) passed into USGS sandbox!
                raise USGSSandboxViolationError(
                    "Detected positive longitudes and low latitudes: Thai or non-US data detected. "
                    "USGS replication sandbox only accepts Western US / Great Basin benchmark data."
                )

        pos_count = int((df[target_col] == 1).sum())
        unl_count = int((df[target_col] == 0).sum())

        return USGSBenchmarkDatasetMetadata(
            dataset_name=(
                "USGS_WesternUS_Mordensky2023_Benchmark"
                if profile == "mordensky_2023"
                else "USGS_GreatBasin_PFA_DeAngelo_Profile"
            ),
            doi=USGS_2023_DATA_DOI,
            profile_name=(
                "MORDENSKY_2023_BASELINE_PROFILE"
                if profile == "mordensky_2023"
                else "USGS_PFA_DEANGELO_PROFILE"
            ),
            spatial_extent="Western United States (approx. -125°W to -102°W, 31°N to 49°N)",
            feature_columns=expected_features,
            target_column=target_col,
            row_count=len(df),
            positive_count=pos_count,
            unlabeled_count=unl_count,
            data_source_tier=data_source_tier,
        )

    def register_experiment(self, experiment: USGSReplicationExperiment) -> None:
        assert_usgs_sandbox_isolation(
            tag=experiment.tag,
            target_region=experiment.target_region,
        )
        self.registered_experiments[experiment.experiment_id] = experiment

    def create_mock_benchmark_dataframe(
        self,
        n_samples: int = 1000,
        profile: Literal["mordensky_2023", "pfa_deangelo"] = "mordensky_2023",
        random_seed: int = 42,
    ) -> pd.DataFrame:
        """Generate synthetic benchmark dataframe conforming strictly to Western US coordinates and distributions.

        Clearly labeled SYNTHETIC_TEST_DATA for unit tests and local pipeline verification.
        """
        rng = np.random.default_rng(random_seed)
        lats = rng.uniform(34.0, 45.0, size=n_samples)
        lons = rng.uniform(-122.0, -112.0, size=n_samples)

        # Sparse positive binary labels mimicking Mordensky 2023 class ratio (~0.05 in sub-sample, ~0.00038 in full grid)
        target = rng.choice([0, 1], size=n_samples, p=[0.95, 0.05])

        if profile == "mordensky_2023":
            heat_flow = rng.normal(85.0, 25.0, size=n_samples)  # mW/m2
            dist_fault = rng.exponential(8.0, size=n_samples)  # km
            dist_magma = rng.exponential(25.0, size=n_samples)  # km
            seismic_dens = rng.exponential(0.15, size=n_samples)  # events/km2
            shmax = rng.normal(45.0, 15.0, size=n_samples)  # MPa

            return pd.DataFrame({
                "latitude": lats,
                "longitude": lons,
                "heat_flow_mw_m2": heat_flow,
                "dist_quaternary_fault_km": dist_fault,
                "dist_quaternary_magma_km": dist_magma,
                "seismic_event_density_per_km2": seismic_dens,
                "max_horizontal_stress_mpa": shmax,
                "is_hydrothermal_system": target,
            })
        else:
            temp_3km = rng.normal(160.0, 30.0, size=n_samples)
            fault_dens = rng.exponential(0.5, size=n_samples)
            slip_dil = rng.uniform(0.1, 0.9, size=n_samples)
            bouguer = rng.normal(-150.0, 25.0, size=n_samples)
            mag_anom = rng.normal(50.0, 100.0, size=n_samples)

            return pd.DataFrame({
                "latitude": lats,
                "longitude": lons,
                "temp_3km_c": temp_3km,
                "fault_density_km_km2": fault_dens,
                "slip_dilation_tendency": slip_dil,
                "bouguer_gravity_mgal": bouguer,
                "magnetic_anomaly_nt": mag_anom,
                "is_hydrothermal_system": target,
            })
