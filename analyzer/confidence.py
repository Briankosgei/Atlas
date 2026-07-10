class ConfidenceEngine:

    def calculate(
        self,
        trend,
        bos,
        choch,
        liquidity,
        momentum
    ):
        score = 0

        # Trend
        if trend["trend"] != "RANGE":
            score += 20

        # BOS
        if bos["bos"]:
            score += 20

        # CHoCH
        if choch["choch"]:
            score += 15

        # Liquidity
        if liquidity["liquidity"]:
            score += 20

        # Momentum
        score += int(momentum["score"] * 0.25)

        return min(score, 100)