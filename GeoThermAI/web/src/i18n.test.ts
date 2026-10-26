import { describe, expect, it } from "vitest";
import { translate } from "./i18n";

describe("bilingual interface copy", () => {
  it("returns English labels", () => {
    expect(translate("en", "geothermalList")).toBe("Geothermal List");
    expect(translate("en", "heatmap")).toBe("Heatmap");
    expect(translate("en", "coverageFootprints")).toBe("Data-availability footprints");
  });

  it("returns Thai labels", () => {
    expect(translate("th", "geothermalList")).toBe("รายการแหล่งความร้อนใต้พิภพ");
    expect(translate("th", "heatmap")).toBe("ฮีตแมป");
    expect(translate("th", "reviewOverlay")).toBe("เรขาคณิตสำหรับตรวจสอบพิกัด");
  });

  it("falls back to the key for unknown copy", () => {
    expect(translate("th", "unknown.copy")).toBe("unknown.copy");
  });
});
