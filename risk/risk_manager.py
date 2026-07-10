from risk.position_size import PositionSizer


class RiskManager:

    def __init__(self):
        self.sizer = PositionSizer()

    def evaluate(
        self,
        symbol,
        trade,
        balance=100,
        risk_percent=1,
    ):

        if not trade["valid"]:
            return {
                "approved": False,
                "reason": trade["reason"],
            }

        stop_distance = abs(
            trade["entry"] - trade["stop_loss"]
        )

        position = self.sizer.calculate(
            symbol=symbol,
            balance=balance,
            risk_percent=risk_percent,
            stop_distance=stop_distance,
        )

        return {
            "approved": True,
            "trade": trade,
            "position": position,
        }