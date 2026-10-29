import { useMemo, useRef, useState, type PointerEvent } from "react";
import {
  Compass,
  Minus,
  Mountain,
  Plus,
  RotateCcw,
  RotateCw,
  X,
} from "lucide-react";
import type { Translator } from "./i18n";

export interface TerrainPreviewTarget {
  name: string;
  longitude: number;
  latitude: number;
  coordinateStatus: string;
  recordId?: string;
}

interface ProjectedPoint {
  x: number;
  y: number;
  depth: number;
  height: number;
}

interface MeshCell {
  key: string;
  points: string;
  depth: number;
  height: number;
}

const GRID_SIZE = 17;

function wrapDegrees(value: number) {
  return ((value % 360) + 360) % 360;
}

function terrainHeight(x: number, y: number, seed: number) {
  const ridge = Math.sin(x * 3.3 + seed) * Math.cos(y * 2.7 - seed * 0.7);
  const hillA = Math.exp(-((x + 0.33) ** 2 + (y - 0.18) ** 2) * 5.2);
  const hillB = Math.exp(-((x - 0.42) ** 2 + (y + 0.28) ** 2) * 8.4);
  const basin = Math.exp(-((x - 0.05) ** 2 + (y - 0.08) ** 2) * 15);
  return Math.max(0.03, 0.18 + ridge * 0.12 + hillA * 0.55 + hillB * 0.32 - basin * 0.12);
}

function projectPoint(
  x: number,
  y: number,
  height: number,
  azimuth: number,
  elevation: number,
  zoom: number,
): ProjectedPoint {
  const angle = (azimuth * Math.PI) / 180;
  const pitch = (elevation * Math.PI) / 180;
  const rotatedX = x * Math.cos(angle) - y * Math.sin(angle);
  const rotatedY = x * Math.sin(angle) + y * Math.cos(angle);
  const scale = 205 * zoom;
  return {
    x: 310 + rotatedX * scale,
    y: 218 + (rotatedY * Math.sin(pitch) - height * Math.cos(pitch) * 1.28) * scale,
    depth: rotatedY * Math.cos(pitch) + height * Math.sin(pitch),
    height,
  };
}

function buildMesh(
  target: TerrainPreviewTarget,
  azimuth: number,
  elevation: number,
  zoom: number,
) {
  const seed =
    (Math.abs(target.longitude * 0.37 + target.latitude * 0.61) % 2.8) + 0.35;
  const points: ProjectedPoint[][] = [];
  for (let row = 0; row < GRID_SIZE; row += 1) {
    const y = -1 + (row / (GRID_SIZE - 1)) * 2;
    points[row] = [];
    for (let column = 0; column < GRID_SIZE; column += 1) {
      const x = -1 + (column / (GRID_SIZE - 1)) * 2;
      const height = terrainHeight(x, y, seed);
      points[row][column] = projectPoint(
        x,
        y,
        height,
        azimuth,
        elevation,
        zoom,
      );
    }
  }

  const cells: MeshCell[] = [];
  for (let row = 0; row < GRID_SIZE - 1; row += 1) {
    for (let column = 0; column < GRID_SIZE - 1; column += 1) {
      const corners = [
        points[row][column],
        points[row][column + 1],
        points[row + 1][column + 1],
        points[row + 1][column],
      ];
      cells.push({
        key: `${row}-${column}`,
        points: corners.map((point) => `${point.x},${point.y}`).join(" "),
        depth: corners.reduce((sum, point) => sum + point.depth, 0) / 4,
        height: corners.reduce((sum, point) => sum + point.height, 0) / 4,
      });
    }
  }
  cells.sort((a, b) => a.depth - b.depth);
  const markerHeight = terrainHeight(0, 0, seed);
  return {
    cells,
    marker: projectPoint(0, 0, markerHeight, azimuth, elevation, zoom),
  };
}

