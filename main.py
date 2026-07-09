from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier
from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector

# --------------------------------------------------
# Mock candle data
# --------------------------------------------------

candles = [
    {"high": 12, "low": 10},
    {"high": 18, "low": 12},
    {"high": 25, "low": 15},
    {"high": 19, "low": 13},
    {"high": 14, "low": 11},
    {"high": 17, "low": 9},
    {"high": 23, "low": 14},
    {"high": 20, "low": 16},
    {"high": 18, "low": 17},
]

# --------------------------------------------------
# Run analyzer pipeline
# --------------------------------------------------

swings = SwingDetector().find_swings(candles)

classified = StructureClassifier().classify(swings)

trend = TrendEngine().detect_trend(classified)

bos = BOSDetector().detect(classified)

choch = CHOCHDetector().detect(classified)

# --------------------------------------------------
# Report
# --------------------------------------------------

print("=" * 40)
print("ATLASTRADER ANALYSIS")
print("=" * 40)

print("\nMarket Structure:")

for item in classified:
    print(
        f"{item['label']:>5}  Price: {item['price']}"
    )

print("\nTrend")
print(trend)

print("\nBreak of Structure")
print(bos)

print("\nChange of Character")
print(choch)