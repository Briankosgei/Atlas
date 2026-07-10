import sys
from pathlib import Path

#add project root to python path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from analyzer.market_analyzer import MarketAnalyzer

st.set_page_config(
    page_title="AtlasTrader",
    page_icon="📈",
    layout="wide",
)

st.title("📈 AtlasTrader Dashboard")

symbols = [
    "XAUUSD",
    "BTCUSD",
    "EURUSD",
    "USDJPY",
    "USDCAD",
    "AUDUSD",
]

analyzer = MarketAnalyzer()

rows = []

for symbol in symbols:

    report = analyzer.analyze(symbol)

    rows.append({
        "Symbol": symbol,
        "Session": "OPEN" if report["session"]["allowed"] else "CLOSED",
        "Price": round(report["price"], 5),
        "Trend": report["trend"]["trend"],
        "Confidence": report["confidence"],
        "Signal": report["signal"]["signal"],
    })

df = pd.DataFrame(rows)

st.dataframe(df, use_container_width=True)