import os
import sys

import streamlit as st

# Add project root to Python path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from analyzer.market_analyzer import MarketAnalyzer

from dashboard.styles import apply_styles
from dashboard.components import metric_card, section_header
from dashboard.tables import render_scanner_table
from dashboard.charts import render_confidence_breakdown


SYMBOLS = [
    "XAUUSD",
    "BTCUSD",
    "EURUSD",
    "USDJPY",
    "USDCAD",
    "AUDUSD",
]


st.set_page_config(
    page_title="AtlasTrader",
    page_icon="📈",
    layout="wide",
)

apply_styles()


@st.cache_resource
def get_analyzer():
    return MarketAnalyzer()


analyzer = get_analyzer()


st.title("📈 AtlasTrader")
st.caption("Institutional-style multi-timeframe market scanner")


with st.spinner("Scanning markets..."):

    reports = [
        analyzer.analyze(symbol)
        for symbol in SYMBOLS
    ]


valid_reports = [
    r for r in reports
    if isinstance(r, dict) and "error" not in r
]


buy_count = sum(
    1 for r in valid_reports
    if r["signal"]["signal"] == "BUY"
)

sell_count = sum(
    1 for r in valid_reports
    if r["signal"]["signal"] == "SELL"
)

avg_conf = round(
    sum(r.get("confidence_score", 0) for r in valid_reports)
    / max(len(valid_reports), 1),
    1,
)


c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Symbols", len(valid_reports))

with c2:
    metric_card("BUY Signals", buy_count, color="green")

with c3:
    metric_card("SELL Signals", sell_count, color="red")

with c4:
    metric_card("Avg Confidence", f"{avg_conf}%")


section_header("Scanner Overview")

render_scanner_table(valid_reports)


section_header("Detailed Analysis")

selected = st.selectbox(
    "Select symbol",
    [r["symbol"] for r in valid_reports],
)

report = next(
    r for r in valid_reports
    if r["symbol"] == selected
)


left, right = st.columns([2, 1])


with left:

    st.subheader(f"{selected} Analysis")

    a, b, c = st.columns(3)

    a.metric("Trend", report["trend"]["trend"])
    b.metric("Confidence", f"{report['confidence_score']}%")
    c.metric("Signal", report["signal"]["signal"])


    st.markdown("### Structure")

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "BOS",
        report["bos"]["direction"]
        if report["bos"]["bos"]
        else "None",
    )

    s2.metric(
        "CHoCH",
        report["choch"]["direction"]
        if report["choch"]["choch"]
        else "None",
    )

    s3.metric(
        "Liquidity",
        report["liquidity"]["direction"]
        if report["liquidity"]["sweep"]
        else "No Sweep",
    )


    st.markdown("### Higher Timeframe Alignment")

    st.write(
        f"**Direction:** {report['alignment']['direction']}"
    )

    st.progress(
        report["alignment"]["confidence"] / 100
    )


    st.markdown("### Confidence Breakdown")

    render_confidence_breakdown(report)


with right:

    st.subheader("Trade Plan")

    trade = report["trade"]

    if trade["valid"]:

        st.success(f"{trade['direction']} setup")

        st.metric("Entry", trade["entry"])
        st.metric("Stop Loss", trade["stop_loss"])
        st.metric("Take Profit", trade["take_profit"])
        st.metric("Risk:Reward", f"1:{trade['rr']}")
        st.metric("ATR", trade["atr"])


        st.markdown("---")

        st.subheader("Risk")

        risk = report["risk"]

        if risk["approved"]:

            pos = risk["position"]

            st.metric("Lot Size", pos["lot_size"])
            st.metric("Risk Amount", f"${pos['risk_amount']}")
            st.metric("Risk %", f"{pos['risk_percent']}%")

        else:

            st.error(risk["reason"])

    else:

        st.warning(trade["reason"])


section_header("Raw Report")

st.json(report)