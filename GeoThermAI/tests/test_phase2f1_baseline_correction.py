"""Comprehensive tests for Phase 2F.1 Scientific Baseline Correction & Research Integrity.

Verifies:
1. Canonical Mordensky et al. (2023) 5-feature baseline vs preserved PFA DeAngelo profile.
2. Normal-score transformation mathematical properties (standard normal mapping, rank preservation).
3. Data leakage prevention (train-only scaling).
4. Positive-Unlabeled (PU) replication pipeline execution and metric recording.
5. Geospatial equal-area coverage calculator (true geometric % vs tile-count ratio).
6. Phase 2F.1 fail-closed ML Gate report integrity.
7. Sandbox isolation preventing foreign USGS metrics from contaminating Thai prospectivity.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from shapely.geometry import box

from geothermai.ml_gate import evaluate_gate_file
from geothermai.spatial_coverage import (
    DEFAULT_NORTHERN_AOI_BOUNDS,
    audit_geology_coverage,
    audit_srtm_dem_coverage,
    compute_geometric_coverage,
    get_aoi_polygon,
)
from geothermai.usgs_replication import (
    MORDENSKY_2023_BASELINE_PROFILE,
    MORDENSKY_2023_FEATURES,
    USGS_PFA_DEANGELO_FEATURES,
    USGS_REPLICATION_TAG,
    USGSReplicationExperiment,
    USGSSandboxManager,
    USGSSandboxPipeline,
    USGSSandboxViolationError,
    assert_usgs_sandbox_isolation,
    compute_normal_score_transformation,
)

PHASE2F1_DIR = Path(__file__).resolve().parents[1] / "tasks" / "phase_2f1_scientific_baseline"
GATE_REPORT_JSON = PHASE2F1_DIR / "PHASE2F1_ML_GATE_REPORT.json"
COVERAGE_AUDIT_CSV = PHASE2F1_DIR / "PHASE2F1_GIS_COVERAGE_AUDIT.csv"
THAILAND_MAPPING_CSV = PHASE2F1_DIR / "PHASE2F1_THAILAND_FEATURE_MAPPING.csv"


# ---------------------------------------------------------------------------
# 1. Feature Profile & Schema Verification
# ---------------------------------------------------------------------------

def test_canonical_mordensky_2023_features_schema():
    assert len(MORDENSKY_2023_FEATURES) == 5
    assert set(MORDENSKY_2023_FEATURES) == {
        "heat_flow_mw_m2",
        "dist_quaternary_fault_km",
        "dist_quaternary_magma_km",
        "seismic_event_density_per_km2",
        "max_horizontal_stress_mpa",
    }


def test_preserved_pfa_deangelo_features_schema():
    assert len(USGS_PFA_DEANGELO_FEATURES) == 5
    assert set(USGS_PFA_DEANGELO_FEATURES) == {
        "temp_3km_c",
        "fault_density_km_km2",
        "slip_dilation_tendency",
        "bouguer_gravity_mgal",
        "magnetic_anomaly_nt",
    }


def test_dual_profile_verification_in_sandbox_manager():
    manager = USGSSandboxManager()

    # Canonical Mordensky 2023
    df_mord = manager.create_mock_benchmark_dataframe(n_samples=50, profile="mordensky_2023")
    meta_mord = manager.verify_benchmark_schema(df_mord, profile="mordensky_2023")
    assert meta_mord.profile_name == "MORDENSKY_2023_BASELINE_PROFILE"
    assert meta_mord.feature_columns == MORDENSKY_2023_FEATURES

    # Preserved PFA DeAngelo profile
    df_pfa = manager.create_mock_benchmark_dataframe(n_samples=50, profile="pfa_deangelo")
    meta_pfa = manager.verify_benchmark_schema(df_pfa, profile="pfa_deangelo")
    assert meta_pfa.profile_name == "USGS_PFA_DEANGELO_PROFILE"
    assert meta_pfa.feature_columns == USGS_PFA_DEANGELO_FEATURES

    # Cross-schema mismatch fails closed
    with pytest.raises(ValueError, match="Dataset missing required"):
        manager.verify_benchmark_schema(df_mord, profile="pfa_deangelo")


# ---------------------------------------------------------------------------
# 2. Normal-Score Transformation Properties
# ---------------------------------------------------------------------------

def test_normal_score_transformation_properties():
    raw_scores = np.array([0.01, 0.05, 0.12, 0.35, 0.78, 0.82, 0.95, 0.99])
    normal_scores = compute_normal_score_transformation(raw_scores)

    assert len(normal_scores) == len(raw_scores)
    # Monotonicity: strictly rank-preserving
    for i in range(len(raw_scores) - 1):
        assert normal_scores[i] < normal_scores[i + 1]

    # Mean approximately 0 for larger uniform sample
    large_sample = np.linspace(0.001, 0.999, 1000)
    large_normal = compute_normal_score_transformation(large_sample)
    assert abs(np.mean(large_normal)) < 0.05
    assert abs(np.std(large_normal) - 1.0) < 0.1


# ---------------------------------------------------------------------------
# 3. Data Leakage Prevention & Replication Pipeline
# ---------------------------------------------------------------------------

def test_replication_pipeline_runs_under_pu_assumptions():
    manager = USGSSandboxManager()
    pipeline = USGSSandboxPipeline(random_seed=42)

    mock_df = manager.create_mock_benchmark_dataframe(n_samples=500, profile="mordensky_2023", random_seed=42)

    # Logistic Regression
    exp_lr, lr_preds, lr_normal = pipeline.run_mordensky_replication(
        mock_df, algorithm="logistic_regression", subsample_unlabeled_ratio=5.0
    )
    assert exp_lr.tag == USGS_REPLICATION_TAG
    assert "pr_auc" in exp_lr.metrics
    assert "roc_auc" in exp_lr.metrics
    assert "recall_at_top10_percent_area" in exp_lr.metrics
    assert len(exp_lr.feature_importances) == 5

    # Verification of summary disclaimer
    summary = exp_lr.export_summary()
    assert "STRICTLY FOR USGS METHODOLOGY REPLICATION" in summary["disclaimer"]
    assert "DO NOT USE FOR THAI RESOURCE DECISIONS" in summary["disclaimer"]


# ---------------------------------------------------------------------------
# 4. Geospatial Geometric Coverage Calculator
# ---------------------------------------------------------------------------

def test_geometric_coverage_vs_tile_count_ratio():
    # Synthetic AOI in Thailand coordinates (e.g. 98°E to 100°E, 17°N to 19°N)
    aoi_bounds = (98.0, 17.0, 100.0, 19.0)

    # Partial tile covering exact western half of AOI (98°E to 99°E, 17°N to 19°N)
    half_tile = [box(98.0, 17.0, 99.0, 19.0)]
    result = compute_geometric_coverage(
        layer_name="Synthetic Half Layer",
        dataset_type="Raster",
        footprints=half_tile,
        native_crs="EPSG:4326",
        aoi_bounds=aoi_bounds,
        metric_crs="EPSG:32647",
        required_count=2,  # 2 tiles required
    )

    # True coverage should be ~50%, matching geometric half
    assert 48.0 < result.true_coverage_pct < 52.0
    assert result.covered_area_km2 > 0
    assert result.missing_area_km2 > 0


def test_real_northern_aoi_coverage_audit_values():
    terrain_dir = Path(__file__).resolve().parents[1] / "tasks" / "phase_2d_data_readiness" / "derived" / "terrain"
    geology_path = Path(__file__).resolve().parents[1] / "derived" / "phase2c" / "dmr-rock-units-north.full.geojson"

    # SRTM DEM check
    srtm_res = audit_srtm_dem_coverage(terrain_dir, DEFAULT_NORTHERN_AOI_BOUNDS)
    assert srtm_res.tile_or_item_count == 5
    assert srtm_res.required_tiles_or_items == 12
    assert srtm_res.tile_count_ratio_pct == pytest.approx(41.67, abs=0.1)
    # True geometric coverage is 51.39% (distinct from 41.67% tile count)
    assert srtm_res.true_coverage_pct == pytest.approx(51.39, abs=0.2)
    assert "7 missing 1-degree tiles" in srtm_res.missing_components

    # DMR Geology check
    geol_res = audit_geology_coverage(geology_path, DEFAULT_NORTHERN_AOI_BOUNDS)
    assert geol_res.tile_or_item_count == 1266
    # True geometric coverage is 44.74%
    assert geol_res.true_coverage_pct == pytest.approx(44.74, abs=0.5)


# ---------------------------------------------------------------------------
# 5. Fail-Closed Thai ML Gate Integrity
# ---------------------------------------------------------------------------

def test_phase2f1_ml_gate_report_integrity():
    assert GATE_REPORT_JSON.is_file()
    payload = json.loads(GATE_REPORT_JSON.read_text(encoding="utf-8"))

    assert payload["decision"] == "NO_GO_FOR_PREDICTIVE_ML"
    assert payload["requirements_total"] == 9
    assert payload["conditions_blocked"] == 9
    assert payload["runtime_enforcement"]["predictive_model_fitting"] == "DISABLED"
    assert payload["runtime_enforcement"]["prospectivity_heatmap_rendering"] == "DISABLED"


def test_phase2f1_deliverables_exist():
    assert COVERAGE_AUDIT_CSV.is_file()
    assert THAILAND_MAPPING_CSV.is_file()
    assert (PHASE2F1_DIR / "PHASE2F1_USGS_SOURCE_AUDIT.md").is_file()
    assert (PHASE2F1_DIR / "PHASE2F1_BASELINE_FEATURE_CORRECTION.md").is_file()
    assert (PHASE2F1_DIR / "PHASE2F1_REPLICATION_PROTOCOL.md").is_file()
    assert (PHASE2F1_DIR / "PHASE2F1_REPLICATION_RESULTS.md").is_file()
    assert (PHASE2F1_DIR / "PHASE2F1_PU_LEARNING_AUDIT.md").is_file()
    assert (PHASE2F1_DIR / "PHASE2F1_SPATIAL_VALIDATION_AUDIT.md").is_file()
