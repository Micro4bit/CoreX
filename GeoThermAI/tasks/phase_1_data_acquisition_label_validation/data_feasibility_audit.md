# GeoThermAI Data Feasibility Audit 02

Date accessed: 2026-10-23  
Scope: Thailand geothermal prospectivity research, Phase 1. This is an acquisition and label audit, not a model experiment.

## Decision

**CONDITIONAL GO** for a tightly bounded northern-Thailand data-engineering pilot and for label curation. There is now verified access to usable geology, an active-fault vector, elevation data, heat-flow observations, and one literature-derived northern hot-spring registry. There is **NO-GO at this time for a claim of validated Thailand-wide or commercial-geothermal predictive AI**.

The critical gate remains independent labels: the verified northern registry has only 16 point records from one publication, spatially clustered systems, and represents surface hot-spring manifestations rather than proven commercial reservoirs. A country-wide authoritative point inventory, a resolved coordinate protocol, and a defensible held-out geography have not yet been established.

## Materials actually accessed

| Candidate | Actual result | Evidence status | Key finding |
|---|---|---|---|
| DMR 1:250,000 rock units | ArcGIS REST service, layer metadata, count query, and five-feature Esri JSON sample | VERIFIED_DOWNLOAD | 7,093 features reported; polygon geometry and EPSG:32647 were returned in Esri JSON. |
| DMR 1:250,000 structures | REST service, metadata, count query, and five-feature attribute sample | VERIFIED_ACCESS | 12,741 features reported, but the sampled query contained no geometry and WFS errored. |
| DMR active-fault zones | ZIP SHP/DBF/PRJ download opened | VERIFIED_DOWNLOAD | 630 polyline records in EPSG:32647; real candidate structural predictor, subject to reuse review. |
| DMR hot-spring map | One-page PDF downloaded and visually inspected | VERIFIED_DOWNLOAD | Temperature-class map only. No point IDs or authoritative coordinate table. |
| Wood & Singharajwarapan (2014) | Ten-page PDF downloaded; Table 1 text-extracted and visually checked | VERIFIED_DOWNLOAD | 16 northern hot-spring records; 15 DMS coordinate pairs, all 16 UTM pairs, 14 reported surface temperatures. |
| IHFC 2024 heat-flow database | XLSX 30.7 MB downloaded and opened | VERIFIED_DOWNLOAD | 91,181 data rows; heat-flow measurements are supplementary evidence, not occurrence labels. |
| SRTM-derived N19E098 | HGT GZ downloaded and decompressed/inspected | VERIFIED_DOWNLOAD | 3,601 × 3,601 one-arc-second samples, no NoData values, elevation 145–2,177 m. |
| Landsat C2 L2 ST | STAC collection query and item metadata accessed | METADATA_ONLY | Direct MTL and raster requests returned HTML, not valid assets. |
| Kapong supplementary geophysics | Public landing-page metadata discovered | METADATA_ONLY | Potential southern case-study evidence; raw files not obtained in this run. |

Full source metadata, URLs, CRS, license notes, formats, and limitations are in `dataset_inventory.csv`.

## Actual inspection results

### Geology and structures

- The rock-unit service declares EPSG:32647 (WGS 84 / UTM zone 47N), a 1:250,000 layer, `OBJECTID`, `TEXT_SYM`, `YEAR_COMPI`, mapped area/length fields, and polygon geometry. Its count endpoint returned 7,093. The Esri JSON sample opened with polygon rings. The service's GeoJSON response had null geometries, therefore GeoJSON must not be used without a separate reproduction test.
- The geological-structure service declares the same CRS, a polyline layer, and fields for type/group, direction, plunge direction and compilation year. Its count endpoint returned 12,741. The sample had meaningful types such as Fault, Fracture and folds, but lacked geometry in the response. This is an unresolved acquisition defect, not a usable distance-to-structure feature.
- The active-fault ZIP is intact: `.shp`, `.shx`, `.dbf`, `.prj`, and UTF-8 `.cpg` were present. The PRJ declares WGS 84 / UTM zone 47N. The DBF has 630 records and fields including fault name/type, strike, dip, `LENGTH_KM`, `MCE`, `SLIP_RATE`, recurrence and dates. It is a mapped active-fault layer, not a full fault/fracture inventory.
- The active-fault catalog labels the license “Creative Commons Attributions” while the resource condition prohibits commercial use and legal citation. Treat reuse terms as **UNRESOLVED** until DMR clarifies the controlling terms.

