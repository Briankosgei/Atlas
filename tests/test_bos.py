from analyzer.bos import BOSDetector

swings = [
    {"label": "HIGH"},
    {"label": "LOW"},
    {"label": "HH"},
    {"label": "HL"},
    {"label": "HH"}
]

bos = BOSDetector()

result = bos.detect(swings)

print("\nBreak of Structure\n")
print(result)