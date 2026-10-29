"""Tests for Exploration Decision Support Engine (Phase 2G)."""

import pytest

from geothermai.decision_support import (
    DecisionSupportEngine,
    ExplorationPriorityTier,
    InvestigationAction,
)
from geothermai.environmental_screening import ConstraintTier


class TestDecisionSupport:
    def test_evaluate_tier_a_feasible_system(self):
        engine = DecisionSupportEngine()
        records = [
            {
                "record_uid": "NORTH_WOOD2014_CR_04",
                "derived_latitude_wgs84": "20.123951",
                "derived_longitude_wgs84": "99.802673",
                "surface_temperature_c": "99.1",
                "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT",
                "published_reference": "Wood and Singharajwarapan (2014)",
            }
        ]
        card = engine.evaluate_hydrothermal_system(
            system_id="MAE_CHAN_SYSTEM",
            system_name="Mae Chan Geothermal System (น้ำพุร้อนป่าตึง)",
            records=records,
            geology_desc="Triassic biotite granite plutons cutting Paleozoic metasediments",
            fault_desc="ENE-WSW trending Mae Chan active fault zone with transtensional dilation",
            res_temp_est=150.0,
            geothermometer_method="Quartz Conductive (Fournier 1977)",
            grid_dist_km=4.5,
        )
        assert card.priority_tier == ExplorationPriorityTier.TIER_A_HIGH_EVIDENCE_FEASIBLE
        assert card.max_surface_temperature_c == 99.1
        assert card.estimated_reservoir_temperature_c == 150.0
        assert InvestigationAction.MAGNETOTELLURIC_RESISTIVITY_SURVEY in card.recommended_actions
        assert InvestigationAction.SHALLOW_TEMPERATURE_GRADIENT_HOLE in card.recommended_actions
        assert "Highest priority for exploration investment" in card.investigation_rationale

    def test_evaluate_tier_b_environmentally_constrained_system(self):
        engine = DecisionSupportEngine()
        records = [
            {
                "record_uid": "NORTH_WOOD2014_CM_01",
                "derived_latitude_wgs84": "19.96",
                "derived_longitude_wgs84": "99.15",
                "surface_temperature_c": "98.5",
                "coordinate_validation_status": "CRS_AND_DMS_CONSISTENT",
                "published_reference": "Wood and Singharajwarapan (2014)",
            }
        ]
        card = engine.evaluate_hydrothermal_system(
            system_id="FANG_SYSTEM",
            system_name="Fang Geothermal Field (ดอยผ้าห่มปก)",
            records=records,
            geology_desc="Fang Cenozoic extensional basin margin granites",
            fault_desc="Mae Chai - Fang active strike-slip/extensional border fault",
            res_temp_est=130.0,
        )
        assert card.priority_tier == ExplorationPriorityTier.TIER_B_HIGH_EVIDENCE_ENVIRONMENTALLY_CONSTRAINED
        assert card.environmental_tier == ConstraintTier.CRITICAL_EXCLUSION
        assert InvestigationAction.STATUTORY_LAND_TENURE_AUDIT in card.recommended_actions
        assert "statutorily barred under National Parks Act" in card.investigation_rationale

    def test_evaluate_tier_e_withheld_coordinate_system(self):
        engine = DecisionSupportEngine()
        records = [
            {
                "record_uid": "NORTH_WOOD2014_CR_02",
                "original_lat": "19.963125",
                "original_lon": "99.680254",
                "surface_temperature_c": "85.0",
                "coordinate_status": "WITHHELD_COORDINATE_MISMATCH",
                "published_reference": "Wood and Singharajwarapan (2014)",
            }
        ]
        card = engine.evaluate_hydrothermal_system(
            system_id="KOK_RIVER_CR02",
            system_name="Kok River Manifestation CR_02",
            records=records,
            geology_desc="Granite basement",
            fault_desc="Kok River fault",
        )
        assert card.priority_tier == ExplorationPriorityTier.TIER_E_WITHHELD_FROM_EXPLORATION
        assert InvestigationAction.PRIMARY_GPS_VERIFICATION in card.recommended_actions
        assert "Field re-survey with dual-frequency GPS is mandatory" in card.investigation_rationale

    def test_evaluate_tier_d_provisional_southern_system(self):
        engine = DecisionSupportEngine()
        records = [
            {
                "record_uid": "SOUTH_NGANSOM2021_RN1",
                "derived_latitude_wgs84": "9.955535",
                "derived_longitude_wgs84": "98.654861",
                "surface_temperature_c": "65.0",
                "coordinate_validation_status": "CRS_INFERRED_NO_DMS_COMPARATOR",
                "published_reference": "Ngansom and Duerrast (2021)",
            }
        ]
        card = engine.evaluate_hydrothermal_system(
            system_id="RANONG_PROVINCE_HOT_SPRINGS",
            system_name="Ranong Geothermal Province",
            records=records,
            geology_desc="Ranong granites and Cretaceous sedimentary sequence",
            fault_desc="Ranong active fault zone",
        )
        assert card.priority_tier == ExplorationPriorityTier.TIER_D_PROVISIONAL_UNRESOLVED_COORDINATES
        assert InvestigationAction.PRIMARY_GPS_VERIFICATION in card.recommended_actions
        assert InvestigationAction.STATUTORY_LAND_TENURE_AUDIT in card.recommended_actions
