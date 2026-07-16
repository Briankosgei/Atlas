import streamlit as st
import plotly.express as px


def show_performance_charts(df):

    st.markdown("---")

    st.markdown("""
# 📈 Performance Analytics

Trade distribution and confidence analysis.

---
""")

    left, right = st.columns(2)

    fig1 = px.pie(
        df,
        names="signal",
        title="BUY vs SELL Distribution",
    )

    left.plotly_chart(
        fig1,
        use_container_width=True,
    )

    fig2 = px.histogram(
        df,
        x="confidence",
        nbins=10,
        title="Confidence Distribution",
    )

    right.plotly_chart(
        fig2,
        use_container_width=True,
    )

    st.markdown("---")

    alignment_counts = (
        df["alignment"]
        .value_counts()
        .reset_index()
    )

    alignment_counts.columns = [
        "alignment",
        "count",
    ]

    fig3 = px.bar(
        alignment_counts,
        x="alignment",
        y="count",
        color="alignment",
        title="Higher Timeframe Alignment Distribution",
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
    )