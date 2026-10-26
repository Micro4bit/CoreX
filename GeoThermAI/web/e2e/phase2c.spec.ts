import { expect, test } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

test("provisional coordinates require opt-in and the choice survives navigation", async ({ page }) => {
  await page.goto("/evidence-map");
  await expect(page.getByText(/^14 records$/).first()).toBeVisible();
  await page.getByRole("button", { name: "List" }).click();
  await page.getByRole("button", { name: /CP1 Chumphon/ }).click();
  await expect(page.getByText(/Hidden until provisional southern coordinates/)).toBeVisible();
  await expect(page.getByText("9.72504, 99.11143")).toHaveCount(0);

  const optIn = page.getByRole("checkbox", { name: /Provisional coordinates/ });
  await optIn.check();
  await expect(page.getByText("9.72504, 99.11143")).toBeVisible();
  await page.getByRole("link", { name: "Data Quality" }).click();
  await page.getByRole("link", { name: "Evidence Map" }).click();
  await expect(page.getByRole("checkbox", { name: /Provisional coordinates/ })).toBeChecked();
  await expect(page.getByText(/^45 records$/).first()).toBeVisible();
});

test("layer toggles, disabled reasons, export gate and coverage legends are wired", async ({ page }) => {
  await page.goto("/evidence-map");
  const coverage = page.getByRole("checkbox", { name: /Data-availability footprints/ });
  const quality = page.getByRole("checkbox", { name: /Coordinate-review geometry/ });
  const geology = page.getByRole("checkbox", { name: /Geological units/ });
  const heatFlow = page.getByRole("checkbox", { name: /IHFC heat-flow observations/ });
  await coverage.check();
  await quality.check();
  await geology.check();
  await heatFlow.check();
  await expect(page.locator(".map-wrap")).toHaveAttribute("data-coverage-visible", "true");
  await expect(page.locator(".map-wrap")).toHaveAttribute("data-quality-review-visible", "true");
  await expect(page.locator(".map-wrap")).toHaveAttribute("data-heat-flow-visible", "true");
  await expect(page.getByText("Data-availability footprints", { exact: true }).last()).toBeVisible();
  await expect(page.getByText("Coordinate-review geometry", { exact: true }).last()).toBeVisible();
  await expect(page.getByText("DMR rock units — descriptive")).toBeVisible();
  await expect(page.getByText("IHFC heat-flow — observed points")).toBeVisible();
  await geology.uncheck();
  await expect(page.locator(".map-wrap")).toHaveAttribute("data-geology-visible", "false");

  const faults = page.getByRole("checkbox", { name: /Active faults/ });
  await expect(faults).toBeDisabled();
  await expect(faults).toHaveAccessibleName(/DMR clarification required/);

  await page.getByRole("button", { name: "Download", exact: true }).click();
  await expect(page.getByRole("button", { name: "Download filtered data" })).toBeDisabled();

  await page.getByRole("button", { name: "Evidence" }).click();
  await expect(page.getByRole("button", { name: "Export evidence detail" })).toBeDisabled();
  await page.getByRole("button", { name: "Inspect location" }).click();
  const canvas = page.locator(".maplibregl-canvas");
  const box = await canvas.boundingBox();
  if (!box) throw new Error("Map canvas was not measurable");
  await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
  await expect(page.getByText(/SRTM availability tile/)).toBeVisible();
  await expect(page.getByText("Publisher / source").first()).toBeVisible();
  await expect(page.getByRole("button", { name: "Export evidence detail" })).toBeDisabled();
  await page.screenshot({ path: path.resolve("screenshots/phase2c-coverage-quality-2026-10-24.png"), fullPage: true });
  await page.screenshot({ path: path.resolve("screenshots/phase2d-ihfc-layer-2026-10-26.png"), fullPage: true });
});

test("controls remain keyboard operable at a small viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/evidence-map");
  const coverage = page.getByRole("checkbox", { name: /Data-availability footprints/ });
  await coverage.focus();
  await page.keyboard.press("Space");
  await expect(coverage).toBeChecked();
  await expect(page.getByRole("button", { name: "Inspect location" })).toBeVisible();
  await page.screenshot({ path: path.resolve("screenshots/phase2c-mobile-complete-2026-10-24.png"), fullPage: true });
});

