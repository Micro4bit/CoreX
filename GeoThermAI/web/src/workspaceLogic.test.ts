import { describe, expect, it } from "vitest";
import { loadAppData, toMapPoints } from "./data";
import {
  calculateMetrics,
  filterRecords,
  type WorkspaceFilterState,
} from "./workspaceLogic";

const records = loadAppData().records;
const layers = loadAppData().layers;
const defaults: WorkspaceFilterState = {
  region: "All Thailand",
  showConsistent: true,
  showProvisional: false,
  missingTemperatureOnly: false,
  sourceConflictsOnly: false,
  showGeology: false,
  showHeatFlow: false,
  showCoverage: false,
  showQualityReview: false,
};

describe("GeoThermAI Phase 1C data contract", () => {
  it("loads the real registry and preserves unique record identifiers", () => {
    expect(records).toHaveLength(47);
    expect(new Set(records.map((record) => record.record_uid)).size).toBe(47);
  });

  it("drops structurally blank CSV rows without fabricating GIS inventory entries", () => {
    expect(layers.length).toBeGreaterThan(0);
    expect(layers.every((layer) => Boolean(layer.layer_id))).toBe(true);
  });

  it("calculates KPI and quality counts from loaded records", () => {
    expect(calculateMetrics(records)).toMatchObject({
      totalRecords: 47,
      sources: 2,
      qualityFlags: 33,
      provisionalValidationUnits: 18,
      coordinateReview: 2,
      provisionalCoordinates: 31,
      missingTemperature: 2,
      sourceConflicts: 32,
    });
  });

  it("excludes provisional and coordinate-review records by default", () => {
    const result = filterRecords(records, defaults);
    expect(result).toHaveLength(14);
    expect(
      result.every(
        (record) =>
          record.coordinate_validation_status === "CRS_AND_DMS_CONSISTENT",
      ),
    ).toBe(true);
  });

  it("requires explicit opt-in before provisional southern locations are returned", () => {
    const result = filterRecords(records, {
      ...defaults,
      showProvisional: true,
    });
    expect(result).toHaveLength(45);
    expect(
      result.filter((record) => record.source_region === "Southern Thailand"),
    ).toHaveLength(31);
  });

  it("always excludes unresolved CR_02 and CM_16 map records", () => {
    const result = filterRecords(records, {
      ...defaults,
      showProvisional: true,
    });
    expect(result.map((record) => record.record_uid)).not.toContain(
      "NORTH_WOOD2014_CR_02",
    );
    expect(result.map((record) => record.record_uid)).not.toContain(
      "NORTH_WOOD2014_CM_16",
    );
  });

  it("applies region and missing-temperature filters", () => {
    const north = filterRecords(records, { ...defaults, region: "North" });
    const missing = filterRecords(records, {
      ...defaults,
      missingTemperatureOnly: true,
    });
    expect(north).toHaveLength(14);
    expect(missing.every((record) => !record.surface_temperature_c)).toBe(true);
  });

  it("never promotes coordinate-review records into map points", () => {
    const points = toMapPoints(records);
    expect(points.filter((point) => point.isCoordinateReview)).toHaveLength(2);
    expect(
      points.filter(
        (point) => !point.isCoordinateReview && !point.isProvisional,
      ),
    ).toHaveLength(14);
  });
});
