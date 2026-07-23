class BOSDetector:
    """
    AtlasTrader Break of Structure (BOS)

    Detects:

        • Bullish BOS
        • Bearish BOS
        • Consecutive BOS
        • Break Strength
        • Fake Breaks
        • Confidence

    Expected Inputs

    structure:
        Classified market structure.

    candles:
        OHLC candles (optional).

    Returns:

        bos
        direction
        strength
        confidence
        broken_level
        consecutive
        fake_break
        reason
    """

    def __init__(self, lookback=6):

        self.lookback = lookback

    ###############################################################

    def _close_confirmation(
        self,
        candles,
        broken_level,
        direction,
    ):
        """
        Confirm BOS using candle close.
        """

        if not candles:
            return True

        close = candles[-1]["close"]

        if direction == "BUY":
            return close > broken_level

        return close < broken_level

    ###############################################################

    def detect(
        self,
        structure,
        candles=None,
    ):

        if not structure or len(structure) < 4:

            return {
                "bos": False,
                "direction": None,
                "strength": 0,
                "confidence": 0,
                "broken_level": None,
                "consecutive": 0,
                "fake_break": False,
                "reason": "Insufficient structure",
            }

        recent = structure[-self.lookback:]

        ###########################################################
        # Count BOS candidates
        ###########################################################

        bullish = 0
        bearish = 0

        last_direction = None

        broken_level = None

        strength = 0

        for swing in recent:

            label = swing.get("label")
            price = swing.get("price")

            if label == "HH":

                bullish += 1

                last_direction = "BUY"

                broken_level = price

                strength = swing.get("strength", "WEAK")

            elif label == "LL":

                bearish += 1

                last_direction = "SELL"

                broken_level = price

                strength = swing.get("strength", "WEAK")

        ###########################################################
        # Decide direction
        ###########################################################

        if bullish == 0 and bearish == 0:

            return {
                "bos": False,
                "direction": None,
                "strength": 0,
                "confidence": 0,
                "broken_level": None,
                "consecutive": 0,
                "fake_break": False,
                "reason": "No BOS detected",
            }

        if bullish >= bearish:

            direction = "BUY"

            consecutive = bullish

        else:

            direction = "SELL"

            consecutive = bearish

        ###########################################################
        # Close confirmation
        ###########################################################

        confirmed = self._close_confirmation(
            candles,
            broken_level,
            direction,
        )

        if not confirmed:

            return {
                "bos": False,
                "direction": direction,
                "strength": 0,
                "confidence": 20,
                "broken_level": broken_level,
                "consecutive": consecutive,
                "fake_break": True,
                "reason": "Break not confirmed by candle close",
            }

        ###########################################################
        # Confidence
        ###########################################################

        confidence = min(
            100,
            60 + (consecutive * 10),
        )

        ###########################################################
        # Strength Score
        ###########################################################

        if strength == "STRONG":

            strength_score = 100

        elif strength == "WEAK":

            strength_score = 60

        else:

            strength_score = 50

        ###########################################################
        # Return
        ###########################################################

        return {

            "bos": True,

            "direction": direction,

            "strength": strength_score,

            "confidence": confidence,

            "broken_level": broken_level,

            "consecutive": consecutive,

            "fake_break": False,

            "reason": f"{direction} BOS confirmed",
        }