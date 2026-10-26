import type { GeothermalRecord } from "./types";

export interface WorkspaceFilterState {
  region: "All Thailand" | "North" | "South";
  showConsistent: boolean;
  showProvisional: boolean;
  missingTemperatureOnly: boolean;
  sourceConflictsOnly: boolean;
  showGeology: boolean;
  showHeatFlow: boolean;
  showCoverage: boolean;
  showQualityReview: boolean;
}

export const conflictRecordIds = new Set(["NORTH_WOOD2014_CR_02"]);

export const isConsistent = (record: GeothermalRecord) =>
  record.coordinate_validation_status === "CRS_AND_DMS_CONSISTENT";
export const isProvisional = (record: GeothermalRecord) =>
  record.coordinate_validation_status === "CRS_INFERRED_NO_DMS_COMPARATOR";
export const needsReview = (record: GeothermalRecord) =>
  !isConsistent(record) && !isProvisional(record);

export function hasDocumentedSourceConflict(record: GeothermalRecord): boolean {
  return (
    conflictRecordIds.has(record.record_uid) ||
    record.source_id === "NGANSOM_DUERRAST_2021_TABLE1"
  );
}

export function filterRecords(
  records: GeothermalRecord[],
  filters: WorkspaceFilterState,
): GeothermalRecord[] {
  return records.filter((record) => {
    const expectedRegion =
      filters.region === "North"
        ? "Northern Thailand"
        : filters.region === "South"
          ? "Southern Thailand"
          : null;
    if (expectedRegion && record.source_region !== expectedRegion) return false;
    if (filters.missingTemperatureOnly && record.surface_temperature_c.trim())
      return false;
    if (filters.sourceConflictsOnly && !hasDocumentedSourceConflict(record))
      return false;
    if (isConsistent(record)) return filters.showConsistent;
    if (isProvisional(record)) return filters.showProvisional;
    return false;
  });
}

export function calculateMetrics(records: GeothermalRecord[]) {
  return {
    totalRecords: records.length,
    sources: new Set(records.map((record) => record.source_id)).size,
    qualityFlags: records.filter((record) => !isConsistent(record)).length,
    provisionalValidationUnits: new Set(
      records.map((record) => record.validation_cluster_id).filter(Boolean),
    ).size,
    coordinateReview: records.filter(needsReview).length,
    provisionalCoordinates: records.filter(isProvisional).length,
    missingTemperature: records.filter(
      (record) => !record.surface_temperature_c.trim(),
    ).length,
    sourceConflicts: records.filter(hasDocumentedSourceConflict).length,
  };
}
