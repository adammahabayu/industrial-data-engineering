import pandas as pd
import streamlit as st

from dashboard.database import get_pipeline_history
from dashboard.components import (
    render_dataframe,
    render_metric_cards,
    render_page_header,
    render_line_chart,
)


def render_pipeline_monitoring() -> None:
    """Render pipeline execution monitoring page."""

    render_page_header(
        title="Pipeline Monitoring",
        description=(
            "Monitor ETL execution history, "
            "pipeline status, and execution performance."
        ),
    )

    st.divider()

    # Retrieve pipeline execution history
    try:
        history = get_pipeline_history()

    except Exception as exc:
        st.error(
            f"Unable to retrieve pipeline history: {exc}"
        )
        return

    if history.empty:
        st.info("No pipeline execution history available.")
        return

    # Prepare data
    history["start_time"] = pd.to_datetime(
        history["start_time"],
        errors="coerce",
    )

    history["duration_seconds"] = pd.to_numeric(
        history["duration_seconds"],
        errors="coerce",
    )

    history["status"] = (
        history["status"]
        .fillna("UNKNOWN")
        .str.upper()
    )

    # Calculate execution metrics
    total_runs = len(history)

    successful_runs = (
        history["status"] == "SUCCESS"
    ).sum()

    failed_runs = (
        history["status"] == "FAILED"
    ).sum()

    average_duration = (
        history["duration_seconds"].mean()
    )

    average_duration = (
        average_duration
        if pd.notna(average_duration)
        else 0
    )

    # Display metrics
    metrics = [
        {
            "label": "Total Executions",
            "value": f"{total_runs:,}",
        },
        {
            "label": "Successful Runs",
            "value": f"{successful_runs:,}",
        },
        {
            "label": "Failed Runs",
            "value": f"{failed_runs:,}",
        },
        {
            "label": "Average Duration",
            "value": f"{average_duration:.3f} sec",
        },
    ]

    render_metric_cards(metrics)

    st.divider()

    # Pipeline status filter
    st.subheader("Execution History")

    available_statuses = sorted(
        history["status"].unique().tolist()
    )

    selected_status = st.selectbox(
        "Filter by pipeline status",
        options=["ALL"] + available_statuses,
    )

    filtered_history = history.copy()

    if selected_status != "ALL":
        filtered_history = filtered_history[
            filtered_history["status"] == selected_status
        ]

    st.caption(
        f"Showing {len(filtered_history):,} "
        f"of {total_runs:,} pipeline executions."
    )

    display_columns = [
        "id",
        "pipeline_name",
        "start_time",
        "duration_seconds",
        "status",
        "rows_input",
        "rows_output",
        "rows_removed",
        "error_message",
    ]

    render_dataframe(
        dataframe=filtered_history[display_columns],
    )

    st.divider()

    # Execution duration chart
    st.subheader("Execution Performance")

    performance_data = history.dropna(
        subset=["start_time", "duration_seconds"]
    ).sort_values("start_time")

    if performance_data.empty:
        st.info("No execution performance data available.")

    else:
        render_line_chart(
            dataframe=performance_data,
            x_column="start_time",
            y_column="duration_seconds",
            title="Pipeline Execution Duration",
            color_column="pipeline_name",
        )

    st.divider()

    # Pipeline execution details
    st.subheader("Execution Details")

    selected_run_id = st.selectbox(
        "Select execution ID",
        options=history["id"].tolist(),
    )

    selected_run = history[
        history["id"] == selected_run_id
    ].iloc[0]

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.write("**Pipeline Name**")
        st.write(selected_run["pipeline_name"])

        st.write("**Execution Status**")
        st.write(selected_run["status"])

        st.write("**Start Time**")
        st.write(str(selected_run["start_time"]))

    with detail_col2:
        st.write("**Duration**")
        st.write(
            f"{selected_run['duration_seconds']} seconds"
        )

        st.write("**Rows Input**")
        st.write(f"{selected_run['rows_input']:,}")

        st.write("**Rows Output**")
        st.write(f"{selected_run['rows_output']:,}")

    st.write("**Rows Removed**")
    st.write(f"{selected_run['rows_removed']:,}")

    if pd.notna(selected_run["error_message"]):
        st.error(
            f"Error message: {selected_run['error_message']}"
        )