export function TerrainPreview3D({
  target,
  onClose,
  t,
}: {
  target: TerrainPreviewTarget;
  onClose: () => void;
  t: Translator;
}) {
  const [azimuth, setAzimuth] = useState(28);
  const [elevation, setElevation] = useState(34);
  const [zoom, setZoom] = useState(1);
  const drag = useRef<{ x: number; y: number; azimuth: number; elevation: number } | null>(
    null,
  );
  const mesh = useMemo(
    () => buildMesh(target, azimuth, elevation, zoom),
    [target, azimuth, elevation, zoom],
  );

  const handlePointerDown = (event: PointerEvent<SVGSVGElement>) => {
    drag.current = {
      x: event.clientX,
      y: event.clientY,
      azimuth,
      elevation,
    };
    event.currentTarget.setPointerCapture(event.pointerId);
  };
  const handlePointerMove = (event: PointerEvent<SVGSVGElement>) => {
    if (!drag.current) return;
    setAzimuth(
      wrapDegrees(drag.current.azimuth + (event.clientX - drag.current.x) * 0.55),
    );
    setElevation(
      Math.max(
        18,
        Math.min(68, drag.current.elevation - (event.clientY - drag.current.y) * 0.28),
      ),
    );
  };

  return (
    <div className="terrain-dialog-backdrop" role="presentation">
      <section
        className="terrain-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="terrain-preview-title"
      >
        <header className="terrain-dialog-header">
          <div className="terrain-dialog-title">
            <span><Mountain size={19} /></span>
            <div>
              <p className="eyebrow">{t("generatedAreaPreview")}</p>
              <h2 id="terrain-preview-title">{target.name}</h2>
            </div>
          </div>
          <button className="terrain-close" onClick={onClose} aria-label={t("close3dPreview")}>
            <X size={19} />
          </button>
        </header>

        <div className="terrain-stage">
          <svg
            viewBox="0 0 620 420"
            role="img"
            aria-label={t("terrain3dAria")}
            onPointerDown={handlePointerDown}
            onPointerMove={handlePointerMove}
            onPointerUp={() => { drag.current = null; }}
            onPointerCancel={() => { drag.current = null; }}
          >
            <defs>
              <linearGradient id="terrain-sky" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0" stopColor="#d9eff4" />
                <stop offset="1" stopColor="#f6f3e9" />
              </linearGradient>
              <filter id="marker-shadow" x="-80%" y="-80%" width="260%" height="260%">
                <feDropShadow dx="0" dy="3" stdDeviation="3" floodOpacity=".25" />
              </filter>
            </defs>
            <rect width="620" height="420" fill="url(#terrain-sky)" />
            <ellipse cx="310" cy="325" rx="245" ry="46" fill="#284b3c" opacity=".12" />
            {mesh.cells.map((cell) => {
              const lightness = 38 + cell.height * 29;
              return (
                <polygon
                  key={cell.key}
                  points={cell.points}
                  fill={`hsl(${136 - cell.height * 25} 30% ${lightness}%)`}
                  stroke="rgba(245,250,246,.33)"
                  strokeWidth=".65"
                />
              );
            })}
            <g
              transform={`translate(${mesh.marker.x} ${mesh.marker.y - 8})`}
              filter="url(#marker-shadow)"
            >
              <line y1="0" y2="34" stroke="#e8503a" strokeWidth="2" />
              <path d="M0 0 C-12 -14 -12 -27 0 -27 C12 -27 12 -14 0 0Z" fill="#e8503a" />
              <circle cy="-17" r="4" fill="#fff" />
            </g>
          </svg>

          <div className="terrain-compass" aria-hidden="true">
            <Compass size={18} style={{ transform: `rotate(${-azimuth}deg)` }} />
            <b>{Math.round(azimuth)}°</b>
          </div>
          <div className="terrain-drag-hint"><RotateCw size={14} /> {t("dragToExplore")}</div>
          <div className="terrain-controls" aria-label={t("terrainControls")}>
            <button onClick={() => setAzimuth((value) => wrapDegrees(value - 30))} aria-label={t("rotateLeft")}>
              <RotateCcw size={16} />
            </button>
            <button onClick={() => setAzimuth((value) => wrapDegrees(value + 30))} aria-label={t("rotateRight")}>
              <RotateCw size={16} />
            </button>
            <button onClick={() => setZoom((value) => Math.min(1.35, value + 0.1))} aria-label={t("zoomIn")}>
              <Plus size={16} />
            </button>
            <button onClick={() => setZoom((value) => Math.max(0.72, value - 0.1))} aria-label={t("zoomOut")}>
              <Minus size={16} />
            </button>
            <button onClick={() => { setAzimuth(28); setElevation(34); setZoom(1); }} aria-label={t("reset3dView")}>
              <RotateCcw size={16} />
            </button>
          </div>
        </div>

        <footer className="terrain-dialog-footer">
          <div>
            <span>{t("coordinates")}</span>
            <b>{target.latitude.toFixed(5)}, {target.longitude.toFixed(5)}</b>
          </div>
          <div>
            <span>{t("coordinateQuality")}</span>
            <b>{target.coordinateStatus}</b>
          </div>
          {target.recordId && (
            <div>
              <span>{t("recordId")}</span>
              <b>{target.recordId}</b>
            </div>
          )}
          <p>{t("terrainPreviewDisclaimer")}</p>
        </footer>
      </section>
    </div>
  );
}
