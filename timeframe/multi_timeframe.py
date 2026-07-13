from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier
from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector


class MultiTimeframeAnalyzer:

    TIMEFRAMES = [
        "1d",
        "4h",
        "1h",
        "15m",
    ]

    def __init__(self, feed):

        self.feed = feed

        self.swing = SwingDetector()
        self.classifier = StructureClassifier()
        self.trend = TrendEngine()
        self.bos = BOSDetector()
        self.choch = CHOCHDetector()

    def analyze(self, symbol):

        report = {}

        for tf in self.TIMEFRAMES:

            candles = self.feed.get_candles(
                symbol,
                interval=tf,
            )

            swings = self.swing.find_swings(candles)

            classified = self.classifier.classify(swings)

            trend = self.trend.detect_trend(classified)

            bos = self.bos.detect(classified)

            choch = self.choch.detect(classified)

            report[tf] = {
                "trend": trend,
                "bos": bos,
                "choch": choch,
            }

        return report