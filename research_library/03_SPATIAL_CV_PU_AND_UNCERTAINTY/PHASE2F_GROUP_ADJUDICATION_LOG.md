# GeoThermAI Phase 2F — Group Adjudication Log & Domain Review Schema
**Independent Hydrothermal System Boundary Review for Thailand**

**Document Version:** 1.0 (Phase 2F)  
**Date:** 2026-10-27 (Asia/Bangkok)  
**Status:** DRAFT ADJUDICATION LOG — **AWAITING DOMAIN EXPERT SIGN-OFF**  
**Input Registry SHA-256:** `93d3bf9cd3c52ffbc207ca3a308c3e6ece1e067caf9c98fe08e85e338ef83c6e` (47 rows)

---

## 1. Scientific Principles for Label Adjudication

In geothermal machine learning, the fundamental unit of analysis for validation and loss calculation must be the **independent hydrothermal system**, NOT individual surface manifestations or registry rows.

### Critical Conceptual Distinctions:
1. **Surface Manifestation (Spring/Seep):** A surface discharge point where thermal fluid escapes along local fracture permeability. Multiple manifestations can share a single underlying convective plume.
2. **Independent Hydrothermal System:** A discrete convective hydrothermal circulation cell possessing its own distinct heat source (e.g. radiogenic granite pluton), deep meteoric recharge zone, and structural conduit network.
3. **Commercial Reservoir:** A permeable, economically producible volume of subsurface fluid with sufficient enthalpy and volume for power generation or industrial direct use.

> [!CAUTION]
> **Strict Non-Claim:**
> The GeoThermAI registry contains **surface manifestations only**. No claim of verified reservoir existence or commercial reserve volume is made or inferred from manifestation locations.

---

## 2. Review of the 18 Provisional Co-Withholding Units

Phase 1B and 1C proposed 18 provisional spatial grouping units based on geographical proximity and administrative clustering:

| Provisional Group ID | Contained Records | Geographic Province | Geological Association | Pending Adjudication Question |
|---|---|---|---|---|
| `KOK_RIVER_GEOTHERMAL_AREAS` | `CR_01`, `CR_02`, `CR_03`, `CR_08` | Chiang Rai (Kok River) | Mae Chan / Kok River fault intersection | **Shared Plume vs Separate Springs:** Do these 4 springs share a single convective reservoir along the Kok River fault, or are they distinct fault-block discharges? |
| `MAE_CHAN_GEOTHERMAL_AREA` | `CR_04` | Chiang Rai (Mae Chan) | Mae Chan active strike-slip fault | **High-Enthalpy System:** Standalone major manifestation (99.1 °C). Is it hydrogeologically isolated from Na Pong (`CR_09`)? |
| `PONG_PHU_FUANG_MAE_SUAI` | `CR_05` | Chiang Rai (Mae Suai) | Mae Suai granite batholith | Standalone granitic contact system. |
| `SOP_PONG_WIANG_PA_PAO` | `CR_06` | Chiang Rai (Wiang Pa Pao) | Wiang Pa Pao fault zone | Standalone granitic fault system. |
| `NA_PONG_NORTH_MAE_CHAN` | `CR_09` | Chiang Rai (North of Mae Chan) | Northern splay of Mae Chan fault | Standalone or structural splay of Mae Chan? |
| `HUAI_SAI_KHAO_PHAN` | `PR_07` | Chiang Rai / Phrae border | Local N-S normal fault | Standalone low-temp manifestation. |
| `SAN_KAMPHAENG` | `CM_01` | Chiang Mai (San Kamphaeng) | San Kamphaeng basin boundary fault | **Major Known System:** Verified deep convective circulation (100.5 °C). Distinct from Doi Saket. |
| `DOI_SAKET_PONG_KUM` | `CM_02` | Chiang Mai (Doi Saket) | Granitic intrusion boundary | Standalone system (~25 km north of San Kamphaeng). |
| `FANG` | `CM_03` | Chiang Mai (Fang Basin) | Fang Basin boundary normal fault | **Producing Geothermal Field:** Verified binary cycle plant (98.1 °C). Hydrogeologically independent. |
| `MAE_CHAN_FAULT_UNSPECIFIED` | `CM_16` | Chiang Mai / Chiang Rai | Text narrative description | **WITHHELD:** Lacks original coordinate measurement; unmappable as ground truth. |
| `BAN_PONG_NAM_RON` | `LPa_04` | Lampang | Wang Nua / Lampang fault corridor | Standalone system. |
| `WIANG_NONG_LOM` | `CR_WNL` | Chiang Rai | Wiang Nong Lom basin | Standalone warm marsh discharge (41 °C). |
| `MAE_JOK_PHRAE` | `PR_02` | Phrae | Wang Chin / Phrae basin fault | Standalone system (71 °C). |
| `SOUTH_CP_GEOTHERMAL_PROVINCE` | `CP1` | Chumphon | Ranong fault system | **PROVISIONAL:** Southern coordinate pending UTM Zone 47/48 resolution. |
| `SOUTH_RN_GEOTHERMAL_PROVINCE` | `RN1`..`RN6` (6 records) | Ranong | Ranong strike-slip fault corridor | **PROVISIONAL:** Multiple springs along Ranong corridor. Must be grouped as 1 system if retained. |
| `SOUTH_SR_GEOTHERMAL_PROVINCE` | `SR1`..`SR9` (9 records) | Surat Thani | Khlong Marui fault zone | **PROVISIONAL:** Clustering along Khlong Marui fault. Requires structural breakdown. |
| `SOUTH_PG_GEOTHERMAL_PROVINCE` | `PG1`..`PG3` (3 records) | Phang Nga (Kapong) | Kapong granitic intrusion | **PROVISIONAL:** Kapong manifestation group. |
| `SOUTH_KB_GEOTHERMAL_PROVINCE` | `KB1`..`KB5` (5 records) | Krabi | Klong Thom fault / carbonate karst | **PROVISIONAL:** Thermal waterfall / emerald pool cluster. |
| `SOUTH_TR_ST_PL_YL` | `TR1`, `ST1`, `PL1`..`PL4`, `YL1` | Trang, Satun, Phatthalung, Yala | Southern granitic belt | **PROVISIONAL:** Isolated southern springs. |

