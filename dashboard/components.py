import plotly.express as px
import streamlit as st


# ============================================================
# PAGE COMPONENTS
# ============================================================

def render_page_header(
    title: str,
    description: str,
) -> None:
    """Render a consistent page header."""

    st.title(title)
    st.caption(description)


def render_metric_cards(metrics: list[dict]) -> None:
    """Render reusable metric cards."""

    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics):
        with column:
            st.metric(
                label=metric["label"],
                value=metric["value"],
                delta=metric.get("delta"),
            )


def render_pipeline_status(status: str) -> None:
    """Render pipeline execution status."""

    status = str(status).upper()

    if status == "SUCCESS":
        st.success("Pipeline completed successfully.")

    elif status == "FAILED":
        st.error("Pipeline execution failed.")

    elif status == "RUNNING":
        st.info("Pipeline is currently running.")

    else:
        st.warning(f"Unknown pipeline status: {status}")


def render_empty_state(message: str) -> None:
    """Render an empty state message."""

    st.info(message)


# ============================================================
# CHART COMPONENTS
# ============================================================

def apply_chart_style(figure) -> None:
    """Apply consistent styling to Plotly charts."""

    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#334155",
        ),
        title=dict(
            font=dict(
                size=17,
                color="#172B4D",
            ),
            x=0,
            xanchor="left",
        ),
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=30,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hoverlabel=dict(
            bgcolor="#142235",
            font_color="#FFFFFF",
        ),
    )

    figure.update_xaxes(
        showgrid=False,
        linecolor="#DCE4EE",
        zeroline=False,
    )

    figure.update_yaxes(
        showgrid=True,
        gridcolor="#EDF1F5",
        linecolor="#DCE4EE",
        zeroline=False,
    )


def render_line_chart(
    dataframe,
    x_column: str,
    y_column: str,
    title: str,
    color_column: str | None = None,
) -> None:
    """Render a reusable interactive line chart."""

    if dataframe.empty:
        render_empty_state(
            "No data available for visualization."
        )
        return

    figure = px.line(
        dataframe,
        x=x_column,
        y=y_column,
        color=color_column,
        title=title,
        markers=True,
    )

    figure.update_traces(
        line=dict(width=2),
        marker=dict(size=5),
    )

    apply_chart_style(figure)

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
        },
    )


def render_bar_chart(
    dataframe,
    x_column: str,
    y_column: str,
    title: str,
) -> None:
    """Render a reusable interactive bar chart."""

    if dataframe.empty:
        render_empty_state(
            "No data available for visualization."
        )
        return

    figure = px.bar(
        dataframe,
        x=x_column,
        y=y_column,
        title=title,
        text_auto=True,
    )

    figure.update_traces(
        marker_color="#2878B5",
        textposition="outside",
        cliponaxis=False,
    )

    apply_chart_style(figure)

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
        },
    )


# ============================================================
# DATA TABLE COMPONENTS
# ============================================================

def render_dataframe(
    dataframe,
    title: str | None = None,
) -> None:
    """Render a reusable styled dataframe table."""

    if title:
        st.subheader(title)

    if dataframe.empty:
        render_empty_state("No records available.")
        return

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
        height=min(
            400,
            40 + (len(dataframe) * 35),
        ),
    )