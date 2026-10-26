import csv
import gzip
import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from shapely.geometry import box

import scripts.audit_landsat_assets as landsat
import scripts.filter_ihfc_thailand as ihfc
from scripts.qc_terrain import build as build_terrain


def _write_minimal_workbook(path: Path) -> None:
    headers = ["q", "lat_NS", "long_EW", "environment", "Domain", "Country", "publication_reference", "Review_status", "Quality_Code", "ID_parent", "ID"]
    rows = [
        ["80", "13", "100", "[onshore (continental)]", "continental", "Thailand", "Ref_A", "completed", "U1", "P1", "A"],
        ["82", "13", "100", "[onshore (continental)]", "continental", "Thailand", "Ref_B", "open to review", "Ux", "P2", "B"],
        ["55", "12", "104", "[onshore (continental)]", "continental", "Vietnam", "Ref_C", "completed", "U2", "P3", "C"],
        ["60", "10", "101", "[offshore (continental)]", "marine", "", "Ref_D", "completed", "U2", "P4", "D"],
    ]
    strings = headers + [value for row in rows for value in row]
    shared = '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' + "".join(f"<si><t>{value}</t></si>" for value in strings) + "</sst>"
    def ref(index: int) -> str:
        return chr(65 + index)
    sheet_rows = []
    header_cells = "".join(f'<c r="{ref(index)}6" t="s"><v>{index}</v></c>' for index in range(len(headers)))
    sheet_rows.append(f'<row r="6">{header_cells}</row>')
    offset = len(headers)
    for row_number, row in enumerate(rows, start=7):
        cells = "".join(f'<c r="{ref(index)}{row_number}" t="s"><v>{offset + (row_number - 7) * len(headers) + index}</v></c>' for index in range(len(row)))
        sheet_rows.append(f'<row r="{row_number}">{cells}</row>')
    sheet = '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' + "".join(sheet_rows) + "</sheetData></worksheet>"
    with ZipFile(path, "w") as archive:
        archive.writestr("xl/sharedStrings.xml", shared)
        archive.writestr("xl/worksheets/sheet1.xml", sheet)


def test_ihfc_filter_preserves_repeated_measurements_and_classifies_context(tmp_path: Path, monkeypatch):
    workbook = tmp_path / "source.xlsx"
    boundary = tmp_path / "boundary.zip"
    boundary.write_bytes(b"synthetic boundary fixture")
    _write_minimal_workbook(workbook)
    monkeypatch.setattr(ihfc, "load_thailand_boundary", lambda _: box(99, 11, 102, 14))
    output = tmp_path / "ihfc.csv"
    summary_path = tmp_path / "summary.json"
    map_output = tmp_path / "ihfc.geojson"
    summary = ihfc.build(workbook, boundary, output, summary_path, tmp_path / "boundary.geojson", map_output)

    rows = list(csv.DictReader(output.open()))
    assert summary["workbookDataRowCount"] == 4
    assert summary["insideThailandRowCount"] == 2
    assert summary["insideThailandDistinctCoordinateCount"] == 1
    assert summary["insideThailandRepeatedRowsBeyondFirst"] == 1
    assert [row["ID"] for row in rows[:2]] == ["A", "B"]
    assert all(row["duplicate_coordinate_count"] == "2" for row in rows[:2])
    assert {row["spatial_class"] for row in rows} == {"INSIDE_THAILAND_BOUNDARY", "NEIGHBORING_COUNTRY", "OFFSHORE_REGIONAL_CONTEXT"}
    map_data = json.loads(map_output.read_text())
    assert len(map_data["features"]) == 2
    assert map_data["features"][0]["properties"]["duplicateCoordinateCount"] == 2
    assert map_data["provenance"]["license"] == "CC BY 4.0"


def test_terrain_pipeline_writes_round_trip_geotiffs_and_seam_audit(tmp_path: Path):
    tiles = []
    for name, value in [("N17E099", 100), ("N18E099", 100), ("N19E098", 100), ("N19E099", 100), ("N20E099", 100)]:
        path = tmp_path / f"{name}.hgt.gz"
        array = np.full((3601, 3601), value, dtype=">i2")
        with gzip.open(path, "wb") as handle:
            handle.write(array.tobytes())
        tiles.append(path)
    summary = build_terrain(tmp_path / "out", tiles)
    assert summary["tileCount"] == 5
    assert all(tile["noDataCount"] == 0 for tile in summary["tiles"])
    assert all(seam["nonMatchingPostCount"] == 0 for seam in summary["seamChecks"])
    assert (tmp_path / "out/N19E099.tif").exists()


def test_landsat_audit_requires_real_tiff_signature(tmp_path: Path, monkeypatch):
    stac = tmp_path / "items.json"
    stac.write_text(json.dumps({"features": [{"id": "scene", "assets": {"lwir11": {"href": "https://example.test/ST.tif", "type": "image/tiff"}}}]}))
    monkeypatch.setattr(landsat, "inspect_url", lambda *_: {"httpStatus": 200, "finalUrl": "https://login.test", "contentType": "text/html", "firstBytesHex": "3c21646f", "isTiffSignature": False, "isHtml": True})
    result = landsat.run(stac, tmp_path / "audit.json")
    assert result["usableRasterCount"] == 0
    assert result["decision"] == "ACCESS_BLOCKED"
