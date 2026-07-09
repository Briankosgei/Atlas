class SwingDetector:
    """
    Detect swing highs and swing lows from OHLC candles.
    """

    def find_swings(self, candles):
        swings = []

        # Start at index 2 and stop 2 candles before the end
        for i in range(2, len(candles) - 2):

            current = candles[i]

            # ---- Swing High ----
            if (
                current["high"] > candles[i - 1]["high"]
                and current["high"] > candles[i - 2]["high"]
                and current["high"] > candles[i + 1]["high"]
                and current["high"] > candles[i + 2]["high"]
            ):

                swings.append({
                    "type": "HIGH",
                    "index": i,
                    "price": current["high"]
                })

            # ---- Swing Low ----
            elif (
                current["low"] < candles[i - 1]["low"]
                and current["low"] < candles[i - 2]["low"]
                and current["low"] < candles[i + 1]["low"]
                and current["low"] < candles[i + 2]["low"]
            ):

                swings.append({
                    "type": "LOW",
                    "index": i,
                    "price": current["low"]
                })

        return swings