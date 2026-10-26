import { describe, expect, it } from "vitest";
import { formatMeasurement, geodesicDistanceMeters, geodesicPathLengthMeters, geodesicPolygonAreaSquareMeters, parseDmsCoordinate } from "./spatialAnalysis";

describe("descriptive WGS84 spatial measurements", () => {
  it("calculates a known equatorial degree distance and converts units", () => {
    const metres = geodesicDistanceMeters([0, 0], [1, 0]);
    expect(metres).toBeCloseTo(111_195.08, 0);
    expect(geodesicPathLengthMeters([[0, 0], [0.5, 0], [1, 0]])).toBeCloseTo(metres, 5);
    expect(formatMeasurement("distance", metres, 2)).toMatchObject({ unit: "km", value: expect.closeTo(111.195, 2), crs: "EPSG:4326" });
  });

  it("calculates a known synthetic one-degree square area", () => {
    const area = geodesicPolygonAreaSquareMeters([[0, 0], [1, 0], [1, 1], [0, 1]]);
    expect(area).toBeGreaterThan(12_300_000_000);
    expect(area).toBeLessThan(12_400_000_000);
    expect(formatMeasurement("area", area, 4).unit).toBe("km²");
  });

  it("parses cardinal DMS values and rejects malformed values", () => {
    expect(parseDmsCoordinate("19 30 00 N")).toBe(19.5);
    expect(parseDmsCoordinate("099 30 00 W")).toBe(-99.5);
    expect(parseDmsCoordinate("19 99 00 N")).toBeNull();
  });
});
