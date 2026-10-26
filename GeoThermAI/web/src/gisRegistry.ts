import type { GisLayer, GisLayerState, RegisteredGisLayer } from "./types";

interface EligibilityRule {
  state: GisLayerState;
  display: boolean;
  coverageDisplay: boolean;
  exportable: boolean;
  reason: string;
  acquisitionDate: string;
  transformationMethod: string;
  geometryCount: number | null;
  sourceRecordCount: number | null;
  uiEligibility: RegisteredGisLayer["uiEligibility"];
  sourceOverrides?: Partial<GisLayer>;
}

const states: Record<string, EligibilityRule> = {
  DMR_ROCK_UNIT_250K_NORTH: {
    state: "AVAILABLE_VERIFIED",
    display: true,
    coverageDisplay: true,
    exportable: false,
    reason:
      "Verified local polygons; reuse terms remain unverified, so display is contextual and geometry export is disabled.",
    acquisitionDate:
      "2026-10-23 (service inspection; exact acquisition timestamp not separately recorded)",
    transformationMethod:
      "Build-time pyproj EPSG:32647 to EPSG:4326; Shapely topology-preserving 25 m simplification in source metres.",
    geometryCount: 1266,
    sourceRecordCount: 1266,
    uiEligibility: "DISPLAY_CONTEXT_ONLY",
  },
  DMR_GEOL_STR_250K_NORTH: {
    state: "UNAVAILABLE_GEOMETRY",
    display: false,
    coverageDisplay: false,
    exportable: false,
    reason:
      "ArcGIS REST returned attributes without geometry even with returnGeometry=true and explicit outSR/pagination.",
    acquisitionDate: "2026-10-23 (service inspection)",
    transformationMethod: "None; no usable geometry was returned.",
    geometryCount: 0,
    sourceRecordCount: 2000,
    uiEligibility: "DISABLED",
  },
  DMR_ACTIVEFAULT_ZONE: {
    state: "RESTRICTED_REUSE",
    display: false,
    coverageDisplay: false,
    exportable: false,
    reason:
      "Local geometry is valid, but catalog CC attribution conflicts with noncommercial/no-legal-citation conditions; DMR clarification required.",
    acquisitionDate:
      "Not recorded in the Phase 1C inventory; catalog resource last updated 2016-08-01.",
    transformationMethod: "None in the public UI; source remains EPSG:32647.",
    geometryCount: 630,
    sourceRecordCount: 630,
    uiEligibility: "DISABLED",
  },
  SRTM_HGT_NORTH: {
    state: "AVAILABLE_VERIFIED",
    display: false,
    coverageDisplay: true,
    exportable: false,
    reason:
      "Five 1 arc-second HGT tiles passed dimension, range, nodata, georeferencing, GeoTIFF round-trip and shared-seam checks; coverage remains incomplete, so the UI exposes footprints only.",
    acquisitionDate:
      "2026-10-23 (four Phase 1C tiles); Phase 1 N19E098 acquisition date not separately recorded.",
    transformationMethod:
      "Big-endian HGT posts were read without value resampling and written to EPSG:4326 GeoTIFF with pixel centers aligned to the one-degree post grid; UI footprints derive from verified tile bounds.",
    geometryCount: 5,
    sourceRecordCount: 5,
    uiEligibility: "COVERAGE_METADATA_ONLY",
    sourceOverrides: {
      local_artifact: "Five source HGT gzip files plus Phase 2D EPSG:4326 GeoTIFF derivatives",
      spatial_coverage: "Five verified one-degree tiles from 98-100 E and 17-21 N; incomplete/non-contiguous northern coverage",
      coordinate_reference: "HGT geographic point posts; derived GeoTIFF EPSG:4326",
      geometry_or_resolution: "1 arc-second, 3601 x 3601 posts per tile",
      actual_inspection: "All five tiles passed dimensions, nodata, elevation-range, round-trip and shared-edge checks in Phase 2D",
      quality_and_missing_data: "No nodata in present tiles; missing outside the five-tile footprint; no extrapolation",
      license_or_permission_status: "SRTM public domain; attribution requested by distribution",
      current_phase1c_use: "Verified coverage footprints only; derived raster not rendered",
    },
  },
  IHFC_2024: {
    state: "AVAILABLE_VERIFIED",
    display: true,
    coverageDisplay: true,
    exportable: true,
    reason:
      "154 measurement rows at 111 coordinates fall inside a validated Natural Earth Thailand boundary; repeated coordinates remain separate, heat-flow uncertainty is absent, and the layer is descriptive only.",
    acquisitionDate:
      "2026-10-23 (local artifact timestamp; exact publisher download timestamp not separately recorded)",
    transformationMethod:
      "Source WGS84 points classified with a Natural Earth 1:10m Thailand covers predicate in EPSG:4326; offshore and neighboring-country records excluded from the map, duplicates retained.",
    geometryCount: 154,
    sourceRecordCount: 91182,
    uiEligibility: "DISPLAY_CONTEXT_ONLY",
    sourceOverrides: {
      local_artifact: "Phase 2D QC CSV plus 154-feature browser GeoJSON derived from immutable IHFC workbook",
      access_status: "AVAILABLE_VERIFIED_DESCRIPTIVE_POINTS",
      spatial_coverage: "154 rows at 111 coordinates inside the Natural Earth Thailand boundary",
      coordinate_reference: "WGS84 geographic latitude/longitude (EPSG:4326)",
      geometry_or_resolution: "Point measurements; spatial support varies by source record",
      actual_inspection: "91,182 workbook rows inspected; polygon clip, duplicate/offshore and provenance audit completed",
      quality_and_missing_data: "28 duplicate-coordinate groups retained; q uncertainty absent for 154/154 Thailand rows; depth mostly absent",
      license_or_permission_status: "CC BY 4.0; retain IHFC/GFZ attribution and DOI",
      current_phase1c_use: "Opt-in descriptive point display and inspection; no interpolation or ML feature",
    },
  },
  KAPONG_VES_ERT: {
    state: "METADATA_ONLY",
    display: false,
    coverageDisplay: false,
    exportable: false,
    reason:
      "CC BY 4.0 provenance exists, but no machine-readable station coordinates were extracted.",
    acquisitionDate: "Not separately recorded; dataset published 2019-11-20.",
    transformationMethod: "None; visual map locations were not digitized.",
    geometryCount: 0,
    sourceRecordCount: 16,
    uiEligibility: "DISABLED",
  },
  LANDSAT_C2_L2_ST: {
    state: "NOT_LOADED",
    display: false,
    coverageDisplay: false,
    exportable: false,
    reason:
      "No Landsat Collection 2 Level-2 Surface Temperature raster asset is present; cloud, QA and data-gap checks cannot run.",
    acquisitionDate: "No raster acquired.",
    transformationMethod: "None; no usable raster exists.",
    geometryCount: 0,
    sourceRecordCount: 0,
    uiEligibility: "DISABLED",
  },
};

