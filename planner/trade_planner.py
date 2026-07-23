from analyzer.atr import ATRCalculator


class TradePlanner:
    """
    AtlasTrader Trade Planner

    Builds a complete trade setup using:

        • ATR
        • Recent Swing High / Low
        • Dynamic Risk Reward
        • Confidence Score

    Returns a standardized trade dictionary consumed by
    RiskManager.
    """

    def __init__(
        self,
        atr_multiplier=1.5,
        swing_lookback=10,
        minimum_rr=2.0,
        default_rr=3.0,
        maximum_rr=4.0,
    ):

        self.atr_multiplier = atr_multiplier
        self.swing_lookback = swing_lookback

        self.minimum_rr = minimum_rr
        self.default_rr = default_rr
        self.maximum_rr = maximum_rr

        self.atr = ATRCalculator()

    ##########################################################

    def _precision(self, price):

        if price >= 10000:
            return 2      # BTC

        if price >= 1000:
            return 2      # Gold

        if price >= 100:
            return 3      # JPY

        return 5          # Forex

    ##########################################################

    def _dynamic_rr(self, confidence):

        if confidence >= 90:
            return self.maximum_rr

        if confidence >= 75:
            return self.default_rr

        return self.minimum_rr

    ##########################################################

    def _recent_swing(self, candles, direction):

        if len(candles) < self.swing_lookback:
            return None

        recent = candles[-self.swing_lookback:]

        try:

            if direction == "BUY":
                return min(c["low"] for c in recent)

            return max(c["high"] for c in recent)

        except Exception:
            return None

    ##########################################################

    def _reject(self, reason):

        return {
            "valid": False,
            "reason": reason,
        }

    ##########################################################

    def plan_trade(
        self,
        direction,
        entry,
        candles,
        confidence=70,
    ):

        ######################################################
        # Validation
        ######################################################

        if direction not in ("BUY", "SELL"):
            return self._reject("No trading signal.")

        if entry is None or entry <= 0:
            return self._reject("Invalid entry price.")

        if not candles or len(candles) < 20:
            return self._reject("Insufficient candle history.")

        ######################################################
        # ATR
        ######################################################

        try:

            atr_result = self.atr.calculate(candles)

            atr = atr_result.get("atr", 0)

        except Exception as exc:

            return self._reject(f"ATR calculation failed: {exc}")

        if atr <= 0:
            return self._reject("ATR unavailable.")

        ######################################################
        # Risk Reward
        ######################################################

        rr = self._dynamic_rr(confidence)

        atr_stop = atr * self.atr_multiplier

        swing = self._recent_swing(
            candles,
            direction,
        )

        ######################################################
        # BUY
        ######################################################

        if direction == "BUY":

            stop_loss = entry - atr_stop

            if swing is not None:
                stop_loss = min(stop_loss, swing)

            risk = entry - stop_loss

            take_profit = entry + (risk * rr)

        ######################################################
        # SELL
        ######################################################

        else:

            stop_loss = entry + atr_stop

            if swing is not None:
                stop_loss = max(stop_loss, swing)

            risk = stop_loss - entry

            take_profit = entry - (risk * rr)

        ######################################################
        # Validation
        ######################################################

        if risk <= 0:
            return self._reject("Invalid stop-loss distance.")

        if take_profit <= 0:
            return self._reject("Invalid take-profit.")

        ######################################################
        # Precision
        ######################################################

        precision = self._precision(entry)

        ######################################################
        # Return
        ######################################################

        return {

            "valid": True,

            "reason": "Trade plan generated.",

            "direction": direction,

            "entry": round(entry, precision),

            "stop_loss": round(stop_loss, precision),

            "take_profit": round(take_profit, precision),

            "risk_distance": round(risk, precision),

            "atr": round(atr, precision),

            "rr": round(rr, 2),

            "confidence": round(confidence),
        }