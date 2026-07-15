import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px

from stats.performance import PerformanceAnalyzer

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AtlasTrader Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 AtlasTrader Dashboard")

# ==========================================================
# PERFORMANCE
# ==========================================================

performance = PerformanceAnalyzer()
stats = performance.summary()

# ==========================================================
# LOAD JOURNAL
# ==========================================================

journal_file = os.path.join(PROJECT_ROOT, "journal", "trades.csv")

if os.path.exists(journal_file):
    df = pd.read_csv(journal_file)
else:
    df = pd.DataFrame()

# ==========================================================
# METRICS
# ==========================================================

if stats:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Trades",
        stats["total_trades"],
    )

    col2.metric(
        "BUY Trades",
        stats["buy_trades"],
    )

    col3.metric(
        "SELL Trades",
        stats["sell_trades"],
    )

    col4.metric(
        "Avg Confidence",
        f"{stats['average_confidence']}%",
    )

# ==========================================================
# TRADE ANALYTICS
# ==========================================================

st.divider()

st.header("📊 Trade Analytics")

if not df.empty:

    # -------------------------
    # Pie + Histogram
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            df,
            names="signal",
            title="BUY vs SELL Distribution",
            hole=0.45,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:

        fig = px.histogram(
            df,
            x="confidence",
            nbins=10,
            title="Confidence Distribution",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # -------------------------
    # Trades Per Symbol
    # -------------------------

    st.subheader("Trades by Symbol")

    symbol_counts = (
        df.groupby("symbol")
        .size()
        .reset_index(name="Trades")
    )

    fig = px.bar(
        symbol_counts,
        x="symbol",
        y="Trades",
        title="Most Traded Symbols",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # -------------------------
    # Higher Timeframe Alignment
    # -------------------------

    st.subheader("Higher Timeframe Alignment")

    alignment_counts = (
        df.groupby("alignment")
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        alignment_counts,
        x="alignment",
        y="Count",
        title="Alignment Statistics",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

# ==========================================================
# TRADE JOURNAL
# ==========================================================

st.divider()

st.header("📋 Trade Journal")

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("No journal entries yet.")