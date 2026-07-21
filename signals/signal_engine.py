class SignalEngine:

    def generate(
        self,
        trend,
        bos,
        choch,
        liquidity,
        momentum,
        alignment,
    ):

        reasons = []

        score = 0

        signal = "WAIT"

        if trend["trend"] == "UPTREND":

            score += 25

            reasons.append("Uptrend")

        elif trend["trend"] == "DOWNTREND":

            score += 25

            reasons.append("Downtrend")

        if bos["bos"]:

            score += 20

            reasons.append("Break of Structure")

        if choch["choch"]:

            score += 15

            reasons.append("Change of Character")

        if liquidity["sweep"]:

            score += 10

            reasons.append("Liquidity Sweep")

        if momentum["strength"] == "STRONG":

            score += 20

            reasons.append("Strong Momentum")

        if alignment["direction"] != "WAIT":

            score += 10

            reasons.append("Higher Timeframe Alignment")

        if trend["trend"] == "UPTREND":

            signal = "BUY"

        elif trend["trend"] == "DOWNTREND":

            signal = "SELL"

        return {

            "signal": signal,

            "score": min(score, 100),

            "reasons": reasons,
        }