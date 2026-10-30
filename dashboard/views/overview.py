import pandas as pd
import streamlit as st

from dashboard.database import (
    get_database_summary,
    get_pipeline_history,
)

from dashboard.components import (
    render_dataframe,
    render_metric_cards,
    render_page_header,
    render_bar_chart,
)


def render_overview() -> None:
    """Render the main dashboard overview page."""

    # Page header
    render_page_header(
        title="Industrial Data Engineering Dashboard",
        description=(
            "Monitor industrial ETL pipelines, "
            "execution performance, and processed data."
        ),
    )

    st.divider()

    # Retrieve database information
    try:
        summary = get_database_summary()
        history = get_pipeline_history()

    except Exception as exc:
        st.error(
            f"Unable to retrieve dashboard data: {exc}"
        )
        return

    # Calculate summary metrics
    total_runs = summary["pipeline_runs"]
    successful_runs = summary["successful_runs"]
    failed_runs = summary["failed_runs"]

    total_records = (
        summary["machine_sensor_readings"]
        + summary["centrifugal_pump_readings"]
    )

    success_rate = (
        successful_runs / total_runs * 100
        if total_runs > 0
        else 0
    )

    # Display metric cards
    metrics = [
        {
            "label": "Total Pipeline Runs",
            "value": f"{total_runs:,}",
        },
        {
            "label": "Success Rate",
            "value": f"{success_rate:.1f}%",
        },
        {
            "label": "Total Sensor Records",
            "value": f"{total_records:,}",
        },
        {
            "label": "Failed Runs",
            "value": f"{failed_runs:,}",
        },
    ]

    render_metric_cards(metrics)

    st.divider()

    # Pipeline execution status
    st.subheader("Pipeline Execution Status")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Successful Executions",
            value=f"{successful_runs:,}",
        )

    with col2:
        st.metric(
            label="Failed Executions",
            value=f"{failed_runs:,}",
        )

    # Pipeline execution summary chart
    if total_runs > 0:

        status_data = pd.DataFrame(
            [
                {
                    "Status": "SUCCESS",
                    "Executions": successful_runs,
                },
                {
                    "Status": "FAILED",
                    "Executions": failed_runs,
                },
            ]
        )

        # Remove statuses with zero executions
        status_data = status_data[
            status_data["Executions"] > 0
        ]

        render_bar_chart(
            dataframe=status_data,
            x_column="Status",
            y_column="Executions",
            title="Pipeline Execution Summary",
        )

    else:
        st.info(
            "No pipeline execution history available."
        )

    st.divider()

    # Sensor data summary
    st.subheader("Sensor Data Summary")

    sensor_col1, sensor_col2 = st.columns(2)

    with sensor_col1:
        st.metric(
            label="Machine Sensor Records",
            value=f"{summary['machine_sensor_readings']:,}",
        )

    with sensor_col2:
        st.metric(
            label="Centrifugal Pump Records",
            value=f"{summary['centrifugal_pump_readings']:,}",
        )

    st.caption(
        "Machine sensor data currently uses synthetic sample records. "
        "Centrifugal pump records come from the external industrial dataset."
    )

    st.divider()

    # Pipeline execution history
    st.subheader("Recent Pipeline Executions")

    if history.empty:

        st.info(
            "No pipeline execution history available."
        )

    else:

        display_columns = [
            "id",
            "pipeline_name",
            "start_time",
            "duration_seconds",
            "status",
            "rows_input",
            "rows_output",
            "rows_removed",
        ]

        render_dataframe(
            dataframe=history[display_columns].head(10),
        )