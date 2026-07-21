from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier

from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector


class MultiTimeframeAnalyzer:

    def __init__(self, feed):

        self.feed = feed

        self.swing = SwingDetector()
        self.classifier = StructureClassifier()

        self.trend = TrendEngine()
        self.bos = BOSDetector()
        self.choch = CHOCHDetector()

        self.timeframes = [
            "4h",
            "1d",
        ]

    def analyze(self, symbol):

        results = {}

        for tf in self.timeframes:

            candles = self.feed.get_candles(
                symbol,
                interval=tf,
            )

            if not candles:

                continue

            swings = self.swing.find_swings(candles)

            structure = self.classifier.classify(swings)

            trend = self.trend.detect_trend(structure)

            bos = self.bos.detect(structure)

            choch = self.choch.detect(structure)

            results[tf] = {
                "trend": trend,
                "bos": bos,
                "choch": choch,
            }

        return results