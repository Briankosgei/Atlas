from analyzer.market_analyzer import MarketAnalyzer
from journal.trade_journal import TradeJournal

symbols = [
    "XAUUSD",
    "BTCUSD",
    "EURUSD",
    "USDJPY",
    "USDCAD",
    "AUDUSD",
]

analyzer = MarketAnalyzer()
journal = TradeJournal()

print("\n" + "=" * 60)
print("              ATLASTRADER MARKET SCAN")
print("=" * 60)

for symbol in symbols:

    report = analyzer.analyze(symbol)

    # ---------------------------------
    # Skip symbols with missing data
    # ---------------------------------

    if "error" in report:
        print(f"\n{symbol}")
        print("-" * 60)
        print(report["error"])
        print("-" * 60)
        continue

    print(f"\n{symbol}")
    print("-" * 60)

    # ---------------------------------
    # Session
    # ---------------------------------

    session = report["session"]

    if session["allowed"]:
        print(f"Session       : OPEN ({session['reason']})")
    else:
        print(f"Session       : CLOSED ({session['reason']})")

    # ---------------------------------
    # Higher Timeframes
    # ---------------------------------

    print("Higher Timeframes")

    for tf, analysis in report["mtf"].items():

        print(
            f"{tf.upper():>4} | "
            f"{analysis['trend']['trend']:<8} | "
            f"BOS: {analysis['bos']['bos']} | "
            f"CHoCH: {analysis['choch']['choch']}"
        )

    print("-" * 60)

    alignment = report["alignment"]

    print()
    print(f"MTF Alignment : {alignment['direction']} {alignment['score']}/4")

    # ---------------------------------
    # Price
    # ---------------------------------

    print(f"Current Price : {report['price']:.5f}")

    # ---------------------------------
    # Trend
    # ---------------------------------

    trend = report["trend"]
    print(f"Trend         : {trend['trend']} ({trend['confidence']}%)")

    # ---------------------------------
    # BOS
    # ---------------------------------

    bos = report["bos"]

    if bos["bos"]:
        print(f"BOS           : YES ({bos['direction']})")
    else:
        print("BOS           : NO")

    # ---------------------------------
    # CHoCH
    # ---------------------------------

    choch = report["choch"]

    if choch["choch"]:
        print(f"CHoCH         : YES ({choch['direction']})")
    else:
        print("CHoCH         : NO")

    # ---------------------------------
    # Liquidity
    # ---------------------------------

    liquidity = report["liquidity"]

    if liquidity["liquidity"]:
        print(f"Liquidity     : YES ({liquidity['direction']})")
    else:
        print("Liquidity     : NO")

    # ---------------------------------
    # Momentum
    # ---------------------------------

    momentum = report["momentum"]
    print(f"Momentum      : {momentum['strength']} ({momentum['score']}%)")

    # ---------------------------------
    # Confidence
    # ---------------------------------

    print(f"Confidence    : {report['confidence']}%")

    # ---------------------------------
    # Signal
    # ---------------------------------

    signal = report["signal"]

    print(f"Signal        : {signal['signal']}")
    print(f"Signal Score  : {signal['score']}")

    print("Reasons:")

    for reason in signal["reasons"]:
        print(f"  ✓ {reason}")

    # ---------------------------------
    # Trade Plan
    # ---------------------------------

    trade = report["trade"]

    if trade["valid"]:

        print()
        print("Trade Plan")
        print(f"Direction     : {trade['direction']}")
        print(f"Entry         : {trade['entry']}")
        print(f"Stop Loss     : {trade['stop_loss']}")
        print(f"Take Profit   : {trade['take_profit']}")
        print(f"Risk Reward   : {trade['rr']}")

    else:

        print()
        print(f"Trade Plan    : {trade['reason']}")

    # ---------------------------------
    # Risk
    # ---------------------------------

    risk = report["risk"]

    if risk["approved"]:

        position = risk["position"]

        print()
        print("Risk Management")
        print(f"Balance       : ${position['balance']}")
        print(f"Risk          : {position['risk_percent']}%")
        print(f"Risk Amount   : ${position['risk_amount']}")
        print(f"Lot Size      : {position['lot_size']}")

        # ---------------------------------
        # Save trade to journal
        # ---------------------------------

        journal.save(report)

        print()
        print("Journal       : Trade saved")

    else:

        print()
        print("Risk Management: Trade rejected")

    print("-" * 60)