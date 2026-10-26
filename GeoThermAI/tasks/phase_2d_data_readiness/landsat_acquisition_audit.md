# Landsat Surface Temperature acquisition audit — 2026-10-26

The local STAC response describes two Landsat 9 Collection 2 Level-2 ST scenes (path 130, rows 047 and 048, acquired 2026-10-16; reported scene cloud cover 13.7% and 12.24%). `scripts/audit_landsat_assets.py` tested the MTL, thermal, ST-QA and QA_PIXEL asset URLs for both scenes.

All eight requests ended at an EROS login page: HTTP 200 but `text/html`, first bytes `<!DOCTYPE`, and no TIFF signature. An anonymous direct cloud-object alternative returned HTTP 403. USGS commercial-cloud access is documented as requester-pays and requires an authorized cloud account. No credentials were available and no file was mislabeled as raster.

Decision: **NO-GO**. Usable raster count is zero; no cloud mask, scale/offset, fill-value, projection, temporal or spatial QA was performed. Exact response evidence is in `derived/landsat_asset_access_audit.json`.

