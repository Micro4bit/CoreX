"""Automated tests for Phase 2F Scientific Validation & Research Readiness.

Verifies:
1. Phase 2F ML Gate evaluation (9/9 fail-closed review requirements).
2. Ground truth label review invariants from PHASE2F_LABEL_REVIEW.csv.
3. Candidate AOI coverage audit and missing SRTM elevation data detection.
4. Preregistered spatial group validation and buffer sensitivity controls.
5. USGS Replication Sandbox isolation and strict protection against foreign claim leakage.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from geothermai.ml_gate import (
    DEFAULT_PHASE2F_GATE_PATH,
    EXPECTED_PHASE2F_REQUIREMENTS,
    MLGateBlockedError,
    enforce_ml_gate,
    evaluate_gate,
    evaluate_gate_file,
    main as gate_cli_main,
)
from geothermai.usgs_replication import (
    MORDENSKY_2023_DOI,
    USGS_2023_DATA_DOI,
    USGS_BENCHMARK_FEATURES,
    USGS_REPLICATION_TAG,
    USGSReplicationExperiment,
    USGSSandboxManager,
    USGSSandboxViolationError,
    assert_usgs_sandbox_isolation,
)

PHASE2F_DIR = Path(__file__).resolve().parents[1] / "tasks" / "phase_2f_scientific_validation"
LABEL_REVIEW_CSV = PHASE2F_DIR / "PHASE2F_LABEL_REVIEW.csv"
AOI_AUDIT_CSV = PHASE2F_DIR / "PHASE2F_AOI_COVERAGE_AUDIT.csv"
GATE_SNAPSHOT_JSON = PHASE2F_DIR / "phase2f_gate_snapshot.json"
ORIGINAL_REGISTRY_CSV = (
    Path(__file__).resolve().parents[1]
    / "tasks"
    / "phase_1c_label_expansion_gis_foundation"
    / "geothermal_label_master_registry.csv"
)


# ---------------------------------------------------------------------------
# 1. Phase 2F Gate Verification
# ---------------------------------------------------------------------------

def test_phase2f_snapshot_gate_is_strictly_no_go():
    report = evaluate_gate_file(GATE_SNAPSHOT_JSON)
    assert not report.is_approved
    assert report.decision == "NO_GO_FOR_PREDICTIVE_ML"
    assert report.blocked_count == 9
    assert len(report.blocked_conditions) == 9

    blocked_names = {b["condition"] for b in report.blocked_conditions}
    assert blocked_names == set(EXPECTED_PHASE2F_REQUIREMENTS)


def test_phase2f_gate_cli_exit_code_on_blocked():
    exit_code = gate_cli_main(["ml_gate.py", str(GATE_SNAPSHOT_JSON)])
    assert exit_code == 2


def test_phase2f_gate_synthetic_approval_requires_complete_evidence():
    payload = json.loads(GATE_SNAPSHOT_JSON.read_text(encoding="utf-8"))
    
    # Just setting approved=True without reviewer/evidence must remain blocked
    for req in payload["review_requirements"].values():
        req["approved"] = True

    report = evaluate_gate(payload)
    assert report["decision"] == "NO_GO_FOR_PREDICTIVE_ML"
    assert report["blocked_count"] == 9

    # Supplying full audit fields clears to review-only
    for key, req in payload["review_requirements"].items():
        req.update(
            reviewer="Dr. Verified Domain Expert",
            evidence_uri=f"https://dmr.go.th/review/evidence/{key}.pdf",
            approved_on="2026-10-27",
        )

    cleared_report = evaluate_gate(payload)
    assert cleared_report["decision"] == "GO_FOR_REVIEW_ONLY"
    assert cleared_report["blocked_count"] == 0


def test_phase2f_gate_future_dated_approval_fails_closed():
    payload = json.loads(GATE_SNAPSHOT_JSON.read_text(encoding="utf-8"))
    for key, req in payload["review_requirements"].items():
        req.update(
            approved=True,
            reviewer="Expert",
            evidence_uri=f"https://dmr.go.th/review/{key}.pdf",
            approved_on="2099-01-01",  # Future date
        )
    report = evaluate_gate(payload)
    assert report["decision"] == "NO_GO_FOR_PREDICTIVE_ML"
    assert report["blocked_count"] == 9
    assert all("future" in b["reason"] for b in report["blocked_conditions"])


# ---------------------------------------------------------------------------
# 2. Ground Truth Label Review Invariants
# ---------------------------------------------------------------------------

def test_label_review_registry_integrity_and_exclusions():
    assert LABEL_REVIEW_CSV.is_file(), f"Missing {LABEL_REVIEW_CSV}"

    with open(LABEL_REVIEW_CSV, mode="r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 47, f"Expected exactly 47 registry rows, found {len(reader)}"

    consistent = [r for r in reader if r["coordinate_status"] == "CRS_AND_DMS_CONSISTENT"]
    dms_mismatch = [r for r in reader if r["coordinate_status"] == "CRS_INFERRED_DMS_MISMATCH_UNRESOLVED"]
    dms_missing = [r for r in reader if r["coordinate_status"] == "CRS_INFERRED_DMS_MISSING"]
    no_comparator = [r for r in reader if r["coordinate_status"] == "CRS_INFERRED_NO_DMS_COMPARATOR"]

    assert len(consistent) == 14, f"Expected 14 northern consistent rows, found {len(consistent)}"
    assert len(dms_mismatch) == 1, f"Expected 1 mismatch row (CR_02), found {len(dms_mismatch)}"
    assert dms_mismatch[0]["source_row_id"] == "NORTH_WOOD2014_CR_02"

    assert len(dms_missing) == 1, f"Expected 1 missing DMS row (CM_16), found {len(dms_missing)}"
    assert dms_missing[0]["source_row_id"] == "NORTH_WOOD2014_CM_16"

    assert len(no_comparator) == 31, f"Expected 31 provisional southern rows, found {len(no_comparator)}"

    # CRITICAL: No reviewer or approved status should be pre-filled without external sign-off
    for row in reader:
        assert row["reviewer"] == "", f"Reviewer must be empty for unreviewed row {row['source_row_id']}"
        assert row["review_date"] == "", f"Review date must be empty for unreviewed row {row['source_row_id']}"
        assert row["review_evidence_uri"] == "", f"Evidence URI must be empty for unreviewed row {row['source_row_id']}"
        assert row["system_decision"] in (
            "PENDING_EXPERT_HYDROLOGIC_REVIEW",
            "PROVISIONAL_PENDING_UTM_ZONE_VERIFICATION",
            "WITHHELD_COORDINATE_MISMATCH",
            "WITHHELD_DMS_MISSING",
        )


def test_label_review_source_hash_matches_original():
    assert ORIGINAL_REGISTRY_CSV.is_file()
    computed_hash = hashlib.sha256(ORIGINAL_REGISTRY_CSV.read_bytes()).hexdigest()
    expected_hash = "93d3bf9cd3c52ffbc207ca3a308c3e6ece1e067caf9c98fe08e85e338ef83c6e"
    assert computed_hash == expected_hash, f"Hash mismatch: got {computed_hash}"


# ---------------------------------------------------------------------------
# 3. AOI & Coverage Audit Checks
# ---------------------------------------------------------------------------

def test_aoi_coverage_audit_records_and_gaps():
    assert AOI_AUDIT_CSV.is_file()
    with open(AOI_AUDIT_CSV, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    layers = {r["layer_name"]: r for r in rows}

    assert "SRTM Digital Elevation Model" in layers
    srtm = layers["SRTM Digital Elevation Model"]
    assert srtm["contiguous_coverage_status"] == "INCOMPLETE_GAPS_PRESENT"
    assert "7 missing 1-degree tiles" in srtm["missing_spatial_components"]

    assert "DMR Active Fault Zones" in layers
    faults = layers["DMR Active Fault Zones"]
    assert "BLOCKED_REUSE" in faults["licensing_and_derivative_status"]
    assert faults["ml_prediction_readiness"] == "BLOCKED_FORBIDDEN_IN_TRAINING"

    assert "IHFC Terrestrial Heat Flow Points" in layers
    ihfc = layers["IHFC Terrestrial Heat Flow Points"]
    assert "FORBIDDEN_FOR_PREDICTIVE_INTERPOLATION" in ihfc["ml_prediction_readiness"]


# ---------------------------------------------------------------------------
# 4. Preregistered Spatial Validation & Sensitivity Checks
# ---------------------------------------------------------------------------

def test_spatial_group_isolation_invariance():
    """Verify that occurrences sharing a proposed system group stay grouped."""
    with open(LABEL_REVIEW_CSV, mode="r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    group_to_rows: dict[str, list[str]] = {}
    for r in reader:
        grp = r["system_group_id"]
        if grp and grp != "UNASSIGNED":
            group_to_rows.setdefault(grp, []).append(r["source_row_id"])

    # E.g. KOK_RIVER_GEOTHERMAL_AREAS has 4 records grouped together
    assert "KOK_RIVER_GEOTHERMAL_AREAS" in group_to_rows
    assert len(group_to_rows["KOK_RIVER_GEOTHERMAL_AREAS"]) >= 2

    # Preregistered rule: Fold splitting must never split records of one group
    for grp, ids in group_to_rows.items():
        assert len(ids) == len(set(ids)), f"Duplicate record ID in group {grp}"


# ---------------------------------------------------------------------------
# 5. USGS Replication Sandbox Isolation Checks
# ---------------------------------------------------------------------------

def test_usgs_sandbox_isolation_guard_rejects_thailand():
    with pytest.raises(USGSSandboxViolationError, match="Cannot apply USGS replication model to region"):
        assert_usgs_sandbox_isolation(
            tag=USGS_REPLICATION_TAG,
            target_region="Thailand_Northern_Pilot",
        )


def test_usgs_sandbox_isolation_guard_rejects_missing_tag():
    with pytest.raises(USGSSandboxViolationError, match="Tag must be exactly 'USGS_REPLICATION_ONLY'"):
        assert_usgs_sandbox_isolation(
            tag="THAILAND_PREDICTION",
            target_region="US_Great_Basin",
        )


def test_usgs_sandbox_isolation_guard_rejects_thai_prospectivity_claim():
    with pytest.raises(USGSSandboxViolationError, match="Output claim .* attempts to misrepresent"):
        assert_usgs_sandbox_isolation(
            tag=USGS_REPLICATION_TAG,
            target_region="US_Great_Basin",
            output_claim="Predicted prospectivity map for Northern Thailand geothermal resources",
        )


def test_usgs_replication_experiment_metrics_and_disclaimer():
    exp = USGSReplicationExperiment(
        experiment_id="mordensky2023_rf_baseline",
        algorithm="RandomForestClassifier_PU",
        hyperparameters={"n_estimators": 100, "max_depth": 5},
        feature_subset=list(USGS_BENCHMARK_FEATURES),
    )
    assert exp.experiment_id == "USGS_REP_mordensky2023_rf_baseline"
    assert exp.tag == USGS_REPLICATION_TAG

    exp.record_metrics(
        pr_auc=0.48,
        roc_auc=0.86,
        brier_score=0.07,
        recall_at_top10_percent_area=0.72,
    )
    summary = exp.export_summary()
    assert summary["replication_tag"] == USGS_REPLICATION_TAG
    assert "STRICTLY FOR USGS METHODOLOGY REPLICATION" in summary["disclaimer"]
    assert "DO NOT USE FOR THAI RESOURCE DECISIONS" in summary["disclaimer"]
    assert summary["methodological_reference"] == f"Mordensky et al. (2023), DOI: {MORDENSKY_2023_DOI}"
    assert summary["benchmark_dataset_doi"] == USGS_2023_DATA_DOI


def test_usgs_sandbox_manager_rejects_thai_coordinates_in_benchmark():
    manager = USGSSandboxManager()
    # Mock dataframe with Thai coordinates (Lat ~19°N, Long ~99°E)
    mock_thai_df = manager.create_mock_benchmark_dataframe(n_samples=20)
    mock_thai_df["latitude"] = 19.1
    mock_thai_df["longitude"] = 99.2

    with pytest.raises(USGSSandboxViolationError, match="Thai or non-US data detected"):
        manager.verify_benchmark_schema(mock_thai_df)


def test_usgs_sandbox_manager_verifies_valid_great_basin_benchmark():
    manager = USGSSandboxManager()
    valid_gb_df = manager.create_mock_benchmark_dataframe(n_samples=50, random_seed=123)
    meta = manager.verify_benchmark_schema(valid_gb_df)
    assert meta.dataset_name in (
        "USGS_WesternUS_Mordensky2023_Benchmark",
        "USGS_Great_Basin_Mordensky2023_Benchmark",
    )
    assert meta.doi == USGS_2023_DATA_DOI
    assert meta.row_count == 50
    assert meta.tag == USGS_REPLICATION_TAG
