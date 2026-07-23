class ConfidenceEngine:
    """
    AtlasTrader Confidence Engine

    Calculates an overall confidence score from every
    major analysis module.

    Weight Distribution
    -------------------
    Trend           : 25
    BOS             : 20
    CHoCH           : 10
    Liquidity       : 10
    Momentum        : 10
    HTF Alignment   : 15
    Volatility      : 10

    TOTAL = 100
    """

    WEIGHTS = {
        "trend": 25,
        "bos": 20,
        "choch": 10,
        "liquidity": 10,
        "momentum": 10,
        "alignment": 15,
        "volatility": 10,
    }

    def _label(self, score):

        if score >= 90:
            return "Excellent"

        elif score >= 80:
            return "Very Strong"

        elif score >= 70:
            return "Strong"

        elif score >= 60:
            return "Good"

        elif score >= 50:
            return "Moderate"

        elif score >= 40:
            return "Weak"

        return "Poor"

    ###############################################################

    def calculate(
        self,
        trend,
        bos,
        choch,
        liquidity,
        momentum,
        alignment,
        volatility,
    ):

        breakdown = {}

        total = 0

        ###############################################################
        # Trend
        ###############################################################

        trend_score = 0

        if trend.get("trend") in ["UPTREND", "DOWNTREND"]:

            confidence = trend.get("confidence", 100)

            trend_score = (
                confidence / 100
            ) * self.WEIGHTS["trend"]

        breakdown["trend"] = round(trend_score, 2)

        total += trend_score

        ###############################################################
        # BOS
        ###############################################################

        bos_score = 0

        if bos.get("bos"):

            strength = bos.get("strength", 1)

            bos_score = min(
                self.WEIGHTS["bos"],
                self.WEIGHTS["bos"] * max(0.25, strength)
            )

        breakdown["bos"] = round(bos_score, 2)

        total += bos_score

        ###############################################################
        # CHOCH
        ###############################################################

        choch_score = 0

        if choch.get("choch"):

            choch_score = self.WEIGHTS["choch"]

        breakdown["choch"] = choch_score

        total += choch_score

        ###############################################################
        # Liquidity
        ###############################################################

        liquidity_score = 0

        if liquidity.get("sweep"):

            strength = liquidity.get("strength", 1)

            liquidity_score = min(
                self.WEIGHTS["liquidity"],
                self.WEIGHTS["liquidity"] * max(0.30, strength)
            )

        breakdown["liquidity"] = round(liquidity_score, 2)

        total += liquidity_score

        ###############################################################
        # Momentum
        ###############################################################

        momentum_strength = (
            momentum.get("strength", "WEAK")
            .upper()
        )

        if momentum_strength == "STRONG":

            momentum_score = self.WEIGHTS["momentum"]

        elif momentum_strength == "MODERATE":

            momentum_score = self.WEIGHTS["momentum"] * 0.7

        elif momentum_strength == "WEAK":

            momentum_score = self.WEIGHTS["momentum"] * 0.4

        else:

            momentum_score = 0

        breakdown["momentum"] = round(momentum_score, 2)

        total += momentum_score

        ###############################################################
        # Higher Timeframe Alignment
        ###############################################################

        alignment_confidence = alignment.get(
            "confidence",
            0,
        )

        alignment_score = (
            alignment_confidence / 100
        ) * self.WEIGHTS["alignment"]

        breakdown["alignment"] = round(
            alignment_score,
            2,
        )

        total += alignment_score

        ###############################################################
        # Volatility
        ###############################################################

        volatility_score = 0

        if volatility.get("tradable", False):

            volatility_score = self.WEIGHTS["volatility"]

        breakdown["volatility"] = volatility_score

        total += volatility_score

        ###############################################################
        # Final Score
        ###############################################################

        total = max(
            0,
            min(100, round(total))
        )

        return {

            "score": total,

            "label": self._label(total),

            "breakdown": breakdown,
        }