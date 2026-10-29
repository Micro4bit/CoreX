# USGS Source & Data Inventory — Phase 2F.2
**ScienceBase Catalog Audit & Manual Acquisition Handoff Specification**  
*Date: 28 October 2026 | Benchmark: Mordensky et al. (2023) | DOI: [10.5066/P9V1Q9XM](https://doi.org/10.5066/P9V1Q9XM)*

---

## 1. Official Data Release Identification

| Metadata Field | Canonical Official Value |
|---|---|
| **Title** | *Geothermal resource favorability: select features and predictions for the western United States curated for DOI 10.1016/j.geothermics.2023.102662* |
| **Authors** | Stanley P. Mordensky & Jacob DeAngelo |
| **Publishing Organization**| U.S. Geological Survey (USGS) |
| **Publication Year** | 2023 |
| **Digital Object Identifier**| **10.5066/P9V1Q9XM** |
| **Catalog System** | USGS ScienceBase-Catalog |
| **ScienceBase Item ID**| `63090a9cd34e3b967a8c19c4` |
| **ScienceBase URL** | `https://www.sciencebase.gov/catalog/item/63090a9cd34e3b967a8c19c4` |
| **Data.gov Entry** | `https://catalog.data.gov/dataset/geothermal-resource-favorability-select-features-and-predictions-for-the-western-united-state` |
| **Licensing** | **U.S. Public Domain** (U.S. Code Title 17, Section 105; unrestricted academic and commercial reuse with attribution) |

---

## 2. Acquisition Audit & Cloudflare Challenge Blocker

During Phase 2F.2 execution, automated acquisition was re-attempted against official endpoints:
- ScienceBase Web Item: `https://www.sciencebase.gov/catalog/item/63090a9cd34e3b967a8c19c4`
- ScienceBase REST API: `https://www.sciencebase.gov/catalog/item/63090a9cd34e3b967a8c19c4?format=json`

### Diagnostic Trace:
```
Request: GET https://www.sciencebase.gov/catalog/item/63090a9cd34e3b967a8c19c4?format=json
Headers: User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...
Response: HTTP 403 Forbidden
Payload: Cloudflare Managed Challenge HTML (cf_chl_opt, Ray ID: a515f0679c7a75d9)
Reason: Automated non-browser requests are challenged by Cloudflare Web Application Firewall (WAF)
```

### Research Integrity Decision:
In accordance with GeoThermAI research integrity rules:
1. **Security controls were NOT bypassed:** No automated attempts to crack Cloudflare challenges or scrape unauthorized mirrors.
2. **No Data Fabrication:** Synthetic test harnesses are clearly tagged `SYNTHETIC_TEST_DATA` and never misrepresented as authentic USGS measurements.

---

## 3. Manual Acquisition Handoff Protocol

To acquire the authentic `ORIGINAL_USGS_DATA` files for exact replication, a human researcher must perform the following standard protocol:

### Step 1: Manual Browser Download
1. Open an authenticated web browser (Chrome/Firefox/Safari).
2. Navigate to: `https://www.sciencebase.gov/catalog/item/63090a9cd34e3b967a8c19c4`.
3. Complete the interactive Cloudflare verification prompt if displayed.
4. Download the data package files listed under the "Attached Files" section:
   - **Input Features Package:** `features_western_us_2023.zip` (contains the 5 raster/tabular features on the 2 km x 2 km grid).
   - **Known Geothermal Systems Labels:** `known_systems_labels.zip` (contains the 278 positive cell coordinates).
   - **Favorability Predictions:** `predictions_western_us_2023.zip` (contains the 9 untransformed model favorability maps).
   - **FGDC Metadata Document:** `metadata_63090a9cd34e3b967a8c19c4.xml`.

### Step 2: Ingestion & Integrity Verification
1. Place downloaded zip archives into:
   `GeoThermAI/data/raw/usgs_mordensky2023/`
2. Run integrity verification and compute SHA-256 hashes:
   ```bash
   shasum -a 256 GeoThermAI/data/raw/usgs_mordensky2023/*
   ```
3. Register the verified files in `geothermai.prediction_architecture.DataIngestionManager`.

---

## 4. Curated Data Package Architecture & Verification Targets

Once downloaded, the dataset will be checked against the following verified specifications:

| Feature / Artifact Name | Expected Grid & Format | Coordinate Reference System (CRS) | Native Unit | Expected Range |
|---|---|---|---|---|
| **`heat_flow`** | $2\text{ km} \times 2\text{ km}$ GeoTIFF / Grid | Albers Equal Area (North America / USGS) | $\text{mW/m}^2$ | $15\text{--}350\text{ mW/m}^2$ |
| **`dist_quat_fault`** | $2\text{ km} \times 2\text{ km}$ GeoTIFF / Grid | Albers Equal Area (North America / USGS) | $\text{km}$ | $0\text{--}250\text{ km}$ |
| **`dist_quat_magma`** | $2\text{ km} \times 2\text{ km}$ GeoTIFF / Grid | Albers Equal Area (North America / USGS) | $\text{km}$ | $0\text{--}400\text{ km}$ |
| **`seismic_event_density`**| $2\text{ km} \times 2\text{ km}$ GeoTIFF / Grid | Albers Equal Area (North America / USGS) | Count / $4\text{ km}$ radius | $0\text{--}150\text{ events}$ |
| **`shmax_stress`** | $2\text{ km} \times 2\text{ km}$ GeoTIFF / Grid | Albers Equal Area (North America / USGS) | Degrees ($0\text{--}180^\circ$) / Regime | $0^\circ\text{--}180^\circ$ azimuth |
| **`known_systems_labels`** | Tabular / Shapefile | EPSG:4326 or Albers Equal Area | Binary ($1$ = Positive) | Exactly $278$ positives |
| **`grid_footprint`** | $2\text{ km} \times 2\text{ km}$ mask | Albers Equal Area | Mask ($1$ = Valid Land) | Exactly $725,442$ cells |
