# GeoThermAI — Phase 2G Source License, Provenance & Legal Derivative Audit
**Geoscience Data Rights, Licensing Restrictions & Inter-Agency Governance Framework**  
*Date: 29 October 2026 | Project: GeoThermAI (CoreX) | Legal & Geospatial Data Governance Team*

---

## 1. Executive Summary & Regulatory Policy

GeoThermAI operates under a strict **fail-closed legal and licensing protocol**. Geospatial data obtained from Thai government portals, academic publications, and international repositories must be rigorously audited before ingestion into predictive or derivative workflows.

### Core Legal Distinction
1. **Internal Research Inspection (Permitted):** Reading, inspecting, quality-checking, and viewing datasets within a closed research and scientific verification environment.
2. **Public Derivative Release (Blocked without Written Agency Authorization):** Publishing vector boundaries, high-resolution derived rasters, or commercial prospectivity maps derived from proprietary or unreleased agency data.
3. **Machine Learning Feature Ingestion (Blocked until Gate Clearance):** Using datasets as predictive training features while data rights, spatial coverage, and independent ground truth remain unresolved.

---

## 2. Agency-by-Agency Licensing and Provenance Audit

| Agency / Publisher | Dataset Name | Native License / Terms Declared | Identified Legal Contradictions / Restrictions | Derivative & ML Status |
|---|---|---|---|---|
| **Department of Mineral Resources (DMR / กรมทรัพยากรธรณี)** | **DMR Active Fault Zones (2016/2023)** | Data.go.th portal metadata declares Creative Commons Attribution (CC-BY); but internal shapefile metadata states "Non-commercial, strictly prohibited for legal or commercial citation without written DMR consent". | **Conflicting Terms:** Open Government portal terms conflict with DMR internal departmental metadata. Commercial exploration or third-party publication legally uncertain. | **BLOCKED FOR ML & DERIVATIVE MAPS:** Requires written formal clarification from Director-General of DMR. |
| **Department of Mineral Resources (DMR / กรมทรัพยากรธรณี)** | **DMR 1:250k Northern Geology (Rock Units)** | ArcGIS REST Service metadata contains no explicit copyright or open license text. | **Unstated Terms:** Standard Royal Thai Government default copyright applies under the Copyright Act B.E. 2537 (1994). No open derivative license granted. | **RESTRICTED REDISTRIBUTION:** Permitted for descriptive contextual display only; raster/vector derivative redistribution disabled. |
| **Department of Mineral Resources (DMR / กรมทรัพยากรธรณี)** | **DMR 1:250k Structural Lines (GEOL_STR_250K)** | Unstated terms; service query returns 2,000 attribute records with zero geometries. | **Service Failure & Data Missing:** Cannot compute fault density or distance without valid geometries. | **WITHHELD FROM WORKFLOW.** |
| **NASA / USGS / AWS Open Data** | **SRTM 1 Arc-Second Global Elevation DEM** | NASA Public Domain policy (US Government Work). | None. Attribution requested. | **PERMITTED FOR RESEARCH & DERIVATIVE USE.** (Gaps in spatial coverage remain). |
| **International Heat Flow Commission (IHFC)** | **IHFC Global Heat Flow Database 2024** | Creative Commons Attribution 4.0 International (CC BY 4.0). DOI: [10.5880/fidgeo.2024.014](https://doi.org/10.5880/fidgeo.2024.014). | **Scientific / Methodological Restriction:** CC-BY permits derivative creation, but interpolating 154 sparse points across Thailand into a continuous predictive raster without physics violates scientific validity. | **PERMITTED FOR DESCRIPTIVE POINT OVERLAY ONLY; SPATIAL INTERPOLATION FORBIDDEN.** |
| **Academic Peer Review (Wood 2014 / Chiang Mai Univ)** | **Northern Thailand Geothermal Resources Registry** | Published in *Geothermics* / academic thesis. Fair-use academic citation. | 2 records withheld due to coordinate mismatches (CR_02 > 1 km discrepancy; CM_16 missing DMS text). | **14 RECORDS PERMITTED FOR SCIENTIFIC AUDIT; 2 WITHHELD.** |
| **Academic Peer Review (Ngansom 2021 / PSU)** | **Southern Thailand Hot Springs Registry** | Published in *Journal of Sustainable Energy & Environment*. Academic citation. | 31 coordinates inferred from regional UTM projection without independent DMS comparator or quadrangle ground verification. | **PROVISIONAL STATUS ONLY; NOT APPROVED FOR MODEL TRAINING.** |
| **Department of Groundwater Resources (DGR / กรมทรัพยากรน้ำบาดาล)** | **DGR 1:100k Hydrogeological Basins & Monitoring** | Official Government Data (Groundwater Act B.E. 2520). | Digital shapefiles not openly downloadable; requires formal inter-agency request under Official Information Act B.E. 2540. | **METADATA CATALOGED; PENDING DGR TRANSFER.** |
| **Thai Meteorological Department (TMD / กรมอุตุนิยมวิทยา)** | **Earthquake Observation Division Seismicity Catalog** | Public Open Meteorological Catalog. | Detection threshold non-uniform across remote mountain ranges (station proximity bias). | **PERMITTED FOR RESEARCH DESCRIPTIVE STUDY (M >= 2.5).** |
| **Department of National Parks (DNP / กรมอุทยานแห่งชาติฯ)** | **DNP National Park & Sanctuary Boundaries (1:50k)** | Official Cadastral Data (National Parks Act B.E. 2562). | Polygons not in open public repository; statutory boundaries determine absolute legal exclusion zones. | **METADATA SCREENING ACTIVE; SHAPEFILE TRANSFER PENDING.** |
| **Royal Forest Department (RFD / กรมป่าไม้)** | **National Reserved Forest Boundaries (1:50k)** | Official Cadastral Data (National Reserved Forests Act B.E. 2507). | Forestry boundaries require formal data-sharing MOU with RFD Geoinformatics Center. | **METADATA SCREENING ACTIVE; SHAPEFILE TRANSFER PENDING.** |
| **Office of National Water Resources (ONWR / สทนช.)** | **Cabinet Watershed Classification (WSC 1A-5)** | Cabinet Resolutions on Watershed Classification. | High legal sensitivity for WSC 1A (prohibition on drilling/mining concessions). Shapefile requires official request. | **METADATA SCREENING ACTIVE; SHAPEFILE TRANSFER PENDING.** |
| **Electricity Generating Authority of Thailand (EGAT / กฟผ.)** | **High-Voltage Transmission Network (115/230/500 kV)** | EGAT Public Planning Reports. | Right-of-way corridors generalized in public maps; planning context only. | **PLANNING CONTEXT ONLY (NOT A PREDICTIVE FEATURE).** |

---

## 3. Statutory Protocol for Inter-Agency Data Acquisition

Under the **Official Information Act B.E. 2540 (พ.ร.บ. ข้อมูลข่าวสารของราชการ พ.ศ. 2540)** and the **Digital Government Development Act B.E. 2562 (พ.ร.บ. การบริหารงานและการให้บริการภาครัฐผ่านระบบดิจิทัล พ.ศ. 2562)**, GeoThermAI establishes the following structured acquisition protocol:

### Step 1: Formal Memorandum of Request (หนังสือขอความอนุเคราะห์ข้อมูลทางวิชาการ)
A formal request signed by the Principal Investigator must be transmitted to:
1. **DMR (กรมทรัพยากรธรณี):** Requesting full 1:50,000 / 1:250,000 active fault polylines, 3D structural dip measurements, and explicit written derivative-mapping release permissions.
2. **DNP (กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช):** Requesting current 1:50,000 cadastral boundary shapefiles for National Parks, Wildlife Sanctuaries, and Non-Hunting Areas.
3. **ONWR / ONEP (สทนช. / สผ.):** Requesting official Watershed Classification GIS coverage (WSC 1A, 1B, 2).
4. **RFD (กรมป่าไม้):** Requesting digital boundary polygons of National Reserved Forests under Section 16 concessions.
5. **DGR (กรมทรัพยากรน้ำบาดาล):** Requesting deep groundwater basin maps and hydrochemical monitoring well databases.

### Step 2: Data-Sharing Agreement & Terms of Use (บันทึกข้อตกลงการใช้ข้อมูล - MOU/SLA)
- Define intellectual property parameters: GeoThermAI uses datasets strictly for non-commercial, evidence-based scientific resource screening.
- Establish attribution clauses and embargo dates for unpublished agency surveys.
- Restrict redistribution of raw agency shapefiles to prevent unauthorized commercial exploitation.

---

## 4. Provenance Verification Checklist for Future Phases

Before any dataset can transition from `BLOCKED` or `METADATA_ONLY` to `APPROVED_FOR_MODEL_FEATURE`:
- [ ] Primary source hash (SHA-256) matches the official agency distribution.
- [ ] Datum transformation parameters from Indian 1975 to WGS84 are mathematically documented.
- [ ] Written derivative release authorization is signed by an authorized agency official.
- [ ] Spatial coverage exceeds 90% of the locked Area of Interest (AOI).
- [ ] Measurement uncertainties and detection limits are documented.
- [ ] Zero target leakage: no feature is derived from known hot spring manifestations.
