#!/usr/bin/env python3
"""Audit Landsat STAC assets without misclassifying login HTML as raster data."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STAC = ROOT / "tasks/phase_1_data_acquisition_label_validation/northern_thailand_stac_items.json"
DEFAULT_OUTPUT = ROOT / "tasks/phase_2d_data_readiness/derived/landsat_asset_access_audit.json"
TIFF_SIGNATURES = {b"II*\x00", b"MM\x00*", b"II+\x00", b"MM\x00+"}


def path_label(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def inspect_url(url: str, timeout: float = 30.0) -> dict[str, Any]:
    request = Request(url, headers={"Range": "bytes=0-15", "User-Agent": "GeoThermAI-Phase2D-Audit/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(16)
            return {
                "httpStatus": response.status,
                "finalUrl": response.geturl(),
                "contentType": response.headers.get("Content-Type", ""),
                "firstBytesHex": body.hex(),
                "isTiffSignature": body[:4] in TIFF_SIGNATURES,
                "isHtml": body.lstrip().lower().startswith(b"<!doctype html") or body.lstrip().lower().startswith(b"<html"),
            }
    except HTTPError as error:
        body = error.read(16)
        return {"httpStatus": error.code, "finalUrl": error.geturl(), "contentType": error.headers.get("Content-Type", ""), "firstBytesHex": body.hex(), "isTiffSignature": body[:4] in TIFF_SIGNATURES, "isHtml": body.lstrip().lower().startswith(b"<!doctype html") or body.lstrip().lower().startswith(b"<html"), "error": str(error)}


def run(stac_path: Path, output: Path, timeout: float = 30.0) -> dict[str, Any]:
    payload = json.loads(stac_path.read_text(encoding="utf-8"))
    attempts: list[dict[str, Any]] = []
    for item in payload.get("features", []):
        for key in ("MTL.json", "lwir11", "qa", "qa_pixel"):
            asset = item.get("assets", {}).get(key)
            if asset and asset.get("href"):
                attempts.append({"itemId": item.get("id"), "asset": key, "declaredType": asset.get("type"), "declaredUrl": asset["href"], **inspect_url(asset["href"], timeout)})
    result = {
        "executedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "stacSource": path_label(stac_path),
        "stacItemCount": len(payload.get("features", [])),
        "attempts": attempts,
        "usableRasterCount": sum(attempt["isTiffSignature"] for attempt in attempts),
        "decision": "AVAILABLE_FOR_QA" if any(attempt["isTiffSignature"] for attempt in attempts) else "ACCESS_BLOCKED",
        "accessExplanation": "The official landsatlook asset URLs redirect anonymous requests to EROS login HTML. Official AWS direct access uses a requester-pays bucket and requires AWS credentials. HTML is not saved or treated as raster data.",
        "scientificBoundary": "Landsat surface temperature is land-surface temperature, not a direct reservoir-temperature measurement or geothermal anomaly proof.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stac", type=Path, default=DEFAULT_STAC)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()
    try:
        print(json.dumps(run(args.stac, args.output, args.timeout), indent=2))
    except URLError as error:
        raise SystemExit(f"Landsat audit failed before an HTTP response: {error}") from error


if __name__ == "__main__":
    main()
