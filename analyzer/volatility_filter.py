from analyzer.atr import ATRCalculator


class VolatilityFilter:

    def __init__(
        self,
        minimum_atr=3,
        maximum_atr=80,
    ):
        self.minimum = minimum_atr
        self.maximum = maximum_atr

    def check(self, candles):

        atr = ATRCalculator().calculate(candles)["atr"]

        if atr < self.minimum:

            return {

                "tradable": False,

                "atr": atr,

                "reason": "Low volatility"

            }

        if atr > self.maximum:

            return {

                "tradable": False,

                "atr": atr,

                "reason": "Extreme volatility"

            }

        return {

            "tradable": True,

            "atr": atr,

            "reason": "Normal volatility"

        }