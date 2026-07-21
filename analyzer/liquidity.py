class LiquidityDetector:

    def detect(self, candles, structure):

        if len(candles) < 3:

            return {
                "sweep": False,
                "direction": None,
            }

        last = candles[-1]
        previous = candles[-2]

        if last["high"] > previous["high"]:

            return {
                "sweep": True,
                "direction": "BUY",
            }

        if last["low"] < previous["low"]:

            return {
                "sweep": True,
                "direction": "SELL",
            }

        return {
            "sweep": False,
            "direction": None,
        }