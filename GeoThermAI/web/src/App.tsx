import {
  lazy,
  Suspense,
  useEffect,
  useMemo,
  useState,
  type Dispatch,
  type SetStateAction,
} from "react";
import {
  NavLink,
  Navigate,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";
import {
  Bell,
  BookOpen,
  Box,
  ChartNoAxesColumnIncreasing,
  ChevronDown,
  ChevronUp,
  CircleAlert,
  Columns3,
  Database,
  Download,
  ExternalLink,
  FileText,
  Flame,
  HelpCircle,
  Home,
  Languages,
  Layers3,
  List,
  Map as MapIcon,
  MapPinned,
  Search,
  ShieldAlert,
  SlidersHorizontal,
  Thermometer,
  X,
} from "lucide-react";
import { loadAppData, sourceForRecord } from "./data";
import {
  evaluateEvidenceExport,
  evaluateLocationExport,
  serializeEvidencePayload,
} from "./evidenceExport";
import { layerById, registerGisLayers } from "./gisRegistry";
import { translate, type Language, type Translator } from "./i18n";
import {
  TerrainPreview3D,
  type TerrainPreviewTarget,
} from "./TerrainPreview3D";
import type {
  GeothermalRecord,
  LocationInspection,
  MeasurementResult,
} from "./types";
import {
  calculateMetrics,
  filterRecords,
  hasDocumentedSourceConflict,
  isConsistent,
  isProvisional,
  needsReview,
  type WorkspaceFilterState,
} from "./workspaceLogic";

const data = loadAppData();
const gisLayers = registerGisLayers(data.layers);
const EvidenceMap = lazy(() =>
  import("./EvidenceMap").then((module) => ({ default: module.EvidenceMap })),
);

const humanise = (value: string) =>
  value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());

export function App() {
  const [search, setSearch] = useState("");
  const [language, setLanguage] = useState<Language>(() =>
    localStorage.getItem("geothermai-language") === "th" ? "th" : "en",
  );
  const [workspaceFilters, setWorkspaceFilters] =
    useState<WorkspaceFilterState>(defaultFilters);
  const navigate = useNavigate();
  const t: Translator = (key) => translate(language, key);
  useEffect(() => {
    localStorage.setItem("geothermai-language", language);
    document.documentElement.lang = language;
  }, [language]);
  return (
    <div className="app-shell">
      <header className="topbar">
        <button
          className="brand"
          onClick={() => navigate("/dashboard")}
          aria-label={t("dashboard")}
        >
          <span>
            GeoTherm<span>AI</span>
          </span>
        </button>
        <nav aria-label={t("dashboard")}>
          <NavItem
            to="/dashboard"
            label={t("dashboard")}
            icon={<Home size={18} />}
          />
          <NavItem
            to="/evidence-map"
            label={t("evidenceMap")}
            icon={<MapIcon size={18} />}
          />
          <NavItem
            to="/data-quality"
            label={t("dataQuality")}
            icon={<Database size={18} />}
          />
          <NavItem
            to="/research-status"
            label={t("researchStatus")}
            icon={<ChartNoAxesColumnIncreasing size={18} />}
          />
        </nav>
        <div className="top-actions">
          <label className="header-search">
            <Search size={16} />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder={t("searchPlaceholder")}
              aria-label={t("searchPlaceholder")}
            />
            <kbd>⌘ K</kbd>
          </label>
          <button
            className="language-toggle"
            onClick={() =>
              setLanguage((current) => (current === "en" ? "th" : "en"))
            }
            aria-label={
              language === "en" ? "เปลี่ยนเป็นภาษาไทย" : "Switch to English"
            }
          >
            <Languages size={15} />
            <b>{language === "en" ? "ไทย" : "EN"}</b>
          </button>
          <button
            className="icon-button"
            aria-label={t("sourceInformation")}
            title={t("sourceInformation")}
            onClick={() => navigate("/research-status")}
          >
            <HelpCircle size={18} />
          </button>
          <button
            className="icon-button nonfunctional"
            aria-label={t("notificationsUnavailable")}
            title={t("notificationsUnavailable")}
          >
            <Bell size={18} />
          </button>
          <div className="profile-chip">
            <span>GT</span>
            <b>{t("research")}</b>
            <ChevronDown size={13} />
          </div>
        </div>
      </header>
      {search.trim() && (
        <SearchResults
          query={search}
          onSelect={() => {
            navigate("/evidence-map");
            setSearch("");
          }}
          t={t}
        />
      )}
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route
            path="/dashboard"
            element={
              <WorkspacePage
                showKpis
                t={t}
                filters={workspaceFilters}
                setFilters={setWorkspaceFilters}
              />
            }
          />
          <Route
            path="/evidence-map"
            element={
              <WorkspacePage
                t={t}
                filters={workspaceFilters}
                setFilters={setWorkspaceFilters}
              />
            }
          />
          <Route path="/data-quality" element={<DataQuality t={t} />} />
          <Route path="/research-status" element={<ResearchStatus t={t} />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function NavItem({
  to,
  label,
  icon,
}: {
  to: string;
  label: string;
  icon: React.ReactNode;
}) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) => (isActive ? "nav-active" : "")}
    >
      {icon}
      <span>{label}</span>
    </NavLink>
  );
}

