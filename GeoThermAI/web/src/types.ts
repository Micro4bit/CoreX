export type Page = "dashboard" | "map" | "quality" | "status";

export interface GeothermalRecord {
  record_uid: string;
  source_id: string;
  source_region: "Northern Thailand" | "Southern Thailand" | string;
  source_record_code: string;
  source_province_or_area: string;
  source_site_name: string;
  observation_type: string;
  source_easting_m: string;
  source_northing_m: string;
  source_longitude_dms: string;
  source_latitude_dms: string;
  reported_coordinate_reference: string;
  working_coordinate_reference: string;
  derived_longitude_wgs84: string;
  derived_latitude_wgs84: string;
  surface_temperature_c: string;
  measurement_properties: string;
  evidence_tier: string;
  coordinate_validation_status: string;
  coordinate_quality_note: string;
  license_or_reuse_status: string;
  deduplication_status: string;
  proposed_site_group_id: string;
  validation_cluster_id: string;
  source_location: string;
  source_url: string;
}

export interface SourceRecord {
  source_id: string;
  source_type: string;
  reference: string;
  publication_date: string;
  source_url: string;
  access_status: string;
  local_artifact: string;
  license_or_reuse_status: string;
  provenance_and_limitations: string;
}

export interface GisLayer {
  layer_id: string;
  layer_category: string;
  publisher_or_source: string;
  source_url: string;
  local_artifact: string;
  access_status: string;
  spatial_coverage: string;
  geometry_or_resolution: string;
  quality_and_missing_data: string;
  license_or_permission_status: string;
  current_phase1c_use: string;
  coordinate_reference?: string;
  units_or_attributes?: string;
  source_date_or_version?: string;
  actual_inspection?: string;
}

export type GisLayerState = "AVAILABLE_VERIFIED" | "METADATA_ONLY" | "UNAVAILABLE_GEOMETRY" | "RESTRICTED_REUSE" | "QUALITY_PENDING" | "NOT_LOADED";

export interface RegisteredGisLayer extends Readonly<GisLayer> {
  readonly state: GisLayerState;
  readonly displayEligible: boolean;
  readonly coverageDisplayEligible: boolean;
  readonly exportEligible: boolean;
  readonly stateReason: string;
  readonly acquisitionDate: string;
  readonly sourceCrs: string;
  readonly scaleOrResolution: string;
  readonly coverage: string;
  readonly transformationMethod: string;
  readonly geometryCount: number | null;
  readonly sourceRecordCount: number | null;
  readonly uiEligibility: "DISPLAY_CONTEXT_ONLY" | "COVERAGE_METADATA_ONLY" | "DISABLED";
}

export interface SpatialEvidenceIntersection {
  id: string;
  layerId: string;
  title: string;
  detail: string;
  publisher: string;
  sourceUrl: string;
  license: string;
  scaleOrResolution: string;
  warning: string;
  exportEligible: boolean;
}

export interface LocationInspection {
  longitude: number;
  latitude: number;
  intersections: SpatialEvidenceIntersection[];
  method: string;
}

export interface MeasurementResult {
  kind: "distance" | "area";
  value: number;
  unit: "m" | "km" | "m²" | "km²";
  vertexCount: number;
  crs: "EPSG:4326";
  method: string;
}

export interface RockFeature {
  attributes: { TEXT_SYM?: string; YEAR_COMPI?: number; OBJECTID?: number };
  geometry?: { rings?: number[][][] };
}

export interface RockLayerFile {
  features: RockFeature[];
}

export interface AppData {
  records: GeothermalRecord[];
  sources: SourceRecord[];
  layers: GisLayer[];
}

export interface MapPoint extends GeothermalRecord {
  longitude: number;
  latitude: number;
  isCoordinateReview: boolean;
  isProvisional: boolean;
}
