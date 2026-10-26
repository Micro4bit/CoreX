# GeoThermAI Phase 2C — GIS Analysis Methods

Date: 2026-10-24

## Scientific boundary

All outputs are descriptive geospatial measurements or evidence-availability statements. They are not geothermal probability, prospectivity, drilling success, reservoir temperature, MW, LCOE, confidence, or cost-saving estimates. Absence of mapped evidence is not a true negative.

## Location inspection

- Input: user map click in WGS84 longitude/latitude (`EPSG:4326`).
- Output: clicked coordinate and intersections with layers that are currently display-eligible, including publisher/source, URL, license, scale/resolution and a layer-specific warning.
- Current intersection layers: simplified DMR northern rock-unit polygons, SRTM file-availability footprints when enabled, and non-authoritative coordinate-review geometry when enabled.
- Method: MapLibre rendered-feature intersection at the clicked screen point.
- Limitation: nominal source scale is 1:250,000; the UI exposes source symbol/year only and does not infer lithology or site geology. A rendered intersection is view/scale dependent and is contextual.

## Coverage and coordinate-quality overlays

- SRTM coverage uses five exact one-degree polygons derived from the standard local HGT filenames `N17E099`, `N18E099`, `N19E099`, `N20E099`, and `N19E098`. It reports local file availability only; no raster values, hillshade, slope or geothermal interpretation are shown.
- CR_02 review geometry contains its working EPSG:32647→4326 representation, published DMS comparator endpoint, and the line between them. Neither endpoint is an authoritative location while the disagreement remains unresolved.
- CM_16 contains only a hollow warning marker at its working UTM representation because the source has no DMS comparator.
- Review geometries are visually distinct hollow/dashed symbols, are disabled by default, and never enter the authoritative observation source.

## User distance measurement

- Each segment uses the haversine great-circle formula on a sphere with mean Earth radius 6,371,008.8 m.
- Multi-segment length is the sum of segment lengths.
- Display converts metres to kilometres at 1,000 m.
- Input/output CRS label is `EPSG:4326`; this is descriptive navigation-scale measurement, not a cadastral survey.

## User area measurement

- Area uses the spherical polygon formula over WGS84 longitude/latitude with the same mean Earth radius.
- Display converts square metres to square kilometres at 1,000,000 m².
- This does not account for cadastral datums, ellipsoidal corrections, terrain surface area, or legal boundaries.

## Distance to mapped faults

Disabled. The local 630-feature active-fault shapefile is geometrically usable, but reuse terms conflict. The DMR structure service still returns no geometry. No substitute, approximation, hand-drawn line, or nearest-distance result is produced.

## Geological preprocessing

- Immutable input: Phase 1C EsriJSON in EPSG:32647.
- Rings are reconstructed using Esri orientation. An unassigned hole now fails the build instead of being silently dropped. Multipart polygons are preserved.
- One invalid derived polygon part (`OBJECTID 14319`) is repaired with Shapely `buffer(0)` before simplification. The manifest records the method, repair count/IDs, zero orphan holes, input/output feature counts and source/output bounds.
- Simplification: Shapely topology-preserving simplification at 25 m in source metres.
- Transform: pyproj EPSG:32647 → EPSG:4326 with `always_xy=True`.
- Output: full-fidelity transformed GeoJSON retained outside the public app; simplified GeoJSON is lazy-fetched by the map.
- QA: known synthetic EPSG:32647 fixture, source immutability assertion, feature count, source SHA-256, vertex counts, byte sizes and Hausdorff deviations.
- Measured 2026-10-24 result: 1,266 features; 188,846 → 113,355 vertices; maximum measured Hausdorff deviation 39.871 m; mean 22.671 m. The measured maximum, not the nominal tolerance, is the applicable disclosure.

## Export

Evidence export runs a license/reuse gate. The two current observation sources state that redistribution permission was not assessed, so raw filtered and selected-record export is disabled. If an explicit reusable source is later added, the implemented JSON path includes the record, source provenance, scientific boundary and missing-evidence fields. A user-clicked location with no restricted intersection may be exported; any unresolved/restricted intersection blocks location export. Geology, SRTM coverage and coordinate-review intersection export remain blocked under current terms.
