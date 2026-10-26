import Papa from "papaparse";
import type { AppData, GeothermalRecord, GisLayer, MapPoint, SourceRecord } from "./types";

import registryText from "../../tasks/phase_1c_label_expansion_gis_foundation/geothermal_label_master_registry.csv?raw";
import sourceText from "../../tasks/phase_1c_label_expansion_gis_foundation/expanded_geothermal_source_inventory.csv?raw";
import layerText from "../../tasks/phase_1c_label_expansion_gis_foundation/verified_gis_layer_inventory.csv?raw";

function parseCsv<T>(text: string): T[] {
  return Papa.parse<T>(text, { header: true, skipEmptyLines: "greedy" }).data.filter((row) =>
    Object.values(row as Record<string, unknown>).some((value) => String(value ?? "").trim()),
  );
}

export function loadAppData(): AppData {
  return {
    records: parseCsv<GeothermalRecord>(registryText),
    sources: parseCsv<SourceRecord>(sourceText),
    layers: parseCsv<GisLayer>(layerText),
  };
}

export function toMapPoints(records: GeothermalRecord[]): MapPoint[] {
  return records.flatMap((record) => {
    const longitude = Number(record.derived_longitude_wgs84);
    const latitude = Number(record.derived_latitude_wgs84);
    if (!Number.isFinite(longitude) || !Number.isFinite(latitude)) return [];
    const status = record.coordinate_validation_status;
    return [{
      ...record,
      longitude,
      latitude,
      isCoordinateReview: status === "CRS_INFERRED_DMS_MISMATCH_UNRESOLVED" || status === "CRS_INFERRED_DMS_MISSING",
      isProvisional: status === "CRS_INFERRED_NO_DMS_COMPARATOR",
    }];
  });
}

export function sourceForRecord(record: GeothermalRecord | null, sources: SourceRecord[]): SourceRecord | undefined {
  return record ? sources.find((source) => source.source_id === record.source_id) : undefined;
}
