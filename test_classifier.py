from analyzer.market_structure.classifier import StructureClassifier

swings = [
    {"type": "HIGH", "price": 25},
    {"type": "LOW", "price": 9},
    {"type": "HIGH", "price": 23},
    {"type": "LOW", "price": 12},
    {"type": "HIGH", "price": 27},
]

classifier = StructureClassifier()

results = classifier.classify(swings)

print("\nMarket Structure\n")

for item in results:
    print(item)