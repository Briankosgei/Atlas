class TrendEngine:
    """
    AtlasTrader Trend Engine

    Determines market trend using market structure.

    Detects:
        • Uptrend
        • Downtrend
        • Sideways

    Also returns:
        • Trend confidence
        • Trend strength
        • Consecutive HH/HL
        • Consecutive LH/LL
    """

    def __init__(self, lookback=6):
        self.lookback = lookback

    def detect_trend(self, structure):

        if not structure or len(structure) < 4:

            return {
                "trend": "SIDEWAYS",
                "confidence": 0,
                "strength": 0,
                "bullish_points": 0,
                "bearish_points": 0,
                "bullish_sequence": 0,
                "bearish_sequence": 0,
                "reason": "Insufficient market structure",
            }

        recent = structure[-self.lookback:]

        bullish = 0
        bearish = 0

        bullish_sequence = 0
        bearish_sequence = 0

        max_bull_sequence = 0
        max_bear_sequence = 0

        for swing in recent:

            label = swing.get("label", "")

            ###############################################
            # Bullish Structure
            ###############################################

            if label in ("HH", "HL"):

                bullish += 1

                bullish_sequence += 1
                bearish_sequence = 0

                max_bull_sequence = max(
                    max_bull_sequence,
                    bullish_sequence,
                )

            ###############################################
            # Bearish Structure
            ###############################################

            elif label in ("LH", "LL"):

                bearish += 1

                bearish_sequence += 1
                bullish_sequence = 0

                max_bear_sequence = max(
                    max_bear_sequence,
                    bearish_sequence,
                )

        total = bullish + bearish

        if total == 0:

            return {
                "trend": "SIDEWAYS",
                "confidence": 0,
                "strength": 0,
                "bullish_points": 0,
                "bearish_points": 0,
                "bullish_sequence": 0,
                "bearish_sequence": 0,
                "reason": "No valid swing labels",
            }

        ###############################################
        # Trend Decision
        ###############################################

        if bullish > bearish:

            trend = "UPTREND"

            confidence = round((bullish / total) * 100)

            strength = min(
                100,
                confidence + (max_bull_sequence * 5),
            )

            reason = (
                f"{bullish} bullish vs "
                f"{bearish} bearish swings"
            )

        elif bearish > bullish:

            trend = "DOWNTREND"

            confidence = round((bearish / total) * 100)

            strength = min(
                100,
                confidence + (max_bear_sequence * 5),
            )

            reason = (
                f"{bearish} bearish vs "
                f"{bullish} bullish swings"
            )

        else:

            trend = "SIDEWAYS"

            confidence = 50

            strength = 20

            reason = "Balanced bullish and bearish structure"

        ###############################################
        # Return
        ###############################################

        return {

            "trend": trend,

            "confidence": confidence,

            "strength": strength,

            "bullish_points": bullish,

            "bearish_points": bearish,

            "bullish_sequence": max_bull_sequence,

            "bearish_sequence": max_bear_sequence,

            "reason": reason,
        }