const landsatCandidate: GisLayer = {
  layer_id: "LANDSAT_C2_L2_ST",
  layer_category: "satellite_surface_temperature",
  publisher_or_source: "U.S. Geological Survey Landsat Collection 2",
  source_url:
    "https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature",
  local_artifact: "No usable raster; metadata response only",
  access_status: "NOT_LOADED",
  spatial_coverage: "Not established",
  coordinate_reference: "Not established",
  geometry_or_resolution: "No raster asset",
  units_or_attributes: "Surface temperature and QA bands would be required",
  source_date_or_version: "Collection 2 Level-2",
  actual_inspection: "No usable raster opened in Phase 2C",
  quality_and_missing_data:
    "Cloud, QA and data-gap checks not possible without the raster asset",
  license_or_permission_status:
    "Not evaluated for a local raster because no raster was obtained",
  current_phase1c_use: "Disabled",
};

export function registerGisLayers(
  sourceLayers: GisLayer[],
): RegisteredGisLayer[] {
  const candidates = sourceLayers.some(
    (source) => source.layer_id === landsatCandidate.layer_id,
  )
    ? sourceLayers
    : [...sourceLayers, landsatCandidate];
  return candidates.map((source) => {
    const resolved: EligibilityRule = states[source.layer_id] ?? {
      state: "NOT_LOADED" as const,
      display: false,
      coverageDisplay: false,
      exportable: false,
      reason: "No Phase 2C eligibility rule has been verified for this layer.",
      acquisitionDate: "Not recorded.",
      transformationMethod: "None recorded.",
      geometryCount: null,
      sourceRecordCount: null,
      uiEligibility: "DISABLED" as const,
    };
    return Object.freeze({
      ...source,
      ...resolved.sourceOverrides,
      state: resolved.state,
      displayEligible: resolved.display,
      coverageDisplayEligible: resolved.coverageDisplay,
      exportEligible: resolved.exportable,
      stateReason: resolved.reason,
      acquisitionDate: resolved.acquisitionDate,
      sourceCrs: source.coordinate_reference || "Not declared",
      scaleOrResolution: source.geometry_or_resolution || "Not recorded",
      coverage: source.spatial_coverage || "Not recorded",
      transformationMethod: resolved.transformationMethod,
      geometryCount: resolved.geometryCount,
      sourceRecordCount: resolved.sourceRecordCount,
      uiEligibility: resolved.uiEligibility,
    });
  });
}

export function layerById(
  layers: RegisteredGisLayer[],
  layerId: string,
): RegisteredGisLayer | undefined {
  return layers.find((layer) => layer.layer_id === layerId);
}
