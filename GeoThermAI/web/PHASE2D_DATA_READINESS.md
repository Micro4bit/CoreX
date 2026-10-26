# Phase 2D data readiness

Date: 2026-10-26

| Dataset | Physical evidence opened | Verified state | Display | Analysis/export |
|---|---|---|---|---|
| Published manifestations | 47-row master registry and source provenance | 14 internally consistent map points; 31 southern provisional; CR_02/CM_16 withheld | Opt-in rules preserved | Evidence browsing only; not independent systems/negatives |
| DMR rock units | 7,743,929-byte EsriJSON and layer metadata | 1,266 polygons; EPSG:32647; 42/42 present symbols matched | Contextual northern layer | Geometry export disabled; predictor use conditional |
| DMR structures | Live ArcGIS metadata/query responses | Attributes returned; geometry count 0 | Disabled | Disabled |
| DMR active faults | Shapefile, XML and catalog metadata | 630 valid lines in EPSG:32647 | Disabled | Disabled pending written permission |
| SRTM | Five physical HGT gzip files | All 3,601², no nodata, exact shared seams; five GeoTIFFs | Footprints only | Terrain processing only within covered tiles |
| IHFC 2024 | Actual OOXML workbook | 91,182 total; 154 Thailand rows/111 coordinates | Opt-in observed points | CC BY display/export with attribution; no interpolation/ML |
| Natural Earth boundary | Official 10m Admin-0 archive | One valid Thailand MultiPolygon, EPSG:4326 | Processing support | Public domain |
| Landsat C2 L2 ST | Two STAC items and eight asset responses | Login HTML, zero TIFFs | Disabled | Disabled |

The machine-readable feature inventory is `tasks/phase_2d_data_readiness/feature_catalog.csv`. Dataset-specific details are in the Phase 2D task folder. Unknown classifications and repeated measurements are retained rather than imputed or silently merged.

Coverage is not geothermal potential. Land-surface temperature is not reservoir temperature. Unobserved locations are not true negatives.

