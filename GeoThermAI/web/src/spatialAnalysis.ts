import type { MeasurementResult } from "./types";

export type LngLat = readonly [number, number];
const EARTH_RADIUS_M = 6_371_008.8;

const radians = (degrees: number) => degrees * Math.PI / 180;

export function parseDmsCoordinate(value: string): number | null {
  const match = value.trim().match(/^(\d{1,3})\s+(\d{1,2})\s+([\d.]+)\s*([NSEW])$/i);
  if (!match) return null;
  const degrees = Number(match[1]);
  const minutes = Number(match[2]);
  const seconds = Number(match[3]);
  if (![degrees, minutes, seconds].every(Number.isFinite) || minutes >= 60 || seconds >= 60) return null;
  const decimal = degrees + minutes / 60 + seconds / 3600;
  return /[SW]/i.test(match[4]) ? -decimal : decimal;
}

export function geodesicDistanceMeters(start: LngLat, end: LngLat): number {
  const latitudeDelta = radians(end[1] - start[1]);
  const longitudeDelta = radians(end[0] - start[0]);
  const startLatitude = radians(start[1]);
  const endLatitude = radians(end[1]);
  const a = Math.sin(latitudeDelta / 2) ** 2
    + Math.cos(startLatitude) * Math.cos(endLatitude) * Math.sin(longitudeDelta / 2) ** 2;
  return 2 * EARTH_RADIUS_M * Math.asin(Math.min(1, Math.sqrt(a)));
}

export function geodesicPathLengthMeters(points: LngLat[]): number {
  return points.slice(1).reduce((total, point, index) => total + geodesicDistanceMeters(points[index], point), 0);
}

export function geodesicPolygonAreaSquareMeters(points: LngLat[]): number {
  if (points.length < 3) return 0;
  const closed = [...points, points[0]];
  let sum = 0;
  for (let index = 0; index < points.length; index += 1) {
    const current = closed[index];
    const next = closed[index + 1];
    sum += radians(next[0] - current[0]) * (2 + Math.sin(radians(current[1])) + Math.sin(radians(next[1])));
  }
  return Math.abs(sum * EARTH_RADIUS_M * EARTH_RADIUS_M / 2);
}

export function formatMeasurement(kind: "distance" | "area", rawValue: number, vertexCount: number): MeasurementResult {
  const large = rawValue >= 1_000_000 && kind === "area" || rawValue >= 1_000 && kind === "distance";
  return {
    kind,
    value: large ? rawValue / (kind === "area" ? 1_000_000 : 1_000) : rawValue,
    unit: kind === "area" ? (large ? "km²" : "m²") : (large ? "km" : "m"),
    vertexCount,
    crs: "EPSG:4326",
    method: kind === "area"
      ? "Spherical polygon area using mean Earth radius; descriptive measurement, not cadastral area."
      : "Great-circle segment sum using the haversine formula and mean Earth radius.",
  };
}
