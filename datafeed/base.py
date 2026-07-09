from abc import ABC, abstractmethod


class DataFeed(ABC):

    @abstractmethod
    def get_candles(self, symbol, interval="1h", limit=500):
        pass

    @abstractmethod
    def get_price(self, symbol):
        pass