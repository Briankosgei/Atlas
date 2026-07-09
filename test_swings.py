from analyzer.market_structure.swings import SwingDetector

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

detector = SwingDetector()

swings = detector.find_swings(candles)

print("\nDetected Swings\n")

for swing in swings:
    print(swing)