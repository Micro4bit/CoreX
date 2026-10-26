# Terrain data QC — 2026-10-26

`scripts/qc_terrain.py` opened all five physical HGT gzip files as big-endian signed 16-bit 3,601 × 3,601 elevation-post grids. It verified filename bounds, one-arc-second spacing, nodata, physical ranges, checksums, edge continuity and GeoTIFF round-trip output.

| Tile | Bounds WGS84 | Min–max m | NoData |
|---|---|---:|---:|
| N17E099 | 99–100 E, 17–18 N | 20–1,377 | 0 |
| N18E099 | 99–100 E, 18–19 N | 107–1,996 | 0 |
| N19E098 | 98–99 E, 19–20 N | 145–2,177 | 0 |
| N19E099 | 99–100 E, 19–20 N | 335–2,020 | 0 |
| N20E099 | 99–100 E, 20–21 N | 357–2,336 | 0 |

All four shared edges match exactly: maximum difference 0 m and zero nonmatching posts. Derived EPSG:4326 GeoTIFFs retain source elevation values and use a half-pixel affine so pixel centers align with HGT posts. Source/derived hashes and sizes are in `derived/terrain/terrain_qc_summary.json`.

Coverage is only five one-degree tiles, not northern Thailand or Thailand. The app therefore exposes verified data-availability footprints, not elevation, slope or hillshade. No missing area is extrapolated. Terrain is context, not evidence of subsurface heat.

