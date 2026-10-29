import numpy as np
import pandas as pd
import pytest

from geothermai.experiment_config import get_default_northern_thailand_experiment_config
from geothermai.ml_gate import MLGateBlockedError
from geothermai.prediction_architecture import (
    BufferedGroupSpatialCrossValidator,
    ModelABaselinePFA,
    ModelBStatisticalML,
    ModelCTreeEnsemble,
    PredictionPipeline,
    TrainFoldOneHotEncoder,
    TrainFoldScaler,
    assert_no_label_leakage,
    calculate_precision_recall_at_k,
    compute_uncertainty_surface,
    validate_positive_labels,
)


def test_pipeline_refuses_to_initialize_under_no_go_gate():
    config = get_default_northern_thailand_experiment_config()
    with pytest.raises(MLGateBlockedError) as exc_info:
        PredictionPipeline(config, bypass_gate_for_testing=False)
    assert "Predictive ML gate is NO-GO" in str(exc_info.value)


def test_assert_no_label_leakage_blocks_target_distance():
    clean_features = ["rock_unit_symbol", "elevation_m", "distance_mapped_fault_m"]
    assert_no_label_leakage(clean_features)  # should not raise

    leaky_features = ["rock_unit_symbol", "distance_known_manifestation_m", "elevation_m"]
    with pytest.raises(ValueError, match="CRITICAL LABEL LEAKAGE"):
        assert_no_label_leakage(leaky_features)


def test_positive_label_validation_filters_withheld_and_inconsistent():
    data = pd.DataFrame([
        {"record_uid": "NR_01", "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT", "site_group_id": "G1"},
        {"record_uid": "NR_02", "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT", "site_group_id": "G1"},
        {"record_uid": "CR_02", "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT", "site_group_id": "G2"},  # Withheld
        {"record_uid": "CM_16", "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT", "site_group_id": "G3"},  # Withheld
        {"record_uid": "ST_01", "coordinate_validation_status": "CRS_INFERRED_NO_DMS_COMPARATOR", "site_group_id": "G4"},  # Provisional
    ])
    result = validate_positive_labels(data)
    assert result.total_count == 5
    assert result.withheld_count == 2
    assert result.consistent_count == 2
    assert len(result.frame) == 2
    assert "CR_02" not in result.frame["record_uid"].values
    assert "CM_16" not in result.frame["record_uid"].values


def test_buffered_group_spatial_cv_enforces_group_and_buffer_isolation():
    # 6 points across 3 groups with known coordinates in UTM (meters)
    # G1 at (0, 0) and (1000, 1000)
    # G2 at (5000, 5000) (within 20km buffer of G1)
    # G3 at (50000, 50000) (outside 20km buffer)
    coords = np.array([
        [0.0, 0.0],
        [1000.0, 1000.0],
        [5000.0, 5000.0],
        [5100.0, 5100.0],
        [50000.0, 50000.0],
        [50100.0, 50100.0],
    ])
    groups = np.array(["G1", "G1", "G2", "G2", "G3", "G3"])
    X = pd.DataFrame({"f1": [1, 2, 3, 4, 5, 6]})
    y = np.array([1, 1, 0, 0, 1, 0])

    cv = BufferedGroupSpatialCrossValidator(n_splits=3, buffer_distance_m=20000.0, random_state=42)
    splits = cv.split(X, y, groups, coords)

    for split in splits:
        # Group isolation
        train_grp_set = set(split.train_groups)
        test_grp_set = set(split.test_groups)
        assert train_grp_set.isdisjoint(test_grp_set)

        # Buffer isolation: check distance between test coords and train coords
        if len(split.train_indices) > 0 and len(split.test_indices) > 0:
            train_c = coords[split.train_indices]
            test_c = coords[split.test_indices]
            dists = np.sqrt(((train_c[:, None, :] - test_c[None, :, :]) ** 2).sum(axis=-1))
            assert np.all(dists >= 20000.0)


