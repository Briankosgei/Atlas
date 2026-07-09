import pandas as pd
import yfinance as yf


class YahooFinanceFeed:

    SYMBOL_MAP = {
        "XAUUSD": "GC=F",
        "BTCUSD": "BTC-USD",
        "EURUSD": "EURUSD=X",
        "USDJPY": "JPY=X",
        "USDCAD": "CAD=X",
        "AUDUSD": "AUDUSD=X",
    }

    def get_candles(self, symbol, interval="1h", limit=500):

        ticker = self.SYMBOL_MAP[symbol]

        data = yf.download(
            ticker,
            interval=interval,
            period="60d",
            progress=False,
            auto_adjust=False,
        )

        # Fix for newer yfinance versions
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.tail(limit)

        candles = []

        for _, row in data.iterrows():
            candles.append({
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
            })

        return candles

    def get_price(self, symbol):
        candles = self.get_candles(symbol, limit=1)
        return candles[-1]["close"]