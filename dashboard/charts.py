import plotly.express as px
import pandas as pd
import streamlit as st


def render_confidence_breakdown(report):

    confidence = report.get("confidence", {})

    breakdown = confidence.get("breakdown", {})

    if not breakdown:
        st.info("No confidence breakdown available.")
        return

    df = pd.DataFrame({
        "Factor": list(breakdown.keys()),
        "Score": list(breakdown.values()),
    })

    fig = px.bar(
        df,
        x="Factor",
        y="Score",
        text="Score",
    )

    fig.update_layout(
        template="plotly_dark",
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="",
        yaxis_title="",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )