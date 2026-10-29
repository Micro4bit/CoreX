"""Thai Geoscience Data Harmonization Engine for GeoThermAI.

Reconciles incompatible schemas, coordinate systems, spatial grids, and physical units
across heterogeneous Thai and international geoscience datasets:
- DMR 1:250k Geology and Active Faults (EPSG:32647 / Indian 1975 / WGS84)
- SRTM 1-arc-second Elevation DEM (WGS84 EPSG:4326)
- IHFC Heat Flow Borehole Database (Global WGS84 point observations)
- Geothermal Manifestation Records (Wood 2014, Ngansom 2021)
- DGR Hydrogeology and Groundwater Sensitivity (Aquifer types, depth, salinity)
- Hot-Spring Geochemistry (Silica & Cation Geothermometry)
- TMD Earthquake Observation Division Seismicity (M >= 2.5 microseismicity)
- Satellite-derived Context (Landsat LST, Bouguer Gravity Anomalies)

CRITICAL ARCHITECTURAL DISTINCTION:
- DATA HARMONIZATION: Unifies schemas, coordinate reference systems (CRS),
  canonical physical units, spatial grid alignment, and missing value encodings.
- MODEL NORMALIZATION / STANDARDIZATION: Model-specific scaling (e.g. z-score,
  min-max, quantile transform) performed downstream strictly inside training folds.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


class HarmonizedCrs(str, enum.Enum):
    """Supported coordinate reference systems for harmonization."""
    GEOGRAPHIC_WGS84 = "EPSG:4326"
    PROJECTED_UTM47N = "EPSG:32647"
    PROJECTED_UTM48N = "EPSG:32648"


class DatasetProvenanceTier(str, enum.Enum):
    """Data provenance and reliability tiers."""
    TIER_1_OFFICIAL_DIRECT = "TIER_1_OFFICIAL_DIRECT"      # Direct primary agency record (e.g. DMR, TMD, DGR)
    TIER_2_PEER_REVIEWED = "TIER_2_PEER_REVIEWED"          # Peer-reviewed publication with verified primary data
    TIER_3_GLOBAL_COMPILATION = "TIER_3_GLOBAL_COMPILATION"# International aggregator (e.g. IHFC, USGS, NASA)
    TIER_4_PROVISIONAL = "TIER_4_PROVISIONAL"              # Secondary or text narrative without independent check
    TIER_5_WITHHELD = "TIER_5_WITHHELD"                    # Unresolved discrepancies or invalid coordinates


class HarmonizationStatus(str, enum.Enum):
    """Harmonization status for individual records or datasets."""
    HARMONIZED_VERIFIED = "HARMONIZED_VERIFIED"
    HARMONIZED_WITH_WARNINGS = "HARMONIZED_WITH_WARNINGS"
    PROVISIONAL_NEEDS_REVIEW = "PROVISIONAL_NEEDS_REVIEW"
    REJECTED_INVALID_CRS = "REJECTED_INVALID_CRS"
    REJECTED_LABEL_LEAKAGE = "REJECTED_LABEL_LEAKAGE"
    REJECTED_SPARSE_INTERPOLATION = "REJECTED_SPARSE_INTERPOLATION"


# Canonical Physical Units dictionary for geoscientific parameters
CANONICAL_PHYSICAL_UNITS: dict[str, str] = {
    "heat_flow": "mW/m^2",
    "temperature": "deg_C",
    "surface_temperature": "deg_C",
    "reservoir_temperature": "deg_C",
    "elevation": "m",
    "slope": "deg",
    "fault_distance": "km",
    "magma_distance": "km",
    "seismic_event_density": "events_per_50km2",
    "stress_azimuth": "deg_azimuth",
    "dilation_tendency": "dimensionless_ratio",
    "bouguer_gravity": "mGal",
    "silica_concentration": "mg/L",
    "cation_concentration": "mg/L",
    "ph": "pH_units",
    "aquifer_depth": "m",
    "aquifer_yield": "m^3/hr",
    "tds": "mg/L",
}

# Features that constitute fatal target leakage if used as predictors
PROHIBITED_PREDICTOR_KEYWORDS: tuple[str, ...] = (
    "manifestation",
    "hot_spring",
    "thermal_spring",
    "target_label",
    "nearest_spring",
    "known_geothermal",
)


@dataclass(frozen=True)
class HarmonizedRecord:
    """Standardized geoscientific observation record."""
    source_id: str
    record_uid: str
    latitude_wgs84: float
    longitude_wgs84: float
    easting_utm47n: float | None
    northing_utm47n: float | None
    feature_family: str
    raw_value: Any
    harmonized_value: float | None
    canonical_unit: str
    uncertainty: float | None
    provenance_tier: DatasetProvenanceTier
    status: HarmonizationStatus
    quality_notes: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HarmonizationSummary:
    """Summary of harmonization batch execution."""
    dataset_name: str
    total_records: int
    harmonized_count: int
    warnings_count: int
    rejected_count: int
    missing_value_count: int
    target_crs: HarmonizedCrs
    status: HarmonizationStatus
    summary_notes: str


class GeoscienceHarmonizer:
    """Harmonizes raw Thai geoscience datasets into unified reference frames."""

    def __init__(self, target_crs: HarmonizedCrs = HarmonizedCrs.GEOGRAPHIC_WGS84) -> None:
        self.target_crs = target_crs

    # -------------------------------------------------------------------------
    # 1. Geothermal Manifestation Records Harmonization
    # -------------------------------------------------------------------------
    @staticmethod
    def harmonize_manifestation_record(row: Mapping[str, Any]) -> HarmonizedRecord:
        """Harmonize a geothermal manifestation record from master label registries."""
        uid = str(row.get("record_uid") or row.get("source_row_id") or "UNKNOWN")
        source_id = str(row.get("source_id") or row.get("published_reference") or "UNKNOWN")
        
        # Latitude / Longitude parsing
        lat_val = row.get("derived_latitude_wgs84") or row.get("original_lat")
        lon_val = row.get("derived_longitude_wgs84") or row.get("original_lon")
        
        try:
            lat = float(lat_val)
            lon = float(lon_val)
            has_valid_coords = (5.5 <= lat <= 20.5) and (97.0 <= lon <= 106.0)
        except (ValueError, TypeError):
            lat, lon = float("nan"), float("nan")
            has_valid_coords = False

        coord_status = str(row.get("coordinate_validation_status") or row.get("coordinate_status") or "")
        
        # Temperature parsing
        temp_raw = row.get("surface_temperature_c")
        temp_val: float | None = None
        if temp_raw is not None and str(temp_raw).strip() not in ("", "Unmeasured", "Not reported"):
            try:
                temp_val = float(temp_raw)
            except (ValueError, TypeError):
                temp_val = None

        # Determine provenance tier and harmonization status
        if not has_valid_coords or "WITHHELD" in coord_status or "MISMATCH" in coord_status:
            tier = DatasetProvenanceTier.TIER_5_WITHHELD
            status = HarmonizationStatus.PROVISIONAL_NEEDS_REVIEW
            notes = "Withheld: coordinate discrepancy or missing DMS comparator (>1 km mismatch or text-only inference)."
        elif "PROVISIONAL" in coord_status or "NO_DMS_COMPARATOR" in coord_status:
            tier = DatasetProvenanceTier.TIER_4_PROVISIONAL
            status = HarmonizationStatus.HARMONIZED_WITH_WARNINGS
            notes = "Provisional: coordinates derived from regional UTM zone without independent ground verification."
        else:
            tier = DatasetProvenanceTier.TIER_2_PEER_REVIEWED
            status = HarmonizationStatus.HARMONIZED_VERIFIED
            notes = "Internally consistent coordinates (<100m DMS-UTM agreement); primary literature verified."

        return HarmonizedRecord(
            source_id=source_id,
            record_uid=uid,
            latitude_wgs84=lat,
            longitude_wgs84=lon,
            easting_utm47n=float(row["source_easting_m"]) if row.get("source_easting_m") else None,
            northing_utm47n=float(row["source_northing_m"]) if row.get("source_northing_m") else None,
            feature_family="surface_manifestation",
            raw_value=temp_raw,
            harmonized_value=temp_val,
            canonical_unit=CANONICAL_PHYSICAL_UNITS["surface_temperature"],
            uncertainty=2.0 if temp_val is not None else None,
            provenance_tier=tier,
            status=status,
            quality_notes=notes,
            metadata={
                "observation_type": row.get("observation_type", "Hot Spring Manifestation"),
                "system_group_id": row.get("proposed_site_group_id") or row.get("system_group_id"),
                "subsurface_proven": False,  # Surface manifestation != commercial reservoir!
            },
        )

    # -------------------------------------------------------------------------
    # 2. IHFC Heat Flow Harmonization (with strict anti-interpolation guardrail)
    # -------------------------------------------------------------------------
    @staticmethod
    def harmonize_ihfc_heat_flow_record(row: Mapping[str, Any]) -> HarmonizedRecord:
        """Harmonize an IHFC global heat flow observation inside Thailand."""
        rec_id = str(row.get("record_id") or row.get("id") or "IHFC_UNKNOWN")
        
        try:
            lat = float(row["latitude"])
            lon = float(row["longitude"])
            q_val = float(row["heat_flow_mw_m2"]) if row.get("heat_flow_mw_m2") is not None else None
        except (ValueError, KeyError, TypeError):
            return HarmonizedRecord(
                source_id="IHFC_2024",
                record_uid=rec_id,
                latitude_wgs84=float("nan"),
                longitude_wgs84=float("nan"),
                easting_utm47n=None,
                northing_utm47n=None,
                feature_family="terrestrial_heat_flow",
                raw_value=None,
                harmonized_value=None,
                canonical_unit=CANONICAL_PHYSICAL_UNITS["heat_flow"],
                uncertainty=None,
                provenance_tier=DatasetProvenanceTier.TIER_3_GLOBAL_COMPILATION,
                status=HarmonizationStatus.REJECTED_INVALID_CRS,
                quality_notes="Malformed coordinates or heat flow value.",
            )

        # Scientific quality checks: 154/154 Thailand records lack explicit uncertainty
        uncertainty = float(row["uncertainty"]) if row.get("uncertainty") is not None and not np.isnan(float(row.get("uncertainty", "nan"))) else None
        
        notes = (
            "Point observation only. SPATIAL INTERPOLATION FORBIDDEN: Sparse borehole points "
            "(63 in North, 154 nationwide) cannot be kriged or interpolated into predictive rasters "
            "without creating fictitious bullseye artifacts. Validation overlay use only."
        )

        return HarmonizedRecord(
            source_id="IHFC_2024",
            record_uid=rec_id,
            latitude_wgs84=lat,
            longitude_wgs84=lon,
            easting_utm47n=None,
            northing_utm47n=None,
            feature_family="terrestrial_heat_flow",
            raw_value=row.get("heat_flow_mw_m2"),
            harmonized_value=q_val,
            canonical_unit=CANONICAL_PHYSICAL_UNITS["heat_flow"],
            uncertainty=uncertainty,
            provenance_tier=DatasetProvenanceTier.TIER_3_GLOBAL_COMPILATION,
            status=HarmonizationStatus.HARMONIZED_WITH_WARNINGS if uncertainty is None else HarmonizedStatus.HARMONIZED_VERIFIED,
            quality_notes=notes,
            metadata={
                "depth_m": row.get("depth_m"),
                "gradient_mk_m": row.get("temp_gradient_mk_m"),
                "interpolation_eligible": False,  # Strict guardrail
                "validation_overlay_eligible": True,
            },
        )

    # -------------------------------------------------------------------------
    # 3. Geochemical Geothermometry Harmonization
    # -------------------------------------------------------------------------
    @staticmethod
    def calculate_quartz_geothermometer(sio2_mg_l: float) -> float | None:
        """Calculate Quartz conductive cooling reservoir temperature (Fournier 1977).
        
        Formula: T_C = 1309 / (5.19 - log10(SiO2)) - 273.15
        """
        if sio2_mg_l <= 0:
            return None
        try:
            val = 1309.0 / (5.19 - np.log10(sio2_mg_l)) - 273.15
            return round(val, 1) if 20.0 <= val <= 350.0 else None
        except Exception:
            return None

    @staticmethod
    def calculate_chalcedony_geothermometer(sio2_mg_l: float) -> float | None:
        """Calculate Chalcedony reservoir temperature (Arnorsson 1975 / Fournier 1977).
        
        Formula: T_C = 1032 / (4.69 - log10(SiO2)) - 273.15
        """
        if sio2_mg_l <= 0:
            return None
        try:
            val = 1032.0 / (4.69 - np.log10(sio2_mg_l)) - 273.15
            return round(val, 1) if 0.0 <= val <= 250.0 else None
        except Exception:
            return None

    @staticmethod
    def calculate_nak_geothermometer(na_mg_l: float, k_mg_l: float) -> float | None:
        """Calculate Na-K cation geothermometer (Giggenbach 1988).
        
        Formula: T_C = 1390 / (1.750 - log10(K/Na_atomic)) - 273.15
        where K and Na are molar/atomic concentrations (mg/L / atomic weight).
        """
        if na_mg_l <= 0 or k_mg_l <= 0:
            return None
        try:
            # Na MW = 22.99 g/mol, K MW = 39.10 g/mol
            # K/Na molar ratio = (K/39.10) / (Na/22.99)
            k_mol = k_mg_l / 39.10
            na_mol = na_mg_l / 22.99
            log_k_na = np.log10(k_mol / na_mol)
            denom = 1.750 - log_k_na
            if denom <= 0:
                return None
            val = (1390.0 / denom) - 273.15
            return round(val, 1) if 50.0 <= val <= 400.0 else None
        except Exception:
            return None

    # -------------------------------------------------------------------------
    # 4. Anti-Leakage Predictor Validation
    # -------------------------------------------------------------------------
    @staticmethod
    def validate_predictor_set_safety(predictor_names: Sequence[str]) -> tuple[bool, list[str]]:
        """Verify that proposed predictors contain zero target leakage or prohibited hot-spring proxies."""
        violations: list[str] = []
        for name in predictor_names:
            lowered = name.lower().strip()
            for kw in PROHIBITED_PREDICTOR_KEYWORDS:
                if kw in lowered:
                    violations.append(f"FATAL LEAKAGE: Feature '{name}' matches prohibited keyword '{kw}'")
        return len(violations) == 0, violations

    # -------------------------------------------------------------------------
    # 5. Harmonization vs Normalization Separation Enforcement
    # -------------------------------------------------------------------------
    @staticmethod
    def enforce_harmonization_separation(
        data: pd.DataFrame,
        is_ml_training_fold: bool = False,
    ) -> pd.DataFrame:
        """Ensure harmonization does NOT perform model-specific normalization.
        
        Harmonization converts units, resolves CRS, and flags missing values.
        It must NEVER apply z-scores, min-max [0,1], or normal scores across the whole
        dataset before spatial cross-validation partitioning.
        """
        df = data.copy()
        
        # Check if caller mistakenly applied global standardization
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col in ("latitude_wgs84", "longitude_wgs84", "easting_utm47n", "northing_utm47n"):
                continue
            vals = df[col].dropna()
            if len(vals) > 10:
                mean = vals.mean()
                std = vals.std()
                # If mean is approximately 0 and std is approximately 1, caller applied pre-split z-score normalization!
                if abs(mean) < 1e-2 and abs(std - 1.0) < 0.05 and not is_ml_training_fold:
                    raise ValueError(
                        f"CRITICAL METHODOLOGICAL LEAKAGE: Column '{col}' exhibits global z-score normalization "
                        f"(mean={mean:.4f}, std={std:.4f}) before cross-validation fold splitting. "
                        f"Harmonization must preserve raw physical units ({CANONICAL_PHYSICAL_UNITS.get(col, 'native')})."
                    )
        return df
