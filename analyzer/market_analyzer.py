from datafeed.yfinance_feed import YahooFinanceFeed

from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier
from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector
from analyzer.liquidity import LiquidityDetector
from analyzer.momentum import MomentumDetector
from analyzer.confidence import ConfidenceEngine
from signals.signal_engine import SignalEngine


class MarketAnalyzer:

    def __init__(self):
        self.feed = YahooFinanceFeed()

        self.swing_detector = SwingDetector()
        self.classifier = StructureClassifier()
        self.trend = TrendEngine()
        self.bos = BOSDetector()
        self.choch = CHOCHDetector()
        self.liquidity = LiquidityDetector()
        self.momentum = MomentumDetector()
        self.confidence = ConfidenceEngine()
        self.signal_engine = SignalEngine()

    def analyze(self, symbol):

        candles = self.feed.get_candles(symbol)

        swings = self.swing_detector.find_swings(candles)

        classified = self.classifier.classify(swings)

        trend = self.trend.detect_trend(classified)

        bos = self.bos.detect(classified)

        choch = self.choch.detect(classified)
        
        liquidity = self.liquidity.detect(
            candles,
            classified
        )

        momentum = self.momentum.detect(candles)

        confidence = self.confidence.calculate(
            trend,
            bos,
            choch,
            liquidity,
            momentum
        )

        signal = self.signal_engine.generate(
            trend,
            bos,
            choch,
            liquidity,
            momentum
        )

        return {
            "symbol": symbol,
            "price": candles[-1]["close"],
            "trend": trend,
            "bos": bos,
            "choch": choch,
            "structure": classified,
            "liquidity": liquidity,
            "momentum": momentum,
            "confidence": confidence,
            "signal": signal,

        }