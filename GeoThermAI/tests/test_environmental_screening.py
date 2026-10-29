"""Tests for Environmental Screening Engine (Phase 2G)."""

import pytest

from geothermai.environmental_screening import (
    ConstraintCategory,
    ConstraintTier,
    DOCUMENTED_SITE_ENVIRONMENTAL_OVERLAPS,
    EnvironmentalScreeningEngine,
    STANDARD_ENVIRONMENTAL_RULES,
)


class TestEnvironmentalScreening:
    def test_standard_rules_catalog_completeness(self):
        engine = EnvironmentalScreeningEngine()
        assert len(engine.rules) >= 8

        # Verify critical statutory exclusions
        crit_rules = engine.get_rules_by_tier(ConstraintTier.CRITICAL_EXCLUSION)
        crit_ids = [r.rule_id for r in crit_rules]
        assert "ENV_RULE_DNP_NATIONAL_PARK" in crit_ids
        assert "ENV_RULE_DNP_WILDLIFE_SANCTUARY" in crit_ids
        assert "ENV_RULE_ONWR_WATERSHED_1A" in crit_ids

        # Verify conditional review rules
        cond_rules = engine.get_rules_by_tier(ConstraintTier.CONDITIONAL_REVIEW)
        cond_ids = [r.rule_id for r in cond_rules]
        assert "ENV_RULE_ONWR_WATERSHED_1B_2" in cond_ids
        assert "ENV_RULE_RFD_RESERVED_FOREST" in cond_ids
        assert "ENV_RULE_DGR_GROUNDWATER_SENSITIVITY" in cond_ids

    def test_fang_geothermal_screening_is_critical_exclusion(self):
        engine = EnvironmentalScreeningEngine()
        eval_res = engine.evaluate_manifestation_site(
            site_id="NORTH_WOOD2014_CM_01",
            site_name="Fang (โป่งน้ำร้อนฝาง)",
            lat=19.96,
            lon=99.15,
        )
        assert eval_res.overall_constraint_tier == ConstraintTier.CRITICAL_EXCLUSION
        assert "Doi Pha Hom Pok National Park" in eval_res.known_overlap_notes
        assert eval_res.eia_required is True
        assert "Cabinet" in eval_res.permitting_pathway
        # Confirms distinction between resource potential and statutory right to drill
        assert "legally off-limits" in eval_res.deployment_suitability_comment

    def test_pa_pae_geothermal_screening(self):
        engine = EnvironmentalScreeningEngine()
        eval_res = engine.evaluate_manifestation_site(
            site_id="NORTH_WOOD2014_CM_03",
            site_name="Pa Pae",
            lat=19.13,
            lon=98.70,
        )
        assert eval_res.overall_constraint_tier == ConstraintTier.CRITICAL_EXCLUSION
        assert "Huai Nam Dang National Park" in eval_res.known_overlap_notes

    def test_mae_chan_screening_is_conditional_review(self):
        engine = EnvironmentalScreeningEngine()
        eval_res = engine.evaluate_manifestation_site(
            site_id="NORTH_WOOD2014_CR_04",
            site_name="Mae Chan (ป่าตึง)",
            lat=20.12,
            lon=99.80,
        )
        assert eval_res.overall_constraint_tier == ConstraintTier.CONDITIONAL_REVIEW
        assert "Outside National Park" in eval_res.known_overlap_notes
        assert "Potentially feasible" in eval_res.deployment_suitability_comment

    def test_unverified_site_fails_closed_to_not_evaluated(self):
        engine = EnvironmentalScreeningEngine()
        eval_res = engine.evaluate_manifestation_site(
            site_id="UNKNOWN_PROVISIONAL_99",
            site_name="Hypothetical Spring",
            lat=18.0,
            lon=99.0,
        )
        assert eval_res.overall_constraint_tier == ConstraintTier.NOT_EVALUATED
        assert "unverified against environmental boundary" in eval_res.deployment_suitability_comment
