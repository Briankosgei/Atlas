from datafeed.yfinance_feed import YahooFinanceFeed
from timeframe.multi_timeframe import MultiTimeframeAnalyzer

feed = YahooFinanceFeed()

mtf = MultiTimeframeAnalyzer(feed)

report = mtf.analyze("XAUUSD")

for tf, result in report.items():

    print("\n", tf)

    print(result["trend"])

    print(result["bos"])

    print(result["choch"])