from datafeed.base import DataFeed


class MockFeed(DataFeed):

    def get_candles(self, symbol, timeframe, bars):

        print(f"Fetching {bars} candles for {symbol} on {timeframe}")

        return []

    def get_current_price(self, symbol):

        print(f"Fetching current price for {symbol}")

        return 0.0