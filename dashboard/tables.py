import os
import streamlit as st
import pandas as pd


def show_signal_summary(scan_results):

    if not scan_results:
        return

    st.markdown("---")
    st.header("📋 Live Signal Summary")

    table = []

    for report in scan_results:

        table.append({

            "Symbol": report["symbol"],
            "Signal": report["signal"]["signal"],
            "Trend": report["trend"]["trend"],
            "Confidence": report["confidence"],
            "Alignment": report["alignment"]["direction"],
            "Momentum": report["momentum"]["strength"]

        })

    df_signals = pd.DataFrame(table)

    df_signals = df_signals.sort_values(
        by="Confidence",
        ascending=False
    )

    st.dataframe(
        df_signals,
        use_container_width=True,
        hide_index=True,
    )


def show_trade_journal(journal_file):

    st.markdown("---")

    st.markdown("""
# 📒 Trade Journal

All executed trade plans are recorded here.

---
""")

    if not os.path.exists(journal_file):

        st.info("No journal entries found.")
        return

    df = pd.read_csv(journal_file)

    df = df.sort_values(
        "time",
        ascending=False
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇ Download Journal CSV",
        df.to_csv(index=False),
        file_name="AtlasTrader_Journal.csv",
        mime="text/csv",
    )

    return df