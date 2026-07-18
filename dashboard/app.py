import sys
import os
import time
from datetime import datetime

import streamlit as st

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, PROJECT_ROOT)

from dashboard.styles import load_css
from dashboard.components import (
    signal_badge,
    show_metrics,
    show_best_trade,
)
from dashboard.tables import (
    show_signal_summary,
    show_trade_journal,
)
from dashboard.charts import show_performance_charts

from stats.performance import PerformanceAnalyzer
from analyzer.market_analyzer import MarketAnalyzer

# PAGE CONFIG
st.set_page_config(
    page_title="AtlasTrader v1.0",
    page_icon="📈",
    layout="wide",
)

load_css()

# SIDEBAR

st.sidebar.title("⚙ AtlasTrader Control Panel")

selected_symbol = st.sidebar.selectbox(
    "Market",
    [
        "ALL",
        "XAUUSD",
        "BTCUSD",
        "EURUSD",
        "USDJPY",
        "USDCAD",
        "AUDUSD",
    ],
)

st.sidebar.divider()

refresh = st.sidebar.checkbox(
    "Auto Refresh",
    value=False,
)

refresh_time = st.sidebar.slider(
    "Refresh every (seconds)",
    5,
    120,
    30,
)

st.sidebar.divider()

highlight_best_trade = st.sidebar.checkbox(
    "Highlight Best Signal",
    value=True,
)

show_journal = st.sidebar.checkbox(
    "Show Trade Journal",
    value=True,
)

show_charts = st.sidebar.checkbox(
    "Show Analytics",
    value=True,
)

st.sidebar.divider()

st.sidebar.subheader("AtlasTrader")

st.sidebar.success("Version 1.0 RC")

st.sidebar.caption("Data Feed")
st.sidebar.write("Yahoo Finance")

st.sidebar.caption("Execution")
st.sidebar.write("Manual Trading")

st.sidebar.caption("Developer")
st.sidebar.write("Brian Kiplagat")

# TITLE
st.markdown("""
# 📈 AtlasTrader v1.0

### Professional Forex Market Scanner

---
""")

st.caption(
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

# LOAD DATA
performance = PerformanceAnalyzer()
stats = performance.summary()

show_metrics(stats)

st.markdown("---")

analyzer = MarketAnalyzer()

ALL_SYMBOLS = [
    "XAUUSD",
    "BTCUSD",
    "EURUSD",
    "USDJPY",
    "USDCAD",
    "AUDUSD",
]

symbols = (
    ALL_SYMBOLS
    if selected_symbol == "ALL"
    else [selected_symbol]
)

# LIVE MARKET
st.markdown("""
# 📊 Live Market Scanner

Live multi-timeframe market analysis

---
""")

scan_results = []

cols = st.columns(3)

for i, symbol in enumerate(symbols):

    report = analyzer.analyze(symbol)

    if "error" in report:
        st.error(f"{symbol}: {report['error']}")
        continue

    scan_results.append(report)

    trend = report["trend"]["trend"]
    confidence = report["confidence"]
    alignment = report["alignment"]["direction"]
    signal = report["signal"]["signal"]

    with cols[i % 3]:

        st.markdown(f"""
### {symbol}

## {signal_badge(signal)}
""")

        st.progress(confidence / 100)

        c1, c2 = st.columns(2)

        c1.metric(
            "Trend",
            trend,
        )

        c2.metric(
            "Confidence",
            f"{confidence}%",
        )

        if alignment == "BUY":
            st.success("Higher TF : BUY")
        elif alignment == "SELL":
            st.error("Higher TF : SELL")
        else:
            st.warning("Higher TF : WAIT")

        if report["trade"]["valid"]:

            trade = report["trade"]

            st.caption(
                f"""
            ATR: {trade['atr']}
            Entry: {trade['entry']}
            Risk Distance: {trade['risk_distance']}
            SL: {trade['stop_loss']}
            TP: {trade['take_profit']}
            RR: 1:{trade['rr']}
            """
            )

# BEST TRADE
if highlight_best_trade and scan_results:

    st.markdown("---")

    show_best_trade(scan_results)

# SIGNAL SUMMARY
show_signal_summary(scan_results)

# JOURNAL

journal_file = os.path.join(
    PROJECT_ROOT,
    "journal",
    "trades.csv",
)

df = None

if show_journal:

    df = show_trade_journal(
        journal_file
    )

# ANALYTICS
if (
    show_charts
    and df is not None
    and not df.empty
):

    show_performance_charts(df)

# AUTO REFRESH

if refresh:

    time.sleep(refresh_time)

    st.rerun()

    