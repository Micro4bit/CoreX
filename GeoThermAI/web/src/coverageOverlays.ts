import type { GeothermalRecord } from "./types";
import { parseDmsCoordinate } from "./spatialAnalysis";

interface CoverageProperties {
  layerId: "SRTM_HGT_NORTH";
  tileName: string;
  description: string;
}

interface ReviewProperties {
  recordUid: string;
  title: string;
  status: string;
  note: string;
  sourceId: string;
  sourceUrl: string;
  license: string;
  representation: string;
}

const hgtTiles = [
  { tileName: "N17E099", west: 99, south: 17 },
  { tileName: "N18E099", west: 99, south: 18 },
  { tileName: "N19E099", west: 99, south: 19 },
  { tileName: "N20E099", west: 99, south: 20 },
  { tileName: "N19E098", west: 98, south: 19 },
] as const;

export function buildCoverageFootprints(): GeoJSON.FeatureCollection<GeoJSON.Polygon, CoverageProperties> {
  return {
    type: "FeatureCollection",
    features: hgtTiles.map(({ tileName, west, south }) => ({
      type: "Feature",
      properties: {
        layerId: "SRTM_HGT_NORTH",
        tileName,
        description: "Local HGT file availability footprint derived from the standard tile filename; no terrain raster is displayed.",
      },
      geometry: {
        type: "Polygon",
        coordinates: [[[west, south], [west + 1, south], [west + 1, south + 1], [west, south + 1], [west, south]]],
      },
    })),
  };
}

export function buildCoordinateReviewOverlay(records: GeothermalRecord[]): GeoJSON.FeatureCollection<GeoJSON.Geometry, ReviewProperties> {
  const reviewRecords = records.filter((record) =>
    record.coordinate_validation_status === "CRS_INFERRED_DMS_MISMATCH_UNRESOLVED"
    || record.coordinate_validation_status === "CRS_INFERRED_DMS_MISSING",
  );
  const features: Array<GeoJSON.Feature<GeoJSON.Geometry, ReviewProperties>> = [];

  reviewRecords.forEach((record) => {
    const workingLongitude = Number(record.derived_longitude_wgs84);
    const workingLatitude = Number(record.derived_latitude_wgs84);
    if (!Number.isFinite(workingLongitude) || !Number.isFinite(workingLatitude)) return;
    const baseProperties: ReviewProperties = {
      recordUid: record.record_uid,
      title: record.source_site_name || record.source_record_code,
      status: record.coordinate_validation_status,
      note: record.coordinate_quality_note,
      sourceId: record.source_id,
      sourceUrl: record.source_url,
      license: record.license_or_reuse_status,
      representation: "Working UTM representation; not an authoritative observation location.",
    };
    features.push({
      type: "Feature",
      properties: baseProperties,
      geometry: { type: "Point", coordinates: [workingLongitude, workingLatitude] },
    });

    const dmsLongitude = parseDmsCoordinate(record.source_longitude_dms);
    const dmsLatitude = parseDmsCoordinate(record.source_latitude_dms);
    if (dmsLongitude === null || dmsLatitude === null) return;
    features.push({
      type: "Feature",
      properties: { ...baseProperties, representation: "Unresolved line between the working UTM transform and published DMS comparator; neither endpoint is promoted as authoritative." },
      geometry: { type: "LineString", coordinates: [[workingLongitude, workingLatitude], [dmsLongitude, dmsLatitude]] },
    });
    features.push({
      type: "Feature",
      properties: { ...baseProperties, representation: "Published DMS comparator endpoint; not an authoritative observation location while the disagreement is unresolved." },
      geometry: { type: "Point", coordinates: [dmsLongitude, dmsLatitude] },
    });
  });

  return { type: "FeatureCollection", features };
}
