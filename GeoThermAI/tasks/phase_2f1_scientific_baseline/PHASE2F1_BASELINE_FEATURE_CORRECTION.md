# Scientific Baseline Feature Correction — Phase 2F.1
**GeoThermAI Research Engineering Audit**  
*Date: 28 October 2026 | Focus: Discrepancy Resolution & Feature Schema Provenance*

---

## 1. The Discrepancy Identified in Phase 2F

In the initial Phase 2F implementation report and prototype sandbox, the following five features were drafted under the label of Mordensky et al. (2023):
1. `temp_3km_c` (Modeled temperature at 3 km depth, °C)
2. `fault_density_km_km2` (Fault trace length density, km/km²)
3. `slip_dilation_tendency` (Normalized tensor dilation/slip tendency, dimensionless)
4. `bouguer_gravity_mgal` (Complete Bouguer gravity anomaly, mGal)
5. `magnetic_anomaly_nt` (Total field magnetic anomaly, nT)

### Scientific Finding:
**These five features do NOT represent the feature set of Mordensky et al. (2023).**

---

## 2. Primary Source Analysis: Mordensky et al. (2023)

In the actual 2023 baseline publication:
> Mordensky, S. P., Lipor, J. J., DeAngelo, J., Burns, E. R., & Lindsey, C. R. (2023).  
> *When less is more: How increasing the complexity of machine learning strategies for geothermal energy assessments may not lead toward better estimates.*  
> *Geothermics*, 110, 102662. DOI: [10.1016/j.geothermics.2023.102662](https://doi.org/10.1016/j.geothermics.2023.102662)

Section 2.1 (*Data Compilation and Feature Selection*) explicitly selects the **five fundamental evidence layers** originally used in the 2008 USGS National Geothermal Resource Assessment (Williams et al., 2008):

| Canonical Variable Name | Feature Family in Mordensky et al. (2023) | Physical Unit | Geological Meaning |
|---|---|---|---|
| `heat_flow_mw_m2` | **Heat Flow** | $\text{mW/m}^2$ | Regional thermal energy flux |
| `dist_quaternary_fault_km` | **Distance to Quaternary Faults** | $\text{km}$ | Permeability & fluid pathway proximity |
| `dist_quaternary_magma_km` | **Distance to Quaternary Magma Body** | $\text{km}$ | Proximity to shallow volcanic/magmatic heat sources |
| `seismic_event_density_per_km2`| **Seismic Event Density** | $\text{events/km}^2$| Ongoing brittle deformation & active fracture maintenance |
| `max_horizontal_stress_mpa` | **Maximum Horizontal Stress** | $\text{MPa}$ | Crustal stress orientation & magnitude controlling dilation |

---

## 3. Provenance of the Phase 2F Features

Where did the Phase 2F features come from?
- `temp_3km_c`, `fault_density_km_km2`, `slip_dilation_tendency`, `bouguer_gravity_mgal`, `magnetic_anomaly_nt` originate from **Geothermal Play Fairway Analysis (PFA)** methodologies (DeAngelo et al., 2024; Faulds et al., 2018) and the subsequent 16-feature Great Basin dataset (Mordensky et al., 2025, *Geothermics* 125, 103450).
- In PFA, gravity and magnetic data are used to image concealed basement structural blocks, while 3D thermal conduction models predict temperatures at 3 km depth.

---

## 4. Resolution & Dual Profile Architecture

To maintain rigorous scientific standards without discarding prior implementation value, GeoThermAI Phase 2F.1 implements a **Dual Profile Architecture** in [`GeoThermAI/src/geothermai/usgs_replication.py`](file:///Users/knight/Development/CoreX/GeoThermAI/src/geothermai/usgs_replication.py):

### Profile A: `MORDENSKY_2023_BASELINE_PROFILE` (Canonical Replication)
- **Reference:** Mordensky et al. (2023), *Geothermics* 110, 102662.
- **Data Release:** DOI [10.5066/P9V1Q9XM](https://doi.org/10.5066/P9V1Q9XM).
- **Features (5):**
  - `heat_flow_mw_m2`
  - `dist_quaternary_fault_km`
  - `dist_quaternary_magma_km`
  - `seismic_event_density_per_km2`
  - `max_horizontal_stress_mpa`
- **Target:** 278 known positive cells within 725,442 total $2\text{ km} \times 2\text{ km}$ cells.

### Profile B: `USGS_PFA_DEANGELO_PROFILE` (Preserved Alternative)
- **Reference:** DeAngelo et al. (2024), *Geothermics* 115, 102882 & Mordensky et al. (2025), *Geothermics* 125, 103450.
- **Features (5):**
  - `temp_3km_c`
  - `fault_density_km_km2`
  - `slip_dilation_tendency`
  - `bouguer_gravity_mgal`
  - `magnetic_anomaly_nt`

### Resulting Safety Guarantees:
- The two studies are **never conflated** under a single profile identifier.
- Automated tests verify that both profiles enforce their exact distinct schemas and prevent cross-contamination.
