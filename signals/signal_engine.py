class SignalEngine:

    def generate(
        self,
        trend,
        bos,
        choch,
        liquidity,
        momentum,
    ):

        reasons = []

        score = 0

        # Trend
        if trend["trend"] == "BULLISH":
            score += 1
            reasons.append("Bullish trend")

        elif trend["trend"] == "BEARISH":
            score -= 1
            reasons.append("Bearish trend")

        # BOS
        if bos["bos"]:

            if bos["direction"] == "BULLISH":
                score += 2
                reasons.append("Bullish BOS")

            else:
                score -= 2
                reasons.append("Bearish BOS")

        # CHoCH
        if choch["choch"]:

            if choch["direction"] == "BULLISH":
                score += 1
                reasons.append("Bullish CHoCH")

            else:
                score -= 1
                reasons.append("Bearish CHoCH")

        # Liquidity
        if liquidity["liquidity"]:

            if liquidity["direction"] == "BULLISH":
                score += 2
                reasons.append("Bullish liquidity sweep")

            else:
                score -= 2
                reasons.append("Bearish liquidity sweep")

        # Momentum
        if momentum["strength"] == "STRONG":
            score *= 1.5
            reasons.append("Strong momentum")

        elif momentum["strength"] == "MODERATE":
            score *= 1.2
            reasons.append("Moderate momentum")

        if score >= 3:
            signal = "BUY"

        elif score <= -3:
            signal = "SELL"

        else:
            signal = "WAIT"

        return {
            "signal": signal,
            "score": round(score, 2),
            "reasons": reasons,
        }