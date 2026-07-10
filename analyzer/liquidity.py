class LiquidityDetector:
    """
    Detect bullish and bearish liquidity sweeps.

    Bullish sweep:
        Current low < Previous swing low
        AND closes above previous swing low

    Bearish sweep:
        Current high > Previous swing high
        AND closes below previous swing high
    """

    def detect(self, candles, swings):

        if len(candles) < 2:
            return {
                "liquidity": False,
                "direction": None
            }

        previous = candles[-2]
        current = candles[-1]

        # -------- Bullish Sweep --------

        if (
            current["low"] < previous["low"]
            and current["close"] > previous["low"]
        ):
            return {
                "liquidity": True,
                "direction": "BULLISH"
            }

        # -------- Bearish Sweep --------

        if (
            current["high"] > previous["high"]
            and current["close"] < previous["high"]
        ):
            return {
                "liquidity": True,
                "direction": "BEARISH"
            }

        return {
            "liquidity": False,
            "direction": None
        }