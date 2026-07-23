class MTFAlignment:
    """
    AtlasTrader Multi-Timeframe Alignment Engine

    Determines the dominant higher timeframe trend using weighted voting.

    Supported timeframes
    --------------------
    15m : 1
    1H  : 2
    4H  : 3
    1D  : 4
    1W  : 5

    Returns
    -------
    direction
        BUY / SELL / WAIT

    score
        Winning weighted score

    total
        Total weighted score

    confidence
        Percentage agreement

    agreement
        Percentage of higher timeframes agreeing

    majority
        BUY / SELL / NONE

    aligned
        True / False

    conflicts
        List of conflicting timeframes

    breakdown
        Trend per timeframe
    """

    WEIGHTS = {
        "15m": 1,
        "30m": 1,
        "1h": 2,
        "4h": 3,
        "1d": 4,
        "1wk": 5,
        "1w": 5,
    }

    def check(self, mtf):

        if not mtf:
            return {
                "direction": "WAIT",
                "majority": "NONE",
                "score": 0,
                "total": 0,
                "confidence": 0,
                "agreement": 0,
                "aligned": False,
                "conflicts": [],
                "breakdown": {},
            }

        buy_weight = 0
        sell_weight = 0
        total_weight = 0

        breakdown = {}

        for timeframe, analysis in mtf.items():

            weight = self.WEIGHTS.get(
                timeframe.lower(),
                1,
            )

            trend = (
                analysis
                .get("trend", {})
                .get("trend", "SIDEWAYS")
            )

            breakdown[timeframe] = trend

            if trend == "UPTREND":

                buy_weight += weight
                total_weight += weight

            elif trend == "DOWNTREND":

                sell_weight += weight
                total_weight += weight

        if total_weight == 0:

            return {
                "direction": "WAIT",
                "majority": "NONE",
                "score": 0,
                "total": 0,
                "confidence": 0,
                "agreement": 0,
                "aligned": False,
                "conflicts": [],
                "breakdown": breakdown,
            }

        #######################################################
        # Majority Direction
        #######################################################

        if buy_weight > sell_weight:

            direction = "BUY"
            majority = "BUY"
            score = buy_weight

        elif sell_weight > buy_weight:

            direction = "SELL"
            majority = "SELL"
            score = sell_weight

        else:

            direction = "WAIT"
            majority = "NONE"
            score = max(buy_weight, sell_weight)

        #######################################################
        # Agreement %
        #######################################################

        confidence = round(
            (score / total_weight) * 100
        )

        agreement = confidence

        #######################################################
        # Conflicting Timeframes
        #######################################################

        conflicts = []

        if majority != "NONE":

            expected = (
                "UPTREND"
                if majority == "BUY"
                else "DOWNTREND"
            )

            for tf, trend in breakdown.items():

                if trend != expected:

                    conflicts.append({
                        "timeframe": tf,
                        "trend": trend,
                    })

        #######################################################
        # Alignment Quality
        #######################################################

        aligned = confidence >= 70

        #######################################################

        return {

            "direction": direction,

            "majority": majority,

            "score": score,

            "total": total_weight,

            "confidence": confidence,

            "agreement": agreement,

            "aligned": aligned,

            "conflicts": conflicts,

            "breakdown": breakdown,
        }