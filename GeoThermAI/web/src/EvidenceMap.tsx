import { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import { type Map as MapLibreMap, type MapMouseEvent } from "maplibre-gl";
import mapLibreWorkerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?url";
import {
  Crosshair,
  Expand,
  MapPin,
  MousePointer2,
  Ruler,
  Satellite,
  SquareDashedMousePointer,
  Trees,
  X,
} from "lucide-react";
import { toMapPoints } from "./data";
import {
  buildCoordinateReviewOverlay,
  buildCoverageFootprints,
} from "./coverageOverlays";
import { layerById } from "./gisRegistry";
import type { Translator } from "./i18n";
import {
  formatMeasurement,
  geodesicPathLengthMeters,
  geodesicPolygonAreaSquareMeters,
  type LngLat,
} from "./spatialAnalysis";
import type {
  GeothermalRecord,
  LocationInspection,
  MeasurementResult,
  RegisteredGisLayer,
  SpatialEvidenceIntersection,
} from "./types";

const basemapStyle: maplibregl.StyleSpecification = {
  version: 8,
  sources: {
    osm: {
      type: "raster",
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "© OpenStreetMap contributors",
    },
  },
  layers: [{ id: "osm", type: "raster", source: "osm" }],
};

const thailandCenter: [number, number] = [100.65, 13.5];

maplibregl.setWorkerUrl(mapLibreWorkerUrl);

type MapTool = "inspect" | "distance" | "area" | null;

export function EvidenceMap({
  records,
  allRecords,
  gisLayers,
  showProvisional = false,
  showGeology = false,
  showHeatFlow = false,
  showCoverage = false,
  showQualityReview = false,
  selectedRecordId,
  onSelect,
  onInspect,
  onPreview3D,
  onMeasurement,
  faultDistanceReason,
  t,
}: {
  records: GeothermalRecord[];
  allRecords: GeothermalRecord[];
  gisLayers: RegisteredGisLayer[];
  showProvisional?: boolean;
  showGeology?: boolean;
  showHeatFlow?: boolean;
  showCoverage?: boolean;
  showQualityReview?: boolean;
  selectedRecordId?: string;
  onSelect?: (record: GeothermalRecord) => void;
  onInspect?: (inspection: LocationInspection) => void;
  onPreview3D?: (location: { longitude: number; latitude: number }) => void;
  onMeasurement?: (measurement: MeasurementResult | null) => void;
  faultDistanceReason?: string;
  t: Translator;
}) {
  const container = useRef<HTMLDivElement>(null);
  const map = useRef<MapLibreMap | null>(null);
  const recordsRef = useRef(records);
  const selectRef = useRef(onSelect);
  const inspectRef = useRef(onInspect);
  const preview3DRef = useRef(onPreview3D);
  const toolRef = useRef<MapTool>(null);
  const [coordinates, setCoordinates] = useState("100.6500° E, 13.5000° N");
  const [tool, setTool] = useState<MapTool>(null);
  const [drawPoints, setDrawPoints] = useState<LngLat[]>([]);
  recordsRef.current = records;
  selectRef.current = onSelect;
  inspectRef.current = onInspect;
  preview3DRef.current = onPreview3D;
  toolRef.current = tool;

  useEffect(() => {
    if (!container.current || map.current) return;
    const instance = new maplibregl.Map({
      container: container.current,
      style: basemapStyle,
      center: thailandCenter,
      zoom: 4.55,
      minZoom: 4,
      maxZoom: 15,
      attributionControl: {},
    });
    map.current = instance;
    instance.addControl(
      new maplibregl.NavigationControl({ showCompass: false }),
      "top-left",
    );
    instance.on("mousemove", (event) =>
      setCoordinates(
        `${event.lngLat.lng.toFixed(4)}° E, ${event.lngLat.lat.toFixed(4)}° N`,
      ),
    );
    instance.on("load", () => {
      instance.addSource("observations", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      instance.addSource("ihfc-heat-flow", {
        type: "geojson",
        data: "/data/ihfc-thailand-points.geojson",
      });
      instance.addSource("measurement", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      instance.addSource("coverage-footprints", {
        type: "geojson",
        data: buildCoverageFootprints(),
      });
      instance.addSource("quality-review", {
        type: "geojson",
        data: buildCoordinateReviewOverlay(allRecords),
      });
      instance.addLayer({
        id: "coverage-fill",
        type: "fill",
        source: "coverage-footprints",
        layout: { visibility: "none" },
        paint: { "fill-color": "#1677ff", "fill-opacity": 0.08 },
      });
      instance.addLayer({
        id: "coverage-line",
        type: "line",
        source: "coverage-footprints",
        layout: { visibility: "none" },
        paint: {
          "line-color": "#0969da",
          "line-width": 2,
          "line-dasharray": [2, 1],
        },
      });
      instance.addLayer({
        id: "quality-review-line",
        type: "line",
        source: "quality-review",
        filter: ["==", ["geometry-type"], "LineString"],
        layout: { visibility: "none" },
        paint: {
          "line-color": "#d9363e",
          "line-width": 3,
          "line-dasharray": [2, 1],
        },
      });
      instance.addLayer({
        id: "quality-review-points",
        type: "circle",
        source: "quality-review",
        filter: ["==", ["geometry-type"], "Point"],
        layout: { visibility: "none" },
        paint: {
          "circle-radius": 8,
          "circle-color": "rgba(255,255,255,.25)",
          "circle-stroke-width": 3,
          "circle-stroke-color": "#d9363e",
        },
      });
      instance.addLayer({
        id: "measurement-fill",
        type: "fill",
        source: "measurement",
        filter: ["==", ["geometry-type"], "Polygon"],
        paint: { "fill-color": "#1677ff", "fill-opacity": 0.12 },
      });
      instance.addLayer({
        id: "measurement-line",
        type: "line",
        source: "measurement",
        paint: {
          "line-color": "#0969da",
          "line-width": 3,
          "line-dasharray": [2, 1],
        },
      });
      instance.addLayer({
        id: "ihfc-heat-flow-points",
        type: "circle",
        source: "ihfc-heat-flow",
        layout: { visibility: "none" },
        paint: {
          "circle-radius": 5,
          "circle-color": "#ffffff",
          "circle-stroke-width": 2,
          "circle-stroke-color": "#0f766e",
        },
      });
      instance.addLayer({
        id: "observation-points",
        type: "circle",
        source: "observations",
        paint: {
          "circle-radius": 6,
          "circle-color": [
            "case",
            ["get", "provisional"],
            "#f59e0b",
            "#e23b35",
          ],
          "circle-stroke-width": 2,
          "circle-stroke-color": "#ffffff",
        },
      });
      instance.addLayer({
        id: "selected-point",
        type: "circle",
        source: "observations",
        filter: ["==", ["get", "recordUid"], ""],
        paint: {
          "circle-radius": 11,
          "circle-color": "rgba(22,119,255,.12)",
          "circle-stroke-width": 3,
          "circle-stroke-color": "#1677ff",
        },
      });
      instance.on("click", "observation-points", (event: MapMouseEvent) => {
        const feature = instance.queryRenderedFeatures(event.point, {
          layers: ["observation-points"],
        })[0];
        const record = recordsRef.current.find(
          (candidate) =>
            candidate.record_uid === feature?.properties?.recordUid,
        );
        if (record) selectRef.current?.(record);
      });
      instance.on("mouseenter", "observation-points", () => {
        instance.getCanvas().style.cursor = "pointer";
      });
      instance.on("mouseleave", "observation-points", () => {
        instance.getCanvas().style.cursor = "";
      });
      instance.on("click", (event: MapMouseEvent) => {
        const activeTool = toolRef.current;
        if (!activeTool) {
          const marker = instance.queryRenderedFeatures(event.point, {
            layers: ["observation-points"],
          })[0];
          if (!marker) {
            preview3DRef.current?.({
              longitude: event.lngLat.lng,
              latitude: event.lngLat.lat,
            });
          }
          return;
        }
        if (activeTool === "inspect") {
          const queryLayers = [
            "geology-fill",
            "ihfc-heat-flow-points",
            "coverage-fill",
            "quality-review-line",
            "quality-review-points",
          ].filter(
            (layerId) =>
              instance.getLayer(layerId) &&
              instance.getLayoutProperty(layerId, "visibility") !== "none",
          );
          const rendered = queryLayers.length
            ? instance.queryRenderedFeatures(event.point, {
                layers: queryLayers,
              })
            : [];
          const seen = new Set<string>();
          const intersections = rendered.flatMap(
            (feature): SpatialEvidenceIntersection[] => {
              const sourceLayer = feature.layer.id;
              const key = `${sourceLayer}-${feature.properties?.objectId ?? feature.properties?.tileName ?? feature.properties?.recordUid ?? feature.properties?.recordId ?? feature.properties?.sourceRow}-${feature.properties?.representation ?? ""}`;
              if (seen.has(key)) return [];
              seen.add(key);
              if (sourceLayer === "geology-fill") {
                const layer = layerById(gisLayers, "DMR_ROCK_UNIT_250K_NORTH");
                const objectId = Number.isFinite(
                  Number(feature.properties?.objectId),
                )
                  ? Number(feature.properties?.objectId)
                  : null;
                return [
                  {
                    id: key,
                    layerId: layer?.layer_id ?? "DMR_ROCK_UNIT_250K_NORTH",
                    title: `DMR rock unit ${objectId ?? "—"}`,
                    detail: `Source symbol ${String(feature.properties?.symbol ?? "unclassified")}; DMR legend label ${String(feature.properties?.legendLabel ?? "not recorded")}; compilation year ${String(feature.properties?.year ?? "not recorded")}.`,
                    publisher:
                      layer?.publisher_or_source ??
                      "Department of Mineral Resources Thailand",
                    sourceUrl: layer?.source_url ?? "",
                    license:
                      layer?.license_or_permission_status ?? "Not verified",
                    scaleOrResolution:
                      layer?.scaleOrResolution ?? "Nominal 1:250,000",
                    warning:
                      "Authoritative service legend text, but still a contextual 1:250,000 boundary intersection—not a field-verified site-geology interpretation.",
                    exportEligible: layer?.exportEligible ?? false,
                  },
                ];
              }
              if (sourceLayer === "ihfc-heat-flow-points") {
                const layer = layerById(gisLayers, "IHFC_2024");
                const measurement = Number(
                  feature.properties?.heatFlowMilliwattsPerSquareMetre,
                );
                const duplicateCount = Number(
                  feature.properties?.duplicateCoordinateCount ?? 1,
                );
                return [
                  {
                    id: key,
                    layerId: layer?.layer_id ?? "IHFC_2024",
                    title: `IHFC measurement ${String(feature.properties?.recordId ?? feature.properties?.sourceRow ?? "—")}`,
                    detail: `Observed heat flow ${Number.isFinite(measurement) ? `${measurement} mW/m²` : "not recorded"}; method ${String(feature.properties?.heatFlowMethod ?? "not specified")}; quality code ${String(feature.properties?.qualityCode ?? "not recorded")}; ${duplicateCount} source row(s) share this coordinate.`,
                    publisher:
                      layer?.publisher_or_source ??
                      "International Heat Flow Commission",
                    sourceUrl:
                      layer?.source_url ??
                      "https://doi.org/10.5880/fidgeo.2024.014",
                    license: layer?.license_or_permission_status ?? "CC BY 4.0",
                    scaleOrResolution:
                      layer?.scaleOrResolution ?? "Point observations",
                    warning:
                      "Descriptive surface heat-flow observation only. Repeated coordinates are not merged; measurement uncertainty is missing, and no reservoir temperature or prospectivity is inferred.",
                    exportEligible: layer?.exportEligible ?? false,
                  },
                ];
              }
              if (sourceLayer === "coverage-fill") {
                const layer = layerById(gisLayers, "SRTM_HGT_NORTH");
                return [
                  {
                    id: key,
                    layerId: layer?.layer_id ?? "SRTM_HGT_NORTH",
                    title: `SRTM availability tile ${String(feature.properties?.tileName ?? "—")}`,
                    detail: String(
                      feature.properties?.description ??
                        "Local file-availability footprint.",
                    ),
                    publisher:
                      layer?.publisher_or_source ??
                      "AWS Terrain Tiles / SRTM distribution",
                    sourceUrl: layer?.source_url ?? "",
                    license:
                      layer?.license_or_permission_status ?? "Not verified",
                    scaleOrResolution:
                      layer?.scaleOrResolution ?? "1 arc-second HGT tile",
                    warning:
                      "Coverage metadata only; elevation, slope and hillshade are not displayed or interpreted.",
                    exportEligible: layer?.exportEligible ?? false,
                  },
                ];
              }
              return [
                {
                  id: key,
                  layerId: "COORDINATE_REVIEW",
                  title: `${String(feature.properties?.recordUid ?? "Review record")} — ${String(feature.properties?.title ?? "")}`,
                  detail: `${String(feature.properties?.representation ?? "Coordinate review representation.")} ${String(feature.properties?.note ?? "")}`,
                  publisher: String(
                    feature.properties?.sourceId ??
                      "Published observation source",
                  ),
                  sourceUrl: String(feature.properties?.sourceUrl ?? ""),
                  license: String(
                    feature.properties?.license ?? "Not recorded",
                  ),
                  scaleOrResolution:
                    "Record-level coordinate representations in EPSG:4326",
                  warning:
                    "Review geometry is explicitly non-authoritative and is not an observation or prospectivity result.",
                  exportEligible: false,
                },
              ];
            },
          );
          inspectRef.current?.({
            longitude: event.lngLat.lng,
            latitude: event.lngLat.lat,
            intersections,
            method:
              "Map click in EPSG:4326; intersections use currently rendered, display-eligible contextual or quality layers and are view/scale dependent.",
          });
          return;
        }
        setDrawPoints((current) => [
          ...current,
          [event.lngLat.lng, event.lngLat.lat],
        ]);
      });
    });
    return () => {
      instance.remove();
      map.current = null;
    };
  }, []);

  useEffect(() => {
    const instance = map.current;
    if (!instance) return;
    const apply = () => {
      const points = toMapPoints(records).filter(
        (point) =>
          !point.isCoordinateReview &&
          (showProvisional || !point.isProvisional),
      );
      const source = instance.getSource("observations") as
        maplibregl.GeoJSONSource | undefined;
      source?.setData({
        type: "FeatureCollection",
        features: points.map((point) => ({
          type: "Feature",
          properties: {
            recordUid: point.record_uid,
            provisional: point.isProvisional,
          },
          geometry: {
            type: "Point",
            coordinates: [point.longitude, point.latitude],
          },
        })),
      });
    };
    if (instance.getSource("observations")) apply();
    else instance.once("load", apply);
  }, [records, showProvisional]);

  useEffect(() => {
    const instance = map.current;
    if (!instance) return;
    const apply = () => {
      ["coverage-fill", "coverage-line"].forEach((layerId) =>
        instance.setLayoutProperty(
          layerId,
          "visibility",
          showCoverage ? "visible" : "none",
        ),
      );
      instance.setLayoutProperty(
        "ihfc-heat-flow-points",
        "visibility",
        showHeatFlow ? "visible" : "none",
      );
      ["quality-review-line", "quality-review-points"].forEach((layerId) =>
        instance.setLayoutProperty(
          layerId,
          "visibility",
          showQualityReview ? "visible" : "none",
        ),
      );
    };
    if (instance.getLayer("coverage-fill")) apply();
    else instance.once("load", apply);
  }, [showCoverage, showHeatFlow, showQualityReview]);

  useEffect(() => {
    const instance = map.current;
    if (!instance) return;
    const apply = () => {
      instance.setFilter("selected-point", [
        "==",
        ["get", "recordUid"],
        selectedRecordId ?? "",
      ]);
      const selected = recordsRef.current.find(
        (record) => record.record_uid === selectedRecordId,
      );
      const longitude = Number(selected?.derived_longitude_wgs84);
      const latitude = Number(selected?.derived_latitude_wgs84);
      if (selected && Number.isFinite(longitude) && Number.isFinite(latitude)) {
        instance.easeTo({
          center: [longitude, latitude],
          zoom: Math.max(instance.getZoom(), 7),
        });
      }
    };
    if (instance.getLayer("selected-point")) apply();
    else instance.once("load", apply);
  }, [selectedRecordId]);

  useEffect(() => {
    const source = map.current?.getSource("measurement") as
      maplibregl.GeoJSONSource | undefined;
    if (!source) return;
    const mutablePoints: GeoJSON.Position[] = drawPoints.map(
      ([longitude, latitude]) => [longitude, latitude],
    );
    const geometry: GeoJSON.Geometry | null =
      tool === "area" && drawPoints.length >= 3
        ? {
            type: "Polygon",
            coordinates: [[...mutablePoints, mutablePoints[0]]],
          }
        : drawPoints.length >= 2
          ? { type: "LineString", coordinates: mutablePoints }
          : null;
    source.setData({
      type: "FeatureCollection",
      features: geometry ? [{ type: "Feature", properties: {}, geometry }] : [],
    });
  }, [drawPoints, tool]);

  useEffect(() => {
    const instance = map.current;
    if (!instance) return;
    const controller = new AbortController();
    let idleHandler: (() => void) | null = null;
    const apply = async () => {
      if (showGeology && !instance.getSource("geology")) {
        performance.clearMarks("geothermai-geology-start");
        performance.clearMarks("geothermai-geology-layer-added");
        performance.clearMarks("geothermai-geology-visible");
        performance.clearMeasures("geothermai-geology-load-and-add");
        performance.clearMeasures("geothermai-geology-activation");
        performance.mark("geothermai-geology-start");
        const response = await fetch(
          "/data/dmr-rock-units-north.simplified.geojson",
          { signal: controller.signal },
        );
        if (!response.ok)
          throw new Error(`Geology asset unavailable: HTTP ${response.status}`);
        const geology = (await response.json()) as GeoJSON.FeatureCollection;
        if (controller.signal.aborted || !showGeology) return;
        instance.addSource("geology", { type: "geojson", data: geology });
        instance.addLayer(
          {
            id: "geology-fill",
            type: "fill",
            source: "geology",
            paint: {
              "fill-color": [
                "match",
                ["get", "symbol"],
                "CPk",
                "#edc86d",
                "TRgr",
                "#d19adf",
                "#86bea1",
              ],
              "fill-opacity": 0.24,
            },
          },
          "observation-points",
        );
        instance.addLayer(
          {
            id: "geology-line",
            type: "line",
            source: "geology",
            paint: {
              "line-color": "#486c5d",
              "line-opacity": 0.42,
              "line-width": 0.7,
            },
          },
          "observation-points",
        );
        performance.mark("geothermai-geology-layer-added");
        performance.measure(
          "geothermai-geology-load-and-add",
          "geothermai-geology-start",
          "geothermai-geology-layer-added",
        );
        idleHandler = () => {
          if (controller.signal.aborted || !instance.getLayer("geology-fill"))
            return;
          performance.mark("geothermai-geology-visible");
          performance.measure(
            "geothermai-geology-activation",
            "geothermai-geology-start",
            "geothermai-geology-visible",
          );
          idleHandler = null;
        };
        instance.once("idle", idleHandler);
      }
      if (!showGeology && instance.getLayer("geology-line")) {
        instance.removeLayer("geology-line");
        instance.removeLayer("geology-fill");
        instance.removeSource("geology");
      }
    };
    const run = () => {
      void apply().catch((error: unknown) => {
        if (!(error instanceof DOMException && error.name === "AbortError"))
          console.error(error);
      });
    };
    if (instance.getSource("observations")) run();
    else instance.once("load", run);
    return () => {
      controller.abort();
      if (idleHandler) instance.off("idle", idleHandler);
    };
  }, [showGeology]);

  const chooseTool = (next: MapTool) => {
    setTool((current) => (current === next ? null : next));
    setDrawPoints([]);
    onMeasurement?.(null);
  };
  const finishMeasurement = () => {
    if (tool === "distance" && drawPoints.length >= 2) {
      onMeasurement?.(
        formatMeasurement(
          "distance",
          geodesicPathLengthMeters(drawPoints),
          drawPoints.length,
        ),
      );
    } else if (tool === "area" && drawPoints.length >= 3) {
      onMeasurement?.(
        formatMeasurement(
          "area",
          geodesicPolygonAreaSquareMeters(drawPoints),
          drawPoints.length,
        ),
      );
    }
  };

  const resetView = () =>
    map.current?.flyTo({ center: thailandCenter, zoom: 4.55 });
  const fullscreen = async () => {
    if (!container.current) return;
    await container.current.parentElement?.requestFullscreen();
    map.current?.resize();
  };

  return (
    <div
      className="map-wrap"
      data-geology-visible={showGeology}
      data-heat-flow-visible={showHeatFlow}
      data-coverage-visible={showCoverage}
      data-quality-review-visible={showQualityReview}
    >
      <div ref={container} className="map-canvas" />
      <div className="basemap-switcher">
        <button className="active">
          <MapPin size={14} /> {t("mapBasemap")}
        </button>
        <button disabled title={t("awaitingRaster")}>
          <Satellite size={14} /> {t("satellite")}
        </button>
        <button disabled title={t("noTerrainRaster")}>
          <Trees size={14} /> {t("terrain")}
        </button>
      </div>
      <div className="map-actions">
        <button
          onClick={resetView}
          title={t("resetMap")}
          aria-label={t("resetMap")}
        >
          <Crosshair size={17} />
        </button>
        <button
          onClick={fullscreen}
          title={t("fullscreen")}
          aria-label={t("fullscreen")}
        >
          <Expand size={17} />
        </button>
      </div>
      <div className="spatial-toolbar" aria-label={t("spatialTools")}>
        <button
          className={tool === "inspect" ? "active" : ""}
          onClick={() => chooseTool("inspect")}
          aria-pressed={tool === "inspect"}
        >
          <MousePointer2 size={14} />
          {t("inspectLocation")}
        </button>
        <button
          className={tool === "distance" ? "active" : ""}
          onClick={() => chooseTool("distance")}
          aria-pressed={tool === "distance"}
        >
          <Ruler size={14} />
          {t("measureDistance")}
        </button>
        <button
          className={tool === "area" ? "active" : ""}
          onClick={() => chooseTool("area")}
          aria-pressed={tool === "area"}
        >
          <SquareDashedMousePointer size={14} />
          {t("measureArea")}
        </button>
        <button disabled title={faultDistanceReason ?? t("faultUnavailable")}>
          <MapPin size={14} />
          {t("mappedFaultDistance")}
        </button>
        {(tool === "distance" || tool === "area") && (
          <>
            <button
              onClick={finishMeasurement}
              disabled={drawPoints.length < (tool === "area" ? 3 : 2)}
            >
              {t("finishMeasurement")} ({drawPoints.length})
            </button>
            <button
              onClick={() => {
                setDrawPoints([]);
                onMeasurement?.(null);
              }}
              aria-label={t("clearMeasurement")}
            >
              <X size={14} />
            </button>
          </>
        )}
      </div>
      <div className="map-legend">
        <b>{t("evidenceLegend")}</b>
        <span>
          <i className="legend-dot consistent" /> {t("internallyConsistent")}
        </span>
        {showProvisional && (
          <span>
            <i className="legend-dot provisional" /> {t("provisionalDisplay")}
          </span>
        )}
        {showGeology && (
          <span>
            <i className="legend-fill" /> {t("geologyLegend")}
          </span>
        )}
        {showHeatFlow && (
          <span>
            <i className="legend-dot heat-flow" /> {t("heatFlowLegend")}
          </span>
        )}
        {showCoverage && (
          <span>
            <i className="legend-coverage" /> {t("coverageFootprints")}
          </span>
        )}
        {showQualityReview && (
          <span>
            <i className="legend-review" /> {t("reviewOverlay")}
          </span>
        )}
        <small>{t("unavailableLayers")}</small>
      </div>
      <div className="coordinate-readout">{coordinates}</div>
    </div>
  );
}
