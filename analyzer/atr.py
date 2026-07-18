import pandas as pd


class ATRCalculator:
    """
    Average True Range (ATR)
    """

    @staticmethod
    def calculate(candles, period=14):

        # Convert list of candles to DataFrame
        df = pd.DataFrame(candles)

        # Normalize column names
        df = df.rename(columns={
            "high": "High",
            "low": "Low",
            "close": "Close"
        })

        required = {"High", "Low", "Close"}

        if not required.issubset(df.columns):
            raise ValueError(
                "Candles must contain high, low and close values."
            )

        high = df["High"]
        low = df["Low"]
        close = df["Close"]

        previous_close = close.shift(1)

        tr = pd.concat(
            [
                high - low,
                (high - previous_close).abs(),
                (low - previous_close).abs(),
            ],
            axis=1,
        ).max(axis=1)

        atr = tr.rolling(period).mean().iloc[-1]

        return {
            "atr": round(float(atr), 2)
        }