function SearchResults({
  query,
  onSelect,
  t,
}: {
  query: string;
  onSelect: () => void;
  t: Translator;
}) {
  const term = query.trim().toLowerCase();
  const results = data.records
    .filter((record) =>
      [
        record.record_uid,
        record.source_site_name,
        record.source_province_or_area,
        record.source_record_code,
      ]
        .join(" ")
        .toLowerCase()
        .includes(term),
    )
    .slice(0, 6);
  return (
    <div className="search-results">
      <p className="eyebrow">{t("matchingRecords")}</p>
      {results.length ? (
        results.map((record) => (
          <button key={record.record_uid} onClick={onSelect}>
            <MapPinned size={15} />{" "}
            {record.source_site_name || record.source_record_code}
            <span>{record.source_region}</span>
          </button>
        ))
      ) : (
        <p>{t("noMatchingRecord")}</p>
      )}
    </div>
  );
}

const defaultFilters: WorkspaceFilterState = {
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

type WorkspaceView = "map" | "list" | "split" | "heatmap";

function WorkspacePage({
  showKpis = false,
  t,
  filters,
  setFilters,
}: {
  showKpis?: boolean;
  t: Translator;
  filters: WorkspaceFilterState;
  setFilters: Dispatch<SetStateAction<WorkspaceFilterState>>;
}) {
  const records = data.records;
  const [selected, setSelected] = useState<GeothermalRecord | null>(
    () =>
      records.find(
        (record) => isConsistent(record) && record.surface_temperature_c,
      ) ?? null,
  );
  const [bottomOpen, setBottomOpen] = useState(true);
  const [view, setView] = useState<WorkspaceView>("map");
  const [inspection, setInspection] = useState<LocationInspection | null>(null);
  const [measurement, setMeasurement] = useState<MeasurementResult | null>(
    null,
  );
  const [terrainTarget, setTerrainTarget] =
    useState<TerrainPreviewTarget | null>(null);
  const filtered = useMemo(
    () => filterRecords(records, filters),
    [records, filters],
  );
  const listRecords = useMemo(
    () =>
      records.filter((record) => {
        const expectedRegion =
          filters.region === "North"
            ? "Northern Thailand"
            : filters.region === "South"
              ? "Southern Thailand"
              : null;
        if (expectedRegion && record.source_region !== expectedRegion)
          return false;
        if (
          filters.missingTemperatureOnly &&
          record.surface_temperature_c.trim()
        )
          return false;
        if (filters.sourceConflictsOnly && !hasDocumentedSourceConflict(record))
          return false;
        return true;
      }),
    [
      records,
      filters.region,
      filters.missingTemperatureOnly,
      filters.sourceConflictsOnly,
    ],
  );
  const update = <K extends keyof WorkspaceFilterState>(
    key: K,
    value: WorkspaceFilterState[K],
  ) => setFilters((current) => ({ ...current, [key]: value }));
  const metrics = calculateMetrics(records);
  const exportDecisions = filtered.map((record) =>
    evaluateEvidenceExport(record, sourceForRecord(record, data.sources)),
  );
  const exportAllowed =
    exportDecisions.length > 0 &&
    exportDecisions.every((decision) => decision.allowed);
  const exportReason = exportAllowed
    ? t("exportAllowed")
    : (exportDecisions.find((decision) => !decision.allowed)?.reason ??
      t("noMatchingRecord"));
  const download = () => {
    if (!exportAllowed) return;
    const payload = exportDecisions.map((decision) => decision.payload);
    downloadJson("geothermai-filtered-evidence.json", payload);
  };
  const handleSelect = (record: GeothermalRecord) => {
    setSelected(record);
    setInspection(null);
    const longitude = Number(record.derived_longitude_wgs84);
    const latitude = Number(record.derived_latitude_wgs84);
    const previewEligible =
      isConsistent(record) ||
      (isProvisional(record) && filters.showProvisional);
    if (
      previewEligible &&
      Number.isFinite(longitude) &&
      Number.isFinite(latitude)
    ) {
      setTerrainTarget({
        name: record.source_site_name || record.source_record_code,
        longitude,
        latitude,
        coordinateStatus: isConsistent(record)
          ? t("internallyConsistent")
          : isProvisional(record)
            ? t("provisionalCoordinate")
            : t("requiresReview"),
        recordId: record.record_uid,
      });
    }
  };
  return (
    <div className={`workspace-page ${showKpis ? "with-kpis" : "map-only"}`}>
      <FilterSidebar
        filters={filters}
        update={update}
        reset={() => setFilters(defaultFilters)}
        records={records}
        t={t}
      />
      <section className="workspace-center">
        {showKpis && (
          <section className="workspace-kpis">
            <KpiCard
              label={t("totalRecords")}
              value={metrics.totalRecords}
              note={t("publishedObservations")}
              icon={<Database size={22} />}
              tone="blue"
            />
            <KpiCard
              label={t("sources")}
              value={metrics.sources}
              note={t("pointSources")}
              icon={<FileText size={22} />}
              tone="orange"
            />
            <KpiCard
              label={t("qualityFlags")}
              value={metrics.qualityFlags}
              note={t("coordinateCaution")}
              icon={<ShieldAlert size={22} />}
              tone="red"
            />
            <KpiCard
              label={t("validationUnits")}
              value={metrics.provisionalValidationUnits}
              note={t("groupingUnits")}
              icon={<Box size={22} />}
              tone="green"
            />
          </section>
        )}
        <div className={`map-frame workspace-view-${view}`}>
          <WorkspaceViewBar
            view={view}
            setView={setView}
            recordCount={view === "list" ? listRecords.length : filtered.length}
            t={t}
          />
          <div className="workspace-view-content">
            {view === "map" && (
              <Suspense
                fallback={
                  <div className="map-loading" role="status">
                    {t("loadingMap")}
                  </div>
                }
              >
                <EvidenceMap
                  records={filtered}
                  allRecords={records}
                  gisLayers={gisLayers}
                  showProvisional={filters.showProvisional}
                  showGeology={filters.showGeology}
                  showHeatFlow={filters.showHeatFlow}
                  showCoverage={filters.showCoverage}
                  showQualityReview={filters.showQualityReview}
                  selectedRecordId={selected?.record_uid}
                  onSelect={handleSelect}
                  onInspect={(value) => {
                    setInspection(value);
                    setSelected(null);
                  }}
                  onPreview3D={({ longitude, latitude }) =>
                    setTerrainTarget({
                      name: t("selectedMapLocation"),
                      longitude,
                      latitude,
                      coordinateStatus: t("mapClickCoordinate"),
                    })
                  }
                  onMeasurement={setMeasurement}
                  faultDistanceReason={
                    layerById(gisLayers, "DMR_ACTIVEFAULT_ZONE")?.stateReason
                  }
                  t={t}
                />
              </Suspense>
            )}
            {view === "list" && (
              <GeothermalList
                records={listRecords}
                selected={selected}
                onSelect={handleSelect}
                t={t}
              />
            )}
            {view === "split" && (
              <div className="split-workspace">
                <div className="split-map">
                  <Suspense
                    fallback={
                      <div className="map-loading" role="status">
                        {t("loadingMap")}
                      </div>
                    }
                  >
                    <EvidenceMap
                      records={filtered}
                      allRecords={records}
                      gisLayers={gisLayers}
                      showProvisional={filters.showProvisional}
                      showGeology={filters.showGeology}
                      showHeatFlow={filters.showHeatFlow}
                      showCoverage={filters.showCoverage}
                      showQualityReview={filters.showQualityReview}
                      selectedRecordId={selected?.record_uid}
                      onSelect={handleSelect}
                      onInspect={(value) => {
                        setInspection(value);
                        setSelected(null);
                      }}
                      onPreview3D={({ longitude, latitude }) =>
                        setTerrainTarget({
                          name: t("selectedMapLocation"),
                          longitude,
                          latitude,
                          coordinateStatus: t("mapClickCoordinate"),
                        })
                      }
                      onMeasurement={setMeasurement}
                      faultDistanceReason={
                        layerById(gisLayers, "DMR_ACTIVEFAULT_ZONE")
                          ?.stateReason
                      }
                      t={t}
                    />
                  </Suspense>
                </div>
                <GeothermalList
                  records={listRecords}
                  selected={selected}
                  onSelect={handleSelect}
                  compact
                  t={t}
                />
              </div>
            )}
            {view === "heatmap" && <HeatmapGate t={t} />}
          </div>
          {view === "map" && (
            <BottomPanel
              open={bottomOpen}
              setOpen={setBottomOpen}
              filtered={filtered}
              showProvisional={filters.showProvisional}
              onDownload={download}
              exportAllowed={exportAllowed}
              exportReason={exportReason}
              t={t}
            />
          )}
        </div>
      </section>
      {inspection || measurement ? (
        <SpatialInsights
          inspection={inspection}
          measurement={measurement}
          onClose={() => {
            setInspection(null);
            setMeasurement(null);
          }}
          t={t}
        />
      ) : (
        <SiteInsights
          selected={selected}
          showProvisionalCoordinates={filters.showProvisional}
          onClose={() => setSelected(null)}
          t={t}
        />
      )}
      {terrainTarget && (
        <TerrainPreview3D
          target={terrainTarget}
          onClose={() => setTerrainTarget(null)}
          t={t}
        />
      )}
    </div>
  );
}

function WorkspaceViewBar({
  view,
  setView,
  recordCount,
  t,
}: {
  view: WorkspaceView;
  setView: (view: WorkspaceView) => void;
  recordCount: number;
  t: Translator;
}) {
  const options: Array<{
    id: WorkspaceView;
    label: string;
    title: string;
    icon: React.ReactNode;
  }> = [
    {
      id: "map",
      label: t("map"),
      title: t("mapView"),
      icon: <MapIcon size={15} />,
    },
    {
      id: "list",
      label: t("list"),
      title: t("listView"),
      icon: <List size={15} />,
    },
    {
      id: "split",
      label: t("split"),
      title: t("splitView"),
      icon: <Columns3 size={15} />,
    },
    {
      id: "heatmap",
      label: t("heatmap"),
      title: t("heatmapView"),
      icon: <Flame size={15} />,
    },
  ];
  return (
    <div className="workspace-viewbar">
      <div>
        {options.map((option) => (
          <button
            key={option.id}
            className={view === option.id ? "active" : ""}
            onClick={() => setView(option.id)}
            aria-pressed={view === option.id}
            title={option.title}
          >
            {option.icon}
            {option.label}
          </button>
        ))}
      </div>
      <span>
        {recordCount} {t("records")}
      </span>
    </div>
  );
}

function GeothermalList({
  records,
  selected,
  onSelect,
  compact = false,
  t,
}: {
  records: GeothermalRecord[];
  selected: GeothermalRecord | null;
  onSelect: (record: GeothermalRecord) => void;
  compact?: boolean;
  t: Translator;
}) {
  return (
    <section className={`geothermal-list ${compact ? "compact" : ""}`}>
      <header>
        <div>
          <h2>{t("geothermalList")}</h2>
          <p>{t("listHint")}</p>
        </div>
        <span>
          {records.length} {t("records")}
        </span>
      </header>
      <div className="geothermal-list-scroll">
        {records.map((record) => {
          const quality = isConsistent(record)
            ? t("internallyConsistent")
            : isProvisional(record)
              ? t("provisionalCoordinate")
              : t("requiresReview");
          return (
            <button
              key={record.record_uid}
              className={`geothermal-list-item ${selected?.record_uid === record.record_uid ? "selected" : ""}`}
              onClick={() => onSelect(record)}
            >
              <span
                className={`record-marker ${isConsistent(record) ? "consistent" : isProvisional(record) ? "provisional" : "review"}`}
              >
                <MapPinned size={16} />
              </span>
              <span className="record-main">
                <b>{record.source_site_name || record.source_record_code}</b>
                <small>
                  {record.source_province_or_area || record.source_region} ·{" "}
                  {record.source_record_code}
                </small>
                <em
                  className={
                    isConsistent(record)
                      ? "consistent"
                      : isProvisional(record)
                        ? "provisional"
                        : "review"
                  }
                >
                  {quality}
                </em>
              </span>
              <span className="record-temperature">
                <Thermometer size={14} />
                <b>
                  {record.surface_temperature_c
                    ? `${record.surface_temperature_c} °C`
                    : t("noTemperature")}
                </b>
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

function HeatmapGate({ t }: { t: Translator }) {
  return (
    <section className="heatmap-gate">
      <div className="heatmap-gate-visual">
        <Flame size={34} />
        <span>{t("heatmapUnavailable")}</span>
      </div>
      <div className="heatmap-gate-copy">
        <p className="eyebrow">{t("analysisHeatmap")}</p>
        <h2>{t("heatmapTitle")}</h2>
        <p>{t("heatmapBody")}</p>
        <div className="heatmap-requirements">
          <article>
            <b>{t("requiredInput")}</b>
            <p>{t("requiredInputText")}</p>
          </article>
          <article>
            <b>{t("currentCandidates")}</b>
            <p>{t("candidatesText")}</p>
          </article>
          <article className="rejected">
            <b>{t("rejectedMethod")}</b>
            <p>{t("rejectedText")}</p>
          </article>
        </div>
      </div>
    </section>
  );
}

function KpiCard({
  label,
  value,
  note,
  icon,
  tone,
}: {
  label: string;
  value: number;
  note: string;
  icon: React.ReactNode;
  tone: string;
}) {
  return (
    <article className="kpi-card">
      <div className={`kpi-icon ${tone}`}>{icon}</div>
      <div>
        <span>{label}</span>
        <strong>{value}</strong>
        <p>{note}</p>
      </div>
    </article>
  );
}

function FilterSidebar({
  filters,
  update,
  reset,
  records,
  t,
}: {
  filters: WorkspaceFilterState;
  update: <K extends keyof WorkspaceFilterState>(
    key: K,
    value: WorkspaceFilterState[K],
  ) => void;
  reset: () => void;
  records: GeothermalRecord[];
  t: Translator;
}) {
  const metrics = calculateMetrics(records);
  const geology = layerById(gisLayers, "DMR_ROCK_UNIT_250K_NORTH");
  const faults = layerById(gisLayers, "DMR_ACTIVEFAULT_ZONE");
  const terrain = layerById(gisLayers, "SRTM_HGT_NORTH");
  const heatFlow = layerById(gisLayers, "IHFC_2024");
  const regionLabel: Record<WorkspaceFilterState["region"], string> = {
    "All Thailand": t("allThailand"),
    North: t("north"),
    South: t("south"),
  };
  return (
    <aside className="filter-panel">
      <div className="sidebar-title">
        <h2>{t("dataFilters")}</h2>
        <ChevronUp size={18} />
      </div>
      <FilterGroup title={t("region")}>
        <div className="region-switch">
          {(["All Thailand", "North", "South"] as const).map((region) => (
            <button
              key={region}
              className={filters.region === region ? "active" : ""}
              onClick={() => update("region", region)}
            >
              {regionLabel[region]}
            </button>
          ))}
        </div>
      </FilterGroup>
      <FilterGroup title={t("evidenceLayers")}>
        <LayerChoice
          color="#e23b35"
          label={t("publishedManifestations")}
          checked
          disabledNote={t("alwaysAvailable")}
          alwaysAvailable
        />
        <LayerChoice
          color="#8a63d2"
          label={t("geologicalUnits")}
          checked={filters.showGeology}
          onChange={(checked) => update("showGeology", checked)}
          disabledNote={geology?.stateReason}
          forceEnabled={geology?.displayEligible}
        />
        <LayerChoice
          color="#0f766e"
          label={t("heatFlowObservations")}
          checked={filters.showHeatFlow}
          onChange={(checked) => update("showHeatFlow", checked)}
          disabledNote={heatFlow?.stateReason}
          forceEnabled={heatFlow?.displayEligible}
        />
        <LayerChoice
          color="#1677ff"
          label={t("coverageFootprints")}
          checked={filters.showCoverage}
          onChange={(checked) => update("showCoverage", checked)}
          disabledNote={t("coverageFootprintsNote")}
          forceEnabled={terrain?.coverageDisplayEligible}
        />
        <LayerChoice
          color="#f04444"
          label={t("activeFaults")}
          disabledNote={faults?.stateReason ?? t("faultUnavailable")}
        />
        <LayerChoice
          color="#6b92a8"
          label={t("terrain")}
          disabledNote={terrain?.stateReason ?? t("noTerrainRaster")}
        />
        <LayerChoice
          color="#708090"
          label={t("adminBoundaries")}
          disabledNote={t("basemapOnly")}
        />
        <LayerChoice
          color="#d86b35"
          label={t("analysisHeatmap")}
          disabledNote={t("awaitingRaster")}
        />
        <LayerChoice
          color="#d6b23e"
          label={t("geothermalPotential")}
          disabledNote={t("notAuthorized")}
        />
      </FilterGroup>
      <FilterGroup title={t("coordinateQuality")}>
        <CountChoice
          label={t("internallyConsistent")}
          count={records.filter(isConsistent).length}
          color="#1677ff"
          checked={filters.showConsistent}
          onChange={(checked) => update("showConsistent", checked)}
        />
        <CountChoice
          label={t("provisionalCoordinates")}
          count={metrics.provisionalCoordinates}
          color="#f59e0b"
          checked={filters.showProvisional}
          onChange={(checked) => update("showProvisional", checked)}
          note={t("provisionalNote")}
        />
        <CountChoice
          label={t("reviewOverlay")}
          count={metrics.coordinateReview}
          color="#ef4444"
          checked={filters.showQualityReview}
          onChange={(checked) => update("showQualityReview", checked)}
          note={t("reviewOverlayNote")}
        />
      </FilterGroup>
      <FilterGroup title={t("additionalFilters")}>
        <CountChoice
          label={t("missingTemperatureOnly")}
          count={metrics.missingTemperature}
          color="#64748b"
          checked={filters.missingTemperatureOnly}
          onChange={(checked) => update("missingTemperatureOnly", checked)}
        />
        <CountChoice
          label={t("sourceConflictsOnly")}
          count={metrics.sourceConflicts}
          color="#8b5cf6"
          checked={filters.sourceConflictsOnly}
          onChange={(checked) => update("sourceConflictsOnly", checked)}
          note={t("conflictNote")}
        />
      </FilterGroup>
      <div className="sidebar-safety">
        <CircleAlert size={15} />
        <span>{t("safetyNote")}</span>
      </div>
      <button className="clear-button" onClick={reset}>
        <SlidersHorizontal size={15} /> {t("clearFilters")}
      </button>
    </aside>
  );
}

function FilterGroup({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="filter-group">
      <h3>{title}</h3>
      {children}
    </section>
  );
}
function LayerChoice({
  color,
  label,
  checked = false,
  onChange,
  disabledNote,
  alwaysAvailable = false,
  forceEnabled = false,
}: {
  color: string;
  label: string;
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabledNote?: string;
  alwaysAvailable?: boolean;
  forceEnabled?: boolean;
}) {
  const disabled = Boolean(disabledNote && !alwaysAvailable && !forceEnabled);
  return (
    <label className={`layer-choice ${disabled ? "disabled" : ""}`}>
      <input
        type="checkbox"
        checked={alwaysAvailable || checked}
        onChange={(event) => onChange?.(event.target.checked)}
        disabled={disabled || alwaysAvailable}
      />
      <i style={{ background: color }} />
      <span>
        {label}
        <small>{disabledNote}</small>
      </span>
    </label>
  );
}
function CountChoice({
  label,
  count,
  color,
  checked = false,
  onChange,
  disabled,
  note,
}: {
  label: string;
  count: number;
  color: string;
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  note?: string;
}) {
  return (
    <label className={`layer-choice ${disabled ? "disabled" : ""}`}>
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange?.(event.target.checked)}
        disabled={disabled}
      />
      <i style={{ background: color }} />
      <span>
        {label}
        <small>{note}</small>
      </span>
      <b>{count}</b>
    </label>
  );
}

function SiteInsights({
  selected,
  showProvisionalCoordinates,
  onClose,
  t,
}: {
  selected: GeothermalRecord | null;
  showProvisionalCoordinates: boolean;
  onClose: () => void;
  t: Translator;
}) {
  const [tab, setTab] = useState("Overview");
  const source = sourceForRecord(selected, data.sources);
  if (!selected)
    return (
      <aside className="insights-panel empty-insights">
        <div className="insights-heading">
          <h2>{t("siteInsights")}</h2>
        </div>
        <MapPinned size={32} />
        <h3>{t("selectSite")}</h3>
        <p>{t("selectSiteHelp")}</p>
      </aside>
    );
  const sameSource = data.records.filter(
    (record) => record.source_id === selected.source_id,
  ).length;
  const exportDecision = evaluateEvidenceExport(selected, source);
  const workingCoordinates = needsReview(selected)
    ? t("coordinateReviewWithheld")
    : isProvisional(selected) && !showProvisionalCoordinates
      ? t("coordinateOptInRequired")
      : `${Number(selected.derived_latitude_wgs84).toFixed(5)}, ${Number(selected.derived_longitude_wgs84).toFixed(5)}`;
  const exportDetail = () => {
    if (exportDecision.allowed && exportDecision.payload)
      downloadJson(
        `geothermai-${selected.record_uid}-evidence.json`,
        exportDecision.payload,
      );
  };
  const tabs = [
    { id: "Overview", label: t("overview") },
    { id: "Evidence", label: t("evidence") },
    { id: "Related", label: t("related") },
  ];
  return (
    <aside className="insights-panel">
      <div className="insights-heading">
        <h2>{t("siteInsights")}</h2>
        <button onClick={onClose} aria-label={t("siteInsights")}>
          <X size={17} />
        </button>
      </div>
      <div className="site-summary">
        <div className="site-visual">
          <MapPinned size={30} />
        </div>
        <div>
          <h3>{selected.source_site_name || selected.source_record_code}</h3>
          <span
            className={`quality-badge ${isConsistent(selected) ? "consistent" : "provisional"}`}
          >
            {isConsistent(selected)
              ? t("internallyConsistent")
              : isProvisional(selected)
                ? t("provisionalCoordinate")
                : t("requiresReview")}
          </span>
          <p>
            {humanise(selected.observation_type)} · {selected.source_region}
          </p>
        </div>
      </div>
      <div className="tabs">
        {tabs.map((item) => (
          <button
            className={tab === item.id ? "active" : ""}
            onClick={() => setTab(item.id)}
            key={item.id}
          >
            {item.label}
            {item.id === "Related" ? ` (${sameSource})` : ""}
          </button>
        ))}
      </div>
      <div className="insight-scroll">
        {tab === "Overview" && (
          <>
            <dl className="detail-list">
              <Detail label={t("recordId")} value={selected.record_uid} />
              <Detail
                label={t("sourceRegion")}
                value={selected.source_region}
              />
              <Detail
                label={t("originalUtm")}
                value={
                  selected.source_easting_m && selected.source_northing_m
                    ? `${selected.source_easting_m} E, ${selected.source_northing_m} N`
                    : t("noTemperature")
                }
              />
              <Detail
                label={t("originalDms")}
                value={
                  selected.source_latitude_dms && selected.source_longitude_dms
                    ? `${selected.source_latitude_dms}; ${selected.source_longitude_dms}`
                    : t("noTemperature")
                }
              />
              <Detail
                label={t("workingCoordinates")}
                value={workingCoordinates}
              />
              <Detail
                label={t("surfaceTemperature")}
                value={
                  selected.surface_temperature_c
                    ? `${selected.surface_temperature_c} °C`
                    : t("noTemperature")
                }
              />
              <Detail
                label={t("coordinateQuality")}
                value={humanise(selected.coordinate_validation_status)}
              />
              <Detail
                label={t("evidenceTier")}
                value={humanise(selected.evidence_tier)}
              />
            </dl>
            <section className="description-block">
              <h4>{t("dataQualityNote")}</h4>
              <p>{selected.coordinate_quality_note}</p>
            </section>
          </>
        )}
        {tab === "Evidence" && (
          <div className="evidence-block">
            <InfoCard
              title={t("publishedSource")}
              text={source?.reference ?? t("noTemperature")}
              icon={<BookOpen size={17} />}
            />
            <InfoCard
              title={t("sourceLocation")}
              text={selected.source_location || t("noTemperature")}
              icon={<FileText size={17} />}
            />
            <InfoCard
              title={t("licenseReuse")}
              text={selected.license_or_reuse_status || t("noTemperature")}
              icon={<ShieldAlert size={17} />}
            />
            {selected.source_url && (
              <a href={selected.source_url} target="_blank" rel="noreferrer">
                {t("openSource")} <ExternalLink size={13} />
              </a>
            )}
            <button
              className="primary-button"
              onClick={exportDetail}
              disabled={!exportDecision.allowed}
              title={exportDecision.reason}
            >
              <Download size={14} /> {t("exportEvidenceDetail")}
            </button>
            <p className="method-note">{exportDecision.reason}</p>
          </div>
        )}
        {tab === "Related" && (
          <div className="evidence-block">
            <InfoCard
              title={t("documentedGroup")}
              text={selected.proposed_site_group_id || t("noTemperature")}
              icon={<Layers3 size={17} />}
            />
            <InfoCard
              title={t("validationGroup")}
              text={selected.validation_cluster_id || t("noTemperature")}
              icon={<Box size={17} />}
            />
            <InfoCard
              title={t("sharedSource")}
              text={`${sameSource} ${t("records")} · ${selected.source_id}`}
              icon={<Database size={17} />}
            />
          </div>
        )}
      </div>
    </aside>
  );
}
function Detail({ label, value }: { label: string; value: string }) {
  return (
    <>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </>
  );
}
function InfoCard({
  title,
  text,
  icon,
}: {
  title: string;
  text: string;
  icon: React.ReactNode;
}) {
  return (
    <article className="info-card">
      <span>{icon}</span>
      <div>
        <b>{title}</b>
        <p>{text}</p>
      </div>
    </article>
  );
}

function SpatialInsights({
  inspection,
  measurement,
  onClose,
  t,
}: {
  inspection: LocationInspection | null;
  measurement: MeasurementResult | null;
  onClose: () => void;
  t: Translator;
}) {
  const exportDecision = inspection
    ? evaluateLocationExport(inspection)
    : { allowed: false, reason: t("selectSpatialTool") };
  const exportInspection = () => {
    if (exportDecision.allowed && exportDecision.payload)
      downloadJson(
        "geothermai-location-inspection.json",
        exportDecision.payload,
      );
  };
  return (
    <aside className="insights-panel">
      <div className="insights-heading">
        <h2>{t("spatialInspection")}</h2>
        <button onClick={onClose} aria-label={t("spatialInspection")}>
          <X size={17} />
        </button>
      </div>
      <div className="insight-scroll spatial-insights">
        {inspection && (
          <section>
            <p className="eyebrow">{t("inspectLocation")}</p>
            <dl className="detail-list">
              <Detail
                label="WGS84"
                value={`${inspection.latitude.toFixed(6)}, ${inspection.longitude.toFixed(6)}`}
              />
              <Detail
                label={t("availableIntersections")}
                value={
                  inspection.intersections.length
                    ? `${inspection.intersections.length} ${t("mappedIntersections")}`
                    : t("noMappedIntersection")
                }
              />
            </dl>
            {inspection.intersections.map((item) => (
              <article className="info-card intersection-card" key={item.id}>
                <span>
                  <Layers3 size={17} />
                </span>
                <div>
                  <b>{item.title}</b>
                  <p>{item.detail}</p>
                  <dl>
                    <dt>{t("publisher")}</dt>
                    <dd>{item.publisher}</dd>
                    <dt>{t("scaleResolution")}</dt>
                    <dd>{item.scaleOrResolution}</dd>
                    <dt>{t("licenseReuse")}</dt>
                    <dd>{item.license}</dd>
                  </dl>
                  {item.sourceUrl && (
                    <a href={item.sourceUrl} target="_blank" rel="noreferrer">
                      {t("openSource")} <ExternalLink size={12} />
                    </a>
                  )}
                  <p className="intersection-warning">{item.warning}</p>
                </div>
              </article>
            ))}
            <p className="method-note">{inspection.method}</p>
          </section>
        )}
        {measurement && (
          <section>
            <p className="eyebrow">
              {measurement.kind === "area"
                ? t("measureArea")
                : t("measureDistance")}
            </p>
            <strong className="measurement-value">
              {measurement.value.toLocaleString(undefined, {
                maximumFractionDigits: 3,
              })}{" "}
              {measurement.unit}
            </strong>
            <dl className="detail-list">
              <Detail label="CRS" value={measurement.crs} />
              <Detail
                label={t("vertices")}
                value={String(measurement.vertexCount)}
              />
            </dl>
            <p className="method-note">{measurement.method}</p>
          </section>
        )}
        {!inspection && !measurement && <p>{t("selectSpatialTool")}</p>}
        <button
          className="primary-button"
          onClick={exportInspection}
          disabled={!exportDecision.allowed}
          title={exportDecision.reason}
        >
          <Download size={14} /> {t("exportEvidenceDetail")}
        </button>
        <p className="method-note">{exportDecision.reason}</p>
        <div className="sidebar-safety">
          <CircleAlert size={15} />
          <span>{t("spatialSafety")}</span>
        </div>
      </div>
    </aside>
  );
}

function downloadJson(filename: string, payload: unknown) {
  const url = URL.createObjectURL(
    new Blob([serializeEvidencePayload(payload)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function BottomPanel({
  open,
  setOpen,
  filtered,
  showProvisional,
  onDownload,
  exportAllowed,
  exportReason,
  t,
}: {
  open: boolean;
  setOpen: (open: boolean) => void;
  filtered: GeothermalRecord[];
  showProvisional: boolean;
  onDownload: () => void;
  exportAllowed: boolean;
  exportReason: string;
  t: Translator;
}) {
  const [tab, setTab] = useState("Timeline & Provenance");
  if (!open)
    return (
      <button className="bottom-reopen" onClick={() => setOpen(true)}>
        <ChevronUp size={15} /> {t("showAnalysis")}
      </button>
    );
  const tabs = [
    { id: "Timeline & Provenance", label: t("timeline") },
    { id: "Data Coverage", label: t("dataCoverage") },
    { id: "Analysis Tools", label: t("analysisTools") },
    { id: "Download", label: t("download") },
  ];
  return (
    <section className="bottom-panel">
      <div className="bottom-tabs">
        {tabs.map((item) => (
          <button
            className={tab === item.id ? "active" : ""}
            onClick={() => setTab(item.id)}
            key={item.id}
          >
            {item.label}
          </button>
        ))}
        <span>
          {filtered.length} {t("records")}
        </span>
        <button
          className="collapse"
          onClick={() => setOpen(false)}
          aria-label={t("showAnalysis")}
        >
          <ChevronDown size={17} />
        </button>
      </div>
      <div className="bottom-content">
        {tab === "Timeline & Provenance" && (
          <div className="timeline">
            <div>
              <i />
              <b>2014</b>
              <span>Northern published table</span>
            </div>
            <div>
              <i />
              <b>2021</b>
              <span>Southern published table</span>
            </div>
            <div>
              <i />
              <b>2026</b>
              <span>Phase 1C evidence screen</span>
            </div>
          </div>
        )}
        {tab === "Data Coverage" && (
          <p>
            <b>{filtered.length}</b> {t("records")}. {t("safetyNote")}
          </p>
        )}
        {tab === "Analysis Tools" && (
          <p>
            <b>{t("descriptiveOnly")}</b> {t("measurementHelp")}
          </p>
        )}
        {tab === "Download" && (
          <div className="download-row">
            <p>
              {exportAllowed
                ? showProvisional
                  ? t("provisionalNote")
                  : t("publishedObservations")
                : exportReason}
            </p>
            <button
              className="primary-button"
              onClick={onDownload}
              disabled={!exportAllowed}
              title={exportReason}
            >
              <Download size={15} /> {t("downloadData")}
            </button>
          </div>
        )}
      </div>
    </section>
  );
}

function DataQuality({ t }: { t: Translator }) {
  const records = data.records;
  const statusCounts = Object.entries(
    records.reduce<Record<string, number>>((acc, record) => {
      acc[record.coordinate_validation_status] =
        (acc[record.coordinate_validation_status] ?? 0) + 1;
      return acc;
    }, {}),
  );
  const review = records.filter(needsReview);
  const missingTemperature = records.filter(
    (record) => !record.surface_temperature_c.trim(),
  );
  return (
    <div className="page quality-page">
      <div className="page-intro">
        <div>
          <p className="eyebrow">{t("dataQuality")}</p>
          <h1>{t("keepUncertainty")}</h1>
          <p>{t("safetyNote")}</p>
        </div>
      </div>
      <section className="quality-grid">
        <Metric
          label={t("coordinateReview")}
          value={review.length}
          note={t("excludedMap")}
        />
        <Metric
          label={t("provisionalCoordinates")}
          value={records.filter(isProvisional).length}
          note={t("mappedWarning")}
        />
        <Metric
          label={t("missingTemperature")}
          value={missingTemperature.length}
          note={t("shownUnavailable")}
        />
        <Metric
          label={t("duplicateCandidates")}
          value={0}
          note={t("noNameMerge")}
        />
      </section>
      <section className="quality-layout">
        <article className="panel">
          <p className="eyebrow">{t("coordinateQuality")}</p>
          <h2>{t("registryStatus")}</h2>
          <table>
            <thead>
              <tr>
                <th>Status</th>
                <th>{t("records")}</th>
                <th>{t("map")}</th>
              </tr>
            </thead>
            <tbody>
              {statusCounts.map(([status, count]) => (
                <tr key={status}>
                  <td>{humanise(status)}</td>
                  <td>{count}</td>
                  <td>
                    {status.includes("CONSISTENT")
                      ? t("internallyConsistent")
                      : status.includes("NO_DMS_COMPARATOR")
                        ? t("mappedWarning")
                        : t("notMapped")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>
        <article className="panel">
          <p className="eyebrow">{t("gisAvailability")}</p>
          <h2>{t("realConstraints")}</h2>
          {gisLayers.map((layer) => (
            <div className="layer-status" key={layer.layer_id}>
              <span
                className={layer.displayEligible ? "available" : "restricted"}
              />
              <div>
                <b>
                  {layer.layer_category?.replaceAll("_", " ") ||
                    "Unclassified layer"}{" "}
                  · {layer.state}
                </b>
                <p>{layer.stateReason}</p>
              </div>
            </div>
          ))}
        </article>
      </section>
      <section className="panel records-table">
        <p className="eyebrow">{t("requiresReview")}</p>
        <h2>{t("sourceValuesRetained")}</h2>
        <table>
          <thead>
            <tr>
              <th>{t("recordId")}</th>
              <th>{t("selectSite")}</th>
              <th>{t("dataQualityNote")}</th>
            </tr>
          </thead>
          <tbody>
            {review.map((record) => (
              <tr key={record.record_uid}>
                <td>{record.record_uid}</td>
                <td>{record.source_site_name || record.source_record_code}</td>
                <td>{record.coordinate_quality_note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
function Metric({
  label,
  value,
  note,
}: {
  label: string;
  value: number;
  note: string;
}) {
  return (
    <article className="panel metric-panel">
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{note}</p>
    </article>
  );
}

function ResearchStatus({ t }: { t: Translator }) {
  const gateConditions = [
    {
      id: "authoritative_label_review",
      name: t("gateAuthoritativeLabels"),
      reason: t("gateAuthoritativeLabelsReason"),
    },
    {
      id: "independent_system_group_review",
      name: t("gateSystemGroups"),
      reason: t("gateSystemGroupsReason"),
    },
    {
      id: "locked_pilot_region",
      name: t("gatePilotRegion"),
      reason: t("gatePilotRegionReason"),
    },
    {
      id: "licensed_predictor_coverage",
      name: t("gatePredictorCoverage"),
      reason: t("gatePredictorCoverageReason"),
    },
    {
      id: "pu_background_protocol",
      name: t("gatePuProtocol"),
      reason: t("gatePuProtocolReason"),
    },
    {
      id: "preregistered_spatial_group_validation",
      name: t("gateSpatialValidation"),
      reason: t("gateSpatialValidationReason"),
    },
    {
      id: "sufficient_independent_groups",
      name: t("gateSufficientGroups"),
      reason: t("gateSufficientGroupsReason"),
    },
    {
      id: "external_geographic_holdout",
      name: t("gateExternalHoldout"),
      reason: t("gateExternalHoldoutReason"),
    },
    {
      id: "rights_and_output_review",
      name: t("gateRightsReview"),
      reason: t("gateRightsReviewReason"),
    },
  ];

  return (
    <div className="page status-page">
      <div className="page-intro">
        <div>
          <p className="eyebrow">{t("researchStatus")}</p>
          <h1>{t("heatmapTitle")}</h1>
          <p>{t("heatmapBody")}</p>
        </div>
        <span className="status-pill amber">
          <ShieldAlert size={15} /> {t("notAuthorized")}
        </span>
      </div>
      <section className="status-grid">
        <article className="panel status-card approved">
          <p className="eyebrow">{t("currentPhase")}</p>
          <h2>Phase 2E — prediction-first research & gate protocol</h2>
          <p>{t("safetyNote")}</p>
        </article>
        <article className="panel status-card blocked">
          <p className="eyebrow">{t("masterDecision")}</p>
          <h2>Predictive ML readiness — No-go (9 Blockers)</h2>
          <p>{t("rejectedText")}</p>
        </article>
        <article className="panel span-2">
          <p className="eyebrow">{t("analysisHeatmap")}</p>
          <div className="two-column-list">
            <div>
              <b>{t("requiredInput")}</b>
              <p>{t("requiredInputText")}</p>
            </div>
            <div>
              <b>{t("currentCandidates")}</b>
              <p>{t("candidatesText")}</p>
            </div>
          </div>
        </article>
        <article className="panel span-2">
          <p className="eyebrow">{t("gateChecklistTitle")}</p>
          <div className="gate-checklist-grid">
            {gateConditions.map((cond) => (
              <div key={cond.id} className="gate-item blocked">
                <div className="gate-header">
                  <span className="gate-badge blocked">NO-GO</span>
                  <b>{cond.name}</b>
                </div>
                <p>{cond.reason}</p>
              </div>
            ))}
          </div>
        </article>
        <article className="panel span-2">
          <p className="eyebrow">{t("plannedModelsTitle")}</p>
          <div className="three-column-list">
            <div>
              <b>Model A — Baseline PFA</b>
              <p>{t("modelADesc")}</p>
            </div>
            <div>
              <b>Model B — Statistical ML</b>
              <p>{t("modelBDesc")}</p>
            </div>
            <div>
              <b>Model C — Tree Ensemble</b>
              <p>{t("modelCDesc")}</p>
            </div>
          </div>
        </article>
      </section>
    </div>
  );
}
