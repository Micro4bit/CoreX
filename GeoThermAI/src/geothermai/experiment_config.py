"""Experiment configuration schemas and preregistered protocols for GeoThermAI.

Ensures fully reproducible, leak-free, and audited predictive experiment definitions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class StudyAreaBounds:
    """Bounding box in EPSG:4326 (WGS84) and target projected CRS."""
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float
    projected_crs: str = "EPSG:32647"  # UTM Zone 47N for Northern Thailand

    def validate(self) -> None:
        if self.min_lon >= self.max_lon:
            raise ValueError(f"Invalid longitude range: {self.min_lon} >= {self.max_lon}")
        if self.min_lat >= self.max_lat:
            raise ValueError(f"Invalid latitude range: {self.min_lat} >= {self.max_lat}")


@dataclass(frozen=True)
class LabelPolicyConfig:
    """Policy for positive geothermal occurrence labels."""
    allowed_evidence_tiers: tuple[str, ...] = ("CRS_AND_DMS_CONSISTENT",)
    withheld_record_ids: tuple[str, ...] = ("CR_02", "CM_16")
    provisional_allowed: bool = False
    expert_grouping_required: bool = True
    provisional_group_column: str = "site_group_id"


@dataclass(frozen=True)
class BackgroundSamplingConfig:
    """Positive-Unlabeled (PU) / background sampling protocol."""
    method: str = "SPATIAL_RANDOM_BACKGROUND"
    background_to_positive_ratio: int = 50
    positive_exclusion_buffer_m: float = 5000.0
    evaluation_assumption: str = "POSITIVE_UNLABELED_EMPIRICAL_RISK"
    prohibit_treating_background_as_true_negatives: bool = True


@dataclass(frozen=True)
class SpatialValidationConfig:
    """Spatial and group holdout validation protocol."""
    method: str = "BUFFERED_GROUP_K_FOLD"
    n_splits: int = 4
    group_column: str = "site_group_id"
    buffer_distance_km: float = 20.0
    leakage_check_enabled: bool = True
    random_seed: int = 20261027


@dataclass(frozen=True)
class FeatureFamilyConfig:
    """Whitelisted feature families and transformation rules."""
    allowed_families: tuple[str, ...] = ("geology", "terrain", "structure")
    ablation_families: tuple[str, ...] = ("geology", "terrain", "structure")
    satellite_enabled: bool = False  # Disabled until usable rasters exist
    heat_flow_interpolation_enabled: bool = False  # Disabled until point density & depth are resolved
    prohibited_features: tuple[str, ...] = (
        "distance_known_manifestation_m",
        "manifestation_density",
        "nearest_label_id",
    )


@dataclass(frozen=True)
class ModelHyperparametersConfig:
    """Configurations for the minimal model comparison."""
    # Model A: Baseline
    model_a_type: str = "PFA_GEOLOGY_BASELINE"
    model_a_description: str = "Play Fairway Analysis expert-scored lithology & structural proximity baseline"

    # Model B: Regularized Logistic Regression
    model_b_type: str = "REGULARIZED_LOGISTIC_REGRESSION"
    model_b_penalty: str = "l2"
    model_b_c: float = 0.1
    model_b_max_iter: int = 1000

    # Model C: Shallow Tree Ensemble
    model_c_type: str = "RANDOM_FOREST"
    model_c_n_estimators: int = 50
    model_c_max_depth: int = 4
    model_c_min_samples_leaf: int = 5
    model_c_random_state: int = 20261027


@dataclass(frozen=True)
class EvaluationMetricConfig:
    """Ranking-oriented evaluation metrics."""
    primary_metric: str = "AVERAGE_PRECISION_PR_AUC"
    secondary_metrics: tuple[str, ...] = (
        "RECALL_AT_TOP_10_PCT_AREA",
        "RECALL_AT_TOP_20_PCT_AREA",
        "PRECISION_AT_K",
        "PU_EMPIRICAL_RISK",
        "SPATIAL_HOLD_OUT_RANK_STABILITY",
    )
    prohibited_metrics: tuple[str, ...] = (
        "NAIVE_CLASSIFICATION_ACCURACY",
        "NAIVE_BINARY_F1_ON_BACKGROUND",
        "FABRICATED_DRILLING_SUCCESS_RATE",
    )


@dataclass(frozen=True)
class ExperimentConfig:
    """Master experiment specification for GeoThermAI prospectivity modeling."""
    experiment_id: str
    study_area_name: str
    bounds: StudyAreaBounds
    label_policy: LabelPolicyConfig = field(default_factory=LabelPolicyConfig)
    background_sampling: BackgroundSamplingConfig = field(default_factory=BackgroundSamplingConfig)
    spatial_validation: SpatialValidationConfig = field(default_factory=SpatialValidationConfig)
    features: FeatureFamilyConfig = field(default_factory=FeatureFamilyConfig)
    models: ModelHyperparametersConfig = field(default_factory=ModelHyperparametersConfig)
    metrics: EvaluationMetricConfig = field(default_factory=EvaluationMetricConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExperimentConfig:
        bounds_data = data["bounds"]
        bounds = StudyAreaBounds(**bounds_data)
        return cls(
            experiment_id=data["experiment_id"],
            study_area_name=data["study_area_name"],
            bounds=bounds,
            label_policy=LabelPolicyConfig(**data.get("label_policy", {})),
            background_sampling=BackgroundSamplingConfig(**data.get("background_sampling", {})),
            spatial_validation=SpatialValidationConfig(**data.get("spatial_validation", {})),
            features=FeatureFamilyConfig(**data.get("features", {})),
            models=ModelHyperparametersConfig(**data.get("models", {})),
            metrics=EvaluationMetricConfig(**data.get("metrics", {})),
        )

    def validate(self) -> None:
        self.bounds.validate()
        # Verify prohibited features are not in allowed list
        for prohibited in self.features.prohibited_features:
            if prohibited in self.features.allowed_families:
                raise ValueError(f"Prohibited feature {prohibited} found in allowed features")
        if self.features.satellite_enabled:
            raise ValueError("Satellite features cannot be enabled without verified rasters")
        if self.features.heat_flow_interpolation_enabled:
            raise ValueError("Heat-flow interpolation cannot be enabled on sparse point observations")


def get_default_northern_thailand_experiment_config() -> ExperimentConfig:
    """Return preregistered baseline experiment config for Northern Thailand pilot."""
    return ExperimentConfig(
        experiment_id="EXP_PILOT_NORTH_2026E",
        study_area_name="Northern Thailand Candidate Pilot (Chiang Mai - Chiang Rai - Lampang)",
        bounds=StudyAreaBounds(
            min_lon=98.0,
            min_lat=17.0,
            max_lon=100.5,
            max_lat=20.5,
            projected_crs="EPSG:32647",
        ),
    )
