// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("./EvidenceMap", () => ({
  EvidenceMap: ({
    records,
    showGeology,
    showHeatFlow,
    showCoverage,
    showQualityReview,
  }: {
    records: unknown[];
    showGeology: boolean;
    showHeatFlow: boolean;
    showCoverage: boolean;
    showQualityReview: boolean;
  }) => (
    <div
      data-testid="evidence-map-mock"
      data-record-count={records.length}
      data-geology={showGeology}
      data-heat-flow={showHeatFlow}
      data-coverage={showCoverage}
      data-quality-review={showQualityReview}
    />
  ),
}));

import { App } from "./App";

beforeEach(() => localStorage.clear());
afterEach(() => cleanup());

describe("Phase 2C workspace integration", () => {
  it("withholds provisional working coordinates until opt-in and preserves the opt-in across routes", async () => {
    render(
      <MemoryRouter initialEntries={["/evidence-map"]}>
        <App />
      </MemoryRouter>,
    );
    fireEvent.click(screen.getByRole("button", { name: "List" }));
    fireEvent.click(
      screen.getByRole("button", { name: /Yang Pa Kael Kok River/ }),
    );
    expect(
      screen.getByText(/Withheld because the coordinate disagreement/),
    ).toBeTruthy();
    expect(screen.queryByText("19.96313, 99.68025")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: /CP1Chumphon/ }));
    expect(
      screen.getByText(/Hidden until provisional southern coordinates/),
    ).toBeTruthy();
    expect(screen.queryByText("9.72504, 99.11143")).toBeNull();

    const optIn = screen.getByRole("checkbox", {
      name: /Provisional coordinates/,
    }) as HTMLInputElement;
    fireEvent.click(optIn);
    expect(optIn.checked).toBe(true);
    expect(screen.getByText("9.72504, 99.11143")).toBeTruthy();

    fireEvent.click(screen.getByRole("link", { name: "Data Quality" }));
    fireEvent.click(screen.getByRole("link", { name: "Evidence Map" }));
    expect(
      (
        screen.getByRole("checkbox", {
          name: /Provisional coordinates/,
        }) as HTMLInputElement
      ).checked,
    ).toBe(true);
    expect(
      (await screen.findByTestId("evidence-map-mock")).getAttribute(
        "data-record-count",
      ),
    ).toBe("45");
  });

  it("connects eligible layer toggles to map state and exposes exact unavailable feedback", async () => {
    render(
      <MemoryRouter initialEntries={["/evidence-map"]}>
        <App />
      </MemoryRouter>,
    );
    const map = await screen.findByTestId("evidence-map-mock");
    const geology = screen.getByRole("checkbox", { name: /Geological units/ });
    const heatFlow = screen.getByRole("checkbox", {
      name: /IHFC heat-flow observations/,
    });
    const coverage = screen.getByRole("checkbox", {
      name: /Data-availability footprints/,
    });
    const quality = screen.getByRole("checkbox", {
      name: /Coordinate-review geometry/,
    });
    fireEvent.click(geology);
    fireEvent.click(heatFlow);
    fireEvent.click(coverage);
    fireEvent.click(quality);
    expect(map.getAttribute("data-geology")).toBe("true");
    expect(map.getAttribute("data-heat-flow")).toBe("true");
    expect(map.getAttribute("data-coverage")).toBe("true");
    expect(map.getAttribute("data-quality-review")).toBe("true");
    fireEvent.click(geology);
    expect(map.getAttribute("data-geology")).toBe("false");

    const faults = screen.getByRole("checkbox", {
      name: /Active faults/,
    }) as HTMLInputElement;
    expect(faults.disabled).toBe(true);
    expect(
      faults.getAttribute("aria-label") ?? faults.closest("label")?.textContent,
    ).toMatch(/DMR clarification required/);
    fireEvent.click(screen.getByRole("button", { name: "Download" }));
    expect(
      (
        screen.getByRole("button", {
          name: "Download filtered data",
        }) as HTMLButtonElement
      ).disabled,
    ).toBe(true);
    expect(screen.getByText(/Raw evidence export blocked/)).toBeTruthy();
  });
});
