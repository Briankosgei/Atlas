from concurrent.futures import ThreadPoolExecutor, as_completed

from analyzer.market_analyzer import MarketAnalyzer
from journal.trade_journal import TradeJournal
from utils.logger import logger


SYMBOLS = [
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
    logger.info(f"Scanning {symbol}")

    try:
        return symbol, analyzer.analyze(symbol)

    except Exception as e:
        logger.exception(symbol)

        return symbol, {
            "symbol": symbol,
            "error": str(e),
        }


print("\n" + "=" * 70)
print("                ATLASTRADER MARKET SCANNER")
print("=" * 70)

with ThreadPoolExecutor(max_workers=4) as executor:

    futures = [
        executor.submit(analyze_symbol, symbol)
        for symbol in SYMBOLS
    ]

    for future in as_completed(futures):

        symbol, report = future.result()

        if "error" in report:

            print(f"\n{symbol}")
            print("-" * 70)
            print(report["error"])
            print("-" * 70)

            continue

        print(f"\n{symbol}")
        print("-" * 70)

        ###################################################
        # SESSION
        ###################################################

        session = report["session"]

        status = "OPEN" if session["allowed"] else "CLOSED"

        print(f"Session          : {status}")
        print(f"Reason           : {session['reason']}")

        ###################################################
        # PRICE
        ###################################################

        print(f"Current Price    : {report['price']}")

        ###################################################
        # TREND
        ###################################################

        trend = report["trend"]

        print(
            f"Trend            : "
            f"{trend['trend']} "
            f"({trend['confidence']}%)"
        )

        ###################################################
        # BOS / CHOCH
        ###################################################

        bos = report["bos"]

        if bos["bos"]:
            print(f"BOS              : {bos['direction']}")
        else:
            print("BOS              : None")

        choch = report["choch"]

        if choch["choch"]:
            print(f"CHoCH            : {choch['direction']}")
        else:
            print("CHoCH            : None")

        ###################################################
        # LIQUIDITY
        ###################################################

        liquidity = report["liquidity"]

        if liquidity["sweep"]:
            print(f"Liquidity Sweep  : YES {liquidity['direction']}")
        else:
            print("Liquidity Sweep  : NO")

        ###################################################
        # MOMENTUM
        ###################################################

        momentum = report["momentum"]

        print(
            f"Momentum         : "
            f"{momentum['strength']} "
            f"({momentum['score']}%)"
        )

        ###################################################
        # VOLATILITY
        ###################################################

        volatility = report["volatility"]

        print(f"ATR        : {volatility['atr']:.5f}")

        status = "PASS" if volatility["tradable"] else "BLOCKED"

        print(f"volatility  : {status}")
        print(f"Reason      : {volatility['reason']}")

        ###################################################
        # MTF
        ###################################################

        alignment = report["alignment"]

        print(
            f"HTF Alignment    : "
            f"{alignment['direction']} "
            f"({alignment['score']}/4)"
        )

        ###################################################
        # TREND STRENGTH
        ###################################################

        strength = report["trend_strength"]

        print(
            f"Trend Strength   : "
            f"{strength['score']}/100"
        )

        ###################################################
        # CONFIDENCE
        ###################################################

        print(
            f"Confidence       : "
            f"{report['confidence']}%"
        )

        ###################################################
        # GRADE
        ###################################################
        grade = report["grade"]

        print(
            f"Signal Grade    : "
            f"{grade['grade']} ({grade['quality']})"
        )

        ###################################################
        # SIGNAL
        ###################################################

        signal = report["signal"]

        print(
            f"Signal           : "
            f"{signal['signal']}"
        )

        print(
            f"Signal Score     : "
            f"{signal['score']}"
        )

        print("Reasons:")

        for reason in signal["reasons"]:
            print(f"   ✓ {reason}")

        ###################################################
        # TRADE PLAN
        ###################################################

        trade = report["trade"]

        if trade["valid"]:

            print("\nTrade Plan")

            print(f"Direction        : {trade['direction']}")
            print(f"Entry            : {trade['entry']}")
            print(f"ATR              : {trade['atr']}")
            print(f"Risk Distance    : {trade['risk_distance']}")
            print(f"Stop Loss        : {trade['stop_loss']}")
            print(f"Take Profit      : {trade['take_profit']}")
            print(f"Risk Reward      : 1:{trade['rr']}")

        else:

            print("\nTrade Plan")
            print("No valid setup.")

        ###################################################
        # RISK
        ###################################################

        risk = report["risk"]

        if risk["approved"]:

            position = risk["position"]

            print("\nRisk Management")

            print(f"Balance          : ${position['balance']}")
            print(f"Risk             : {position['risk_percent']}%")
            print(f"Risk Amount      : ${position['risk_amount']}")
            print(f"Lot Size         : {position['lot_size']}")

            journal.save(report)

        else:

            print("\nRisk Management")
            print("Trade Rejected")

        print("-" * 70)

        logger.info(
            f"{symbol} | "
            f"{signal['signal']} | "
            f"Confidence={report['confidence']} | "
            f"Grade={report['grade']}"
        )

print("\nScan Complete.\n")