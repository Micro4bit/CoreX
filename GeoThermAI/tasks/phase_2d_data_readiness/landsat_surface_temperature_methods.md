# Landsat Surface Temperature method gate

When real USGS Collection 2 Level-2 ST assets become available, the pipeline must preserve product ID and MTL metadata, verify GeoTIFF signatures with Rasterio, reproject only through a recorded transform, apply the official ST scale factor `0.00341802` and offset `149.0 K`, and treat DN 0 as fill. QA_PIXEL and ST QA/cloud information must be used; cloud/shadow, fill and missing-ST pixels must be masked before analysis.

Acquisitions must be compared across seasons and land-cover conditions. Land-surface temperature is an atmospheric/land-surface product, not deep reservoir temperature. Any future satellite feature requires a preregistered ablation against a geology-only baseline under the same independent spatial folds. No raster or ablation is authorized or available in Phase 2D.