test("performance profile captures load, geology readiness, heap, filtering and pan frames", async ({ page }) => {
  await page.goto("/evidence-map", { waitUntil: "load" });
  const beforeHeap = await page.evaluate(() => {
    const memory = (performance as Performance & { memory?: { usedJSHeapSize: number } }).memory;
    return memory?.usedJSHeapSize ?? null;
  });
  await page.getByRole("checkbox", { name: /Geological units/ }).check();
  await page.waitForFunction(() => performance.getEntriesByName("geothermai-geology-activation").length > 0);
  const geology = await page.evaluate(() => ({
    loadAndAddMs: performance.getEntriesByName("geothermai-geology-load-and-add").at(-1)?.duration ?? null,
    visibleReadyMs: performance.getEntriesByName("geothermai-geology-activation").at(-1)?.duration ?? null,
  }));
  const afterHeap = await page.evaluate(() => {
    const memory = (performance as Performance & { memory?: { usedJSHeapSize: number } }).memory;
    return memory?.usedJSHeapSize ?? null;
  });

  const filterStarted = performance.now();
  await page.getByRole("checkbox", { name: /Provisional coordinates/ }).check();
  await expect(page.getByText(/^45 records$/).first()).toBeVisible();
  const provisionalFilterMs = performance.now() - filterStarted;

  await page.evaluate(() => {
    const target = window as typeof window & { __phase2cFrames?: number[]; __phase2cFrameStart?: number };
    target.__phase2cFrames = [];
    target.__phase2cFrameStart = performance.now();
    const sample = (timestamp: number) => {
      target.__phase2cFrames!.push(timestamp);
      if (timestamp - target.__phase2cFrameStart! < 1_200) requestAnimationFrame(sample);
    };
    requestAnimationFrame(sample);
  });
  const canvas = page.locator(".maplibregl-canvas");
  const box = await canvas.boundingBox();
  if (!box) throw new Error("Map canvas was not measurable");
  await page.mouse.move(box.x + box.width * 0.65, box.y + box.height * 0.5);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width * 0.35, box.y + box.height * 0.5, { steps: 30 });
  await page.mouse.up();
  await page.waitForTimeout(1_250);
  const frameProfile = await page.evaluate(() => {
    const frames = (window as typeof window & { __phase2cFrames?: number[] }).__phase2cFrames ?? [];
    const gaps = frames.slice(1).map((timestamp, index) => timestamp - frames[index]);
    const duration = frames.length > 1 ? frames.at(-1)! - frames[0] : 0;
    return { sampleCount: frames.length, approximateFps: duration > 0 ? (frames.length - 1) * 1000 / duration : null, maxFrameGapMs: gaps.length ? Math.max(...gaps) : null };
  });
  const navigation = await page.evaluate(() => {
    const entry = performance.getEntriesByType("navigation")[0] as PerformanceNavigationTiming;
    const scripts = performance.getEntriesByType("resource").filter((resource) => resource.name.includes("/src/") || resource.name.includes("/assets/")).reduce((sum, resource) => sum + ((resource as PerformanceResourceTiming).transferSize || 0), 0);
    return { domInteractiveMs: entry.domInteractive, loadEventMs: entry.loadEventEnd, transferredScriptBytes: scripts };
  });
  const result = {
    runAt: new Date().toISOString(),
    environment: "Local Playwright Chromium against Vite development server; single run, not cross-browser.",
    navigation,
    geology,
    heap: { beforeBytes: beforeHeap, afterBytes: afterHeap, deltaBytes: beforeHeap !== null && afterHeap !== null ? afterHeap - beforeHeap : null },
    provisionalFilterMs,
    panFrameProfile: frameProfile,
  };
  await mkdir(path.resolve("test-results"), { recursive: true });
  await writeFile(path.resolve("test-results/phase2c-performance.json"), `${JSON.stringify(result, null, 2)}\n`);
  expect(geology.visibleReadyMs).not.toBeNull();
  expect(frameProfile.sampleCount).toBeGreaterThan(10);
});
