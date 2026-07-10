class TradePlanner:

    def __init__(self):
        self.rr = 3.0

    def plan(self, symbol, price, signal):

        if signal["signal"] == "WAIT":
            return {
                "valid": False,
                "reason": "No trading signal"
            }

        direction = signal["signal"]

        # Default stop distances
        stop_distances = {
            "XAUUSD": 10.0,
            "BTCUSD": 500.0,
            "EURUSD": 0.0050,
            "USDJPY": 0.50,
            "USDCAD": 0.0050,
            "AUDUSD": 0.0050,
        }

        sl_distance = stop_distances.get(symbol, 0.0050)

        if direction == "BUY":
            entry = price
            stop = price - sl_distance
            take = price + (sl_distance * self.rr)

        else:
            entry = price
            stop = price + sl_distance
            take = price - (sl_distance * self.rr)

        return {
            "valid": True,
            "symbol": symbol,
            "direction": direction,
            "entry": round(entry, 5),
            "stop_loss": round(stop, 5),
            "take_profit": round(take, 5),
            "rr": f"1:{int(self.rr)}",
        }