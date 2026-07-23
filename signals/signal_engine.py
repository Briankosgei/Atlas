class SignalEngine:
    """
    AtlasTrader Institutional Signal Engine

    Decision hierarchy:

        1. Trend
        2. Higher Timeframe Alignment
        3. BOS
        4. CHoCH
        5. Liquidity
        6. Momentum
        7. Volatility

    Outputs:

        BUY
        SELL
        WAIT

    Along with:

        Score
        Reasons
        Conflicts
        Risk Level
        Confidence
    """

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

        reasons = []
        conflicts = []

        score = 0

        signal = "WAIT"

        ############################################################
        # Extract Values
        ############################################################

        trend_direction = trend.get("trend", "SIDEWAYS")

        htf_direction = alignment.get("direction", "WAIT")

        momentum_strength = momentum.get(
            "strength",
            "WEAK",
        ).upper()

        trade_allowed = volatility.get(
            "tradable",
            True,
        )

        ############################################################
        # 1. Volatility Filter
        ############################################################

        if not trade_allowed:

            return {

                "signal": "WAIT",

                "score": 0,

                "confidence": 0,

                "risk": "HIGH",

                "reasons": [
                    volatility.get(
                        "reason",
                        "Volatility filter rejected trade",
                    )
                ],

                "conflicts": [],
            }

        ############################################################
        # 2. Sideways Market
        ############################################################

        if trend_direction == "SIDEWAYS":

            return {

                "signal": "WAIT",

                "score": 5,

                "confidence": 5,

                "risk": "HIGH",

                "reasons": [
                    "Market is sideways"
                ],

                "conflicts": [],
            }

        ############################################################
        # 3. Trend
        ############################################################

        if trend_direction == "UPTREND":

            signal = "BUY"

            score += 30

            reasons.append("Uptrend")

        elif trend_direction == "DOWNTREND":

            signal = "SELL"

            score += 30

            reasons.append("Downtrend")

        ############################################################
        # 4. Higher Timeframe Alignment
        ############################################################

        if htf_direction == "WAIT":

            conflicts.append(
                "Higher timeframe not aligned"
            )

        elif htf_direction == signal:

            score += 20

            reasons.append(
                "Higher timeframe aligned"
            )

        else:

            conflicts.append(
                "Trend conflicts with Higher Timeframe"
            )

            score -= 25

        ############################################################
        # 5. BOS
        ############################################################

        if bos.get("bos"):

            if bos.get("direction") == signal:

                score += 20

                reasons.append(
                    "Break of Structure"
                )

            else:

                conflicts.append(
                    "BOS opposes trend"
                )

                score -= 15

        ############################################################
        # 6. CHoCH
        ############################################################

        if choch.get("choch"):

            if choch.get("direction") == signal:

                score += 10

                reasons.append(
                    "Change of Character"
                )

            else:

                conflicts.append(
                    "CHoCH opposes trend"
                )

                score -= 10

        ############################################################
        # 7. Liquidity
        ############################################################

        if liquidity.get("sweep"):

            if liquidity.get("direction") == signal:

                score += 10

                reasons.append(
                    "Liquidity Sweep"
                )

            else:

                conflicts.append(
                    "Liquidity against signal"
                )

                score -= 10

        ############################################################
        # 8. Momentum
        ############################################################

        if momentum_strength == "STRONG":

            score += 15

            reasons.append(
                "Strong Momentum"
            )

        elif momentum_strength == "MODERATE":

            score += 8

            reasons.append(
                "Moderate Momentum"
            )

        else:

            conflicts.append(
                "Weak Momentum"
            )

        ############################################################
        # Clamp Score
        ############################################################

        score = max(
            0,
            min(score, 100)
        )

        ############################################################
        # Confidence
        ############################################################

        confidence = score

        ############################################################
        # Risk Level
        ############################################################

        if confidence >= 85:

            risk = "LOW"

        elif confidence >= 70:

            risk = "MEDIUM"

        else:

            risk = "HIGH"

        ############################################################
        # Final Decision
        ############################################################

        if confidence < 70:

            signal = "WAIT"

        ############################################################
        # Return
        ############################################################

        return {

            "signal": signal,

            "score": score,

            "confidence": confidence,

            "risk": risk,

            "reasons": reasons,

            "conflicts": conflicts,
        }