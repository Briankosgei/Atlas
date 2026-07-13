class MTFAlignment:

    def check(self, mtf):

        trends = {
            "1d": mtf["1d"]["trend"]["trend"],
            "4h": mtf["4h"]["trend"]["trend"],
            "1h": mtf["1h"]["trend"]["trend"],
            "15m": mtf["15m"]["trend"]["trend"],
        }

        bullish = sum(t == "BULLISH" for t in trends.values())
        bearish = sum(t == "BEARISH" for t in trends.values())

        if bullish >= 3:
            return {
                "direction": "BUY",
                "aligned": True,
                "score": bullish,
            }

        if bearish >= 3:
            return {
                "direction": "SELL",
                "aligned": True,
                "score": bearish,
            }

        return {
            "direction": "WAIT",
            "aligned": False,
            "score": max(bullish, bearish),
        }