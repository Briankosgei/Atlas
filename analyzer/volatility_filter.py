from analyzer.atr import ATRCalculator


class VolatilityFilter:
    """
    Filters trades based on ATR volatility.

    Each instrument has its own acceptable ATR range.
    """

    LIMITS = {

        # Gold
        "XAUUSD": (5.0, 80.0),

        # Bitcoin
        "BTCUSD": (100.0, 2000.0),

        # Major Forex
        "EURUSD": (0.00030, 0.01000),
        "AUDUSD": (0.00030, 0.01000),
        "USDCAD": (0.00030, 0.01000),

        # JPY Pair
        "USDJPY": (0.030, 0.800),
    }

    def check(self, candles, symbol):
        """
        Returns whether current ATR is suitable for trading.
        """

        atr = ATRCalculator().calculate(candles)["atr"]

        # Default limits if symbol isn't configured
        minimum, maximum = self.LIMITS.get(symbol, (1.0, 100.0))

        if atr < minimum:

            return {
                "tradable": False,
                "atr": atr,
                "minimum": minimum,
                "maximum": maximum,
                "reason": "Low volatility",
            }

        if atr > maximum:

            return {
                "tradable": False,
                "atr": atr,
                "minimum": minimum,
                "maximum": maximum,
                "reason": "Extreme volatility",
            }

        return {
            "tradable": True,
            "atr": atr,
            "minimum": minimum,
            "maximum": maximum,
            "reason": "Normal volatility",
        }