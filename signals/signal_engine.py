class SignalEngine:

    def generate(
        self,
        trend,
        bos,
        choch,
        liquidity,
        momentum,
        mtf_alignment,
    ):

        reasons = []
        score = 0

        # ---------------- Trend ----------------

        if trend["trend"] == "BULLISH":
            score += 1
            reasons.append("Bullish trend")

        elif trend["trend"] == "BEARISH":
            score -= 1
            reasons.append("Bearish trend")

        # ---------------- BOS ----------------

        if bos["bos"]:

            if bos["direction"] == "BULLISH":
                score += 2
                reasons.append("Bullish BOS")
            else:
                score -= 2
                reasons.append("Bearish BOS")

        # ---------------- CHoCH ----------------

        if choch["choch"]:

            if choch["direction"] == "BULLISH":
                score += 1
                reasons.append("Bullish CHoCH")
            else:
                score -= 1
                reasons.append("Bearish CHoCH")

        # ---------------- Liquidity ----------------

        if liquidity["liquidity"]:

            if liquidity["direction"] == "BULLISH":
                score += 2
                reasons.append("Bullish liquidity sweep")
            else:
                score -= 2
                reasons.append("Bearish liquidity sweep")

        # ---------------- Momentum ----------------

        if momentum["strength"] == "STRONG":
            score *= 1.5
            reasons.append("Strong momentum")

        elif momentum["strength"] == "MODERATE":
            score *= 1.2
            reasons.append("Moderate momentum")

        # ---------------- Raw Signal ----------------

        if score >= 3:
            signal = "BUY"

        elif score <= -3:
            signal = "SELL"

        else:
            signal = "WAIT"

        # ======================================================
        # Higher Timeframe Filter
        # ======================================================

        if mtf_alignment["aligned"]:

            if signal != "WAIT":

                if signal != mtf_alignment["direction"]:

                    signal = "WAIT"
                    score = 0

                    reasons.append(
                        "Rejected by Higher Timeframe Alignment"
                    )

        else:

            signal = "WAIT"
            score = 0

            reasons.append(
                "Higher Timeframes Not Aligned"
            )

        return {
            "signal": signal,
            "score": round(score, 2),
            "reasons": reasons,
        }