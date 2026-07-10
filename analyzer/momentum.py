class MomentumDetector:
    """
    Measures the strength of the latest candle.
    """

    def detect(self, candles):

        if len(candles) < 2:
            return {
                "strength": "UNKNOWN",
                "score": 0
            }

        last = candles[-1]

        body = abs(last["close"] - last["open"])
        range_size = last["high"] - last["low"]

        if range_size == 0:
            return {
                "strength": "WEAK",
                "score": 0
            }

        ratio = body / range_size

        if ratio > 0.70:
            strength = "STRONG"
            score = 100

        elif ratio > 0.50:
            strength = "MODERATE"
            score = 70

        else:
            strength = "WEAK"
            score = 30

        return {
            "strength": strength,
            "score": score
        }