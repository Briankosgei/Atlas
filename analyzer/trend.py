class TrendEngine:
    """
    Detects market trend from classified swings.

    Expected input:
    [
        {"type":"HIGH","price":...,"label":"HH"},
        {"type":"LOW","price":...,"label":"HL"},
        ...
    ]
    """

    def detect_trend(self, structure):

        highs = [
            s for s in structure
            if s["type"] == "HIGH"
        ]

        lows = [
            s for s in structure
            if s["type"] == "LOW"
        ]

        if len(highs) < 2 or len(lows) < 2:
            return {
                "trend": "SIDEWAYS",
                "confidence": 0,
            }

        last_high = highs[-1]
        prev_high = highs[-2]

        last_low = lows[-1]
        prev_low = lows[-2]

        higher_high = (
            last_high["price"] > prev_high["price"]
            or last_high["label"] == "HH"
        )

        lower_high = (
            last_high["price"] < prev_high["price"]
            or last_high["label"] == "LH"
        )

        higher_low = (
            last_low["price"] > prev_low["price"]
            or last_low["label"] == "HL"
        )

        lower_low = (
            last_low["price"] < prev_low["price"]
            or last_low["label"] == "LL"
        )

        if higher_high and higher_low:
            return {
                "trend": "UPTREND",
                "confidence": 90,
            }

        if lower_high and lower_low:
            return {
                "trend": "DOWNTREND",
                "confidence": 90,
            }

        return {
            "trend": "SIDEWAYS",
            "confidence": 50,
        }