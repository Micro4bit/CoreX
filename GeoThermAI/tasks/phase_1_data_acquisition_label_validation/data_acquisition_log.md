# Data Acquisition Log

Run date: 2026-10-23  
All times/dates in this log refer to the current audit run. Raw downloads were retained without destructive modification in this task folder.

| Source / action | URL or local result | Outcome | File opened / inspection performed |
|---|---|---|---|
| DMR rock-unit service metadata | <https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/ROCK_UNIT_250K/MapServer?f=pjson> | Accessed | Service reports Map, Query, Data; EPSG:32647; one polygon layer; max record count 2,000. |
| DMR rock-unit count and sample | MapServer layer 0 `/query` | Downloaded sample | Count response = 7,093. Five-feature Esri JSON sample opened; attributes and polygon rings inspected. GeoJSON sample had null geometry. |
| DMR structure service metadata | <https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/GEOL_STR_250K/MapServer?f=pjson> | Accessed | EPSG:32647; one polyline layer; max record count 2,000. |
| DMR structure count and sample | MapServer layer 0 `/query` | Accessed | Count response = 12,741. Five-feature attribute sample inspected; geometry was absent. WFS GetCapabilities attempt returned a server error page. |
| DMR active-fault catalog | <https://data.go.th/api/3/action/package_show?id=activefault> | Accessed | Resource URL, metadata, license label, and resource-use conditions captured in `activefault_catalog_metadata.json`. |
| DMR active-fault ZIP | <https://data.go.th/dataset/2f32b01e-6ae7-4b66-aa2c-730a87051793/resource/27e1c1df-6e87-4303-87ea-fcd9a941b8c0/download/zone_activefault_20230419_091427.zip> | Downloaded and opened | ZIP contains SHP/SHX/DBF/PRJ/CPG. Parsed DBF header: 630 records; parsed SHP header: polyline shape type; inspected first record; PRJ reads WGS 84 / UTM zone 47N. |
| DMR hot-spring PDF | <https://www.dmr.go.th/wp-content/uploads/2022/09/thailand11.pdf> | Downloaded and opened | One-page, 492,484-byte PDF. Metadata says created 2007. Rendered page visually inspected: national symbol map and three temperature classes, no point register. |
| Northern hot-spring paper | <https://publications.mygeoenergynow.org/grc/1033597.pdf> | Downloaded and opened | Ten-page PDF. Text extraction and page-2 visual rendering inspected Table 1. Transcribed 16 rows into `northern_hot_spring_label_registry_wood2014.csv`; CSV parsing confirmed 16 unique codes. |
| IHFC 2024 heat-flow workbook | <https://www.ihfc-iugg.org/user/downloads/data/R2024/IHFC_2024_GHFDB.xlsx> | Downloaded and opened | 30,728,338-byte XLSX. Workbook opened read-only with one sheet. Data headers occur at row 6; data rows = 91,181. A rectangular Thailand-window audit was run and logged in the feasibility report. |
| SRTM-derived HGT tile | <https://s3.amazonaws.com/elevation-tiles-prod/skadi/N19/N19E098.hgt.gz> | Downloaded and opened | 16,104,565-byte GZ. Decompressed to 3,601 × 3,601 signed 16-bit samples; min/max 145/2,177 m; zero `-32768` NoData samples. |
| Landsat L2 ST collection | <https://landsatlook.usgs.gov/stac-server/collections/landsat-c2l2-st> | Metadata accessed; data acquisition failed | STAC query for a northern-Thailand bounding box returned two item records. Direct MTL JSON and ST_B10 requests returned HTML, not product files. No raster was opened. |
| Kapong Mendeley data | <https://data.mendeley.com/datasets/37ng92rj85/1> | Metadata only | Landing-page metadata was located via source search. Attempted public metadata endpoint returned HTML, so no raw supplementary file was downloaded or opened. |
| Southern hot-spring article mirror | <https://www.thaiscience.info/Journals/Article/ENVA/10994463.pdf> | Inaccessible in this run | Download request returned HTML rather than a PDF. No table count or coordinates were extracted. |

## Raw-file integrity notes

- Raw data were kept separate from the derived northern label registry.
- Some failed requests intentionally remain as HTML response artifacts in the raw acquisition folders so the access barrier can be reproduced; they must not be parsed as GIS/JSON data.
- No raw data, label, or geometry was overwritten.

## Not performed

- No national bulk export of the DMR rock-unit service.
- No successful download of DMR structural geometry.
- No country-boundary clip of IHFC data.
- No Landsat surface-temperature raster processing.
- No satellite, DEM, geology, or label resampling/reprojection.
- No model fit, feature engineering, or model-performance calculation.
