import pandas as pd

from geothermai.coordinate_utils import coordinate_category, displayable_observations


def test_provisional_coordinates_are_excluded_until_explicitly_enabled():
    observations = pd.DataFrame(
        [
            {
                "record_uid": "CONSISTENT",
                "derived_longitude_wgs84": 99.0,
                "derived_latitude_wgs84": 19.0,
                "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT",
            },
            {
                "record_uid": "PROVISIONAL",
                "derived_longitude_wgs84": 98.0,
                "derived_latitude_wgs84": 8.0,
                "coordinate_validation_status": "CRS_INFERRED_NO_DMS_COMPARATOR",
            },
            {
                "record_uid": "REVIEW",
                "derived_longitude_wgs84": 97.0,
                "derived_latitude_wgs84": 7.0,
                "coordinate_validation_status": "CRS_INFERRED_DMS_MISMATCH_UNRESOLVED",
            },
        ]
    )
    default_points = displayable_observations(observations)
    opted_in_points = displayable_observations(observations, include_provisional=True)
    assert default_points["record_uid"].tolist() == ["CONSISTENT"]
    assert opted_in_points["record_uid"].tolist() == ["CONSISTENT", "PROVISIONAL"]
    assert coordinate_category("CRS_INFERRED_DMS_MISSING") == "review_required"
