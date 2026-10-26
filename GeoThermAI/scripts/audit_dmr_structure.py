#!/usr/bin/env python3
"""Reproducibly audit the DMR geological-structure ArcGIS query response.

The audit records response shape only. It never substitutes missing geometry or
publishes returned feature attributes as a new dataset.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
QUERY_URL = "https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/GEOL_STR_250K/MapServer/0/query"
LAYER_URL = "https://gisportal.dmr.go.th/arcgis/rest/services/GEOL/GEOL_STR_250K/MapServer/0"
DEFAULT_OUTPUT = ROOT / "tasks/phase_2d_data_readiness/derived/dmr-structure-query-audit.json"


def summarize_response(status: int, payload: Any, content_type: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"httpStatus": status, "contentType": content_type, "responseType": type(payload).__name__, "topLevelKeys": [], "featureCount": 0, "geometryCount": 0, "error": "Response was not a JSON object"}
    features = payload.get("features") if isinstance(payload.get("features"), list) else []
    return {
        "httpStatus": status,
        "contentType": content_type,
        "responseType": "object",
        "topLevelKeys": sorted(payload.keys()),
        "objectIdCount": len(payload.get("objectIds", [])) if isinstance(payload.get("objectIds"), list) else None,
        "featureCount": len(features),
        "geometryCount": sum(1 for feature in features if isinstance(feature, dict) and feature.get("geometry")),
        "exceededTransferLimit": payload.get("exceededTransferLimit"),
        "error": payload.get("error"),
    }


def request_query(params: dict[str, Any], timeout: float, base_url: str = QUERY_URL) -> tuple[int, Any, str]:
    url = f"{base_url}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "GeoThermAI-Phase2D-Audit/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "")
            return response.status, json.loads(body), content_type
    except HTTPError as error:
        body = error.read()
        content_type = error.headers.get("Content-Type", "") if error.headers else ""
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"error": {"message": body.decode("utf-8", errors="replace")[:500]}}
        return error.code, payload, content_type


def run_audit(timeout: float = 30.0) -> dict[str, Any]:
    common = {"where": "1=1", "outFields": "*", "returnGeometry": "true", "outSR": "4326"}
    attempts: list[dict[str, Any]] = []

    metadata_params = {"f": "pjson"}
    status, metadata, content_type = request_query(metadata_params, timeout, LAYER_URL)
    metadata_summary = summarize_response(status, metadata, content_type)
    if isinstance(metadata, dict):
        metadata_summary.update({
            "name": metadata.get("name"),
            "geometryType": metadata.get("geometryType"),
            "supportedQueryFormats": metadata.get("supportedQueryFormats"),
            "maxRecordCount": metadata.get("maxRecordCount"),
            "objectIdField": metadata.get("objectIdField"),
            "sourceSpatialReference": metadata.get("sourceSpatialReference") or metadata.get("extent", {}).get("spatialReference"),
        })
    attempts.append({"name": "layer_metadata", "parameters": metadata_params, "summary": metadata_summary})

    ids_params = {"where": "1=1", "returnIdsOnly": "true", "f": "json"}
    status, ids_payload, content_type = request_query(ids_params, timeout)
    ids_summary = summarize_response(status, ids_payload, content_type)
    attempts.append({"name": "return_ids", "parameters": ids_params, "summary": ids_summary})
    object_ids = ids_payload.get("objectIds", []) if isinstance(ids_payload, dict) else []
    sample_ids = object_ids[:25] if isinstance(object_ids, list) else []

    query_attempts = [
        ("offset_json_4326", {**common, "resultOffset": 0, "resultRecordCount": 25, "f": "json"}),
        ("offset_json_32647", {**common, "outSR": "32647", "resultOffset": 0, "resultRecordCount": 25, "f": "json"}),
        ("object_ids_json", {**common, "objectIds": ",".join(map(str, sample_ids)), "f": "json"}),
        ("object_ids_esrijson", {**common, "objectIds": ",".join(map(str, sample_ids[:5])), "f": "esriJSON"}),
        ("object_ids_geojson", {**common, "objectIds": ",".join(map(str, sample_ids[:5])), "f": "geojson"}),
        ("offset_geojson_4326", {**common, "resultOffset": 0, "resultRecordCount": 25, "f": "geojson"}),
    ]
    for name, params in query_attempts:
        status, payload, content_type = request_query(params, timeout)
        attempts.append({"name": name, "parameters": params, "summary": summarize_response(status, payload, content_type)})

    return {
        "endpoint": QUERY_URL,
        "executedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scientificBoundary": "Response-shape audit only; missing geometry is not approximated or replaced.",
        "attempts": attempts,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()
    try:
        result = run_audit(args.timeout)
    except URLError as error:
        raise SystemExit(f"DMR audit failed before receiving an HTTP response: {error}") from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
