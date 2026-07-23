class TrendStrength:
    """
    AtlasTrader Trend Strength Engine

    Calculates an overall trend quality score.

    Components
    ----------
    Trend            : 30
    BOS              : 20
    CHoCH            : 10
    Momentum         : 15
    HTF Alignment    : 15
    Liquidity Sweep  : 5
    Volatility       : 5

    Maximum = 100
    """

    def calculate(
        self,
        trend,
        bos,
        choch,
        momentum,
        alignment,
        liquidity,
        volatility,
    ):

        score = 0
        reasons = []

        ####################################################
        # Trend (30)
        ####################################################

        trend_name = trend.get("trend", "SIDEWAYS")

        if trend_name == "UPTREND":
            score += 30
            reasons.append("Uptrend")

        elif trend_name == "DOWNTREND":
            score += 30
            reasons.append("Downtrend")

        ####################################################
        # BOS (20)
        ####################################################

        if bos.get("bos", False):
            score += 20
            reasons.append("Break of Structure")

        ####################################################
        # CHoCH (10)
        ####################################################

        if choch.get("choch", False):
            score += 10
            reasons.append("Change of Character")

        ####################################################
        # Momentum (15)
        ####################################################

        momentum_score = momentum.get("score", 0)

        score += round((momentum_score / 100) * 15)

        if momentum_score >= 70:
            reasons.append("Strong Momentum")
        elif momentum_score >= 40:
            reasons.append("Moderate Momentum")

        ####################################################
        # Higher Timeframe Alignment (15)
        ####################################################

        alignment_confidence = alignment.get("confidence", 0)

        score += round((alignment_confidence / 100) * 15)

        if alignment_confidence >= 60:
            reasons.append("HTF Alignment")

        ####################################################
        # Liquidity Sweep (5)
        ####################################################

        if liquidity.get("sweep", False):
            score += 5
            reasons.append("Liquidity Sweep")

        ####################################################
        # Volatility (5)
        ####################################################

        if volatility.get("tradable", True):
            score += 5
            reasons.append("Healthy Volatility")

        ####################################################
        # Final Score
        ####################################################

        score = max(0, min(score, 100))

        ####################################################
        # Strength Rating
        ####################################################

        if score >= 85:
            rating = "VERY STRONG"

        elif score >= 70:
            rating = "STRONG"

        elif score >= 50:
            rating = "MODERATE"

        elif score >= 30:
            rating = "WEAK"

        else:
            rating = "VERY WEAK"

        ####################################################
        # Return
        ####################################################

        return {
            "score": score,
            "rating": rating,
            "reasons": reasons,
        }