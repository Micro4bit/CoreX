# GeoThermAI Phase 2C — GIS Layer Provenance

Date: 2026-10-24

This registry describes evidence availability, not geothermal potential. `display eligible` means eligible in this local research workspace only; it does not grant redistribution rights.

| Layer | State | Publisher / source | Local artifact | CRS / scale / resolution | Inspection and transformation | Permission | Display / export |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DMR rock units, northern extract | `AVAILABLE_VERIFIED` | Department of Mineral Resources Thailand; `https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/ROCK_UNIT_250K/MapServer/0` | `../tasks/phase_1c_label_expansion_gis_foundation/rock_unit_250k_northern_esrijson.json` | EPSG:32647; nominal 1:250,000; 1,266 polygons | Source opened and hashed. Build preprocessing transforms to EPSG:4326. A 25 m topology-preserving simplification is used for display; full transformed geometry is retained under `../derived/phase2c/`. Exact metrics are in `public/data/dmr-rock-units-north.manifest.json`. | Service metadata contained no copyright statement; reuse terms remain unverified. | Local contextual display: yes. Geometry export: no. No lithology legend or site geology claim. |
| DMR geological structures | `UNAVAILABLE_GEOMETRY` | DMR ArcGIS REST; `https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/GEOL_STR_250K/MapServer/0` | `../tasks/phase_1c_label_expansion_gis_foundation/geol_str_250k_northern_esrijson.json`; audit `../derived/phase2c/dmr-structure-query-audit.json` | Service declares EPSG:32647 polyline | Reproducible live audit on 2026-10-24: `returnIdsOnly=true` returned 12,741 ObjectIDs. Offset queries with `returnGeometry=true` and `outSR=4326`/`32647` each returned 25 attribute features and zero geometry; the tested ObjectID batch returned zero features; `f=esriJSON` returned HTTP 400. | Service/catalog metadata is not treated as blanket permission. | Display/export/distance: no. |
| DMR active-fault zones | `RESTRICTED_REUSE` | DMR via data.go.th; `https://data.go.th/dataset/activefault` | `../tasks/phase_1_data_acquisition_label_validation/N_ZONE_ACTIVEFAULT_20230419_091427.shp` and sidecars | EPSG:32647; 630 line records | Opened with GeoPandas: 616 LineString + 14 MultiLineString, all 630 valid and non-empty. Bounds: 345954.409, 810291.167, 753132.522, 2254853.547 m. | Catalog says CC Attribution while resource conditions prohibit commercial use and legal citation. DMR clarification is required before rendering, analysis, or export. | Display/export/distance: no. |
| SRTM HGT northern tiles | `QUALITY_PENDING` | AWS Terrain Tiles / SRTM distribution; `https://s3.amazonaws.com/elevation-tiles-prod/skadi/` | Four Phase 1C tiles `N17E099`–`N20E099`; Phase 1 tile `N19E098` | Filename-derived WGS84 tile convention; 3,601 × 3,601 at 1 arc-second | Five exact one-degree file-availability footprints are available. The four Phase 1C tiles were previously decompressed and had no `-32768`; the Phase 1 tile has file-presence evidence only. Raster display and terrain analysis remain disabled. | Reuse terms were not verified in this run. | File-coverage footprints: yes. Terrain/hillshade/export: no. |
| IHFC 2024 heat flow | `METADATA_ONLY` | International Heat Flow Commission; DOI `10.5880/fidgeo.2024.014` | `../tasks/phase_1_data_acquisition_label_validation/IHFC_2024_GHFDB.xlsx` | Geographic latitude/longitude fields; Phase 1 profile reports 91,181 data rows; CRS not declared in workbook | The real 30,728,338-byte XLSX was opened as an OOXML archive. Sheet `data release2024` declares `A1:BV91188`; row 6 contains `q`, `q_uncertainty`, `lat_NS`, `long_EW`, `elevation`, `environment`, `qc`, `qc_uncertainty` and method/depth fields. Sample rows explicitly include offshore environment values. The prior rectangular filter mixed offshore, duplicates, and neighboring-country records. No validated Thailand boundary is available. | Terms not re-audited. | Metadata only. No national interpolation or point layer. |
| Kapong VES/ERT | `METADATA_ONLY` | Mendeley Data / Duerrast Pirarai Ngansom | `../tasks/phase_1c_label_expansion_gis_foundation/kapong_geophysical_appendix.pdf` | Visual UTM maps; no machine-readable station table | PDF/hash were previously verified; no points were digitized. | CC BY 4.0 in downloaded metadata. | Provenance only. |
| Landsat Collection 2 L2 Surface Temperature | `NOT_LOADED` | USGS Landsat STAC metadata | Only an MTL response artifact exists; no ST raster | No usable raster | Prior direct asset requests returned HTML rather than product data. Cloud, QA and data-gap masks were therefore not run. | Not evaluated for a local raster because no raster was obtained. | Disabled. |

## Typed registry metadata used by the UI

`src/gisRegistry.ts` augments the immutable Phase 1C CSV rows without mutating them. Every registered candidate carries the following explicit runtime fields: `acquisitionDate`, `sourceCrs`, `scaleOrResolution`, `coverage`, `transformationMethod`, `geometryCount`, `sourceRecordCount`, `state`, `displayEligible`, `coverageDisplayEligible`, `exportEligible`, and `uiEligibility`.

| Layer | Acquisition record | Loaded/derived geometry count | Transformation / UI eligibility |
| --- | --- | ---: | --- |
| DMR rock units | 2026-10-23 service inspection; exact acquisition timestamp was not separately recorded | 1,266 | Build-time pyproj 32647→4326 plus 25 m Shapely simplification; `DISPLAY_CONTEXT_ONLY` |
| DMR structures | 2026-10-23 service inspection | 0 usable geometries | No transformation; `DISABLED` |
| DMR active faults | Acquisition date not recorded; catalog last updated 2016-08-01 | 630 | Source retained in EPSG:32647; `DISABLED` |
| SRTM HGT | Four Phase 1C tiles dated 2026-10-23; Phase 1 tile date not separately recorded | 5 tile footprints | Filename-bound footprints only; `COVERAGE_METADATA_ONLY` |
| IHFC 2024 | Local artifact timestamp 2026-10-23; publisher download timestamp not separately recorded | 0; 91,181 source rows remain metadata-only | No validated Thailand clip; `DISABLED` |
| Kapong VES/ERT | Acquisition date not separately recorded; dataset published 2019-11-20 | 0; 16 source stations/sections are not machine-readable coordinates | No coordinate transformation; `DISABLED` |
| Landsat ST | No raster acquired | 0 | No processing; `DISABLED` |

Unknown acquisition timestamps are kept explicit rather than inferred.

## Permission blocker to send to DMR

Please clarify whether the active-fault shapefile and the DMR rock-unit/structure services may be reproduced in a local and/or public research visualization, exported as derived geometry, and used for noncommercial distance/intersection analysis. The catalog's CC Attribution label conflicts with its explicit noncommercial and no-legal-citation conditions; until clarified, GeoThermAI keeps active-fault rendering, distance calculations, and geometry export disabled.
