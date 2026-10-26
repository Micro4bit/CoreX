"""Paths and presentation constants for the local GeoThermAI MVP."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = PROJECT_ROOT / "tasks"
PHASE_1C = TASKS_ROOT / "phase_1c_label_expansion_gis_foundation"
PHASE_1 = TASKS_ROOT / "phase_1_data_acquisition_label_validation"

OBSERVATIONS_CSV = PHASE_1C / "geothermal_label_master_registry.csv"
SOURCE_INVENTORY_CSV = PHASE_1C / "expanded_geothermal_source_inventory.csv"
GIS_INVENTORY_CSV = PHASE_1C / "verified_gis_layer_inventory.csv"
ROCK_UNITS_ESRIJSON = PHASE_1C / "rock_unit_250k_northern_esrijson.json"
ACTIVE_FAULTS_SHP = PHASE_1 / "N_ZONE_ACTIVEFAULT_20230419_091427.shp"
TERRAIN_SUMMARY_CSV = PHASE_1C / "northern_terrain_variable_summary.csv"

APP_TITLE = "GeoThermAI — Geospatial Evidence Explorer"
SCIENTIFIC_SCOPE_NOTICE = (
    "This tool displays published surface thermal-manifestation observations and "
    "descriptive GIS context. It does not predict commercial geothermal reservoirs, "
    "resource potential, drilling success, MW, or LCOE."
)

COORDINATE_REVIEW_STATUSES = {
    "CRS_INFERRED_DMS_MISMATCH_UNRESOLVED",
    "CRS_INFERRED_DMS_MISSING",
}
PROVISIONAL_STATUSES = {"CRS_INFERRED_NO_DMS_COMPARATOR"}
