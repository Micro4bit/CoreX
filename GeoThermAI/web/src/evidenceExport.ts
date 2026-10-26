import type { GeothermalRecord, LocationInspection, SourceRecord } from "./types";

export interface ExportDecision {
  allowed: boolean;
  reason: string;
  payload?: Record<string, unknown>;
}

export function evaluateEvidenceExport(record: GeothermalRecord, source?: SourceRecord): ExportDecision {
  const reuse = source?.license_or_reuse_status || record.license_or_reuse_status;
  if (!reuse || /NOT_STATED|NOT_VERIFIED|not assessed/i.test(reuse)) {
    return { allowed: false, reason: `Raw evidence export blocked: reuse permission is unresolved (${reuse || "not recorded"}). Citation metadata remains visible in the UI.` };
  }
  return {
    allowed: true,
    reason: `Export allowed under recorded terms: ${reuse}`,
    payload: {
      exportType: "descriptive-evidence-detail",
      scientificBoundary: "Published surface observation; not a reservoir, prospectivity score, or prediction.",
      record: { ...record },
      source: source ? { ...source } : null,
      missingEvidence: [
        !record.surface_temperature_c && "surface_temperature_c",
        !record.source_latitude_dms && "source_latitude_dms",
        !record.source_longitude_dms && "source_longitude_dms",
      ].filter(Boolean),
    },
  };
}

export function evaluateLocationExport(inspection: LocationInspection): ExportDecision {
  const restricted = inspection.intersections.find((intersection) => !intersection.exportEligible);
  if (restricted) {
    return { allowed: false, reason: `Location export blocked: ${restricted.layerId} has unresolved or restricted reuse terms.` };
  }
  return {
    allowed: true,
    reason: "Location inspection export is eligible because it contains only the user's WGS84 click and export-eligible metadata.",
    payload: {
      exportType: "descriptive-location-inspection",
      scientificBoundary: "Evidence availability and descriptive intersections only; absence is not a true negative or geothermal prospectivity result.",
      location: { longitude: inspection.longitude, latitude: inspection.latitude, crs: "EPSG:4326" },
      method: inspection.method,
      intersections: inspection.intersections.map((intersection) => ({ ...intersection })),
      missingEvidence: inspection.intersections.length ? [] : ["No display-eligible layer intersection was found at the rendered click point."],
    },
  };
}

export function serializeEvidencePayload(payload: unknown): string {
  return `${JSON.stringify(payload, null, 2)}\n`;
}
