import json
from pathlib import Path

from pyproj import Transformer

from scripts.preprocess_geology import build


def test_preprocesses_known_epsg_32647_fixture_without_mutating_source(tmp_path: Path):
    lon, lat = 99.0, 18.0
    to_utm = Transformer.from_crs(4326, 32647, always_xy=True)
    x, y = to_utm.transform(lon, lat)
    fixture = {
        "spatialReference": {"wkid": 32647},
        "features": [{
            "attributes": {"OBJECTID": 1, "TEXT_SYM": "TEST", "YEAR_COMPI": 2026},
            "geometry": {"rings": [[[x, y], [x, y + 100], [x + 100, y + 100], [x + 100, y], [x, y]]]},
        }],
    }
    source = tmp_path / "source.json"
    original = json.dumps(fixture)
    source.write_text(original)

    manifest = build(source, tmp_path / "out", tolerance_m=0)
    output = json.loads((tmp_path / "out/dmr-rock-units-north.full.geojson").read_text())
    first = output["features"][0]["geometry"]["coordinates"][0][0]

    assert first[0] == pytest.approx(lon, abs=1e-7)
    assert first[1] == pytest.approx(lat, abs=1e-7)
    assert manifest["sourceCrs"] == "EPSG:32647"
    assert manifest["topologyRepairCount"] == 0
    assert manifest["orphanHoleCount"] == 0
    assert manifest["inputFeatureCount"] == manifest["featureCount"] == 1
    assert manifest["outputBoundsWgs84"] is not None
    assert source.read_text() == original


def test_rejects_unexpected_source_crs(tmp_path: Path):
    source = tmp_path / "source.json"
    source.write_text(json.dumps({"spatialReference": {"wkid": 4326}, "features": []}))
    with pytest.raises(ValueError, match="EPSG:32647"):
        build(source, tmp_path / "out", tolerance_m=25)


def test_rejects_an_unassigned_hole_instead_of_silently_dropping_it(tmp_path: Path):
    fixture = {
        "spatialReference": {"wkid": 32647},
        "features": [{
            "attributes": {"OBJECTID": 99},
            "geometry": {"rings": [
                [[500000, 2000000], [500000, 2000100], [500100, 2000100], [500100, 2000000], [500000, 2000000]],
                [[600000, 2100000], [600100, 2100000], [600100, 2100100], [600000, 2100100], [600000, 2100000]],
            ]},
        }],
    }
    source = tmp_path / "source.json"
    source.write_text(json.dumps(fixture))
    with pytest.raises(ValueError, match="refusing to drop"):
        build(source, tmp_path / "out", tolerance_m=0)


def test_adds_only_metadata_backed_legend_labels(tmp_path: Path):
    lon, lat = 99.0, 18.0
    to_utm = Transformer.from_crs(4326, 32647, always_xy=True)
    x, y = to_utm.transform(lon, lat)
    source = tmp_path / "source.json"
    source.write_text(json.dumps({
        "spatialReference": {"wkid": 32647},
        "features": [{"attributes": {"OBJECTID": 1, "TEXT_SYM": "Qa", "YEAR_COMPI": 2026}, "geometry": {"rings": [[[x, y], [x, y + 100], [x + 100, y + 100], [x + 100, y], [x, y]]]}}],
    }))
    metadata = tmp_path / "metadata.json"
    metadata.write_text(json.dumps({"drawingInfo": {"renderer": {"uniqueValueInfos": [{"value": "250K-0010-Qa", "label": "Qa authoritative label"}]}}}))
    manifest = build(source, tmp_path / "out", 0, metadata_path=metadata)
    output = json.loads((tmp_path / "out/dmr-rock-units-north.simplified.geojson").read_text())
    assert output["features"][0]["properties"]["legendLabel"] == "Qa authoritative label"
    assert manifest["matchedSourceSymbolCount"] == 1
    assert manifest["unmatchedSourceSymbols"] == []


import pytest
