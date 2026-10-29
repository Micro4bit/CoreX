# Pilot AOI & Feature Gate: provisional decision

**Candidate from Phase 2E report:** Northern rectangle 98.0°–100.5° E and 17.0°–20.5° N; NOT finalized; not a recommendation that its bounds are geographically, legally, or geologically optimal.

## Decision table (no invented overlap percentages)
| Layer | Reported count | Current allowable role | Action to get ML-ready |
|---|---:|---|---|
| Geothermal registry | 47 rows, 14 internally consistent | Evidence viewer only | Expert group adjudication; withheld and provisional exclusions |
| DMR geology | 1,266 polygons / 42 symbols | Northern contextual display | Obtain training/derivative written terms; verify AOI polygon intersection and input resolution |
| Active faults | 630 local lines; 0 live service geometries | Disabled | Written DMR permission and geometry/provenance verification |
| SRTM | 5 × 3601² HGT verified | Terrain footprint / covered tile QC | Acquire contiguous pilot coverage, inspect seam/nodata, derive scale-appropriate features |
| IHFC heat flow | 154 Thailand entries, 111 locations | Observed point display only | Do not interpolate/use as predictor without justified spatial support and uncertainties |
| Landsat ST | 0 validated TIFFs | Disabled | Valid raster+QA acquisition, seasonal scene protocol, sensor QA and cloud masking |
| Satellite gravity | No acquired pipeline dataset | Research lead | Check scientific interpretation, permissions and actual delivered raster before proposing feature |

## Lock procedure
1. Produce actual AOI vector boundary and footprint intersection map with provenance and CRS. No map-derived geometry should leave system if restricted.
2. For each candidate AOI, compute: verified independent positive groups; valid licensed predictors; contiguous coverage after scientifically defensible resampling; independent geographic test support.
3. Set an exclusion mask where critical predictors are unavailable; **unknown coverage does not mean low prospectivity**.
4. Document physically meaningful grid cell size and candidate resolution; avoid inventing 100-m or 2-km precision.
5. Domain and dataset owner sign-off needed before `study_area_locked: true`.

Reference channels: https://www.usgs.gov/faqs/where-can-i-get-global-elevation-data ; https://data.dmr.go.th/dataset/zone-acttivefault . Listing or showing a layer does not automatically grant unrestricted redistribution or model training rights.
