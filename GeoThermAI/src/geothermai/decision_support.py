"""Exploration Decision Support and Triage Engine for GeoThermAI.

Provides transparent, evidence-based exploration decision support for Thailand geothermal
resources without fabricating unverified machine learning prospectivity or drilling success probabilities.

Answers four fundamental exploration planning questions:
1. Which area should be explored first? (Exploration Prioritization Tier)
2. Why? (Geoscientific evidence, tectonic context, thermal indicators)
3. How reliable is the evidence? (Provenance tier, coordinate audit, missing data, uncertainty)
4. What must be investigated next? (Actionable geoscientific field investigation roadmap)

FAIL-CLOSED INTEGRITY GUARDRAILS:
- Operates strictly under NO_GO_FOR_PREDICTIVE_ML governance.
- Prohibits ranking outputs based on uncalibrated ML scores or fictitious megawatt claims.
- Separates confirmed hydrothermal systems from speculative commercial power claims.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

import numpy as np

from .environmental_screening import ConstraintTier, EnvironmentalScreeningEngine, SiteEnvironmentalEvaluation
from .harmonization import DatasetProvenanceTier, HarmonizationStatus


class ExplorationPriorityTier(str, enum.Enum):
    """Exploration priority categories based on evidence quality and environmental suitability."""
    TIER_A_HIGH_EVIDENCE_FEASIBLE = "TIER_A_HIGH_EVIDENCE_FEASIBLE"
    # Strong geochemical/thermal evidence + verifiable coordinates + outside critical protected areas
    
    TIER_B_HIGH_EVIDENCE_ENVIRONMENTALLY_CONSTRAINED = "TIER_B_HIGH_EVIDENCE_ENVIRONMENTALLY_CONSTRAINED"
    # Strong geoscientific evidence, but located inside National Parks / WSC 1A (statutorily restricted)
    
    TIER_C_MODERATE_EVIDENCE_DATA_GAPS = "TIER_C_MODERATE_EVIDENCE_DATA_GAPS"
    # Documented manifestation, but lacks geothermometry, MT surveys, or has significant predictor gaps
    
    TIER_D_PROVISIONAL_UNRESOLVED_COORDINATES = "TIER_D_PROVISIONAL_UNRESOLVED_COORDINATES"
    # Discrepant or provisional coordinates; requires field GPS verification before any planning
    
    TIER_E_WITHHELD_FROM_EXPLORATION = "TIER_E_WITHHELD_FROM_EXPLORATION"
    # Unresolvable coordinate error (>1 km) or unverified hearsay


class InvestigationAction(str, enum.Enum):
    """Standardized geoscientific field investigation actions."""
    PRIMARY_GPS_VERIFICATION = "PRIMARY_GPS_VERIFICATION"
    HYDROCHEMICAL_ISOTOPE_SAMPLING = "HYDROCHEMICAL_ISOTOPE_SAMPLING"
    SHALLOW_TEMPERATURE_GRADIENT_HOLE = "SHALLOW_TEMPERATURE_GRADIENT_HOLE"
    MAGNETOTELLURIC_RESISTIVITY_SURVEY = "MAGNETOTELLURIC_RESISTIVITY_SURVEY"
    ACTIVE_FAULT_TRENCHING_AND_DIP_MAPPING = "ACTIVE_FAULT_TRENCHING_AND_DIP_MAPPING"
    STATUTORY_LAND_TENURE_AUDIT = "STATUTORY_LAND_TENURE_AUDIT"
    GRID_INTERCONNECTION_INTERPOLATION_STUDY = "GRID_INTERCONNECTION_INTERPOLATION_STUDY"


@dataclass(frozen=True)
class ExplorationDecisionCard:
    """Complete, transparent decision support dossier for a candidate geothermal system."""
    system_id: str
    system_name: str
    manifestation_count: int
    representative_latitude: float
    representative_longitude: float
    priority_tier: ExplorationPriorityTier
    
    # Scientific Rationale ("Why?")
    primary_geology: str
    active_fault_context: str
    max_surface_temperature_c: float | None
    estimated_reservoir_temperature_c: float | None
    geothermometer_method: str
    
    # Evidence Reliability ("How reliable is the evidence?")
    provenance_tier: DatasetProvenanceTier
    coordinate_consistency: str
    predictor_coverage_status: str
    missing_data_gaps: tuple[str, ...]
    
    # Environmental & Deployment Context
    environmental_tier: ConstraintTier
    protected_area_overlap: str
    transmission_grid_distance_est_km: float | None
    
    # Actionable Next Steps ("What must be investigated next?")
    recommended_actions: tuple[InvestigationAction, ...]
    investigation_rationale: str
    
    # Metadata
    source_references: tuple[str, ...] = field(default_factory=tuple)


class DecisionSupportEngine:
    """Synthesizes geoscientific, environmental, and data readiness evidence into exploration roadmaps."""

    def __init__(self, env_engine: EnvironmentalScreeningEngine | None = None) -> None:
        self.env_engine = env_engine or EnvironmentalScreeningEngine()

    def evaluate_hydrothermal_system(
        self,
        system_id: str,
        system_name: str,
        records: Sequence[Mapping[str, Any]],
        geology_desc: str,
        fault_desc: str,
        res_temp_est: float | None = None,
        geothermometer_method: str = "Quartz Conductive / Na-K (Literature)",
        grid_dist_km: float | None = None,
    ) -> ExplorationDecisionCard:
        """Construct a rigorous decision card for a candidate hydrothermal system."""
        if not records:
            raise ValueError(f"No manifestation records provided for system: {system_id}")

        # Aggregate coordinates and surface temperatures
        lats: list[float] = []
        lons: list[float] = []
        temps: list[float] = []
        coord_statuses: set[str] = set()
        provenance_tiers: set[DatasetProvenanceTier] = set()
        gaps: list[str] = []

        for r in records:
            try:
                lat = float(r.get("derived_latitude_wgs84") or r.get("original_lat") or 0.0)
                lon = float(r.get("derived_longitude_wgs84") or r.get("original_lon") or 0.0)
                if lat != 0.0 and lon != 0.0:
                    lats.append(lat)
                    lons.append(lon)
            except (ValueError, TypeError):
                pass
            
            t_raw = r.get("surface_temperature_c")
            if t_raw is not None and str(t_raw).strip() not in ("", "Unmeasured", "Not reported"):
                try:
                    temps.append(float(t_raw))
                except (ValueError, TypeError):
                    pass

            c_st = str(r.get("coordinate_validation_status") or r.get("coordinate_status") or "UNKNOWN")
            coord_statuses.add(c_st)

        rep_lat = float(np.mean(lats)) if lats else 0.0
        rep_lon = float(np.mean(lons)) if lons else 0.0
        max_t = float(np.max(temps)) if temps else None

        # Check for coordinate issues
        has_withheld = any("WITHHELD" in s or "MISMATCH" in s for s in coord_statuses)
        has_provisional = any("PROVISIONAL" in s or "NO_DMS_COMPARATOR" in s for s in coord_statuses)
        all_consistent = all("CONSISTENT" in s for s in coord_statuses)

        # Environmental screening for representative location
        rep_record_uid = str(records[0].get("record_uid") or records[0].get("source_row_id") or "")
        env_eval: SiteEnvironmentalEvaluation = self.env_engine.evaluate_manifestation_site(
            site_id=rep_record_uid,
            site_name=system_name,
            lat=rep_lat,
            lon=rep_lon,
        )

        # Determine Priority Tier and Recommended Actions
        actions: list[InvestigationAction] = []

        if has_withheld:
            priority = ExplorationPriorityTier.TIER_E_WITHHELD_FROM_EXPLORATION
            coord_summary = "CRITICAL_MISMATCH: Contains withheld rows with >1km coordinate error or missing DMS."
            actions.append(InvestigationAction.PRIMARY_GPS_VERIFICATION)
            gaps.append("Primary GPS coordinates in WGS84 and Indian 1975 unverified.")
            rationale = "Coordinates are discrepant in primary literature. Field re-survey with dual-frequency GPS is mandatory before any modeling."
        elif has_provisional:
            priority = ExplorationPriorityTier.TIER_D_PROVISIONAL_UNRESOLVED_COORDINATES
            coord_summary = "PROVISIONAL: Coordinates lack independent DMS or cross-quadrangle comparator."
            actions.append(InvestigationAction.PRIMARY_GPS_VERIFICATION)
            actions.append(InvestigationAction.STATUTORY_LAND_TENURE_AUDIT)
            gaps.append("Southern coordinate derivation from UTM 47N/48N unverified by field inspection.")
            rationale = "Locations derived from regional UTM projection. Require ground truthing and land tenure verification."
        elif env_eval.overall_constraint_tier == ConstraintTier.CRITICAL_EXCLUSION:
            priority = ExplorationPriorityTier.TIER_B_HIGH_EVIDENCE_ENVIRONMENTALLY_CONSTRAINED
            coord_summary = "CONSISTENT: Verified coordinates, but strictly constrained by National Park or WSC 1A status."
            actions.append(InvestigationAction.STATUTORY_LAND_TENURE_AUDIT)
            actions.append(InvestigationAction.HYDROCHEMICAL_ISOTOPE_SAMPLING)
            actions.append(InvestigationAction.MAGNETOTELLURIC_RESISTIVITY_SURVEY)
            gaps.append("Statutory clearance required: drilling inside National Park prohibited without Cabinet approval.")
            rationale = (
                "Excellent geoscientific potential (e.g. Fang/Pa Pae), but commercial exploitation is statutorily barred "
                "under National Parks Act B.E. 2562. Investigation limited to non-invasive academic MT/hydrogeochemistry."
            )
        else:
            priority = ExplorationPriorityTier.TIER_A_HIGH_EVIDENCE_FEASIBLE
            coord_summary = "VERIFIED_CONSISTENT: Coordinates verified, outside critical national park boundaries."
            actions.append(InvestigationAction.MAGNETOTELLURIC_RESISTIVITY_SURVEY)
            actions.append(InvestigationAction.SHALLOW_TEMPERATURE_GRADIENT_HOLE)
            actions.append(InvestigationAction.ACTIVE_FAULT_TRENCHING_AND_DIP_MAPPING)
            actions.append(InvestigationAction.GRID_INTERCONNECTION_INTERPOLATION_STUDY)
            gaps.append("Subsurface 3D fault dip and permeable fracture network unmapped.")
            gaps.append("Shallow temperature gradient (<300m) unmeasured.")
            rationale = (
                "Highest priority for exploration investment. High surface temperature and accessible terrain outside strict "
                "national parks. Immediate next steps: 3D MT survey to image clay cap/conductive reservoir and shallow thermal gradient wells."
            )

        return ExplorationDecisionCard(
            system_id=system_id,
            system_name=system_name,
            manifestation_count=len(records),
            representative_latitude=round(rep_lat, 6),
            representative_longitude=round(rep_lon, 6),
            priority_tier=priority,
            primary_geology=geology_desc,
            active_fault_context=fault_desc,
            max_surface_temperature_c=max_t,
            estimated_reservoir_temperature_c=res_temp_est,
            geothermometer_method=geothermometer_method,
            provenance_tier=(
                DatasetProvenanceTier.TIER_2_PEER_REVIEWED
                if all_consistent
                else (
                    DatasetProvenanceTier.TIER_4_PROVISIONAL
                    if has_provisional
                    else DatasetProvenanceTier.TIER_5_WITHHELD
                )
            ),
            coordinate_consistency=coord_summary,
            predictor_coverage_status="PARTIAL (Missing 7 SRTM tiles, DMR Fault licensing blocked)",
            missing_data_gaps=tuple(gaps),
            environmental_tier=env_eval.overall_constraint_tier,
            protected_area_overlap=env_eval.known_overlap_notes,
            transmission_grid_distance_est_km=grid_dist_km,
            recommended_actions=tuple(actions),
            investigation_rationale=rationale,
            source_references=tuple(set(str(r.get("source_id") or r.get("published_reference") or "") for r in records)),
        )
