import { describe, expect, it } from "vitest";
import { loadAppData, sourceForRecord } from "./data";
import { evaluateEvidenceExport, evaluateLocationExport, serializeEvidencePayload } from "./evidenceExport";

describe("evidence export licensing gate", () => {
  it("blocks current registry rows whose redistribution permission was not assessed", () => {
    const data = loadAppData();
    const record = data.records[0];
    const decision = evaluateEvidenceExport(record, sourceForRecord(record, data.sources));
    expect(decision.allowed).toBe(false);
    expect(decision.reason).toMatch(/permission is unresolved/i);
  });

  it("includes provenance and scientific limits when permission is explicit", () => {
    const data = loadAppData();
    const record = data.records[0];
    const source = { ...sourceForRecord(record, data.sources)!, license_or_reuse_status: "CC BY 4.0" };
    const decision = evaluateEvidenceExport(record, source);
    expect(decision.allowed).toBe(true);
    expect(decision.payload).toMatchObject({ exportType: "descriptive-evidence-detail", record: { record_uid: record.record_uid }, source: { source_id: record.source_id } });
    expect(decision.payload).not.toHaveProperty("prospectivityScore");
    expect(serializeEvidencePayload(decision.payload)).toContain("descriptive-evidence-detail");
  });

  it("exports an empty location inspection but blocks intersections with unresolved reuse", () => {
    const base = { longitude: 100, latitude: 18, method: "Rendered click in EPSG:4326", intersections: [] };
    expect(evaluateLocationExport(base)).toMatchObject({ allowed: true, payload: { exportType: "descriptive-location-inspection" } });
    expect(evaluateLocationExport({ ...base, intersections: [{ id: "x", layerId: "DMR_ROCK_UNIT_250K_NORTH", title: "Context", detail: "Context", publisher: "DMR", sourceUrl: "https://example.test", license: "NOT_VERIFIED", scaleOrResolution: "1:250,000", warning: "Context only", exportEligible: false }] })).toMatchObject({ allowed: false, reason: expect.stringContaining("DMR_ROCK_UNIT_250K_NORTH") });
  });
});
