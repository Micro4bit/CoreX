#!/usr/bin/env python3
"""Build provenance-preserving Phase 1C geothermal label and source inventories.

This script combines the existing Phase 1B northern Table 1 registry with a
separate southern Table 1 that was visually inspected in Ngansom & Duerrast
(2021). It preserves source coordinate fields and adds derived WGS 84 decimal
coordinates in separate columns. It does not deduplicate records by name.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from pyproj import Transformer


TASK_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TASK_DIR.parents[1]
NORTH_REGISTRY = PROJECT_DIR / "tasks/phase_1b_coordinate_label_integrity/validated_hot_spring_registry.csv"
NORTH_GROUPS = PROJECT_DIR / "tasks/phase_1b_coordinate_label_integrity/geothermal_site_groups.csv"

# Exact source values transcribed from the visually inspected Table 1 on p. 40
# of Ngansom & Duerrast (2021). The paper's prose says 30 samples, whereas the
# table enumerates 31 rows; both facts are preserved in the provenance output.
SOUTHERN_RECORDS = (
    ("CP", "CP1", 512222, 1075014, 50),
    ("RN", "RN1", 462169, 1100516, 65), ("RN", "RN2", 460000, 1094700, 40),
    ("RN", "RN3", 461030, 1093400, 45), ("RN", "RN4", 462290, 1094275, 50),
    ("RN", "RN5", 456192, 1080300, 46), ("RN", "RN6", 470810, 1060430, 75),
    ("SR", "SR1", 521107, 1034893, 45), ("SR", "SR2", 520518, 1033905, 40),
    ("SR", "SR3", 522412, 1031459, 60), ("SR", "SR4", 555129, 1009502, 41),
    ("SR", "SR5", 545897, 972938, 42), ("SR", "SR6", 503522, 979890, 53),
    ("SR", "SR7", 529417, 991895, 70), ("SR", "SR8", 530806, 991094, 56),
    ("SR", "SR9", 524947, 977116, 62),
    ("PG", "PG1", 441455, 960807, 78), ("PG", "PG2", 437870, 975306, 55),
    ("PG", "PG3", 420496, 918037, 45),
    ("KB", "KB1", 499622, 900439, 45), ("KB", "KB2", 500183, 891731, 47),
    ("KB", "KB3", 510462, 888220, 45), ("KB", "KB4", 512329, 873475, 47),
    ("KB", "KB5", 523171, 876867, 47),
    ("TR", "TR1", 551391, 818787, 52), ("ST", "ST1", 628046, 756311, 50),
    ("PL", "PL1", 625096, 823266, 57), ("PL", "PL2", 608944, 810077, 46),
    ("PL", "PL3", 604490, 816432, 50), ("PL", "PL4", 615661, 850513, 41),
    ("YL", "YL1", 729730, 646758, 80),
)

PROVINCE_NAMES = {
    "CP": "Chumphon", "RN": "Ranong", "SR": "Surat Thani", "PG": "Phang Nga",
    "KB": "Krabi", "TR": "Trang", "ST": "Satun", "PL": "Phatthalung", "YL": "Yala",
}

SOURCE_FIELDS = (
    "source_id", "source_type", "reference", "publication_date", "source_url", "access_status",
    "local_artifact", "source_coordinate_reference", "source_identifiers", "measured_properties",
    "evidence_tier", "license_or_reuse_status", "provenance_and_limitations",
)
REGISTRY_FIELDS = (
    "record_uid", "source_id", "source_region", "source_record_code", "source_province_or_area",
    "source_site_name", "observation_type", "source_easting_m", "source_northing_m", "source_longitude_dms",
    "source_latitude_dms", "reported_coordinate_reference", "working_coordinate_reference",
    "derived_longitude_wgs84", "derived_latitude_wgs84", "surface_temperature_c", "measurement_properties",
    "evidence_tier", "coordinate_validation_status", "coordinate_quality_note", "license_or_reuse_status",
    "deduplication_status", "proposed_site_group_id", "validation_cluster_id", "crossmatch_status",
    "source_location", "source_url",
)


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_sources() -> list[dict[str, str]]:
    return [
        {
            "source_id": "WOOD_SINGHARAJWAPAN_2014_TABLE1", "source_type": "peer_reviewed_conference_paper",
            "reference": "Wood, S.H. & Singharajwarapan, F.S. (2014), Geothermal Systems of Northern Thailand and Their Association With Faults Active During the Quaternary, GRC Transactions 38, 607-615.",
            "publication_date": "2014", "source_url": "https://publications.mygeoenergynow.org/grc/1033597.pdf",
            "access_status": "VERIFIED_DOWNLOAD_OPENED", "local_artifact": "../phase_1_data_acquisition_label_validation/wood_singharajwarapan_2014_northern_thailand.pdf",
            "source_coordinate_reference": "Table 1: WGS84 UTM, zone not printed; DMS present for 15/16 rows.",
            "source_identifiers": "16 source codes", "measured_properties": "surface temperature for 14 rows; flow rate where reported",
            "evidence_tier": "VERIFIED_DOWNLOAD_PRIMARY_TABLE", "license_or_reuse_status": "NOT_STATED_IN_PDF; citation required; redistribution permission not assessed",
            "provenance_and_limitations": "Phase 1B retains source strings. CR_02 coordinate and temperature text/table conflicts; CM_16 lacks DMS.",
        },
        {
            "source_id": "NGANSOM_DUERRAST_2021_TABLE1", "source_type": "peer_reviewed_journal_article",
            "reference": "Ngansom, W. & Duerrast, H. (2021), Geochemical Characterization of Hot Spring Waters from Southern Thailand as the Base for Geothermal Energy Utilization, EnvironmentAsia 14(3), 37-49, Table 1 p. 40.",
            "publication_date": "2021 (exact publication day not verified from PDF)", "source_url": "https://tshe.org/ea/pdf/EA14%283%29/EA14%283%29_04.pdf",
            "access_status": "VERIFIED_DOWNLOAD_OPENED", "local_artifact": "ngansom_duerrast_2021_southern_hot_springs.pdf",
            "source_coordinate_reference": "Table 1: Location UTM (WGS-84); zone not printed.",
            "source_identifiers": "31 Table 1 codes across 9 named geothermal provinces", "measured_properties": "surface temperature",
            "evidence_tier": "VERIFIED_DOWNLOAD_PEER_REVIEWED_TABLE", "license_or_reuse_status": "NOT_STATED_IN_PDF; citation required; redistribution permission not assessed",
            "provenance_and_limitations": "Paper prose says 30 samples, but visually inspected Table 1 enumerates 31 rows. UTM zone lacks independent DMS confirmation in this run.",
        },
        {
            "source_id": "DMR_HOT_SPRING_PAGE", "source_type": "official_agency_web_inventory_page",
            "reference": "Department of Mineral Resources, Thailand, น้ำพุร้อน (Hot springs) web page.",
            "publication_date": "NOT_STATED", "source_url": "https://www.dmr.go.th/ด้านธรณีวิทยา/ธรณีวิทยาพื้นฐาน/น้ำพุร้อน/",
            "access_status": "VERIFIED_DOWNLOAD_OPENED_NO_COORDINATE_TABLE", "local_artifact": "dmr_hot_spring_official_page.html",
            "source_coordinate_reference": "No coordinate-level table verified in this run.", "source_identifiers": "hot-spring codes/names visible in HTML table",
            "measured_properties": "page displays selected physical/chemical columns", "evidence_tier": "OFFICIAL_CONTEXT_NOT_COORDINATE_LABEL_SOURCE",
            "license_or_reuse_status": "NOT_STATED_ON_INSPECTED_PAGE", "provenance_and_limitations": "Not promoted to point labels because an authoritative coordinate inventory was not found or downloaded.",
        },
        {
            "source_id": "KAPONG_MENDELEY_2019", "source_type": "open_geophysical_supplement",
            "reference": "Duerrast, H., Pirarai, K. & Ngansom, W. (2019), Data for: Geological Setting and Hydrogeothermal Characteristics of the Kapong Non-Volcanic Hot Spring Area in Southern Thailand, DOI 10.17632/37ng92rj85.1.",
            "publication_date": "2019-11-20", "source_url": "https://data.mendeley.com/datasets/37ng92rj85/1",
            "access_status": "VERIFIED_DOWNLOAD_OPENED", "local_artifact": "kapong_geophysical_appendix.pdf; kapong_mendeley_metadata.json",
            "source_coordinate_reference": "Visual Google Earth location maps; no machine-readable station-coordinate table extracted.",
            "source_identifiers": "13 VES stations and 3 ERT cross sections per source metadata", "measured_properties": "electrical-resistivity survey results",
            "evidence_tier": "VERIFIED_DOWNLOAD_GEOSPATIAL_CONTEXT_NOT_LABEL_TABLE", "license_or_reuse_status": "CC BY 4.0 per downloaded metadata",
            "provenance_and_limitations": "Do not digitize appendix map positions as authoritative station coordinates. Not used as occurrence labels or map points.",
        },
        {
            "source_id": "NGANSOM_DUERRAST_2019_ATTEMPT", "source_type": "peer_reviewed_article_attempt",
            "reference": "Ngansom & Duerrast (2019), Assessment and Ranking of Hot Springs Sites Representing Geothermal Resources in Southern Thailand.",
            "publication_date": "2019", "source_url": "https://www.thaiscience.info/Journals/Article/CMJS/10990598.pdf",
            "access_status": "FAILED_DOWNLOAD_HTML_NOT_PDF", "local_artifact": "ngansom_duerrast_2019_southern_hot_spring_assessment_failed_download.html",
            "source_coordinate_reference": "NOT_INSPECTED", "source_identifiers": "NOT_INSPECTED", "measured_properties": "NOT_INSPECTED",
            "evidence_tier": "NOT_USABLE_THIS_RUN", "license_or_reuse_status": "NOT_VERIFIED", "provenance_and_limitations": "HTTP request returned a redirecting HTML lander rather than a PDF; no records were extracted.",
        },
    ]


def build_registry() -> list[dict[str, str]]:
    groups = {row["source_code"]: row for row in csv.DictReader(NORTH_GROUPS.open(encoding="utf-8"))}
    northern = list(csv.DictReader(NORTH_REGISTRY.open(encoding="utf-8")))
    rows: list[dict[str, str]] = []
    for row in northern:
        group = groups[row["source_code"]]
        rows.append({
            "record_uid": f"NORTH_WOOD2014_{row['source_code']}", "source_id": "WOOD_SINGHARAJWAPAN_2014_TABLE1",
            "source_region": "Northern Thailand", "source_record_code": row["source_code"], "source_province_or_area": "Northern Thailand (paper study area)",
            "source_site_name": row["site_name"], "observation_type": "surface_hot_spring_manifestation",
            "source_easting_m": row["utm_easting_m_wgs84"], "source_northing_m": row["utm_northing_m_wgs84"],
            "source_longitude_dms": row["longitude_dms"], "source_latitude_dms": row["latitude_dms"],
            "reported_coordinate_reference": "Table 1 WGS84 UTM; zone not printed", "working_coordinate_reference": row["selected_utm_crs"],
            "derived_longitude_wgs84": row["transformed_longitude_decimal_wgs84"], "derived_latitude_wgs84": row["transformed_latitude_decimal_wgs84"],
            "surface_temperature_c": row["surface_temperature_c"], "measurement_properties": "surface temperature and flow rate retained from Table 1 where reported",
            "evidence_tier": "VERIFIED_DOWNLOAD_PRIMARY_TABLE", "coordinate_validation_status": row["coordinate_validation_status"],
            "coordinate_quality_note": row["coordinate_qc_note"], "license_or_reuse_status": "NOT_STATED_IN_PDF",
            "deduplication_status": "RETAINED; no name-only merge", "proposed_site_group_id": group["site_group_id"],
            "validation_cluster_id": group["validation_cluster_id"], "crossmatch_status": "NO_SOUTHERN_CODE_OR_GEOGRAPHIC_OVERLAP_EXPECTED; not merged",
            "source_location": "Table 1", "source_url": "https://publications.mygeoenergynow.org/grc/1033597.pdf",
        })

    transformer = Transformer.from_crs(32647, 4326, always_xy=True)
    for province, code, east, north, temperature in SOUTHERN_RECORDS:
        lon, lat = transformer.transform(east, north)
        cluster = f"SOUTH_{province}_GEOTHERMAL_PROVINCE"
        rows.append({
            "record_uid": f"SOUTH_NGANSOM2021_{code}", "source_id": "NGANSOM_DUERRAST_2021_TABLE1",
            "source_region": "Southern Thailand", "source_record_code": code, "source_province_or_area": PROVINCE_NAMES[province],
            "source_site_name": "", "observation_type": "surface_hot_spring_manifestation",
            "source_easting_m": str(east), "source_northing_m": str(north), "source_longitude_dms": "", "source_latitude_dms": "",
            "reported_coordinate_reference": "Table 1 UTM (WGS-84); zone not printed", "working_coordinate_reference": "EPSG:32647 (inferred working CRS; not source-verified)",
            "derived_longitude_wgs84": f"{lon:.8f}", "derived_latitude_wgs84": f"{lat:.8f}", "surface_temperature_c": str(temperature),
            "measurement_properties": "surface temperature", "evidence_tier": "VERIFIED_DOWNLOAD_PEER_REVIEWED_TABLE",
            "coordinate_validation_status": "CRS_INFERRED_NO_DMS_COMPARATOR", "coordinate_quality_note": "No DMS coordinates in Table 1; EPSG:32647 transform is a working representation, not a correction.",
            "license_or_reuse_status": "NOT_STATED_IN_PDF", "deduplication_status": "RETAINED; unique source code; no name-only merge",
            "proposed_site_group_id": cluster, "validation_cluster_id": cluster,
            "crossmatch_status": "NO_NORTHERN_CODE_OR_GEOGRAPHIC_OVERLAP_EXPECTED; not merged", "source_location": "Table 1 p. 40",
            "source_url": "https://tshe.org/ea/pdf/EA14%283%29/EA14%283%29_04.pdf",
        })
    return rows


def main() -> None:
    if not NORTH_REGISTRY.exists() or not NORTH_GROUPS.exists():
        raise FileNotFoundError("Required Phase 1B registry/group inputs are missing.")
    sources = build_sources()
    registry = build_registry()
    write_csv(TASK_DIR / "expanded_geothermal_source_inventory.csv", SOURCE_FIELDS, sources)
    write_csv(TASK_DIR / "geothermal_label_master_registry.csv", REGISTRY_FIELDS, registry)
    north_count = sum(row["source_region"] == "Northern Thailand" for row in registry)
    south_count = sum(row["source_region"] == "Southern Thailand" for row in registry)
    print(f"run_date={date.today().isoformat()}")
    print(f"registry_records={len(registry)} northern={north_count} southern={south_count}")
    print("southern_table_rows=31; paper_prose_reports_30_samples=YES")
    print(f"source_inventory_rows={len(sources)}")


if __name__ == "__main__":
    main()
