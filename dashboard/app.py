import streamlit as st

from dashboard.views.overview import render_overview
from dashboard.views.pipeline_monitoring import (
    render_pipeline_monitoring,
)
from dashboard.views.sensor_analytics import (
    render_sensor_analytics,
)
from dashboard.views.data_quality import (
    render_data_quality,
)

st.set_page_config(
    page_title="Industrial Data Engineering",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global dashboard styling
st.markdown(
    """
    <style>
        /* Main application */
        .stApp {
            background-color: #F4F7FB;
            color: #1E293B;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1600px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #142235;
        }

        [data-testid="stSidebar"] * {
            color: #E2E8F0;
        }

        [data-testid="stSidebar"] hr {
            border-color: #334155;
        }

        /* Headings */
        h1, h2, h3 {
            color: #172B4D;
            font-weight: 700;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }

        [data-testid="stMetricLabel"] {
            color: #64748B;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: #0F2942;
            font-weight: 700;
        }

        /* Select boxes */
        [data-testid="stSelectbox"] {
            background-color: #FFFFFF;
            border-radius: 8px;
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            overflow: hidden;
        }

        /* Dividers */
        hr {
            border-color: #DCE4EE;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def main() -> None:
    """Run the industrial data engineering dashboard."""

    st.sidebar.title("Industrial Data Platform")

    st.sidebar.caption(
        "ETL Pipeline Monitoring & Analytics"
    )

    st.sidebar.divider()

    selected_page = st.sidebar.radio(
        "Navigation",
        options=[
            "Overview",
            "Pipeline Monitoring",
            "Sensor Analytics",
            "Data Quality",
        ],
    )

    # Render selected page
    if selected_page == "Overview":
        render_overview()

    elif selected_page == "Pipeline Monitoring":
        render_pipeline_monitoring()

    elif selected_page == "Sensor Analytics":
        render_sensor_analytics()

    elif selected_page == "Data Quality":
        render_data_quality()


if __name__ == "__main__":
    main()