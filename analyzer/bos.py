class BOSDetector:
    """
    Detects a simple Break of Structure (BOS).
    """

    def detect(self, classified_swings):

        if len(classified_swings) < 2:
            return {
                "bos": False,
                "direction": None
            }

        last = classified_swings[-1]["label"]

        if last == "HH":
            return {
                "bos": True,
                "direction": "BULLISH"
            }

        if last == "LL":
            return {
                "bos": True,
                "direction": "BEARISH"
            }

        return {
            "bos": False,
            "direction": None
        }