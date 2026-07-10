from risk.risk_manager import RiskManager

manager = RiskManager()

trade = {
    "valid": True,
    "direction": "BUY",
    "entry": 1.1000,
    "stop_loss": 1.0950,
    "take_profit": 1.1150,
    "rr": "1:3",
}

report = manager.evaluate(
    symbol="EURUSD",
    trade=trade,
    balance=100,
    risk_percent=1,
)

print(report)