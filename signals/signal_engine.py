class SignalEngine:
    """
    AtlasTrader Institutional Signal Engine

    Produces BUY, SELL or WAIT using weighted scoring.

    BUY and SELL are scored independently, then compared.
    """

    BUY_THRESHOLD = 60
    SELL_THRESHOLD = 60

    def generate(
        self,
        trend,
        bos,
        choch,
        liquidity,
        momentum,
        alignment,
        volatility,
    ):

        buy_score = 0
        sell_score = 0

        reasons = []
        conflicts = []

        ###########################################################
        # Volatility Filter
        ###########################################################

        if not volatility.get("tradable", True):

            return {
                "signal": "WAIT",
                "score": 0,
                "confidence": 0,
                "risk": "HIGH",
                "reasons": [
                    volatility.get(
                        "reason",
                        "Volatility filter rejected trade."
                    )
                ],
                "conflicts": [],
            }

        ###########################################################
        # Trend
        ###########################################################

        trend_direction = trend.get("trend", "SIDEWAYS")

        if trend_direction == "UPTREND":
            buy_score += 30
            reasons.append("Uptrend")

        elif trend_direction == "DOWNTREND":
            sell_score += 30
            reasons.append("Downtrend")

        else:
            reasons.append("Sideways market")

        ###########################################################
        # BOS
        ###########################################################

        if bos.get("bos"):

            if bos.get("direction") == "BUY":
                buy_score += 20
                reasons.append("Bullish BOS")

            elif bos.get("direction") == "SELL":
                sell_score += 20
                reasons.append("Bearish BOS")

        ###########################################################
        # CHoCH
        ###########################################################

        if choch.get("choch"):

            if choch.get("direction") == "BUY":
                buy_score += 15
                reasons.append("Bullish CHoCH")

            elif choch.get("direction") == "SELL":
                sell_score += 15
                reasons.append("Bearish CHoCH")

        ###########################################################
        # Liquidity
        ###########################################################

        if liquidity.get("sweep"):

            if liquidity.get("direction") == "BUY":
                buy_score += 10
                reasons.append("Bullish liquidity sweep")

            elif liquidity.get("direction") == "SELL":
                sell_score += 10
                reasons.append("Bearish liquidity sweep")

        ###########################################################
        # Momentum
        ###########################################################

        strength = momentum.get("strength", "WEAK").upper()

        if strength == "STRONG":
            buy_score += 20
            sell_score += 20
            reasons.append("Strong momentum")

        elif strength == "MODERATE":
            buy_score += 10
            sell_score += 10
            reasons.append("Moderate momentum")

        else:
            conflicts.append("Weak momentum")

        ###########################################################
        # Higher Timeframe Alignment
        ###########################################################

        htf = alignment.get("direction", "WAIT")

        if htf == "BUY":
            buy_score += 15
            reasons.append("HTF BUY alignment")

        elif htf == "SELL":
            sell_score += 15
            reasons.append("HTF SELL alignment")

        else:
            conflicts.append("No HTF alignment")

        ###########################################################
        # Clamp
        ###########################################################

        buy_score = max(0, min(100, buy_score))
        sell_score = max(0, min(100, sell_score))

        ###########################################################
        # Final Decision
        ###########################################################

        signal = "WAIT"
        confidence = max(buy_score, sell_score)
        score = confidence

        if buy_score >= self.BUY_THRESHOLD and buy_score > sell_score:
            signal = "BUY"

        elif sell_score >= self.SELL_THRESHOLD and sell_score > buy_score:
            signal = "SELL"

        ###########################################################
        # Risk
        ###########################################################

        if confidence >= 85:
            risk = "LOW"

        elif confidence >= 70:
            risk = "MEDIUM"

        else:
            risk = "HIGH"

        ###########################################################
        # Return
        ###########################################################

        return {
            "signal": signal,
            "score": score,
            "confidence": confidence,
            "risk": risk,
            "buy_score": buy_score,
            "sell_score": sell_score,
            "reasons": reasons,
            "conflicts": conflicts,
        }