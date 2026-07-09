from datafeed.mock_feed import MockFeed

feed = MockFeed()

feed.get_candles("XAUUSD", "H1", 500)

feed.get_current_price("XAUUSD")