class TrendEngine:
    """
    Determines the market trend from classified market structure.
    """

    def detect_trend(self, classified_swings):

        hh = 0
        hl = 0
        lh = 0
        ll = 0

        for swing in classified_swings:

            label = swing["label"]

            if label == "HH":
                hh += 1

            elif label == "HL":
                hl += 1

            elif label == "LH":
                lh += 1

            elif label == "LL":
                ll += 1

        bullish_score = hh + hl
        bearish_score = lh + ll

        total = bullish_score + bearish_score

        if total == 0:
            return {
                "trend": "RANGE",
                "confidence": 0
            }

        confidence = round(max(bullish_score, bearish_score) / total * 100)

        if bullish_score > bearish_score:
            trend = "BULLISH"

        elif bearish_score > bullish_score:
            trend = "BEARISH"

        else:
            trend = "RANGE"

        return {
            "trend": trend,
            "confidence": confidence
        }