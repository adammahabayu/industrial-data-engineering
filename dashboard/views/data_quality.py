import pandas as pd
import streamlit as st

from dashboard.database import get_pump_sensor_data
from dashboard.components import (
    render_dataframe,
    render_metric_cards,
    render_page_header,
    render_bar_chart,
)


def render_data_quality() -> None:
    """Render data quality monitoring page."""

    render_page_header(
        title="Data Quality",
        description=(
            "Monitor data completeness, missing values, "
            "duplicate records, and dataset consistency."
        ),
    )

    st.divider()

    # Retrieve processed pump data
    try:
        dataframe = get_pump_sensor_data()

    except Exception as exc:
        st.error(
            f"Unable to retrieve data quality information: {exc}"
        )
        return

    if dataframe.empty:
        st.info("No processed data available for analysis.")
        return

    # Calculate data quality metrics
    total_rows = len(dataframe)
    total_columns = len(dataframe.columns)
    total_cells = total_rows * total_columns

    missing_cells = int(dataframe.isna().sum().sum())

    missing_percentage = (
        missing_cells / total_cells * 100
        if total_cells > 0
        else 0
    )

    duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    complete_rows = int(
        dataframe.notna().all(axis=1).sum()
    )

    completeness_percentage = (
        complete_rows / total_rows * 100
        if total_rows > 0
        else 0
    )

    # Display quality metrics
    metrics = [
        {
            "label": "Total Records",
            "value": f"{total_rows:,}",
        },
        {
            "label": "Missing Cells",
            "value": f"{missing_cells:,}",
        },
        {
            "label": "Duplicate Rows",
            "value": f"{duplicate_rows:,}",
        },
        {
            "label": "Data Completeness",
            "value": f"{completeness_percentage:.2f}%",
        },
    ]

    render_metric_cards(metrics)

    st.divider()

    # Missing value analysis
    st.subheader("Missing Values by Column")

    missing_data = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Missing Values": [
                int(dataframe[column].isna().sum())
                for column in dataframe.columns
            ],
        }
    )

    missing_data["Missing Percentage"] = (
        missing_data["Missing Values"]
        / total_rows
        * 100
    )

    missing_data = missing_data.sort_values(
        by="Missing Values",
        ascending=False,
    )

    render_dataframe(
        dataframe=missing_data,
    )

    # Missing value visualization
    columns_with_missing = missing_data[
        missing_data["Missing Values"] > 0
    ]

    if not columns_with_missing.empty:
        render_bar_chart(
            dataframe=columns_with_missing,
            x_column="Column",
            y_column="Missing Values",
            title="Missing Values Distribution",
        )
    else:
        st.success("No missing values detected.")

    st.divider()

    # Dataset completeness
    st.subheader("Dataset Completeness")

    completeness_data = pd.DataFrame(
        {
            "Metric": [
                "Complete Rows",
                "Incomplete Rows",
            ],
            "Records": [
                complete_rows,
                total_rows - complete_rows,
            ],
        }
    )

    render_bar_chart(
        dataframe=completeness_data,
        x_column="Metric",
        y_column="Records",
        title="Complete vs Incomplete Records",
    )

    st.metric(
        label="Overall Missing Cell Percentage",
        value=f"{missing_percentage:.2f}%",
    )

    st.divider()

    # Duplicate analysis
    st.subheader("Duplicate Record Analysis")

    if duplicate_rows > 0:
        st.warning(
            f"Detected {duplicate_rows:,} duplicate records."
        )

        duplicate_data = dataframe[
            dataframe.duplicated(keep=False)
        ]

        render_dataframe(
            dataframe=duplicate_data.head(100),
            title="Duplicate Record Samples",
        )

    else:
        st.success("No duplicate records detected.")

    st.divider()

    # Dataset preview
    st.subheader("Processed Dataset Preview")

    render_dataframe(
        dataframe=dataframe.head(100),
    )

    st.caption(
        "Data quality metrics are calculated from the "
        "processed centrifugal pump dataset."
    )