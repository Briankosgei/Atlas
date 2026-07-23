class CHOCHDetector:
    """
    AtlasTrader Change of Character (CHoCH)

    Detects:

        • Bullish CHoCH
        • Bearish CHoCH
        • Trend Reversal
        • Internal / External CHoCH
        • Confidence

    Expected Input:
        Classified market structure.

    Returns:

        choch
        direction
        confidence
        structure
        previous_trend
        current_trend
        reason
    """

    def __init__(self, lookback=6):

        self.lookback = lookback

    ###############################################################

    def detect(self, structure):

        if not structure or len(structure) < 5:

            return {
                "choch": False,
                "direction": None,
                "confidence": 0,
                "structure": None,
                "previous_trend": None,
                "current_trend": None,
                "reason": "Insufficient structure",
            }

        recent = structure[-self.lookback:]

        labels = [s.get("label") for s in recent]

        ###########################################################
        # Previous Trend
        ###########################################################

        bullish = labels.count("HH") + labels.count("HL")
        bearish = labels.count("LH") + labels.count("LL")

        if bullish > bearish:
            previous_trend = "UPTREND"
        elif bearish > bullish:
            previous_trend = "DOWNTREND"
        else:
            previous_trend = "SIDEWAYS"

        ###########################################################
        # Latest Swing
        ###########################################################

        latest = recent[-1]

        label = latest.get("label")
        structure_type = latest.get("structure", "UNKNOWN")

        ###########################################################
        # Bullish CHoCH
        ###########################################################

        if previous_trend == "DOWNTREND" and label in ("HH", "HL"):

            confidence = 70

            if structure_type == "EXTERNAL":
                confidence += 20

            return {

                "choch": True,

                "direction": "BUY",

                "confidence": min(confidence, 100),

                "structure": structure_type,

                "previous_trend": previous_trend,

                "current_trend": "UPTREND",

                "reason": "Bullish Change of Character",
            }

        ###########################################################
        # Bearish CHoCH
        ###########################################################

        if previous_trend == "UPTREND" and label in ("LL", "LH"):

            confidence = 70

            if structure_type == "EXTERNAL":
                confidence += 20

            return {

                "choch": True,

                "direction": "SELL",

                "confidence": min(confidence, 100),

                "structure": structure_type,

                "previous_trend": previous_trend,

                "current_trend": "DOWNTREND",

                "reason": "Bearish Change of Character",
            }

        ###########################################################
        # No CHoCH
        ###########################################################

        return {

            "choch": False,

            "direction": None,

            "confidence": 0,

            "structure": None,

            "previous_trend": previous_trend,

            "current_trend": previous_trend,

            "reason": "No Change of Character",
        }