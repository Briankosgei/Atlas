from concurrent.futures import ThreadPoolExecutor, as_completed

from analyzer.market_analyzer import MarketAnalyzer
from journal.trade_journal import TradeJournal
from utils.logger import logger


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


def analyze_symbol(symbol):
    """
    Analyze a single symbol.
    This function runs inside a worker thread.
    """

    logger.info(f"Scanning {symbol}")

    try:
        report = analyzer.analyze(symbol)
        return symbol, report

    except Exception as e:

        logger.exception(f"{symbol} crashed")

        return symbol, {
            "symbol": symbol,
            "error": str(e),
        }


print("\n" + "=" * 60)
print("              ATLASTRADER MARKET SCAN")
print("=" * 60)

# --------------------------------------------------
# Analyze all symbols in parallel
# --------------------------------------------------

with ThreadPoolExecutor(max_workers=4) as executor:

    futures = [
        executor.submit(analyze_symbol, symbol)
        for symbol in symbols
    ]

    for future in as_completed(futures):

        symbol, report = future.result()

        # ---------------------------------
        # Handle Errors
        # ---------------------------------

        if "error" in report:

            logger.warning(f"{symbol} | {report['error']}")

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
        # Multi-Timeframe
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

        print(
            f"Momentum      : {momentum['strength']} ({momentum['score']}%)"
        )

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
        # Risk Management
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

            journal.save(report)

        else:

            print()
            print("Risk Management: Trade rejected")

        logger.info(
            f"{symbol} | "
            f"{signal['signal']} | "
            f"Confidence={report['confidence']}% | "
            f"Alignment={alignment['direction']}"
        )

        print("-" * 60)

print("\nScan Complete.\n")