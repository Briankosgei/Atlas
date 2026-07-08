from datetime import datetime
from analyzer.symbols import SymbolManager


class SessionManager:
    """
    Determines whether trading is allowed for a symbol
    based on its configured trading days.
    """

    def __init__(self):
        self.symbol_manager = SymbolManager()
        self.symbol_manager.load()

    def can_trade(self, symbol_name):
        today = datetime.utcnow().strftime("%A")

        for symbol in self.symbol_manager.enabled_symbols():
            if symbol["name"] == symbol_name:
                return today in symbol["trading_days"]

        return False


if __name__ == "__main__":

    session = SessionManager()

    print("\n===== Trading Session Check =====\n")

    for symbol in session.symbol_manager.enabled_symbols():

        allowed = session.can_trade(symbol["name"])

        status = "✅ ALLOWED" if allowed else "❌ BLOCKED"

        print(f"{symbol['name']:10} {status}")