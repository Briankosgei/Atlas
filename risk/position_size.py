class PositionSizer:
    """
    Calculates position size based on account balance,
    risk percentage and stop loss distance.
    """

    def __init__(self):

        self.pip_values = {
            "EURUSD": 10,
            "AUDUSD": 10,
            "USDCAD": 10,
            "USDJPY": 9,
            "XAUUSD": 1,
            "BTCUSD": 1,
        }

    def calculate(
        self,
        symbol,
        balance,
        risk_percent,
        stop_distance,
    ):

        risk_amount = balance * (risk_percent / 100)

        pip_value = self.pip_values.get(symbol, 10)

        lot_size = risk_amount / (stop_distance * pip_value)

        lot_size = max(0.01, round(lot_size, 2))

        return {
            "balance": balance,
            "risk_percent": risk_percent,
            "risk_amount": round(risk_amount, 2),
            "lot_size": lot_size,
        }