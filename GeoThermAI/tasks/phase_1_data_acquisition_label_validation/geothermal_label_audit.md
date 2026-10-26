# Geothermal Label Audit

Date accessed: 2026-10-23  
Target under review: observable geothermal/hot-spring manifestation for a research screening experiment. This is **not** the target “economically exploitable geothermal reservoir.”

## Verdict

There is a credible, georeferenced **northern literature registry for label curation**, but there is not yet a Thailand-wide, independently validated training-label set. The correct Phase 1 stance is **positive-unlabeled / background-sampling research**, conditional on site grouping and coordinate verification. It is not a conventional positive-vs-true-negative classification problem.

## Label-source results

| Source | Records and coordinates | Temperature / type | Reliability and use | Status |
|---|---|---|---|---|
| DMR Thailand hot-spring map PDF | National symbol map; no count claimed in this audit; no IDs or coordinate table | Three temperature classes: >80°C, 60–79°C, <60°C | Official contextual map only. Manual digitization would create approximate, non-authoritative coordinates and is not allowed as a ground-truth label source. | VERIFIED_DOWNLOAD, unsuitable as label table |
| Wood & Singharajwarapan (2014), Table 1 | 16 northern records; all have WGS84 UTM East/North, 15 additionally show DMS longitude/latitude | 14 report surface temperature; rows are named hot springs/systems | Directly usable for a provisional, cited northern registry only after coordinate-system check and system-level deduplication. | VERIFIED_DOWNLOAD |
| IHFC 2024 Global Heat Flow Database | Broad geographic filter returned 460 rectangular-window records, 322 coordinates; this is not a country-clipped count | Heat-flow observations, largely not hot springs; 291 rows are offshore in that window | Supplementary physical evidence only. Never convert to geothermal-occurrence positives. | VERIFIED_DOWNLOAD |
| Kapong supplementary dataset | Landing page describes locations/results for 13 VES stations and 3 ERT sections | Geophysical survey stations, not a regional label inventory | Could support a local case study if raw data are acquired and licensing is confirmed. | METADATA_ONLY |

## Verified northern registry

`northern_hot_spring_label_registry_wood2014.csv` was manually transcribed from the visually inspected Table 1, preserving reported values rather than fabricating coordinates:

- 16 source codes and 16 unique source-code rows.
- 16/16 have reported UTM East/North values.
- 15/16 have DMS longitude and latitude in the table; `CM_16` reports UTM only.
- 14/16 have a reported surface-temperature value. `CR_01` and `CR_08` do not.
- The table heading says WGS84 UTM but does not state the UTM zone/hemisphere. Do not transform its UTM coordinates until that is verified. The DMS fields can be independently compared to a defensible transform as a quality-control test; they must not be overwritten.
- Table rows include close manifestations around named systems and faults. A row count is not an independent-site count. Curate `site_group_id`, source/measurement date, occurrence class, and coordinate-confidence fields before any model split.

## Positive-label meaning

The accepted provisional positive means: **a published, georeferenced surface hot-spring/thermal-manifestation observation**. It does not mean:

- a confirmed reservoir;
- electricity-grade temperature or flow;
- an economically recoverable resource;
- a production well;
- a negative label for every place without a record.

Surface temperature is a property of the recorded manifestation. It is not a deep-reservoir temperature. The northern table itself includes observations from 41°C to 100.5°C among the reported values, so a threshold policy must be a future explicit design decision, not an implicit cleanup rule.

## Duplicate, missingness, and coordinate-quality findings

No duplicate source codes occur in the 16-row transcription. That is not a spatial-duplicate test. It does not establish that the observations are different geothermal systems or temporally independent. The immediate quality checks are:

1. Confirm each UTM zone/hemisphere and compare transformed UTM positions with the reported DMS position where both exist.
2. Review each row against its cited source and its likely hydrothermal-system membership.
3. Preserve rows without temperature as occurrence evidence with a missing-temperature flag. Do not impute a temperature.
4. Retain source code, citation, publication year, reported coordinates and raw value fields; add all cleaning decisions in a separate audit column.
5. Search for overlaps with an authoritative DMR inventory only after that inventory can be obtained; do not merge by name alone.

IHFC contains numerous duplicate coordinates in a broad regional window: 104 duplicate-coordinate groups and 138 rows beyond the first among 460 rows. Its duplicate pattern is a separate heat-flow measurement/provenance issue and must not be conflated with thermal-spring label duplicates.

## Sampling and leakage protocol

Use background / positive-unlabeled (PU) methods rather than labeling all unrecorded cells as negatives.

1. Define an accessible study mask and generate background only within that mask.
2. Exclude an explicit buffer around every positive from background sampling; buffer size is **TBD** after coordinates and positional uncertainty are audited.
3. Do not use any label-derived feature, such as distance to this hot-spring registry, density of these positives, a map digitized from the DMR hot-spring PDF, or a proxy generated from the target locations.
4. Split by complete site group or spatial block before fitting preprocessing, sampling, feature selection, tuning and threshold choice.
5. Report only ranking/enrichment or held-out recall metrics appropriate to the sampling design, with uncertainty across groups/blocks. Do not describe outputs as calibrated occurrence probability without separate support.

## Minimum label gate before predictive modeling

1. Confirm the coordinate reference for all 16 literature records.
2. Obtain and audit an official Thai point inventory, or document that it is unavailable and restrict the first experiment to the literature registry with strong caveats.
3. Create a provenance-preserving site-group table and quantify the number of independent groups.
4. Demonstrate at least one geographically separated held-out group/block with no preprocessing or sampling leakage.
5. Acquire an independent southern or other-region registry before making an out-of-region claim.

Until these pass, GeoThermAI may create an evidence map or descriptive GIS overlay, but must not claim validated national prospectivity prediction.

## Primary sources

- DMR hot-spring map: <https://www.dmr.go.th/น้ำพุร้อน-แผนที่แหล่งน้ำพุร้อนในประเทศไทย/>
- Wood & Singharajwarapan (2014), Table 1: <https://publications.mygeoenergynow.org/grc/1033597.pdf>
- IHFC Global Heat Flow Database 2024: <https://www.ihfc-iugg.org/user/downloads/data/R2024/IHFC_2024_GHFDB.xlsx>, DOI <https://doi.org/10.5880/fidgeo.2024.014>
