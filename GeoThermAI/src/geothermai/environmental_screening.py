"""Environmental and Deployment Screening Engine for GeoThermAI.

Implements an independent multi-tier environmental, legal, and infrastructure
screening layer for geothermal exploration in Thailand.

REGULATORY AND LEGAL FOUNDATION:
1. National Parks Act B.E. 2562 (2019) (DNP / Department of National Parks, Wildlife and Plant Conservation)
2. Wild Animal Conservation and Protection Act B.E. 2562 (2019) (Wildlife Sanctuaries / Non-Hunting Areas)
3. Cabinet Resolutions on Watershed Classification (ONWR / DWR - WSC 1A, 1B, 2, 3, 4, 5)
4. National Reserved Forests Act B.E. 2507 (1964) (RFD / Royal Forest Department)
5. Agricultural Land Reform Act B.E. 2518 (1975) (ALRO / ส.ป.ก.)
6. Groundwater Act B.E. 2520 (1977) (DGR / Department of Groundwater Resources)
7. Town and Country Planning & Municipal Regulations (DPT)

CRITICAL ARCHITECTURAL PRINCIPLES:
- SEPARATION OF RESOURCE POTENTIAL FROM DEPLOYMENT SUITABILITY:
  High subsurface geological favorability does NOT equal legal right to drill or commercial feasibility.
  Surface manifestations frequently occur within protected headwater forests (e.g. Fang within Doi Pha Hom Pok NP).
- HONEST SPATIAL DATA AVAILABILITY:
  If official vector polygons are not yet held locally, report DATASET_NOT_LOCAL_ACQUIRED rather than
  synthesizing fictitious government boundaries.
- NOT AN EIA EQUIVALENT:
  This screening tool provides early-stage reconnaissance constraint flagging; it is NOT an Environmental
  Impact Assessment (EIA) approval or drilling permit.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


class ConstraintTier(str, enum.Enum):
    """Hierarchy of environmental, statutory, and land-use constraints."""
    CRITICAL_EXCLUSION = "CRITICAL_EXCLUSION"       # Legally prohibited for commercial drilling / mining
    CONDITIONAL_REVIEW = "CONDITIONAL_REVIEW"       # Requires ministerial permits, EIA/IEE approval, or derogation
    MONITORED_FEASIBILITY = "MONITORED_FEASIBILITY" # Standard regulatory permits and environmental monitoring
    NOT_EVALUATED = "NOT_EVALUATED"                 # Constraint layer missing or unverified


class ConstraintCategory(str, enum.Enum):
    """Categories of environmental and deployment screening."""
    PROTECTED_AREA = "PROTECTED_AREA"               # National Parks, Wildlife Sanctuaries
    FOREST_AND_LAND_USE = "FOREST_AND_LAND_USE"     # Reserved Forests, ALRO Land
    WATERSHED_HEADWATER = "WATERSHED_HEADWATER"     # Cabinet Watershed Classification (WSC 1A/1B/2)
    GROUNDWATER_SENSITIVITY = "GROUNDWATER_SENSITIVITY" # Potable aquifers, high-yield protection
    COMMUNITY_BUFFER = "COMMUNITY_BUFFER"           # Settlement proximity, noise, H2S dispersion
    INFRASTRUCTURE_PROXIMITY = "INFRASTRUCTURE_PROXIMITY" # Grid connection lines, sub-stations, roads


@dataclass(frozen=True)
class EnvironmentalConstraintRule:
    """Definition of an individual statutory or environmental constraint rule."""
    rule_id: str
    category: ConstraintCategory
    governing_statute_th: str
    governing_agency: str
    tier: ConstraintTier
    description_en: str
    description_th: str
    spatial_data_source: str
    local_data_status: str  # AVAILABLE_VERIFIED, METADATA_ONLY, NOT_ACQUIRED


# Comprehensive Registry of Thai Environmental Screening Rules
STANDARD_ENVIRONMENTAL_RULES: tuple[EnvironmentalConstraintRule, ...] = (
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_DNP_NATIONAL_PARK",
        category=ConstraintCategory.PROTECTED_AREA,
        governing_statute_th="พ.ร.บ. อุทยานแห่งชาติ พ.ศ. 2562 (มาตรา 19 ห้ามยึดถือ ครอบครอง หรือทำลายทรัพยากร)",
        governing_agency="DNP (กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช)",
        tier=ConstraintTier.CRITICAL_EXCLUSION,
        description_en="National Parks are strictly protected under Section 19 of the National Parks Act B.E. 2562. Commercial exploration drilling and mining are strictly prohibited without specific legislative or royal decree exemptions.",
        description_th="พื้นที่อุทยานแห่งชาติได้รับการคุ้มครองอย่างเข้มงวดตามมาตรา 19 แห่ง พ.ร.บ. อุทยานแห่งชาติ พ.ศ. 2562 ห้ามขุดเจาะหรือทำเหมืองเพื่อการพาณิชย์โดยเด็ดขาด",
        spatial_data_source="DNP National Park Boundaries Shapefile (1:50,000)",
        local_data_status="METADATA_ONLY",
    ),
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_DNP_WILDLIFE_SANCTUARY",
        category=ConstraintCategory.PROTECTED_AREA,
        governing_statute_th="พ.ร.บ. สงวนและคุ้มครองสัตว์ป่า พ.ศ. 2562 (มาตรา 53-55)",
        governing_agency="DNP (กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช)",
        tier=ConstraintTier.CRITICAL_EXCLUSION,
        description_en="Wildlife Sanctuaries and Non-Hunting Areas represent strict biodiversity conservation zones with total prohibition on industrial surface disturbance.",
        description_th="เขตรักษาพันธุ์สัตว์ป่าและเขตห้ามล่าสัตว์ป่า มีสถานะคุ้มครองความหลากหลายทางชีวภาพขั้นสูงสุด ห้ามรบกวนพื้นผิวเพื่อกิจกรรมอุตสาหกรรม",
        spatial_data_source="DNP Wildlife Sanctuary Boundaries (1:50,000)",
        local_data_status="METADATA_ONLY",
    ),
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_ONWR_WATERSHED_1A",
        category=ConstraintCategory.WATERSHED_HEADWATER,
        governing_statute_th="มติคณะรัฐมนตรี เรื่องชั้นคุณภาพลุ่มน้ำ (ลุ่มน้ำชั้นที่ 1A)",
        governing_agency="ONWR / DWR (สำนักงานทรัพยากรน้ำแห่งชาติ / กรมทรัพยากรน้ำ)",
        tier=ConstraintTier.CRITICAL_EXCLUSION,
        description_en="Class 1A Watersheds represent pristine headwater forests with significant erosion risks. Cabinet resolutions strictly prohibit mining, drilling, or clear-cutting without an extraordinary Cabinet resolution.",
        description_th="พื้นที่ลุ่มน้ำชั้นที่ 1A เป็นพื้นที่ป่าต้นน้ำแท้จริง มีความเสี่ยงต่อการพังทลายของดินสูง มติ ครม. ห้ามประทานบัตรเหมืองแร่หรือขุดเจาะโดยเด็ดขาด เว้นแต่ได้รับอนุมัติเป็นกรณีพิเศษจากคณะรัฐมนตรี",
        spatial_data_source="ONWR/ONEP Watershed Classification GIS Database (1:50,000)",
        local_data_status="NOT_ACQUIRED",
    ),
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_ONWR_WATERSHED_1B_2",
        category=ConstraintCategory.WATERSHED_HEADWATER,
        governing_statute_th="มติคณะรัฐมนตรี เรื่องชั้นคุณภาพลุ่มน้ำ (ลุ่มน้ำชั้นที่ 1B และชั้นที่ 2)",
        governing_agency="ONWR / ONEP (สผ.)",
        tier=ConstraintTier.CONDITIONAL_REVIEW,
        description_en="Class 1B and Class 2 Watersheds require comprehensive Environmental Impact Assessment (EIA) approval by ONEP and compensatory reforestation plans prior to any site development.",
        description_th="พื้นที่ลุ่มน้ำชั้นที่ 1B และ 2 ต้องจัดทำรายงานการประเมินผลกระทบสิ่งแวดล้อม (EIA) และได้รับความเห็นชอบจาก สผ. รวมถึงแผนปลูกป่าทดแทนก่อนเริ่มดำเนินการ",
        spatial_data_source="ONWR/ONEP Watershed Classification GIS Database (1:50,000)",
        local_data_status="NOT_ACQUIRED",
    ),
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_RFD_RESERVED_FOREST",
        category=ConstraintCategory.FOREST_AND_LAND_USE,
        governing_statute_th="พ.ร.บ. ป่าสงวนแห่งชาติ พ.ศ. 2507 (มาตรา 16 และ 13/1)",
        governing_agency="RFD (กรมป่าไม้)",
        tier=ConstraintTier.CONDITIONAL_REVIEW,
        description_en="National Reserved Forests require formal forestry concession permits from the Royal Forest Department under Section 16, subject to forest maintenance fees and environmental mitigation.",
        description_th="พื้นที่ป่าสงวนแห่งชาติ ต้องได้รับอนุญาตเข้าทำประโยชน์ตามมาตรา 16 แห่ง พ.ร.บ. ป่าสงวนแห่งชาติ พ.ศ. 2507 จากกรมป่าไม้ พร้อมวางหลักประกันและค่าธรรมเนียมบำรุงป่า",
        spatial_data_source="RFD National Reserved Forest Boundaries (1:50,000)",
        local_data_status="NOT_ACQUIRED",
    ),
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_ALRO_LAND_REFORM",
        category=ConstraintCategory.FOREST_AND_LAND_USE,
        governing_statute_th="พ.ร.บ. การปฏิรูปที่ดินเพื่อเกษตรกรรม พ.ศ. 2518",
        governing_agency="ALRO (สำนักงานการปฏิรูปที่ดินเพื่อเกษตรกรรม - ส.ป.ก.)",
        tier=ConstraintTier.CONDITIONAL_REVIEW,
        description_en="Agricultural Land Reform (ALRO) areas are reserved strictly for agricultural farmers. Energy and mining infrastructure require statutory clearance and approval by the Central Land Reform Committee.",
        description_th="เขตปฏิรูปที่ดินเพื่อเกษตรกรรม (ส.ป.ก.) จัดสรรเพื่อเกษตรกรรมเป็นหลัก การใช้ที่ดินเพื่อโครงสร้างพื้นฐานพลังงานต้องได้รับความเห็นชอบจากคณะกรรมการปฏิรูปที่ดินเพื่อเกษตรกรรม",
        spatial_data_source="ALRO Cadastral GIS Database (1:50,000)",
        local_data_status="NOT_ACQUIRED",
    ),
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_DGR_GROUNDWATER_SENSITIVITY",
        category=ConstraintCategory.GROUNDWATER_SENSITIVITY,
        governing_statute_th="พ.ร.บ. น้ำบาดาล พ.ศ. 2520 (และการประกาศเขตวิกฤติน้ำบาดาล)",
        governing_agency="DGR (กรมทรัพยากรน้ำบาดาล)",
        tier=ConstraintTier.CONDITIONAL_REVIEW,
        description_en="Geothermal drilling intersects shallow and intermediate hydrogeological aquifers. Strict casing, cementing, and wellhead integrity standards are mandatory under DGR regulations to prevent thermal or mineral cross-contamination of drinking water aquifers.",
        description_th="การเจาะสำรวจความร้อนใต้พิภพต้องตัดผ่านชั้นน้ำบาดาลตื้นและลึก ต้องปฏิบัติตามมาตรฐานการกรุบ่อและซีเมนต์บ่อตามกฎกระทรวงเพื่อป้องกันการปนเปื้อนแร่ธาตุและความร้อนลงสู่ชั้นน้ำบาดาลบริโภค",
        spatial_data_source="DGR Hydrogeological Map of Thailand (1:100,000)",
        local_data_status="METADATA_ONLY",
    ),
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_SETTLEMENT_BUFFER",
        category=ConstraintCategory.COMMUNITY_BUFFER,
        governing_statute_th="พ.ร.บ. การสาธารณสุข พ.ศ. 2535 และข้อบัญญัติท้องถิ่น / ผังเมืองรวม",
        governing_agency="DPT (กรมโยธาธิการและผังเมือง) และองค์กรปกครองส่วนท้องถิ่น (อปท.)",
        tier=ConstraintTier.MONITORED_FEASIBILITY,
        description_en="Drilling operations require a minimum setback (recommended 500 m to 1 km) from residential areas, schools, and hospitals to mitigate noise, vibrations, and hydrogen sulfide (H2S) gas dispersion.",
        description_th="การขุดเจาะทดสอบต้องมีระยะเว้นห่างจากชุมชน โรงพยาบาล และโรงเรียน (แนะนำ 500 ม. - 1 กม.) เพื่อควบคุมผลกระทบทางเสียง ความสั่นสะเทือน และการแพร่กระจายของก๊าซไฮโดรเจนซัลไฟด์ (H2S)",
        spatial_data_source="DPT Municipal and Settlement Boundaries",
        local_data_status="METADATA_ONLY",
    ),
    EnvironmentalConstraintRule(
        rule_id="ENV_RULE_GRID_CORRIDOR",
        category=ConstraintCategory.INFRASTRUCTURE_PROXIMITY,
        governing_statute_th="พ.ร.บ. การไฟฟ้าฝ่ายผลิตแห่งประเทศไทย พ.ศ. 2511",
        governing_agency="EGAT / PEA (กฟผ. / กฟภ.)",
        tier=ConstraintTier.MONITORED_FEASIBILITY,
        description_en="Commercial viability depends heavily on distance to existing 115 kV / 230 kV high-voltage transmission lines or sub-stations. Transmission spur costs exceeding 10-15 km can render small-scale geothermal binary projects economically infeasible.",
        description_th="ความเป็นไปได้เชิงพาณิชย์ขึ้นอยู่กับระยะทางถึงสายส่งไฟฟ้าแรงสูง 115 kV / 230 kV หรือสถานีไฟฟ้าย่อยของ กฟผ./กฟภ. ค่าใช้จ่ายสายส่งเชื่อมต่อเกิน 10-15 กม. อาจทำให้โครงการขนาดเล็กไม่คุ้มค่าทางเศรษฐศาสตร์",
        spatial_data_source="EGAT Transmission System Network Map",
        local_data_status="METADATA_ONLY",
    ),
)


@dataclass(frozen=True)
class SiteEnvironmentalEvaluation:
    """Evaluation result for a specific candidate geothermal site."""
    site_id: str
    site_name: str
    latitude: float
    longitude: float
    overall_constraint_tier: ConstraintTier
    flagged_rules: tuple[EnvironmentalConstraintRule, ...]
    known_overlap_notes: str
    eia_required: bool
    permitting_pathway: str
    deployment_suitability_comment: str


# Documented Protected Area Overlaps for Primary Thai Hot Springs (Wood 2014, DMR 2012)
DOCUMENTED_SITE_ENVIRONMENTAL_OVERLAPS: dict[str, dict[str, Any]] = {
    "NORTH_WOOD2014_CM_01": {  # Fang Geothermal Field
        "name": "Fang (โป่งน้ำร้อนฝาง)",
        "tier": ConstraintTier.CRITICAL_EXCLUSION,
        "protected_area": "Doi Pha Hom Pok National Park (อุทยานแห่งชาติดอยผ้าห่มปก)",
        "watershed_class": "WSC 1A / 1B",
        "notes": "Existing 0.3 MW EGAT binary plant operates under historical special derogation established in 1989 prior to the 2019 National Parks Act. Any new commercial expansion or exploratory deep drilling would require extraordinary Cabinet exemption.",
    },
    "NORTH_WOOD2014_CM_02": {  # San Kamphaeng
        "name": "San Kamphaeng (น้ำพุร้อนสันกำแพง)",
        "tier": ConstraintTier.CONDITIONAL_REVIEW,
        "protected_area": "Mae On National Reserved Forest / Cooperative Village Zone",
        "watershed_class": "WSC 2 / 3",
        "notes": "Operates as a cooperative tourism center. Deep drilling requires RFD Section 16 forest concession and groundwater protection casing review.",
    },
    "NORTH_WOOD2014_CM_03": {  # Pa Pae
        "name": "Pa Pae (โป่งเดือดป่าแป๋)",
        "tier": ConstraintTier.CRITICAL_EXCLUSION,
        "protected_area": "Huai Nam Dang National Park (อุทยานแห่งชาติห้วยน้ำดัง)",
        "watershed_class": "WSC 1A",
        "notes": "Geyser manifestation located entirely within Huai Nam Dang National Park. Strict exclusion applies under National Parks Act B.E. 2562.",
    },
    "NORTH_WOOD2014_CR_04": {  # Mae Chan
        "name": "Mae Chan (น้ำพุร้อนป่าตึง / แม่จัน)",
        "tier": ConstraintTier.CONDITIONAL_REVIEW,
        "protected_area": "Municipal / Community Tourism Zone (Outside National Park)",
        "watershed_class": "WSC 3",
        "notes": "Located on local administrative / public land. Outside National Parks. Favorable for community-scale binary or agricultural direct use, subject to local municipal permits and standard DGR groundwater protection.",
    },
    "NORTH_WOOD2014_CR_06": {  # Sop Pong / Wiang Pa Pao
        "name": "Sop Pong (น้ำพุร้อนสบโป่ง / แม่ขะจาน)",
        "tier": ConstraintTier.CONDITIONAL_REVIEW,
        "protected_area": "National Reserved Forest Zone / Highway Corridor",
        "watershed_class": "WSC 2",
        "notes": "Adjacent to Chiang Mai - Chiang Rai highway corridor. RFD forest concession required. Excellent transport and power line access.",
    },
}


class EnvironmentalScreeningEngine:
    """Evaluates candidate sites and regions against Thai environmental and land-use rules."""

    def __init__(self, rules: Sequence[EnvironmentalConstraintRule] = STANDARD_ENVIRONMENTAL_RULES) -> None:
        self.rules = tuple(rules)

    def get_rules_by_tier(self, tier: ConstraintTier) -> list[EnvironmentalConstraintRule]:
        return [r for r in self.rules if r.tier == tier]

    def get_rules_by_category(self, cat: ConstraintCategory) -> list[EnvironmentalConstraintRule]:
        return [r for r in self.rules if r.category == cat]

    def evaluate_manifestation_site(
        self,
        site_id: str,
        site_name: str,
        lat: float,
        lon: float,
    ) -> SiteEnvironmentalEvaluation:
        """Perform preliminary environmental screening on a known geothermal site."""
        documented = DOCUMENTED_SITE_ENVIRONMENTAL_OVERLAPS.get(site_id)
        
        if documented:
            tier = documented["tier"]
            flagged = [
                r for r in self.rules
                if (tier == ConstraintTier.CRITICAL_EXCLUSION and r.tier == ConstraintTier.CRITICAL_EXCLUSION)
                or (tier == ConstraintTier.CONDITIONAL_REVIEW and r.tier == ConstraintTier.CONDITIONAL_REVIEW)
            ]
            notes = f"Documented overlap: {documented['protected_area']} ({documented['watershed_class']}). {documented['notes']}"
            eia = True
            pathway = (
                "Special Cabinet Resolution Exemption required"
                if tier == ConstraintTier.CRITICAL_EXCLUSION
                else "Ministry of Natural Resources and Environment (MNRE) Section 16 Permit + ONEP EIA"
            )
            comment = (
                "High subsurface temperature documented, but commercial drilling legally off-limits without legislative exception."
                if tier == ConstraintTier.CRITICAL_EXCLUSION
                else "Potentially feasible under conditional statutory permitting and community environmental agreement."
            )
        else:
            # For sites without specific field documentation, flag as requiring official GIS overlay
            tier = ConstraintTier.NOT_EVALUATED
            flagged = []
            notes = "Specific cadastral and watershed class overlap unverified; requires official DNP/RFD/ONWR GIS overlay."
            eia = True
            pathway = "Comprehensive environmental review and tenure audit required prior to site licensing."
            comment = "Subsurface thermal evidence unverified against environmental boundary; do not proceed with field work until tenure audit completes."

        return SiteEnvironmentalEvaluation(
            site_id=site_id,
            site_name=site_name,
            latitude=lat,
            longitude=lon,
            overall_constraint_tier=tier,
            flagged_rules=tuple(flagged),
            known_overlap_notes=notes,
            eia_required=eia,
            permitting_pathway=pathway,
            deployment_suitability_comment=comment,
        )
