class MTFAlignment:
    """
    Determines higher-timeframe alignment.
    Works with any number of timeframes.
    """

    def check(self, mtf):

        if not mtf:
            return {
                "direction": "WAIT",
                "score": 0,
            }

        buy = 0
        sell = 0

        for tf, analysis in mtf.items():

            trend = analysis["trend"]["trend"]

            if trend == "UPTREND":
                buy += 1

            elif trend == "DOWNTREND":
                sell += 1

        if buy > sell:

            direction = "BUY"

            score = buy

        elif sell > buy:

            direction = "SELL"

            score = sell

        else:

            direction = "WAIT"

            score = 0

        return {
            "direction": direction,
            "score": score,
        }