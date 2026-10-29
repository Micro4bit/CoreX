# Label Provenance and Deduplication — Phase 1C

Date: 2026-10-23  
Status: **EXECUTED** source acquisition and registry construction. No predictive model was fitted.

## Objective and label meaning

The master registry records published **surface hot-spring / thermal-manifestation observations**. It does not label commercial reservoirs, proven resources, MW capacity, boreholes, geophysical stations, or unrecorded geography as negative. `geothermal_label_master_registry.csv` preserves reported coordinates in source fields and places all derived WGS 84 values in separate columns.

## Sources actually acquired and opened

| Source | Actual coordinate evidence | Records retained | Evidence status |
|---|---|---:|---|
| Wood & Singharajwarapan (2014), Table 1 p. 608 | WGS84 UTM for 16 rows; 15 DMS pairs | 16 northern rows | VERIFIED_DOWNLOAD_PRIMARY_TABLE |
| Ngansom & Duerrast (2021), Table 1 p. 40 | WGS-84 UTM easting/northing and surface temperature | 31 southern rows | VERIFIED_DOWNLOAD_PEER_REVIEWED_TABLE |
| DMR hot-spring page | Official HTML contains inventory/context fields, but no verified coordinate-point table | 0 new coordinate labels | VERIFIED_DOWNLOAD_OPENED_NO_COORDINATE_TABLE |
| Kapong Mendeley supplement | Metadata says 13 VES and 3 ERT lines; downloaded appendix maps are visual, not coordinate tables | 0 labels | VERIFIED_DOWNLOAD_GEOSPATIAL_CONTEXT_NOT_LABEL_TABLE |

The attempted Ngansom & Duerrast (2019) PDF URL returned a redirecting HTML lander, not a PDF. It is logged as a failed acquisition and supplied no records.

## New southern registry: actual result

The downloaded 2021 Table 1 was visually checked and enumerates **31** coded rows across nine named geothermal provinces: Chumphon (1), Ranong (6), Surat Thani (9), Phang Nga (3), Krabi (5), Trang (1), Satun (1), Phatthalung (4), and Yala (1). The paper prose says “thirty” samples. This is a source-internal record-count conflict, retained in the source inventory; no row was discarded or invented to force either number.

The table prints `UTM (WGS-84)` but no UTM zone and no DMS comparator. EPSG:32647 is stored only as an **inferred working CRS** for derived display coordinates. It is not a verified correction of the published source. Every southern row has `CRS_INFERRED_NO_DMS_COMPARATOR`.

## Deduplication and cross-match protocol

1. Preserve each source row with `record_uid = source + source code`.
2. Do not merge on matching-looking place names, map proximity, province name or temperature.
3. North/south sources use disjoint codes and occupy distinct broad regions; their records were not merged. Southern Table 1 does not provide site names beyond codes, so a name-based cross-match is not possible.
4. North rows inherit their Phase 1B source values, coordinate flags, candidate site groups and conservative validation clusters.
5. South rows are co-withheld at the **nine named geothermal-province** level. This is a leakage safeguard, not a claim that every province is one hydrothermal system or that all 31 records are independent systems.

## Group-count result

| Unit | North | South | Combined |
|---|---:|---:|---:|
| Observations retained | 16 | 31 | 47 |
| Candidate/source grouping | 13 candidate site groups | 9 named geothermal provinces | Not an independent-system count |
| Conservative co-withholding units | 9 | 9 | 18 provisional units |

The **18** count is a maximum provisional validation-unit count, not proof of 18 independent geothermal systems. North has unresolved `CR_02` and `CM_16`; southern province grouping needs source-level hydrogeologic review and a UTM-zone check. Therefore no independent-system total sufficient for model selection has been established.

## Critical label and coordinate limitations

- `CR_02` has a 1,872.76 m UTM-to-DMS discrepancy, and its 85°C Table 1 value conflicts with a 73°C Kok River maximum in article prose.
- `CM_16` has no DMS comparator.
- The southern table’s 31 rows conflict with prose saying 30 samples; its UTM zone is not printed.
- Hot-spring temperatures are surface observations, not reservoir temperatures. Geothermometer estimates, wells and VES/ERT stations are different evidence classes and are not silently converted to the positive label.
- The DMR page was not used to manufacture point coordinates; its official status does not repair the missing coordinate inventory.

## Leakage controls for any future work

- Never use distance/density to this master registry, a digitized DMR hot-spring map, or survey products that encode the same sites as predictors for labels derived from them.
- Assign entire `validation_cluster_id` groups before background selection, preprocessing, feature selection and thresholding.
- Use background/positive-unlabeled logic; unlabeled cells are not negative observations.
- Treat the southern table as a geographically separate source registry, not an automatically valid test set. Coordinate-reference and grouping gates must pass first.

## Concrete next action

Request or locate DMR’s underlying coordinate-level hot-spring database with identifiers, datum/zone, survey date and reuse terms. Independently verify the southern UTM zone from the authors or an authoritative inventory, then review province-to-system relationships before authorizing a held-out north-to-south experiment.
