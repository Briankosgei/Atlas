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
        """
        Evaluate a trade and calculate the appropriate position size.

        Returns:
            {
                approved: bool,
                reason: str,
                trade: dict,
                position: float
            }
        """

        # Trade rejected by planner
        if not trade.get("valid", False):
            return {
                "approved": False,
                "reason": trade.get(
                    "reason",
                    "Trade rejected by planner."
                ),
                "trade": trade,
                "position": 0.0,
            }

        # Calculate stop distance
        stop_distance = abs(
            trade["entry"] - trade["stop_loss"]
        )

        # Prevent division by zero
        if stop_distance <= 0:
            return {
                "approved": False,
                "reason": "Invalid stop-loss distance.",
                "trade": trade,
                "position": 0.0,
            }

        try:
            position = self.sizer.calculate(
                symbol=symbol,
                balance=balance,
                risk_percent=risk_percent,
                stop_distance=stop_distance,
            )

        except ZeroDivisionError:
            return {
                "approved": False,
                "reason": "Position sizing failed (division by zero).",
                "trade": trade,
                "position": 0.0,
            }

        except Exception as e:
            return {
                "approved": False,
                "reason": str(e),
                "trade": trade,
                "position": 0.0,
            }

        return {
            "approved": True,
            "reason": "Trade approved.",
            "trade": trade,
            "position": position,
        }