import pandas as pd
import streamlit as st

from dashboard.database import (
    get_machine_sensor_data,
    get_pump_sensor_data,
)
from dashboard.components import (
    render_dataframe,
    render_metric_cards,
    render_page_header,
    render_line_chart,
)


def render_sensor_analytics() -> None:
    """Render sensor data analytics page."""

    render_page_header(
        title="Sensor Analytics",
        description=(
            "Explore industrial sensor readings "
            "and analyze machine operating conditions."
        ),
    )

    st.divider()

    # Select dataset
    selected_dataset = st.selectbox(
        "Select sensor dataset",
        options=[
            "Centrifugal Pump",
            "Machine Sensors",
        ],
    )

    # Retrieve selected dataset
    try:
        if selected_dataset == "Centrifugal Pump":
            dataframe = get_pump_sensor_data()
            timestamp_column = "Timestamp"

        else:
            dataframe = get_machine_sensor_data()
            timestamp_column = "timestamp"

    except Exception as exc:
        st.error(
            f"Unable to retrieve sensor data: {exc}"
        )
        return

    if dataframe.empty:
        st.info("No sensor records available.")
        return

    # Convert timestamp
    dataframe[timestamp_column] = pd.to_datetime(
        dataframe[timestamp_column],
        errors="coerce",
    )

    dataframe = dataframe.dropna(
        subset=[timestamp_column]
    )

    if dataframe.empty:
        st.warning("No valid timestamp records available.")
        return

    # Identify numeric sensor columns
    numeric_columns = dataframe.select_dtypes(
        include="number"
    ).columns.tolist()

    if not numeric_columns:
        st.warning("No numeric sensor columns available.")
        return

    st.subheader("Dataset Overview")

    # Dataset metrics
    metrics = [
        {
            "label": "Total Records",
            "value": f"{len(dataframe):,}",
        },
        {
            "label": "Total Columns",
            "value": f"{len(dataframe.columns):,}",
        },
        {
            "label": "Numeric Variables",
            "value": f"{len(numeric_columns):,}",
        },
    ]

    render_metric_cards(metrics)

    st.divider()

    # Sensor selection
    st.subheader("Sensor Trend Analysis")

    selected_sensor = st.selectbox(
        "Select sensor variable",
        options=numeric_columns,
    )

    # Render sensor trend
    render_line_chart(
        dataframe=dataframe,
        x_column=timestamp_column,
        y_column=selected_sensor,
        title=f"{selected_sensor} Over Time",
    )

    st.divider()

    # Statistical summary
    st.subheader("Sensor Statistical Summary")

    statistics = (
        dataframe[numeric_columns]
        .describe()
        .T
        .reset_index()
        .rename(
            columns={
                "index": "Sensor",
            }
        )
    )

    render_dataframe(
        dataframe=statistics,
    )

    st.divider()

    # Missing value analysis
    st.subheader("Missing Value Analysis")

    missing_data = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Missing Values": [
                dataframe[column].isna().sum()
                for column in dataframe.columns
            ],
        }
    )

    missing_data["Missing Percentage"] = (
        missing_data["Missing Values"]
        / len(dataframe)
        * 100
    )

    render_dataframe(
        dataframe=missing_data,
    )

    st.divider()

    # Raw sensor records
    st.subheader("Sensor Records")

    render_dataframe(
        dataframe=dataframe.head(100),
    )

    st.caption(
        "Displaying the first 100 records from the selected dataset."
    )