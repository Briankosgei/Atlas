class ConfidenceEngine:

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

        score = 0

        if trend["trend"] != "SIDEWAYS":
            score += 20

        if bos["bos"]:
            score += 20

        if choch["choch"]:
            score += 10

        if liquidity["sweep"]:
            score += 10

        score += momentum["score"] * 0.20

        score += alignment["score"] * 10

        if volatility.get("trade_allowed", True):
            score += 10

        return min(round(score), 100)