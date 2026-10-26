import pandas as pd

from geothermai.data_validation import REQUIRED_OBSERVATION_COLUMNS, validate_observations


def valid_row() -> dict[str, object]:
    row = {column: "available" for column in REQUIRED_OBSERVATION_COLUMNS}
    row.update(
        {
            "record_uid": "OBS_001",
            "derived_longitude_wgs84": "99.1",
            "derived_latitude_wgs84": "18.2",
            "surface_temperature_c": "42",
        }
    )
    return row


def test_valid_observation_schema_has_no_schema_errors():
    result = validate_observations(pd.DataFrame([valid_row()]))
    assert result.is_schema_valid
    assert result.duplicate_record_ids == ()
    assert result.invalid_coordinate_ids == ()


def test_missing_required_columns_are_reported():
    result = validate_observations(pd.DataFrame([{"record_uid": "OBS_001"}]))
    assert "source_id" in result.missing_columns


def test_duplicate_identifiers_are_reported():
    row = valid_row()
    result = validate_observations(pd.DataFrame([row, row.copy()]))
    assert result.duplicate_record_ids == ("OBS_001",)


def test_malformed_or_out_of_range_coordinates_are_reported():
    malformed = valid_row()
    malformed["record_uid"] = "BAD_TEXT"
    malformed["derived_longitude_wgs84"] = "not-a-number"
    out_of_range = valid_row()
    out_of_range["record_uid"] = "BAD_RANGE"
    out_of_range["derived_latitude_wgs84"] = "100"
    result = validate_observations(pd.DataFrame([malformed, out_of_range]))
    assert set(result.invalid_coordinate_ids) == {"BAD_TEXT", "BAD_RANGE"}


def test_missing_crs_and_temperature_are_reported():
    row = valid_row()
    row["working_coordinate_reference"] = ""
    row["surface_temperature_c"] = ""
    result = validate_observations(pd.DataFrame([row]))
    assert result.missing_crs_ids == ("OBS_001",)
    assert result.missing_temperature_ids == ("OBS_001",)
