from analyzer.market_analyzer import MarketAnalyzer

symbols = [
    "XAUUSD",
    "BTCUSD",
    "EURUSD",
    "USDJPY",
    "USDCAD",
    "AUDUSD",
]

analyzer = MarketAnalyzer()

print("\n" + "=" * 60)
print("              ATLASTRADER MARKET SCAN")
print("=" * 60)

for symbol in symbols:

    report = analyzer.analyze(symbol)

    print(f"\n{symbol}")
    print("-" * 60)

    # Current Price
    print(f"Current Price : {report['price']:.5f}")

    # Trend
    trend = report["trend"]
    print(f"Trend         : {trend['trend']} ({trend['confidence']}%)")

    # BOS
    bos = report["bos"]
    if bos["bos"]:
        print(f"BOS           : YES ({bos['direction']})")
    else:
        print("BOS           : NO")

    # CHoCH
    choch = report["choch"]
    if choch["choch"]:
        print(f"CHoCH         : YES ({choch['direction']})")
    else:
        print("CHoCH         : NO")

    # Liquidity
    liquidity = report["liquidity"]
    if liquidity["liquidity"]:
        print(f"Liquidity     : YES ({liquidity['direction']})")
    else:
        print("Liquidity     : NO")

    # Momentum
    momentum = report["momentum"]
    print(f"Momentum      : {momentum['strength']} ({momentum['score']}%)")

    # Confidence
    print(f"Confidence    : {report['confidence']}%")

    # Signal
    signal = report["signal"]
    print(f"Signal        : {signal['signal']}")
    print(f"Signal Score  : {signal['score']}")

    # Reasons
    print("Reasons:")
    for reason in signal["reasons"]:
        print(f"  ✓ {reason}")

    print("-" * 60)