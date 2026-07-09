from datafeed.yfinance_feed import YahooFinanceFeed

feed = YahooFinanceFeed()

price = feed.get_price("XAUUSD")

print("\nCurrent Gold Price")
print(price)

candles = feed.get_candles("XAUUSD")

print("\nDownloaded candles:", len(candles))