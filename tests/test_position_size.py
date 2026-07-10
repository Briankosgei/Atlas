from risk.position_size import PositionSizer

sizer = PositionSizer()

trade = sizer.calculate(
    symbol="EURUSD",
    balance=100,
    risk_percent=1,
    stop_distance=50,
)

print(trade)