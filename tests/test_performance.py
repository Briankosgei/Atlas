from stats.performance import PerformanceAnalyzer

performance = PerformanceAnalyzer()

stats = performance.summary()

if stats is None:

    print("No journal data found.")

else:

    print("\n========== PERFORMANCE ==========\n")

    print(f"Total Trades      : {stats['total_trades']}")
    print(f"BUY Trades        : {stats['buy_trades']}")
    print(f"SELL Trades       : {stats['sell_trades']}")

    print()

    print(f"BUY Alignment     : {stats['aligned_buy']}")
    print(f"SELL Alignment    : {stats['aligned_sell']}")

    print()

    print(f"Average Confidence: {stats['average_confidence']}%")