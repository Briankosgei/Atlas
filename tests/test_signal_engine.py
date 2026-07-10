from signals.signal_engine import SignalEngine

engine = SignalEngine()

trend = {"trend": "BULLISH"}
bos = {"bos": True, "direction": "BULLISH"}
choch = {"choch": False, "direction": None}
liquidity = {"liquidity": True, "direction": "BULLISH"}
momentum = {"strength": "STRONG", "score": 100}

signal = engine.generate(
    trend,
    bos,
    choch,
    liquidity,
    momentum,
)

print(signal)