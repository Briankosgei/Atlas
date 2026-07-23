import pandas as pd


class ATRCalculator:
    """
    Average True Range (ATR)
    Works for Forex, Gold, Crypto and Indices.
    """

    @staticmethod
    def calculate(candles, period=14):

        if candles is None or len(candles) < period + 1:
            return {
                "atr": 0.0
            }

        df = pd.DataFrame(candles)

        # Normalize column names
        df = df.rename(columns={
            "high": "High",
            "low": "Low",
            "close": "Close",
        })

        required = {"High", "Low", "Close"}

        if not required.issubset(df.columns):
            raise ValueError(
                "Candles must contain high, low and close values."
            )

        high = df["High"].astype(float)
        low = df["Low"].astype(float)
        close = df["Close"].astype(float)

        previous_close = close.shift(1)

        tr = pd.concat(
            [
                high - low,
                (high - previous_close).abs(),
                (low - previous_close).abs(),
            ],
            axis=1,
        ).max(axis=1)

        atr = tr.rolling(window=period).mean().iloc[-1]

        if pd.isna(atr):
            atr = 0.0

        return {
            "atr": float(atr)
        }