### Raster/supporting data

- `N19E098.hgt.gz` decompressed to 25,934,402 bytes = 12,967,201 signed 16-bit samples = 3,601². Under the standard HGT tile convention, it spans 98–99°E and 19–20°N at one arc-second. It contains zero `-32768` NoData samples, with observed elevation 145–2,177 m. HGT carries no embedded CRS metadata; assign its convention-derived geographic reference only after provenance review.
- The IHFC workbook contains one sheet and 91,181 data rows after six header/metadata rows. The actual field row includes `q`, `q_uncertainty`, `name`, `lat_NS`, `long_EW`, `elevation`, `environment`, `qc`, references, and thermal-conductivity metadata. A broad 5–21°N / 97–106°E rectangular filter yielded 460 rows, 322 distinct coordinate pairs, 104 duplicate-coordinate groups, and 291 offshore rows. It must be clipped to a Thailand boundary and reviewed by source/reference; it is not a label table.
- An anonymous USGS STAC request returned Landsat C2 L2 ST item metadata and asset URLs. The subsequent direct metadata and range-read raster requests returned HTML instead of product files. No Landsat raster has been inspected, and its status must remain METADATA_ONLY.

## Reproducible provenance and transformations

Original downloads are retained, unmodified, in this task folder. The only derived file is `northern_hot_spring_label_registry_wood2014.csv`, a 16-row transcription of Table 1 in Wood & Singharajwarapan (2014). It retains source UTM and DMS strings rather than silently transforming coordinates. Before use in a GIS, confirm the UTM zone/hemisphere from the source/author or an independent authoritative reference, then generate a separate transformed file with the exact transformation recorded.

Do not derive a predictor from the same hot-spring locations that define the positive class. In particular, distance-to-known-hot-spring is prohibited in a model that is evaluated against those locations.

## Geographic validation feasibility

The evidence supports a **site-grouped northern pilot feasibility test**, not a broad generalization claim.

1. Treat the 16 table rows as manifestations, not automatically 16 independent systems. Group records by hydrothermal system after source review.
2. Build folds from spatial blocks and/or whole system groups before sampling, feature transforms, tuning, or thresholding. Block size is **TBD** and must be chosen from observed clustering and geological scale, with sensitivity analysis rather than a convenient fixed value.
3. Do not call unrecorded locations negatives. Use background or positive-unlabeled sampling and report sensitivity to background definition/exclusion buffers.
4. The current southern evidence is not an independently curated held-out label registry. A north-to-south transfer result is unsupported until an independent southern occurrence table is acquired and audited.
5. With very few independent groups, report fold-level dispersion and maps of training/held-out groups. Avoid a single random split and avoid probability/calibration claims.

## Sources

- DMR rock units REST: <https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/ROCK_UNIT_250K/MapServer>
- DMR geological structures REST: <https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/GEOL_STR_250K/MapServer>
- DMR active-fault download: <https://data.go.th/dataset/2f32b01e-6ae7-4b66-aa2c-730a87051793/resource/27e1c1df-6e87-4303-87ea-fcd9a941b8c0/download/zone_activefault_20230419_091427.zip>
- DMR hot-spring map: <https://www.dmr.go.th/น้ำพุร้อน-แผนที่แหล่งน้ำพุร้อนในประเทศไทย/>
- Wood, S.H. & Singharajwarapan, F.S. (2014), *Geothermal Systems of Northern Thailand and Their Association With Faults Active During the Quaternary*, GRC Transactions 38, 607–615: <https://publications.mygeoenergynow.org/grc/1033597.pdf>
- IHFC 2024 Global Heat Flow Database: <https://www.ihfc-iugg.org/user/downloads/data/R2024/IHFC_2024_GHFDB.xlsx>, DOI <https://doi.org/10.5880/fidgeo.2024.014>
- Landsat ST STAC: <https://landsatlook.usgs.gov/stac-server/collections/landsat-c2l2-st>

## Limitations and next action

No model was trained. No national label inventory, country-boundary clip, full geological export, Landsat raster, or independent south-region label set was acquired. The immediate next action is a reproducible label-collation protocol: obtain DMR's underlying inventory or written data permission, validate the 16 northern coordinates against original sources, merge only records with provenance/measurement dates, then re-run the site-group and spatial-block feasibility gate.
