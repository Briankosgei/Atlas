from risk.position_size import PositionSizer


class RiskManager:
    """
    AtlasTrader Risk Manager

    Responsibilities
    ----------------
    • Validate trade
    • Validate account
    • Validate risk settings
    • Validate stop-loss
    • Calculate position size
    • Enforce maximum limits
    • Return standardized output
    """

    def __init__(
        self,
        max_risk_percent=2.0,
        max_position_size=100.0,
    ):

        self.sizer = PositionSizer()

        self.max_risk_percent = float(max_risk_percent)
        self.max_position_size = float(max_position_size)

    ##########################################################

    def _reject(
        self,
        reason,
        trade=None,
        position=None,
    ):

        return {
            "approved": False,
            "reason": reason,
            "trade": trade,
            "position": position,
        }

    ##########################################################

    def evaluate(
        self,
        symbol,
        trade,
        balance=100.0,
        risk_percent=1.0,
    ):

        ######################################################
        # Validate Trade Object
        ######################################################

        if trade is None:
            return self._reject("Trade object is None.")

        if not isinstance(trade, dict):
            return self._reject("Trade must be a dictionary.")

        if not trade.get("valid", False):
            return self._reject(
                trade.get("reason", "Trade rejected."),
                trade=trade,
            )

        ######################################################
        # Validate Account
        ######################################################

        try:
            balance = float(balance)
            risk_percent = float(risk_percent)
        except Exception:
            return self._reject(
                "Invalid account parameters.",
                trade=trade,
            )

        if balance <= 0:
            return self._reject(
                "Account balance must be greater than zero.",
                trade=trade,
            )

        ######################################################
        # Validate Risk %
        ######################################################

        if risk_percent <= 0:
            return self._reject(
                "Risk percent must be greater than zero.",
                trade=trade,
            )

        if risk_percent > self.max_risk_percent:
            return self._reject(
                f"Risk exceeds maximum ({self.max_risk_percent}%).",
                trade=trade,
            )

        ######################################################
        # Validate Prices
        ######################################################

        try:

            entry = float(trade["entry"])
            stop = float(trade["stop_loss"])

        except Exception:

            return self._reject(
                "Trade prices are invalid.",
                trade=trade,
            )

        stop_distance = abs(entry - stop)

        if stop_distance <= 0:
            return self._reject(
                "Invalid stop-loss distance.",
                trade=trade,
            )

        ######################################################
        # Position Size
        ######################################################

        try:

            position = self.sizer.calculate(
                symbol=symbol,
                balance=balance,
                risk_percent=risk_percent,
                stop_distance=stop_distance,
            )

        except Exception as exc:

            return self._reject(
                f"Position sizing failed: {exc}",
                trade=trade,
            )

        ######################################################
        # Validate Position Result
        ######################################################

        if position is None:
            return self._reject(
                "PositionSizer returned None.",
                trade=trade,
            )

        if not isinstance(position, dict):
            return self._reject(
                "Invalid PositionSizer response.",
                trade=trade,
            )

        lot_size = float(position.get("lot_size", 0))

        if lot_size <= 0:
            return self._reject(
                "Calculated lot size is zero.",
                trade=trade,
                position=position,
            )

        if lot_size > self.max_position_size:
            return self._reject(
                f"Lot size exceeds maximum ({self.max_position_size}).",
                trade=trade,
                position=position,
            )

        ######################################################
        # Normalize Position Object
        ######################################################

        position.update({
            "balance": balance,
            "risk_percent": risk_percent,
            "risk_amount": round(
                balance * risk_percent / 100,
                2,
            ),
            "stop_distance": round(stop_distance, 5),
        })

        ######################################################
        # Approved
        ######################################################

        return {
            "approved": True,
            "reason": "Trade approved.",
            "trade": trade,
            "position": position,
        }