from analyzer.atr import ATRCalculator


class TradePlanner:

    def __init__(
        self,
        atr_multiplier=1.5,
        risk_reward=3.0,
    ):
        self.atr_multiplier = atr_multiplier
        self.risk_reward = risk_reward

    def plan_trade(
        self,
        direction,
        entry,
        candles,
    ):

        # Reject invalid directions
        if direction not in ["BUY", "SELL"]:
            return {
                "valid": False,
                "reason": "No valid trading signal",
            }

        atr = ATRCalculator().calculate(candles)["atr"]

        risk = atr * self.atr_multiplier

        if direction == "BUY":

            stop_loss = entry - risk

            take_profit = (
                entry
                + (risk * self.risk_reward)
            )

        else:  # SELL

            stop_loss = entry + risk

            take_profit = (
                entry
                - (risk * self.risk_reward)
            )

        return {

            "valid": True,

            "reason": "ATR-based trade generated",

            "direction": direction,

            "entry": round(entry, 2),

            "stop_loss": round(stop_loss, 2),

            "take_profit": round(take_profit, 2),

            "atr": round(atr, 2),

            "risk_distance": round(risk, 2),

            "rr": self.risk_reward,
        }