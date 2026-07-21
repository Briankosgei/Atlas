class TrendStrength:

    def calculate(
        self,
        trend,
        bos,
        choch,
        momentum,
        alignment,
        liquidity,
    ):
        score = 0

        # Trend
        if trend["trend"] != "SIDEWAYS":
            score += 30

        # BOS
        if bos["bos"]:
            score += 20

        # CHoCH
        if choch["choch"]:
            score += 10

        # Momentum
        strength = momentum.get("strength", "").upper()

        if strength == "STRONG":
            score += 20

        elif strength == "MODERATE":
            score += 10

        # HTF Alignment
        direction = alignment.get("direction", "WAIT")

        if direction != "WAIT":
            score += 15

        # Liquidity
        if liquidity.get("sweep"):
            score += 5

        return {
            "score": min(score, 100)
        }