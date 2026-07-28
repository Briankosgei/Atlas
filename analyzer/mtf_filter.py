class MTFAlignment:
    """
    AtlasTrader Multi-Timeframe Alignment

    Combines trends from multiple timeframes using weighted voting.

    Supports multiple analyzer formats.

    Accepted values:

        trend -> UPTREND / DOWNTREND / SIDEWAYS

        direction -> BUY / SELL / WAIT

    Returns a standardized alignment report.
    """

    WEIGHTS = {
        "15m": 1,
        "30m": 1,
        "1h": 2,
        "4h": 3,
        "1d": 4,
        "1w": 5,
        "1wk": 5,
    }

    ############################################################

    def _extract_trend(self, analysis):
        """
        Supports multiple analyzer outputs.
        """

        if not isinstance(analysis, dict):
            return "SIDEWAYS"

        # format:
        # {"trend":{"trend":"UPTREND"}}

        if isinstance(analysis.get("trend"), dict):

            t = analysis["trend"].get("trend")

            if t:
                return t.upper()

            d = analysis["trend"].get("direction")

            if d == "BUY":
                return "UPTREND"

            if d == "SELL":
                return "DOWNTREND"

        # format:
        # {"trend":"UPTREND"}

        t = analysis.get("trend")

        if isinstance(t, str):

            t = t.upper()

            if t in (
                "UPTREND",
                "DOWNTREND",
                "SIDEWAYS",
            ):
                return t

        # format:
        # {"direction":"BUY"}

        d = analysis.get("direction")

        if d == "BUY":
            return "UPTREND"

        if d == "SELL":
            return "DOWNTREND"

        return "SIDEWAYS"

    ############################################################

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

        buy = 0
        sell = 0
        total = 0

        breakdown = {}

        for tf, analysis in mtf.items():

            trend = self._extract_trend(analysis)

            breakdown[tf] = trend

            weight = self.WEIGHTS.get(tf.lower(), 1)

            if trend == "UPTREND":

                buy += weight
                total += weight

            elif trend == "DOWNTREND":

                sell += weight
                total += weight

        if total == 0:

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

        if buy > sell:

            direction = "BUY"
            score = buy

        elif sell > buy:

            direction = "SELL"
            score = sell

        else:

            direction = "WAIT"
            score = max(buy, sell)

        confidence = round((score / total) * 100)

        aligned = confidence >= 60

        conflicts = []

        expected = (
            "UPTREND"
            if direction == "BUY"
            else "DOWNTREND"
        )

        if direction != "WAIT":

            for tf, trend in breakdown.items():

                if trend not in (
                    expected,
                    "SIDEWAYS",
                ):
                    conflicts.append({
                        "timeframe": tf,
                        "trend": trend,
                    })

        return {

            "direction": direction,

            "majority": direction if direction != "WAIT" else "NONE",

            "score": score,

            "total": total,

            "confidence": confidence,

            "agreement": confidence,

            "aligned": aligned,

            "conflicts": conflicts,

            "breakdown": breakdown,
        }