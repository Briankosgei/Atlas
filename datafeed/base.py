from abc import ABC, abstractmethod


class DataFeed(ABC):
    """
    Base class for every market data provider.
    """

    @abstractmethod
    def get_candles(self, symbol, timeframe, bars):
        """
        Return OHLC candle data.

        Example:
            symbol = "XAUUSD"
            timeframe = "H1"
            bars = 500
        """
        pass

    @abstractmethod
    def get_current_price(self, symbol):
        """
        Return current bid/ask price.
        """
        pass