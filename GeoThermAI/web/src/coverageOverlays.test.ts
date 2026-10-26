import { describe, expect, it } from "vitest";
import { loadAppData } from "./data";
import { buildCoordinateReviewOverlay, buildCoverageFootprints } from "./coverageOverlays";
import { geodesicDistanceMeters, parseDmsCoordinate } from "./spatialAnalysis";

describe("coverage and coordinate-quality overlays", () => {
  it("derives five exact one-degree availability footprints from inspected HGT filenames", () => {
    const footprints = buildCoverageFootprints();
    expect(footprints.features).toHaveLength(5);
    expect(footprints.features.map((feature) => feature.properties.tileName)).toEqual(["N17E099", "N18E099", "N19E099", "N20E099", "N19E098"]);
    expect(footprints.features[0].geometry.coordinates[0]).toEqual([[99, 17], [100, 17], [100, 18], [99, 18], [99, 17]]);
  });

  it("shows review representations without promoting them into observation points", () => {
    const overlay = buildCoordinateReviewOverlay(loadAppData().records);
    const recordIds = new Set(overlay.features.map((feature) => feature.properties.recordUid));
    expect(recordIds).toEqual(new Set(["NORTH_WOOD2014_CR_02", "NORTH_WOOD2014_CM_16"]));
    expect(overlay.features.filter((feature) => feature.geometry.type === "LineString")).toHaveLength(1);
    expect(overlay.features.every((feature) => /authoritative/i.test(feature.properties.representation))).toBe(true);
  });

  it("parses the CR_02 DMS comparator and preserves the documented kilometre-scale disagreement", () => {
    const longitude = parseDmsCoordinate("099 40 48.65 E");
    const latitude = parseDmsCoordinate("19 56 46.35 N");
    expect(longitude).toBeCloseTo(99.6801806, 6);
    expect(latitude).toBeCloseTo(19.9462083, 6);
    expect(geodesicDistanceMeters([99.68025428, 19.96312509], [longitude!, latitude!])).toBeGreaterThan(1_800);
  });
});
