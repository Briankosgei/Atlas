import streamlit as st


def signal_badge(signal):
    if signal == "BUY":
        return "🟢 BUY"
    elif signal == "SELL":
        return "🔴 SELL"
    return "🟡 WAIT"


def show_metrics(stats):
    """Top dashboard performance metrics."""

    if not stats:
        return

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📒 Trades",
        stats["total_trades"],
    )

    c2.metric(
        "🟢 BUY",
        stats["buy_trades"],
    )

    c3.metric(
        "🔴 SELL",
        stats["sell_trades"],
    )

    c4.metric(
        "🎯 Avg Confidence",
        f"{stats['average_confidence']}%",
    )


def show_best_trade(scan_results):

    valid = [
        r for r in scan_results
        if r["trade"]["valid"]
    ]

    if not valid:
        return

    best = max(
        valid,
        key=lambda x: x["confidence"]
    )

    trade = best["trade"]

    st.markdown("---")
    st.markdown("## 🏆 Best Opportunity")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Market",
        best["symbol"]
    )

    c2.metric(
        "Signal",
        trade["direction"]
    )

    c3.metric(
        "Confidence",
        f"{best['confidence']}%"
    )

    st.progress(best["confidence"] / 100)

    if best["confidence"] >= 80:
        st.success("High Confidence Trade")
    elif best["confidence"] >= 60:
        st.info("Good Confidence Trade")
    else:
        st.warning("Low Confidence Trade")

    left, right = st.columns(2)

    left.markdown("### Entry Plan")
    left.write(f"Entry : **{trade['entry']}**")
    left.write(f"Stop : **{trade['stop_loss']}**")
    left.write(f"Target : **{trade['take_profit']}**")

    right.markdown("### Market")
    right.write(f"Trend : **{best['trend']['trend']}**")
    right.write(f"Alignment : **{best['alignment']['direction']}**")
    right.write(f"Momentum : **{best['momentum']['strength']}**")