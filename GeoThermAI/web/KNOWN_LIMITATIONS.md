# GeoThermAI Web — Known Limitations

Date: 2026-10-24

## Scientific and data limits

- Predictive geothermal potential is not validated or enabled.
- The 47 registry rows are published surface manifestations, not confirmed independent systems or commercial resources.
- Southern coordinates use an inferred working CRS and require explicit display opt-in. The opt-in persists across in-app routes and resets safely on a full reload.
- `CR_02` has an unresolved coordinate disagreement; `CM_16` lacks an independent DMS comparator. Neither is mapped as authoritative.
- The southern source contains a 31-row table versus 30-sample prose discrepancy.
- Validation clusters are provisional grouping units and have not been domain-verified as independent geothermal systems.

## GIS limits

- Active-fault geometry exists locally and is valid, but rendering, export and distance analysis remain disabled because reuse conditions conflict.
- Geological structures still returned attributes without usable geometry after explicit `returnGeometry`, `outSR`, offset and ObjectID query attempts.
- DMR rock-unit geometry is northern-only, nominally 1:250,000, and lacks an obtained lithologic legend. It is descriptive context only.
- The heat-flow workbook has not completed a Thailand-specific clip and provenance review.
- No approved satellite or terrain basemap source is configured.
- No geothermal-potential raster is created or displayed.
- Coverage overlays show only the exact bounds of five local HGT filenames. Four Phase 1C tiles have recorded raster QA; the additional Phase 1 tile is a file-presence footprint only.
- Coordinate-review geometry is non-authoritative: CR_02 shows the unresolved separation between its working UTM transform and DMS comparator; CM_16 shows only its working UTM representation because no DMS comparator exists.

## Product and performance limits

- The application is local and has no authentication, notification service, or backend database. The notification affordance is visibly nonfunctional.
- The OSM basemap requires internet connectivity; evidence data remains local.
- Geology is preprocessed to a 4.59 MB lazy-fetched GeoJSON and no longer ships as a 7.3 MB JavaScript chunk. The public geometry is simplified for display; exact deviation is disclosed in the manifest.
- Current observation-source redistribution permission was not assessed, so raw filtered/detail exports are disabled.
- Current observation-source exports remain disabled. If a future source records explicit permission, selected/filtered JSON export includes provenance, coordinate uncertainty, missing-evidence fields and scientific boundaries; the app does not grant additional rights.
- The production app shell is 393.79 kB minified; workspace routes lazy-load a 1,081.54 kB EvidenceMap/MapLibre chunk. Vite still emits a warning for the map chunk.

## Security validation limit

- `npm audit` reports zero known package vulnerabilities.
- HawkScan DAST is not completed because the required HawkScan CLI v6.0.0+ is absent and no API key/config is available. The app must not be described as DAST-certified until that scan and its quality gate execute successfully.
