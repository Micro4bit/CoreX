"""Tests for Thai Geoscience Data Harmonization Engine (Phase 2G)."""

import numpy as np
import pandas as pd
import pytest

from geothermai.harmonization import (
    CANONICAL_PHYSICAL_UNITS,
    DatasetProvenanceTier,
    GeoscienceHarmonizer,
    HarmonizationStatus,
    HarmonizedCrs,
    HarmonizedRecord,
)


class TestGeoscienceHarmonization:
    def test_canonical_units_defined(self):
        assert CANONICAL_PHYSICAL_UNITS["heat_flow"] == "mW/m^2"
        assert CANONICAL_PHYSICAL_UNITS["surface_temperature"] == "deg_C"
        assert CANONICAL_PHYSICAL_UNITS["fault_distance"] == "km"
        assert CANONICAL_PHYSICAL_UNITS["seismic_event_density"] == "events_per_50km2"
        assert CANONICAL_PHYSICAL_UNITS["dilation_tendency"] == "dimensionless_ratio"

    def test_harmonize_consistent_manifestation(self):
        row = {
            "record_uid": "TEST_CR_01",
            "source_id": "WOOD2014",
            "derived_latitude_wgs84": "19.946018",
            "derived_longitude_wgs84": "99.728477",
            "source_easting_m": "576200",
            "source_northing_m": "2205400",
            "surface_temperature_c": "85.5",
            "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT",
            "proposed_site_group_id": "KOK_RIVER",
        }
        record = GeoscienceHarmonizer.harmonize_manifestation_record(row)
        assert record.status == HarmonizationStatus.HARMONIZED_VERIFIED
        assert record.provenance_tier == DatasetProvenanceTier.TIER_2_PEER_REVIEWED
        assert record.canonical_unit == "deg_C"
        assert record.harmonized_value == 85.5
        assert record.metadata["subsurface_proven"] is False

    def test_harmonize_withheld_manifestation(self):
        row = {
            "record_uid": "TEST_CR_02",
            "source_id": "WOOD2014",
            "original_lat": "19.963125",
            "original_lon": "99.680254",
            "coordinate_status": "WITHHELD_COORDINATE_MISMATCH",
            "surface_temperature_c": "85.0",
        }
        record = GeoscienceHarmonizer.harmonize_manifestation_record(row)
        assert record.provenance_tier == DatasetProvenanceTier.TIER_5_WITHHELD
        assert record.status == HarmonizationStatus.PROVISIONAL_NEEDS_REVIEW
        assert "Withheld" in record.quality_notes

    def test_harmonize_provisional_southern_manifestation(self):
        row = {
            "record_uid": "TEST_RN_01",
            "source_id": "NGANSOM2021",
            "derived_latitude_wgs84": "9.955535",
            "derived_longitude_wgs84": "98.654861",
            "coordinate_validation_status": "CRS_INFERRED_NO_DMS_COMPARATOR",
            "surface_temperature_c": "65.0",
        }
        record = GeoscienceHarmonizer.harmonize_manifestation_record(row)
        assert record.provenance_tier == DatasetProvenanceTier.TIER_4_PROVISIONAL
        assert record.status == HarmonizationStatus.HARMONIZED_WITH_WARNINGS

    def test_harmonize_ihfc_heat_flow_anti_interpolation(self):
        row = {
            "record_id": "IHFC_TH_001",
            "latitude": "18.5",
            "longitude": "99.0",
            "heat_flow_mw_m2": "78.2",
            "uncertainty": None,
            "depth_m": 250.0,
        }
        record = GeoscienceHarmonizer.harmonize_ihfc_heat_flow_record(row)
        assert record.canonical_unit == "mW/m^2"
        assert record.harmonized_value == 78.2
        assert record.uncertainty is None
        # Must strictly forbid spatial interpolation
        assert record.metadata["interpolation_eligible"] is False
        assert "SPATIAL INTERPOLATION FORBIDDEN" in record.quality_notes

    def test_geothermometer_calculations(self):
        # Quartz geothermometer: 100 mg/L SiO2
        # Fournier (1977): 1309 / (5.19 - log10(100)) - 273.15 = 1309 / (5.19 - 2) - 273.15 = 1309 / 3.19 - 273.15 = 410.34 - 273.15 = 137.2 °C
        t_qtz = GeoscienceHarmonizer.calculate_quartz_geothermometer(100.0)
        assert t_qtz is not None
        assert 135.0 <= t_qtz <= 140.0

        # Chalcedony geothermometer: 100 mg/L SiO2
        # Arnorsson (1975): 1032 / (4.69 - 2) - 273.15 = 1032 / 2.69 - 273.15 = 383.64 - 273.15 = 110.5 °C
        t_chalc = GeoscienceHarmonizer.calculate_chalcedony_geothermometer(100.0)
        assert t_chalc is not None
        assert 108.0 <= t_chalc <= 113.0

        # Na-K geothermometer: Na=100 mg/L, K=15 mg/L
        t_nak = GeoscienceHarmonizer.calculate_nak_geothermometer(100.0, 15.0)
        assert t_nak is not None
        assert 150.0 <= t_nak <= 250.0

    def test_validate_predictor_set_safety_catches_leakage(self):
        safe_predictors = [
            "heat_flow_mw_m2",
            "dist_quaternary_fault_km",
            "elevation_m",
            "bouguer_gravity_mgal",
        ]
        is_safe, violations = GeoscienceHarmonizer.validate_predictor_set_safety(safe_predictors)
        assert is_safe is True
        assert len(violations) == 0

        leaked_predictors = [
            "heat_flow_mw_m2",
            "distance_to_known_hot_spring",
            "manifestation_density",
        ]
        is_safe, violations = GeoscienceHarmonizer.validate_predictor_set_safety(leaked_predictors)
        assert is_safe is False
        assert len(violations) == 2
        assert any("hot_spring" in v for v in violations)
        assert any("manifestation" in v for v in violations)

    def test_enforce_harmonization_separation_prevents_global_normalization(self):
        # Create a dataframe with artificially pre-normalized z-scores
        np.random.seed(42)
        n = 50
        norm_vals = np.random.normal(0.0, 1.0, n)
        # Ensure exact mean=0 and std=1
        norm_vals = (norm_vals - norm_vals.mean()) / norm_vals.std()
        
        df = pd.DataFrame({
            "elevation_m": norm_vals,
            "latitude_wgs84": np.linspace(17, 20, n),
            "longitude_wgs84": np.linspace(98, 100, n),
        })

        with pytest.raises(ValueError, match="CRITICAL METHODOLOGICAL LEAKAGE"):
            GeoscienceHarmonizer.enforce_harmonization_separation(df, is_ml_training_fold=False)

        # But within an ML training fold, downstream scaling is permitted
        result = GeoscienceHarmonizer.enforce_harmonization_separation(df, is_ml_training_fold=True)
        assert isinstance(result, pd.DataFrame)
