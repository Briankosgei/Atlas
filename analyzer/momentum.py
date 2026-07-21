class MomentumDetector:

    def detect(self, candles):

        if len(candles) < 10:

            return {
                "strength": "WEAK",
                "score": 0,
            }

        close = candles[-1]["close"]
        old = candles[-10]["close"]

        change = abs(close - old)

        if change > close * 0.02:

            return {
                "strength": "STRONG",
                "score": 90,
            }

        if change > close * 0.01:

            return {
                "strength": "MODERATE",
                "score": 70,
            }

        return {
            "strength": "WEAK",
            "score": 40,
        }