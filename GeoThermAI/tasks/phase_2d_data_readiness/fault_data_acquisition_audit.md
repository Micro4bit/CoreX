# DMR structures and active-fault acquisition audit — 2026-10-26

## Geological-structure service

Endpoint: `https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/GEOL_STR_250K/MapServer/0/query`.

`scripts/audit_dmr_structure.py` first inspected layer metadata and then issued non-identical request variants. Metadata returned HTTP 200, polygon geometry type, a 2,000-record limit, and supported formats `JSON, geoJSON, PBF`. Offset JSON queries in EPSG:4326 and EPSG:32647 each returned 25 feature attribute records and **zero geometries**. Offset GeoJSON also returned 25 features and **zero geometries**. `returnIdsOnly` returned object IDs, but ObjectID-batched JSON/GeoJSON returned zero features; `f=esriJSON` returned HTTP 400 “Output format not supported.” Every geometry query used `returnGeometry=true`.

Machine evidence: `derived/dmr-structure-query-audit.json` (Phase 2C) and `tasks/phase_2d_data_readiness/derived/dmr-structure-query-audit.json` (Phase 2D). No substitute lines were drawn. Status: `UNAVAILABLE_GEOMETRY`.

## Active-fault file

The local shapefile has 630 valid features in EPSG:32647: 616 LineStrings and 14 MultiLineStrings. It is technically suitable for distance-to-mapped-feature calculation. The data.go.th catalog simultaneously states “Creative Commons Attributions” and restrictive conditions: no legal citation, no commercial use, and a DMR liability disclaimer. A public download is therefore not treated as blanket redistribution/derivative-analysis permission.

Status: `RESTRICTED_REUSE`; public rendering, export and mapped-fault distance remain disabled pending written clarification.

