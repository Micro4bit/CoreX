"""Streamlit entry point for the GeoThermAI Phase 2A evidence explorer."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pydeck as pdk
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from config.settings import (  # noqa: E402
    APP_TITLE,
    GIS_INVENTORY_CSV,
    OBSERVATIONS_CSV,
    ROCK_UNITS_ESRIJSON,
    SCIENTIFIC_SCOPE_NOTICE,
    SOURCE_INVENTORY_CSV,
    TERRAIN_SUMMARY_CSV,
)
from geothermai.coordinate_utils import displayable_observations, map_color  # noqa: E402
from geothermai.data_loader import (  # noqa: E402
    load_csv_inventory,
    load_observations,
    load_rock_units_geojson,
)
from geothermai.evidence_engine import describe_evidence_availability  # noqa: E402
from geothermai.model_interface import predictive_model_status  # noqa: E402
from geothermai.provenance import evidence_summary_markdown, record_provenance  # noqa: E402


st.set_page_config(page_title="GeoThermAI", page_icon="🗺️", layout="wide")


@st.cache_data(show_spinner=False)
def app_data() -> tuple[pd.DataFrame, object, pd.DataFrame, pd.DataFrame]:
    observations, validation = load_observations(OBSERVATIONS_CSV)
    return (
        observations,
        validation,
        load_csv_inventory(SOURCE_INVENTORY_CSV),
        load_csv_inventory(GIS_INVENTORY_CSV),
    )


@st.cache_data(show_spinner=False)
def terrain_summary() -> pd.DataFrame | None:
    if not TERRAIN_SUMMARY_CSV.is_file():
        return None
    return pd.read_csv(TERRAIN_SUMMARY_CSV)


@st.cache_data(show_spinner=False)
def rock_units() -> object:
    return load_rock_units_geojson(ROCK_UNITS_ESRIJSON)


def quality_metrics(observations: pd.DataFrame, validation: object) -> dict[str, int]:
    longitude = pd.to_numeric(observations["derived_longitude_wgs84"], errors="coerce")
    latitude = pd.to_numeric(observations["derived_latitude_wgs84"], errors="coerce")
    return {
        "records": len(observations),
        "missing_coordinates": int(longitude.isna().sum() + latitude.isna().sum()),
        "review_required": int(
            observations["coordinate_validation_status"].str.contains(
                "MISMATCH|MISSING", na=False
            ).sum()
        ),
        "provisional": int(
            observations["coordinate_validation_status"].eq(
                "CRS_INFERRED_NO_DMS_COMPARATOR"
            ).sum()
        ),
        "missing_temperature": len(validation.missing_temperature_ids),
    }


def observations_for_filters(
    observations: pd.DataFrame, selected_sources: list[str], selected_regions: list[str]
) -> pd.DataFrame:
    return observations.loc[
        observations["source_id"].isin(selected_sources)
        & observations["source_region"].isin(selected_regions)
    ].copy()


def build_map(
    points: pd.DataFrame, show_geology: bool, show_terrain: bool
) -> tuple[pdk.Deck, list[str]]:
    warnings: list[str] = []
    if points.empty:
        return pdk.Deck(), ["No displayable observations match the selected filters."]
    points = points.copy()
    points["fill_color"] = points["coordinate_category"].map(map_color)
    layers: list[object] = []
    if show_geology:
        geological = rock_units()
        if geological.usable and geological.data:
            layers.append(
                pdk.Layer(
                    "GeoJsonLayer",
                    geological.data,
                    id="rock-units",
                    opacity=0.18,
                    stroked=True,
                    filled=True,
                    get_fill_color=[71, 85, 105, 25],
                    get_line_color=[100, 116, 139, 110],
                    line_width_min_pixels=1,
                    pickable=True,
                )
            )
        else:
            warnings.append(f"Rock-unit context unavailable: {geological.message}")
    if show_terrain:
        summary = terrain_summary()
        if summary is None:
            warnings.append("Terrain summary is unavailable; no terrain context is displayed.")
        else:
            warnings.append(
                "Terrain context is available as a source-derived summary below; it is not a prospectivity layer."
            )
    layers.append(
        pdk.Layer(
            "ScatterplotLayer",
            points,
            id="thermal-observations",
            get_position="[longitude, latitude]",
            get_fill_color="fill_color",
            get_radius=4800,
            radius_min_pixels=5,
            radius_max_pixels=10,
            pickable=True,
        )
    )
    view = pdk.ViewState(
        latitude=float(points["latitude"].mean()),
        longitude=float(points["longitude"].mean()),
        zoom=6.3 if points["source_region"].nunique() > 1 else 8.6,
        pitch=0,
    )
    return (
        pdk.Deck(
            layers=layers,
            initial_view_state=view,
            map_style="light",
            tooltip={
                "html": "<b>{source_record_code}</b><br/>{source_site_name}<br/>"
                "Region: {source_region}<br/>Coordinate status: {coordinate_validation_status}",
                "style": {"backgroundColor": "#0f172a", "color": "white"},
            },
        ),
        warnings,
    )


def show_overview(metrics: dict[str, int], sources: pd.DataFrame) -> None:
    st.header("Overview")
    st.info(SCIENTIFIC_SCOPE_NOTICE)
    st.markdown(
        "Use this MVP to inspect published observations, provenance, and available GIS context. "
        "It is intentionally an evidence explorer—not an AI prediction tool."
    )
    a, b, c, d = st.columns(4)
    a.metric("Loaded observation records", metrics["records"])
    b.metric("Published sources", len(sources))
    c.metric("Coordinate-review records", metrics["review_required"])
    d.metric("Missing temperature values", metrics["missing_temperature"])
    st.subheader("Current research boundary")
    st.warning(
        "Predictive ML is not authorized in this MVP. Coordinate conflicts, inferred southern "
        "UTM interpretation, missing authoritative inventory data, and GIS licensing/coverage "
        "questions remain visible rather than being resolved by the application."
    )


def show_map(observations: pd.DataFrame, sources: pd.DataFrame) -> None:
    st.header("GIS Explorer")
    st.caption("Marker color communicates coordinate handling, not temperature, resource quality, or potential.")
    left, right = st.columns([1, 3])
    with left:
        source_ids = st.multiselect(
            "Sources", sorted(observations["source_id"].unique()), default=sorted(observations["source_id"].unique())
        )
        regions = st.multiselect(
            "Regions", sorted(observations["source_region"].unique()), default=sorted(observations["source_region"].unique())
        )
        provisional = st.checkbox(
            "Include provisional southern coordinates", value=False,
            help="These source coordinates use a working CRS that has no independent DMS comparator.",
        )
        geology = st.checkbox("Show northern geological units", value=False)
        terrain = st.checkbox("Show terrain-context availability", value=False)
        st.markdown("**Legend**")
        st.markdown("- Blue: internally consistent UTM/DMS display coordinate\n- Amber: provisional source-CRS interpretation\n- Red: coordinate review required (not plotted)")
    filtered = observations_for_filters(observations, source_ids, regions)
    plotted = displayable_observations(filtered, include_provisional=provisional)
    deck, messages = build_map(plotted, geology, terrain)
    with right:
        st.pydeck_chart(deck, use_container_width=True)
        for message in messages:
            st.caption(message)
    if terrain:
        summary = terrain_summary()
        if summary is not None:
            st.subheader("Available northern terrain summary")
            st.dataframe(summary, use_container_width=True, hide_index=True)
    st.subheader("Source identification")
    st.dataframe(
        sources[["source_id", "reference", "publication_date", "evidence_tier", "license_or_reuse_status"]],
        use_container_width=True,
        hide_index=True,
    )


def show_data_quality(observations: pd.DataFrame, validation: object, layers: pd.DataFrame) -> None:
    st.header("Data Quality")
    metrics = quality_metrics(observations, validation)
    a, b, c, d = st.columns(4)
    a.metric("Total records", metrics["records"])
    b.metric("Missing display coordinate values", metrics["missing_coordinates"])
    c.metric("Records requiring review", metrics["review_required"])
    d.metric("Provisional coordinate records", metrics["provisional"])
    if validation.missing_columns:
        st.error(f"Observation schema is missing required columns: {', '.join(validation.missing_columns)}")
    if validation.duplicate_record_ids:
        st.error(f"Duplicate record IDs: {', '.join(validation.duplicate_record_ids)}")
    if validation.invalid_coordinate_ids:
        st.error(f"Invalid numeric coordinates: {', '.join(validation.invalid_coordinate_ids)}")
    if validation.missing_crs_ids:
        st.warning(f"Records missing CRS information: {', '.join(validation.missing_crs_ids)}")
    st.subheader("Records by source and region")
    st.dataframe(
        observations.groupby(["source_id", "source_region"], dropna=False).size().reset_index(name="record_count"),
        use_container_width=True,
        hide_index=True,
    )
    st.subheader("Coordinate validation status")
    st.dataframe(
        observations.groupby("coordinate_validation_status", dropna=False).size().reset_index(name="record_count"),
        use_container_width=True,
        hide_index=True,
    )
    st.subheader("GIS layer availability and licensing")
    st.dataframe(
        layers[["layer_id", "layer_category", "access_status", "license_or_permission_status", "quality_and_missing_data"]],
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        "Layer status is read from the local verified GIS inventory. A locally present file does not imply cleared reuse or scientific suitability."
    )


def show_source_registry(observations: pd.DataFrame, sources: pd.DataFrame) -> None:
    st.header("Source Registry")
    query = st.text_input("Filter published observations", placeholder="Record ID, site, source, province…")
    searchable = observations.fillna("").astype(str).agg(" ".join, axis=1)
    filtered = observations.loc[searchable.str.contains(query, case=False, na=False)] if query else observations
    display_columns = [
        "record_uid", "source_region", "source_record_code", "source_site_name",
        "surface_temperature_c", "coordinate_validation_status", "license_or_reuse_status",
    ]
    st.dataframe(filtered[display_columns], use_container_width=True, hide_index=True)
    st.subheader("Source-level registry")
    st.dataframe(sources, use_container_width=True, hide_index=True)
    if filtered.empty:
        return
    selected_id = st.selectbox("Inspect record provenance", filtered["record_uid"].tolist())
    record = filtered.loc[filtered["record_uid"] == selected_id].iloc[0]
    st.dataframe(record_provenance(record), use_container_width=True, hide_index=True)


def show_evidence_explorer(observations: pd.DataFrame, layers: pd.DataFrame) -> None:
    st.header("Evidence Explorer")
    st.info("This workflow reports evidence availability and data gaps. It does not calculate a potential score.")
    selected_id = st.selectbox("Select a published observation", observations["record_uid"].tolist(), key="evidence_record")
    record = observations.loc[observations["record_uid"] == selected_id].iloc[0]
    availability = describe_evidence_availability(record, layers)
    st.subheader(f"Observation: {availability.record_uid}")
    st.write(f"Coordinate status: `{availability.coordinate_status}`")
    first, second = st.columns(2)
    first.markdown("**Locally inspected layer records**")
    first.write(list(availability.available_layer_ids) or "None")
    second.markdown("**Unavailable or restricted layer records**")
    second.write(list(availability.unavailable_or_restricted_layer_ids) or "None")
    st.warning(availability.interpretation_notice)
    summary = evidence_summary_markdown(record, layers)
    st.download_button(
        "Download documented evidence summary (.md)",
        data=summary,
        file_name=f"evidence_summary_{selected_id}.md",
        mime="text/markdown",
    )


def show_research_status() -> None:
    st.header("Research Status")
    st.success("Current product boundary: descriptive geospatial evidence exploration.")
    st.warning("Predictive research readiness: not authorized / not validated.")
    st.markdown(
        "**Known blockers retained in the local research record:**\n\n"
        "- Northern CR_02 has an unresolved source-coordinate discrepancy; CM_16 lacks a DMS comparator.\n"
        "- Southern source UTM-zone interpretation remains an inferred working CRS; its 31-row table conflicts with prose saying 30 samples.\n"
        "- Structural geometry, licensing/reuse terms, authoritative occurrence inventory, and independent validation design remain incomplete."
    )


def show_ai_module() -> None:
    st.header("AI Module")
    contract = predictive_model_status()
    st.error(contract.status)
    st.markdown("**Future model prerequisites**")
    st.write(list(contract.required_inputs))
    st.markdown("**Required future outputs**")
    st.write(list(contract.required_outputs))
    st.caption("No predictive model, simulated result, heatmap, or performance metric is included in this MVP.")


def main() -> None:
    st.title(APP_TITLE)
    try:
        observations, validation, sources, layers = app_data()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()
    except Exception as exc:
        st.exception(exc)
        st.stop()
    metrics = quality_metrics(observations, validation)
    page = st.sidebar.radio(
        "Section",
        ["Overview", "GIS Explorer", "Data Quality", "Source Registry", "Evidence Explorer", "Research Status", "AI Module"],
    )
    st.sidebar.caption("Data backend: local Phase 1C research artifacts")
    if page == "Overview":
        show_overview(metrics, sources)
    elif page == "GIS Explorer":
        show_map(observations, sources)
    elif page == "Data Quality":
        show_data_quality(observations, validation, layers)
    elif page == "Source Registry":
        show_source_registry(observations, sources)
    elif page == "Evidence Explorer":
        show_evidence_explorer(observations, layers)
    elif page == "Research Status":
        show_research_status()
    else:
        show_ai_module()


if __name__ == "__main__":
    main()