def test_train_fold_scaler_prevents_leakage():
    scaler = TrainFoldScaler()
    with pytest.raises(ValueError, match="Scaler is not fitted yet"):
        scaler.transform(np.array([[1.0, 2.0]]))

    X_train = np.array([[10.0, 100.0], [20.0, 200.0], [30.0, 300.0]])
    X_test = np.array([[15.0, 150.0]])

    scaled_train = scaler.fit_transform(X_train)
    assert np.allclose(np.mean(scaled_train, axis=0), [0.0, 0.0])

    # Transform test set using TRAIN statistics
    scaled_test = scaler.transform(X_test)
    assert np.allclose(scaled_test, [[-0.61237244, -0.61237244]])


def test_train_fold_one_hot_encoder_handles_unseen():
    encoder = TrainFoldOneHotEncoder()
    train_cats = ["Granite", "Basalt", "Limestone"]
    encoder.fit(train_cats)

    encoded = encoder.transform(["Granite", "Unknown_Rock", "Basalt"])
    # 3 known categories + 1 unknown column = 4 columns
    assert encoded.shape == (3, 4)
    # "Granite" is at index 1 (sorted: Basalt=0, Granite=1, Limestone=2, Unknown=3)
    assert encoded[0, 1] == 1.0
    # "Unknown_Rock" goes to the last unknown column (index 3)
    assert encoded[1, 3] == 1.0


def test_model_comparators_produce_valid_bounds():
    X = np.array([[0.2, 0.8], [0.5, 0.5], [0.9, 0.1]])
    y = np.array([1, 0, 1])

    model_a = ModelABaselinePFA()
    model_a.fit(X, y)
    preds_a = model_a.predict_favorability(X)
    assert np.all((preds_a >= 0.0) & (preds_a <= 1.0))

    model_b = ModelBStatisticalML(C=0.1)
    model_b.fit(X, y)
    preds_b = model_b.predict_favorability(X)
    assert np.all((preds_b >= 0.0) & (preds_b <= 1.0))

    model_c = ModelCTreeEnsemble()
    model_c.fit(X, y)
    preds_c = model_c.predict_favorability(X)
    assert np.all((preds_c >= 0.0) & (preds_c <= 1.0))


def test_precision_recall_at_k():
    scores = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0])
    y_true = np.array([1,   1,   0,   0,   0,   0,   0,   0,   0,   0])
    # Top 20% (k=2) captures both positives
    metrics = calculate_precision_recall_at_k(scores, y_true, k_ratio=0.2)
    assert metrics["precision_at_20pct"] == 1.0
    assert metrics["recall_at_20pct"] == 1.0
    assert metrics["positives_captured"] == 2


def test_uncertainty_surface_suppresses_low_coverage():
    preds = np.array([0.9, 0.8, 0.7])
    coverage = np.array([1.0, 0.5, 0.1])  # 0.1 is below 0.3 threshold
    surface = compute_uncertainty_surface(preds, coverage, threshold=0.3)
    assert surface.suppressed_prediction[0] == 0.9  # unchanged (full coverage)
    assert surface.suppressed_prediction[2] < 0.7   # discounted due to low coverage


def test_end_to_end_pipeline_simulation():
    config = get_default_northern_thailand_experiment_config()
    pipeline = PredictionPipeline(config, bypass_gate_for_testing=True)

    # 12 synthetic instances across 4 groups
    np.random.seed(42)
    coords = np.random.uniform(0, 100000, size=(12, 2))
    groups = np.array(["G1", "G1", "G1", "G2", "G2", "G2", "G3", "G3", "G3", "G4", "G4", "G4"])
    X = pd.DataFrame({
        "rock_score": np.random.uniform(0, 1, 12),
        "fault_proximity": np.random.uniform(0, 1, 12),
        "elevation": np.random.uniform(200, 1500, 12),
    })
    y = np.array([1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])

    results = pipeline.fit_and_evaluate(X, y, groups, coords)
    assert results["experiment_id"] == "EXP_PILOT_NORTH_2026E"
    assert len(results["folds"]) == 4
    for fold in results["folds"]:
        assert "Model_A_Baseline" in fold["model_metrics"]
        assert "Model_B_LogisticRegression" in fold["model_metrics"]
        assert "Model_C_TreeEnsemble" in fold["model_metrics"]
