from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier

from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector


# --------------------------------------------
# Sample Market Data
# --------------------------------------------

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

# --------------------------------------------
# Analysis Pipeline
# --------------------------------------------

swing_detector = SwingDetector()
classifier = StructureClassifier()

trend_engine = TrendEngine()
bos_detector = BOSDetector()
choch_detector = CHOCHDetector()

swings = swing_detector.find_swings(candles)
structure = classifier.classify(swings)

trend = trend_engine.detect_trend(structure)
bos = bos_detector.detect(structure)
choch = choch_detector.detect(structure)

# --------------------------------------------
# Report
# --------------------------------------------

print("=" * 50)
print("           ATLASTRADER ANALYSIS")
print("=" * 50)

print("\nMarket Structure")

if structure:
    for item in structure:
        print(f"{item['label']:>5} | {item['price']}")
else:
    print("No structure detected.")

print("\nTrend")
print(trend)

print("\nBreak of Structure")
print(bos)

print("\nChange of Character")
print(choch)

print("\nAnalysis Complete.")