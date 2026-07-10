from datetime import datetime, timezone


class SessionManager:

    FOREX_SYMBOLS = {
        "XAUUSD",
        "EURUSD",
        "USDJPY",
        "USDCAD",
        "AUDUSD",
    }

    CRYPTO_SYMBOLS = {
        "BTCUSD",
    }

    def is_market_open(self, symbol):

        now = datetime.now(timezone.utc)

        weekday = now.weekday()
        hour = now.hour

        # BTC trades all week
        if symbol in self.CRYPTO_SYMBOLS:
            return {
                "allowed": True,
                "reason": "Crypto market open",
            }

        # Friday Saturday Sunday
        if weekday >= 4:
            return {
                "allowed": False,
                "reason": "Weekend filter",
            }

        # Thursday after 21 UTC
        if weekday == 3 and hour >= 21:
            return {
                "allowed": False,
                "reason": "Thursday cutoff",
            }

        return {
            "allowed": True,
            "reason": "Trading session open",
        }