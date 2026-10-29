import { describe, expect, it } from "vitest";
import { loadAppData } from "./data";
import { layerById, registerGisLayers } from "./gisRegistry";

describe("Phase 2D GIS layer registry", () => {
  it("assigns permission and geometry states from inspected inventory", () => {
    const layers = registerGisLayers(loadAppData().layers);
    expect(layerById(layers, "DMR_ROCK_UNIT_250K_NORTH")).toMatchObject({
      state: "AVAILABLE_VERIFIED",
      displayEligible: true,
      coverageDisplayEligible: true,
      exportEligible: false,
      geometryCount: 1266,
      sourceCrs: expect.stringContaining("32647"),
      uiEligibility: "DISPLAY_CONTEXT_ONLY",
    });
    expect(layerById(layers, "DMR_GEOL_STR_250K_NORTH")).toMatchObject({
      state: "UNAVAILABLE_GEOMETRY",
      displayEligible: false,
    });
    expect(layerById(layers, "DMR_ACTIVEFAULT_ZONE")).toMatchObject({
      state: "RESTRICTED_REUSE",
      displayEligible: false,
      exportEligible: false,
    });
    expect(layerById(layers, "IHFC_2024")).toMatchObject({
      state: "AVAILABLE_VERIFIED",
      displayEligible: true,
      exportEligible: true,
      geometryCount: 154,
      sourceRecordCount: 91182,
    });
    expect(layerById(layers, "SRTM_HGT_NORTH")).toMatchObject({
      state: "AVAILABLE_VERIFIED",
      displayEligible: false,
      coverageDisplayEligible: true,
      geometryCount: 5,
    });
    expect(layerById(layers, "LANDSAT_C2_L2_ST")).toMatchObject({
      state: "NOT_LOADED",
      displayEligible: false,
      coverageDisplayEligible: false,
      geometryCount: 0,
    });
    expect(layerById(layers, "DNP_PROTECTED_AREAS")).toMatchObject({
      state: "METADATA_ONLY",
      displayEligible: false,
      exportEligible: false,
      uiEligibility: "DISABLED",
    });
    expect(layerById(layers, "ONWR_WATERSHED_CLASSES")).toMatchObject({
      state: "METADATA_ONLY",
      displayEligible: false,
      exportEligible: false,
      uiEligibility: "DISABLED",
    });
    expect(layerById(layers, "RFD_FOREST_RESERVES")).toMatchObject({
      state: "METADATA_ONLY",
      displayEligible: false,
      exportEligible: false,
      uiEligibility: "DISABLED",
    });
    expect(layerById(layers, "DGR_GROUNDWATER_SENSITIVITY")).toMatchObject({
      state: "METADATA_ONLY",
      displayEligible: false,
      exportEligible: false,
      uiEligibility: "DISABLED",
    });
    expect(
      layers.every(
        (layer) =>
          layer.acquisitionDate &&
          layer.transformationMethod &&
          layer.scaleOrResolution &&
          layer.coverage,
      ),
    ).toBe(true);
  });

  it("does not mutate source inventory fields", () => {
    const source = loadAppData().layers;
    const before = JSON.stringify(source);
    registerGisLayers(source);
    expect(JSON.stringify(source)).toBe(before);
  });
});
