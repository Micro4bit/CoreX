import pandas as pd

from geothermai.evidence_engine import describe_evidence_availability
from geothermai.model_interface import predictive_model_status
from geothermai.provenance import evidence_summary_markdown


def test_evidence_output_has_no_numerical_potential_score():
    record = pd.Series(
        {
            "record_uid": "OBS_001",
            "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT",
            "source_id": "SOURCE",
            "source_region": "Northern Thailand",
            "reported_coordinate_reference": "WGS84 UTM",
            "working_coordinate_reference": "EPSG:32647",
            "coordinate_quality_note": "Checked",
            "license_or_reuse_status": "NOT_STATED",
            "source_url": "https://example.test/source",
        }
    )
    layers = pd.DataFrame(
        [
            {
                "layer_id": "GEOLOGY",
                "access_status": "VERIFIED_DOWNLOAD_OPENED",
                "license_or_permission_status": "NOT_VERIFIED",
            }
        ]
    )
    result = describe_evidence_availability(record, layers)
    report = evidence_summary_markdown(record, layers).lower()
    assert "score" in result.interpretation_notice.lower()
    assert "geothermal potential score" in report
    assert "0." not in report


def test_geometry_unavailable_layer_is_not_reported_as_usable_evidence_context():
    record = pd.Series(
        {"record_uid": "OBS_001", "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT"}
    )
    layers = pd.DataFrame(
        [
            {"layer_id": "ROCK", "access_status": "VERIFIED_DOWNLOAD_OPENED"},
            {"layer_id": "STRUCTURES", "access_status": "VERIFIED_ACCESS_GEOMETRY_UNAVAILABLE"},
        ]
    )
    result = describe_evidence_availability(record, layers)
    assert result.available_layer_ids == ("ROCK",)
    assert result.unavailable_or_restricted_layer_ids == ("STRUCTURES",)


def test_predictive_model_is_explicitly_disabled():
    model = predictive_model_status()
    assert not model.enabled
    assert model.status == "Predictive model not yet validated or enabled."
