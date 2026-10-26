import pandas as pd

from geothermai.data_loader import load_observations
from geothermai.provenance import record_provenance


def test_real_registry_preserves_source_coordinate_fields():
    path = __import__("config.settings", fromlist=["OBSERVATIONS_CSV"]).OBSERVATIONS_CSV
    observations, validation = load_observations(path)
    assert validation.is_schema_valid
    assert len(observations) == 47
    cr_02 = observations.loc[observations["record_uid"] == "NORTH_WOOD2014_CR_02"].iloc[0]
    assert cr_02["source_easting_m"] == "571176"
    assert cr_02["source_northing_m"] == "2207545"
    provenance = record_provenance(cr_02)
    assert "source_easting_m" in provenance["field"].tolist()


def test_missing_optional_gis_file_is_a_graceful_state(tmp_path):
    from geothermai.data_loader import inspect_optional_file

    result = inspect_optional_file(tmp_path / "not-present.geojson", "TEST_LAYER")
    assert not result.available
    assert not result.usable
    assert "unavailable" in result.message
