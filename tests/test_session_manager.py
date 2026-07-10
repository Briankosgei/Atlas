from analyzer.session_manager import SessionManager

manager = SessionManager()

symbols = [
    "XAUUSD",
    "BTCUSD",
    "EURUSD",
]

for symbol in symbols:

    session = manager.is_market_open(symbol)

    print(symbol)
    print(session)
    print()