# Coordinate Quality-Control Report — Phase 1B

Date: 2026-10-23  
Status: **EXECUTED** coordinate comparison; source correction is **NOT AUTHORIZED / NOT VERIFIED**.

## Objective

Preserve and test, rather than overwrite, the 16 coordinate records in Table 1 of Wood & Singharajwarapan (2014). The table describes **surface hot-spring manifestations**. It is not evidence that any record is a commercially viable geothermal resource.

## Materials actually inspected

- `../phase_1_data_acquisition_label_validation/wood_singharajwarapan_2014_northern_thailand.pdf` — original ten-page paper, including a visual rendering of p. 608/Table 1 and text extraction from the original PDF.
- `../phase_1_data_acquisition_label_validation/northern_hot_spring_label_registry_wood2014.csv` — the source-preserving 16-row Phase 1 transcription.
- GeoThermAI project-reference documents and Phase 1 audit outputs in their recorded project locations.

No standalone file named “Master Review” was present under `/Users/knight/Development/CoreX` when searched during this run. This report does not substitute another document for that missing input.

## Reproducible method

**VERIFIED source fact:** Table 1 (p. 608) labels the projected columns `WGS84 UTM East` and `WGS84 UTM North`, but does not print a UTM zone or hemisphere. It prints DMS longitude/latitude for 15 records and no DMS pair for `CM_16`.

**RESULT — CRS selection:** EPSG:32647, *WGS 84 / UTM zone 47N*, is the defensible working CRS. The 99°E source locations lie within UTM zone 47N (central meridian 99°E). This is corroborated, not merely assumed: `coordinate_validation.py` transformed every UTM pair with adjacent northern-zone candidates using `pyproj 3.7.2` / PROJ 9.5.1, parsed the original DMS strings independently, and measured WGS 84 geodesic distance with `pyproj.Geod(ellps="WGS84")`.

| Candidate CRS | DMS-comparable records | Median discrepancy (m) | Minimum (m) | Maximum (m) |
|---|---:|---:|---:|---:|
| EPSG:32646 — WGS 84 / UTM zone 46N | 15 | 628,062.674 | 626,998.010 | 635,481.791 |
| **EPSG:32647 — WGS 84 / UTM zone 47N** | **15** | **0.372** | **0.080** | **1,872.764** |
| EPSG:32648 — WGS 84 / UTM zone 48N | 15 | 628,063.029 | 626,998.496 | 635,476.041 |

Interpretation thresholds in this QC are deliberately conservative and apply to agreement between two representations in the same printed table, not to absolute field-survey accuracy: `<=50 m` = internally consistent; `>1 km` = unresolved mismatch; absent DMS = not comparable.

## Per-record result

All DMS strings, UTM strings and other source fields are retained byte-for-byte as CSV field values in `validated_hot_spring_registry.csv`; derived fields are appended.

| Code | UTM→DMS discrepancy (m) | Comparison result | Confidence | Validation status |
|---|---:|---|---|---|
| CR_01 | 0.23 | Match within 50 m | High | CRS and DMS consistent |
| CR_02 | 1,872.76 | Mismatch over 1 km | Low | Unresolved |
| CR_03 | 0.39 | Match within 50 m | High | CRS and DMS consistent |
| CR_04 | 0.13 | Match within 50 m | High | CRS and DMS consistent |
| CR_05 | 29.21 | Match within 50 m | High | CRS and DMS consistent |
| CR_06 | 0.08 | Match within 50 m | High | CRS and DMS consistent |
| CR_08 | 0.40 | Match within 50 m | High | CRS and DMS consistent |
| CR_09 | 0.26 | Match within 50 m | High | CRS and DMS consistent |
| PR_07 | 2.47 | Match within 50 m | High | CRS and DMS consistent |
| CM_01 | 0.35 | Match within 50 m | High | CRS and DMS consistent |
| CM_02 | 0.31 | Match within 50 m | High | CRS and DMS consistent |
| CM_03 | 0.37 | Match within 50 m | High | CRS and DMS consistent |
| CM_16 | — | DMS missing | Low | CRS inferred; not comparable |
| LPa_04 | 0.26 | Match within 50 m | High | CRS and DMS consistent |
| CR_WNL | 2.10 | Match within 50 m | High | CRS and DMS consistent |
| PR_02 | 4.24 | Match within 50 m | High | CRS and DMS consistent |

## Focus records and interpretation discipline

### CR_02 — unresolved 1.873 km mismatch

**RESULT:** EPSG:32647 transforms the reported UTM pair to 99.68025428°E, 19.96312509°N. The printed DMS pair is 99.68018056°E, 19.94620833°N; the WGS 84 geodesic separation is **1,872.76 m**.

**HYPOTHESIS, not a correction:** the reported DMS latitude minute (`56`) may be a typographic or transcription error: retaining the printed seconds but changing only that minute to `57` would place the DMS latitude much nearer the UTM transformation. This is not verified by an erratum, original field notebook, author confirmation, or an independent authoritative registry. Therefore neither source coordinate is changed, and `CR_02` must be co-withheld with the Kok River group and run as an inclusion/exclusion sensitivity case if any future baseline is permitted.

### CR_05 — 29.21 m discrepancy

**RESULT:** The 29.21 m difference is within this report’s 50 m internal-consistency threshold. It is not evidence that either printed coordinate is wrong. Small representation/measurement/rounding differences are plausible **hypotheses**, but this run did not inspect field-survey methods and establishes no cause. No correction was made.

### CM_16 — DMS absent

**VERIFIED source fact:** Table 1 lists `551755`, `2220975` and 68.1°C, but has blank DMS longitude/latitude cells. EPSG:32647 yields a derived working point of 99.49502677°E, 20.08509728°N. Because there is no Table 1 DMS pair to test, this is a CRS-based transform, not coordinate validation. It remains low confidence until an original field source or authoritative inventory is checked.

### CR_02 temperature — separate label conflict retained

**VERIFIED source fact:** Table 1 reports a surface temperature of **85°C** for `CR_02`. On p. 612, the paper’s prose says that the Kok River geothermal areas (`CR_01`, `CR_02`, `CR_03`, `CR_08`) have a maximum temperature of **73°C**. This is an internal source conflict, distinct from the coordinate discrepancy. The registry retains the Table 1 value, labels it `TABLE_TEXT_INTERNAL_CONFLICT`, and records both statements; it does not infer a corrected temperature. A future label definition must choose and document a source-precedence rule or obtain the measurement record.

## What is verified versus unresolved

- **VERIFIED:** EPSG:32647 is overwhelmingly more internally consistent than tested adjacent zones; 13 of 15 DMS-comparable records are within 5 m, and CR_05 is within 50 m.
- **VERIFIED:** `CR_02` is an internal mismatch under that CRS; `CM_16` lacks a DMS comparator.
- **UNKNOWN:** which coordinate representation, if any, is erroneous for `CR_02`; the survey precision and datum realization used for each printed coordinate; the independent positional accuracy of `CM_16`.
- **Required next evidence:** source dataset/field notebook, published erratum, author confirmation, or an authoritative Thai registry with provenance. Do not use a web-map snap as a surrogate for this evidence.

## Limitations

This is coordinate consistency QA, not a field resurvey, geocoding exercise, or geothermal-resource assessment. High internal agreement does not establish that a hot spring is an independent system or a commercially viable resource.
