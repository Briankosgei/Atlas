import pandas as pd
import streamlit as st


def render_scanner_table(reports):

    rows = []

    for r in reports:

        rows.append({
            "Symbol": r["symbol"],
            "Price": round(r["price"], 5),
            "Trend": r["trend"]["trend"],
            "HTF": r["alignment"]["direction"],
            "Confidence": f"{r['confidence_score']}%",
            "Signal": r["signal"]["signal"],
            "Grade": r["grade"]["grade"],
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )