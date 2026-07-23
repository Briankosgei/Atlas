import math


class PositionSizer:
    """
    AtlasTrader Position Sizing Engine

    Calculates position size using:

        • Account Balance
        • Risk Percentage
        • Stop Loss Distance
        • Symbol Specifications

    Returns a consistent dictionary used by the Risk Manager.

    Easily extendable for MT5 symbol information later.
    """

    SYMBOLS = {

        "EURUSD": {
            "pip_size": 0.0001,
            "pip_value": 10.0,
            "min_lot": 0.01,
            "max_lot": 100.0,
            "lot_step": 0.01,
        },

        "AUDUSD": {
            "pip_size": 0.0001,
            "pip_value": 10.0,
            "min_lot": 0.01,
            "max_lot": 100.0,
            "lot_step": 0.01,
        },

        "USDCAD": {
            "pip_size": 0.0001,
            "pip_value": 10.0,
            "min_lot": 0.01,
            "max_lot": 100.0,
            "lot_step": 0.01,
        },

        "USDJPY": {
            "pip_size": 0.01,
            "pip_value": 9.0,
            "min_lot": 0.01,
            "max_lot": 100.0,
            "lot_step": 0.01,
        },

        "XAUUSD": {
            "pip_size": 0.10,
            "pip_value": 1.0,
            "min_lot": 0.01,
            "max_lot": 100.0,
            "lot_step": 0.01,
        },

        "BTCUSD": {
            "pip_size": 1.0,
            "pip_value": 1.0,
            "min_lot": 0.01,
            "max_lot": 100.0,
            "lot_step": 0.01,
        },
    }

    def calculate(
        self,
        symbol,
        balance,
        risk_percent,
        stop_distance,
    ):
        """
        Calculate lot size.

        Returns
        -------
        {
            balance,
            risk_percent,
            risk_amount,
            stop_distance,
            pip_distance,
            pip_value,
            lot_size
        }
        """

        ########################################################
        # Validate Symbol
        ########################################################

        if symbol not in self.SYMBOLS:
            raise ValueError(f"Unsupported symbol: {symbol}")

        ########################################################
        # Validate Inputs
        ########################################################

        if balance <= 0:
            raise ValueError("Balance must be greater than zero.")

        if risk_percent <= 0:
            raise ValueError("Risk percent must be greater than zero.")

        if stop_distance <= 0:
            raise ValueError("Stop distance must be greater than zero.")

        spec = self.SYMBOLS[symbol]

        ########################################################
        # Risk Amount
        ########################################################

        risk_amount = balance * (risk_percent / 100)

        ########################################################
        # Price Distance -> Pip Distance
        ########################################################

        pip_distance = stop_distance / spec["pip_size"]

        if pip_distance <= 0:
            raise ValueError("Invalid pip distance.")

        ########################################################
        # Raw Lot Size
        ########################################################

        raw_lot = risk_amount / (
            pip_distance * spec["pip_value"]
        )

        ########################################################
        # Clamp Between Min/Max
        ########################################################

        raw_lot = max(
            spec["min_lot"],
            min(
                raw_lot,
                spec["max_lot"],
            ),
        )

        ########################################################
        # Round to Broker Step
        ########################################################

        step = spec["lot_step"]

        lot_size = (
            math.floor(raw_lot / step)
            * step
        )

        lot_size = round(lot_size, 2)

        ########################################################
        # Final Validation
        ########################################################

        if lot_size < spec["min_lot"]:
            lot_size = spec["min_lot"]

        ########################################################
        # Return (PERMANENT API)
        ########################################################

        return {

            "balance": round(balance, 2),

            "risk_percent": round(risk_percent, 2),

            "risk_amount": round(risk_amount, 2),

            "stop_distance": round(stop_distance, 5),

            "pip_distance": round(pip_distance, 2),

            "pip_value": spec["pip_value"],

            "lot_size": lot_size,
        }