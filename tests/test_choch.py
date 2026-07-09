from analyzer.choch import CHOCHDetector

swings = [
    {"label": "HH"},
    {"label": "HL"},
    {"label": "HH"},
    {"label": "LL"},
]

detector = CHOCHDetector()

result = detector.detect(swings)

print("\nChange of Character\n")
print(result)