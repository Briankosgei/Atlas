class CHOCHDetector:
    """
    Detects a Change of Character (CHoCH).
    """

    def detect(self, classified_swings):

        if len(classified_swings) < 2:
            return {
                "choch": False,
                "direction": None
            }

        previous = classified_swings[-2]["label"]
        current = classified_swings[-1]["label"]

        # Bullish → Bearish
        if previous in ("HH", "HL") and current == "LL":
            return {
                "choch": True,
                "direction": "BEARISH"
            }

        # Bearish → Bullish
        if previous in ("LL", "LH") and current == "HH":
            return {
                "choch": True,
                "direction": "BULLISH"
            }

        return {
            "choch": False,
            "direction": None
        }