from analyzer.trend import TrendEngine

classified = [
    {"label": "HIGH"},
    {"label": "LOW"},
    {"label": "HH"},
    {"label": "HL"},
    {"label": "HH"},
    {"label": "HL"},
]

engine = TrendEngine()

result = engine.detect_trend(classified)

print("\nTrend Analysis\n")
print(result)