---

## 3. Explicit Adjudication Questions for External Experts

To transition the ML Gate condition `independent_system_group_review` from BLOCKED to APPROVED, a qualified external structural geologist and hydrogeologist must provide written answers to the following 5 questions:

1. **Question 1 (Kok River System Boundary):**  
   *Are `CR_01`, `CR_02`, `CR_03`, and `CR_08` manifestations of a single continuous hydrothermal reservoir along the Kok River fault corridor, or do geochemical isotope and temperature profiles indicate separate local convection cells?*
2. **Question 2 (Effective Independent Systems in Northern Pilot):**  
   *Based on structural segmentation of the Mae Chan, Mae Tha, and Fang fault systems, what is the authoritative count and spatial boundary of distinct independent hydrothermal systems among the 14 consistent northern manifestations? (Estimated: 6–10 systems).*
3. **Question 3 (Withheld Records Policy):**  
   *Do you confirm that `CR_02` (unresolvable >1 km UTM-DMS mismatch) and `CM_16` (narrative text without measured coordinates) must be strictly withheld from training splits to prevent label noise and model contamination?*
4. **Question 4 (Southern Thailand Provisional Status):**  
   *Given that the 31 southern records in Ngansom & Duerrast (2021) lack independent DMS validation and span the UTM Zone 47N/48N boundary, do you confirm that they must remain excluded from Northern Thailand pilot training?*
5. **Question 5 (Spatial Buffer Scale):**  
   *What is the recommended minimum spatial exclusion buffer (e.g. 10 km, 15 km, 20 km) required to eliminate hydrological and thermal autocorrelation between adjacent training and test manifestations in Northern Thailand?*

---

## 4. Formal Domain Expert Sign-Off Protocol

When formal review is conducted, the expert must complete and sign this audit schema:

```
+-------------------------------------------------------------------------------+
| GEO-THERM-AI ADJUDICATION SIGN-OFF SCHEMA (PHASE 2F)                          |
+-------------------------------------------------------------------------------+
| Reviewer Name: ______________________________________________________________ |
| Professional Title: _________________________________________________________ |
| Academic / Agency Affiliation: ______________________________________________ |
| Geological Specialization: [ ] Structural Geology  [ ] Hydrogeology           |
|                           [ ] Geothermal Exploration [ ] Geophysics          |
| Review Date (YYYY-MM-DD): ___________________________________________________ |
| Input Registry Version: tasks/phase_1c_.../geothermal_label_master_registry.csv|
| Input Registry SHA-256: 93d3bf9cd3c52ffbc207ca3a308c3e6ece1e067caf9c98fe08e85|
| Completed Adjudication Sheet: PHASE2F_LABEL_REVIEW.csv                         |
|                                                                               |
| Formal Statement:                                                             |
| "I have reviewed the 47 manifestation records, their coordinate validation    |
| statuses, and proposed system groupings. I confirm that the assigned          |
| independent system groupings represent distinct hydrothermal systems based    |
| on available structural and hydrochemical evidence, and that withheld        |
| records are properly excluded from model training."                           |
|                                                                               |
| Signature: _________________________________ Date: _________________________  |
+-------------------------------------------------------------------------------+
```

*Status as of Phase 2F:* **AWAITING EXPERT CONSULTATION — NO FAKE SIGNATURES OR APPROVALS MANUFACTURED.**
