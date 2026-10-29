"""Comprehensive verification tests for Phase 2F.2 Research Replication & Thailand Readiness.

Verifies:
1. Geodesic area calculation on WGS84 ellipsoid vs conformal UTM Zone 47N distortion.
2. Real GIS coverage audits for SRTM DEM, DMR 1:250k Geology, and combined intersection.
3. Multi-predictor combined overlap (33.80% coverage, 8,630 eligible 2km grid cells).
4. USGS Replication outcome taxonomy (5 levels) and strict sandbox isolation.
5. Canonical Mordensky et al. (2023) feature unit definitions and native search parameters.
6. Fail-closed ML Gate status (9/9 conditions blocked, NO_GO_FOR_PREDICTIVE_ML).
7. Phase 2F.2 governance deliverables existence and synchronization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import get_args

import geopandas as gpd
import pytest
from shapely.geometry import box

from geothermai.spatial_coverage import (
    DEFAULT_NORTHERN_AOI_BOUNDS,
    audit_geology_coverage,
    audit_srtm_dem_coverage,
    compute_combined_predictors_overlap,
    compute_geodesic_area_km2,
    compute_geometric_coverage,
    get_aoi_polygon,
)
from geothermai.usgs_replication import (
    MORDENSKY_2023_BASELINE_PROFILE,
    MORDENSKY_2023_FEATURES,
    USGS_PFA_DEANGELO_FEATURES,
    USGS_REPLICATION_TAG,
    ReplicationOutcome,
    USGSReplicationExperiment,
    USGSSandboxManager,
    USGSSandboxPipeline,
    USGSSandboxViolationError,
    assert_usgs_sandbox_isolation,
)

BASE_DIR = Path(__file__).resolve().parents[1]
PHASE2F2_DIR = BASE_DIR / "tasks" / "phase_2f2_replication_verification"
GATE_REPORT_JSON = PHASE2F2_DIR / "PHASE2F2_ML_GATE_REPORT.json"
WEB_REPORT_MD = BASE_DIR / "web" / "PHASE2F2_IMPLEMENTATION_REPORT.md"
TERRAIN_DIR = BASE_DIR / "tasks" / "phase_2d_data_readiness" / "derived" / "terrain"
GEOLOGY_PATH = BASE_DIR / "derived" / "phase2c" / "dmr-rock-units-north.full.geojson"


# ---------------------------------------------------------------------------
# 1. Geodesic Ellipsoidal Area vs Conformal Planar Distortion
# ---------------------------------------------------------------------------

def test_geodesic_vs_planar_area_calculation():
    """Verify that ellipsoidal geodesic calculation eliminates UTM 47N conformal distortion."""
    aoi_poly = get_aoi_polygon(DEFAULT_NORTHERN_AOI_BOUNDS)

    # 1. True Geodesic Ellipsoidal Area on WGS84
    geodesic_area_km2 = compute_geodesic_area_km2(aoi_poly)
    assert geodesic_area_km2 == pytest.approx(102125.39, abs=0.5)

    # 2. Planar UTM Zone 47N (EPSG:32647) Projected Area
    gdf = gpd.GeoDataFrame(geometry=[aoi_poly], crs="EPSG:4326").to_crs("EPSG:32647")
    planar_area_km2 = float(gdf.geometry.iloc[0].area / 1e6)
    assert planar_area_km2 == pytest.approx(102028.50, abs=0.5)

    # Conformal projection underestimates area by ~96.89 km² at this latitude (17°N - 20.5°N)
    diff_km2 = geodesic_area_km2 - planar_area_km2
    assert diff_km2 > 90.0
    assert diff_km2 == pytest.approx(96.89, abs=1.0)


# ---------------------------------------------------------------------------
# 2. Real GIS Coverage Audits
# ---------------------------------------------------------------------------

def test_real_srtm_dem_geodesic_coverage():
    """Verify SRTM DEM geodesic coverage: 51.37%, 52,466.80 km², 7 missing tiles."""
    result = audit_srtm_dem_coverage(TERRAIN_DIR, DEFAULT_NORTHERN_AOI_BOUNDS)
    assert result.tile_or_item_count == 5
    assert result.required_tiles_or_items == 12
    assert result.true_coverage_pct == pytest.approx(51.37, abs=0.1)
    assert result.covered_area_km2 == pytest.approx(52466.80, abs=1.0)
    assert result.missing_area_km2 == pytest.approx(49658.59, abs=1.0)
    assert result.calculation_method == "Geodesic_WGS84_Ellipsoid"
    assert "7 missing 1-degree tiles" in result.missing_components
    assert result.coverage_status == "PARTIAL_COVERAGE"


def test_real_geology_geodesic_coverage():
    """Verify DMR 1:250k Geology geodesic coverage: 44.73%, 45,675.59 km²."""
    result = audit_geology_coverage(GEOLOGY_PATH, DEFAULT_NORTHERN_AOI_BOUNDS)
    assert result.tile_or_item_count == 1266
    assert result.true_coverage_pct == pytest.approx(44.73, abs=0.1)
    assert result.covered_area_km2 == pytest.approx(45675.59, abs=1.0)
    assert result.missing_area_km2 == pytest.approx(56449.80, abs=1.0)
    assert result.calculation_method == "Geodesic_WGS84_Ellipsoid"
    assert result.coverage_status == "PARTIAL_COVERAGE"


def test_combined_predictors_overlap():
    """Verify combined overlap (SRTM DEM ∩ DMR Geology): 33.80%, 8,630 eligible cells."""
    srtm_res = audit_srtm_dem_coverage(TERRAIN_DIR, DEFAULT_NORTHERN_AOI_BOUNDS)
    geol_res = audit_geology_coverage(GEOLOGY_PATH, DEFAULT_NORTHERN_AOI_BOUNDS)

    comb_res = compute_combined_predictors_overlap(
        srtm_res.polygon,
        geol_res.polygon,
        DEFAULT_NORTHERN_AOI_BOUNDS,
    )

    assert comb_res.true_coverage_pct == pytest.approx(33.80, abs=0.1)
    assert comb_res.covered_area_km2 == pytest.approx(34523.06, abs=1.0)
    assert comb_res.missing_area_km2 == pytest.approx(67602.33, abs=1.0)
    assert comb_res.eligible_2km_grid_cells == 8630
    assert comb_res.coverage_status == "PARTIAL_COVERAGE"

    # Multi-predictor intersection is strictly smaller than either predictor individually
    assert comb_res.covered_area_km2 < srtm_res.covered_area_km2
    assert comb_res.covered_area_km2 < geol_res.covered_area_km2


# ---------------------------------------------------------------------------
# 3. USGS Replication Taxonomy & Pipeline Sandbox Isolation
# ---------------------------------------------------------------------------

def test_replication_outcome_taxonomy():
    """Verify the 5-tier ReplicationOutcome taxonomy."""
    outcomes = get_args(ReplicationOutcome)
    assert set(outcomes) == {
        "EXACT_REPLICATION",
        "PARTIAL_REPLICATION",
        "METHOD_ADAPTATION",
        "SYNTHETIC_SOFTWARE_TEST",
        "NOT_REPRODUCED",
    }


def test_usgs_replication_pipeline_synthetic_execution():
    """Verify synthetic replication execution assigns SYNTHETIC_SOFTWARE_TEST and tags output."""
    manager = USGSSandboxManager()
    df_mock = manager.create_mock_benchmark_dataframe(n_samples=100, profile="mordensky_2023")
    pipeline = USGSSandboxPipeline(random_seed=42)
    exp, raw_preds, norm_scores = pipeline.run_mordensky_replication(
        df=df_mock,
        algorithm="logistic_regression",
        outcome_class="SYNTHETIC_SOFTWARE_TEST",
    )
    summary = exp.export_summary()

    assert summary["replication_tag"] == USGS_REPLICATION_TAG
    assert summary["replication_outcome"] == "SYNTHETIC_SOFTWARE_TEST"
    assert summary["algorithm"] == "logistic_regression"
    assert "pr_auc" in summary["metrics"]
    assert "roc_auc" in summary["metrics"]
    assert "brier_score" in summary["metrics"]
    assert "recall_at_top10_percent_area" in summary["metrics"]


def test_usgs_isolation_guard_detects_contamination():
    """Verify that foreign USGS experiments cannot contaminate Thailand predictive systems."""
    # Valid call passes
    assert_usgs_sandbox_isolation(
        tag=USGS_REPLICATION_TAG,
        target_region="Western United States / Great Basin",
    )

    # Invalid tag fails closed
    with pytest.raises(USGSSandboxViolationError, match="Tag must be exactly"):
        assert_usgs_sandbox_isolation(
            tag="THAILAND_PREDICTION_ACTIVE",
            target_region="Western United States / Great Basin",
        )

    # Thai target region fails closed
    with pytest.raises(USGSSandboxViolationError, match="Cannot apply USGS replication model to region"):
        assert_usgs_sandbox_isolation(
            tag=USGS_REPLICATION_TAG,
            target_region="Northern Thailand",
        )

    # Output claim misattribution fails closed
    with pytest.raises(USGSSandboxViolationError, match="attempts to misrepresent"):
        assert_usgs_sandbox_isolation(
            tag=USGS_REPLICATION_TAG,
            target_region="Western United States",
            output_claim="This models Thai geothermal prospectivity",
        )


# ---------------------------------------------------------------------------
# 4. Feature Unit Audit & Search Parameter Definitions
# ---------------------------------------------------------------------------

def test_mordensky_2023_feature_units_and_definitions():
    """Verify canonical feature set and native search parameters from Mordensky (2023)."""
    assert len(MORDENSKY_2023_FEATURES) == 5

    # Check native feature catalog CSV in Phase 2F.2
    unit_audit_csv = PHASE2F2_DIR / "PHASE2F2_FEATURE_UNIT_AUDIT.csv"
    assert unit_audit_csv.is_file()
    content = unit_audit_csv.read_text(encoding="utf-8")

    # Invariants for seismic event density and max horizontal stress
    assert "seismic_event_density_per_km2" in content
    assert "M>=3 earthquakes within 4 km search radius" in content or "4 km radius" in content
    assert "max_horizontal_stress_direction_deg" in content
    assert "INCORRECTLY ASSUMED AS MPa" in content


# ---------------------------------------------------------------------------
# 5. Phase 2F.2 Governance Artifacts & Synchronization
# ---------------------------------------------------------------------------

def test_phase2f2_governance_artifacts_exist():
    """Verify all 11 required Phase 2F.2 governance deliverables exist."""
    required_files = [
        "PHASE2F2_RESEARCH_PIPELINE.md",
        "PHASE2F2_USGS_SOURCE_INVENTORY.md",
        "PHASE2F2_FEATURE_UNIT_AUDIT.csv",
        "PHASE2F2_REPLICATION_PROTOCOL.md",
        "PHASE2F2_REPLICATION_RESULTS.md",
        "PHASE2F2_THAILAND_FEATURE_MAPPING.csv",
        "PHASE2F2_GIS_COVERAGE_AUDIT.csv",
        "PHASE2F2_SPATIAL_VALIDATION_AUDIT.md",
        "PHASE2F2_ML_GATE_REPORT.json",
        "PHASE2F2_COMPETITION_PROPOSAL_TH.md",
        "PHASE2F2_IMPLEMENTATION_REPORT.md",
    ]
    for filename in required_files:
        p = PHASE2F2_DIR / filename
        assert p.is_file(), f"Missing Phase 2F.2 governance artifact: {filename}"


def test_web_implementation_report_synced():
    """Verify that web/PHASE2F2_IMPLEMENTATION_REPORT.md exists and is synchronized."""
    assert WEB_REPORT_MD.is_file()
    source_md = PHASE2F2_DIR / "PHASE2F2_IMPLEMENTATION_REPORT.md"
    assert WEB_REPORT_MD.read_text(encoding="utf-8") == source_md.read_text(encoding="utf-8")


def test_phase2f2_ml_gate_fail_closed():
    """Verify that Phase 2F.2 ML Gate remains fail-closed at NO_GO_FOR_PREDICTIVE_ML."""
    assert GATE_REPORT_JSON.is_file()
    data = json.loads(GATE_REPORT_JSON.read_text(encoding="utf-8"))

    assert data["decision"] == "NO_GO_FOR_PREDICTIVE_ML"
    assert data["requirements_total"] == 9
    assert data["conditions_blocked"] == 9
    assert data["runtime_enforcement"]["predictive_model_fitting"] == "DISABLED"
    assert data["runtime_enforcement"]["prospectivity_heatmap_rendering"] == "DISABLED"
    assert data["geodesic_coverage_summary"]["aoi_geodesic_area_km2"] == 102125.39
    assert data["geodesic_coverage_summary"]["srtm_dem_geodesic_coverage_pct"] == 51.37
    assert data["geodesic_coverage_summary"]["dmr_geology_geodesic_coverage_pct"] == 44.73
    assert data["geodesic_coverage_summary"]["combined_predictors_geodesic_coverage_pct"] == 33.80
    assert data["geodesic_coverage_summary"]["eligible_2km_grid_cells"] == 8630
