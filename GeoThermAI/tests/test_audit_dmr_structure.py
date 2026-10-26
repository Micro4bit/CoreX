from scripts.audit_dmr_structure import summarize_response


def test_summarizes_geometry_absence_without_inventing_features():
    payload = {"features": [{"attributes": {"OBJECTID": 1}}, {"attributes": {"OBJECTID": 2}}], "exceededTransferLimit": True}
    summary = summarize_response(200, payload, "application/json")
    assert summary["featureCount"] == 2
    assert summary["geometryCount"] == 0
    assert summary["exceededTransferLimit"] is True


def test_summarizes_arcgis_error_shape():
    summary = summarize_response(400, {"error": {"code": 400, "message": "Output format not supported"}}, "application/json")
    assert summary["httpStatus"] == 400
    assert summary["featureCount"] == 0
    assert summary["geometryCount"] == 0
    assert summary["error"]["code"] == 400
