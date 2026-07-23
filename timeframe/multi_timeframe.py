from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier

from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector
from analyzer.liquidity import LiquidityDetector
from analyzer.momentum import MomentumDetector


class MultiTimeframeAnalyzer:
    """
    AtlasTrader Multi-Timeframe Analyzer

    Performs complete higher-timeframe analysis.

    Each timeframe returns:

        • Trend
        • BOS
        • CHoCH
        • Liquidity
        • Momentum
        • Structure
        • Swing Count

    The result is consumed by the
    MTF Alignment Engine.
    """

    DEFAULT_TIMEFRAMES = [
        "1h",
        "4h",
        "1d",
        "1wk",
    ]

    MINIMUM_CANDLES = 50

    def __init__(self, feed, timeframes=None):

        self.feed = feed

        self.swing_detector = SwingDetector()
        self.classifier = StructureClassifier()

        self.trend_engine = TrendEngine()
        self.bos_detector = BOSDetector()
        self.choch_detector = CHOCHDetector()
        self.liquidity_detector = LiquidityDetector()
        self.momentum_engine = MomentumDetector()

        self.timeframes = (
            timeframes
            if timeframes
            else self.DEFAULT_TIMEFRAMES
        )

    ##############################################################

    def _empty_result(self, reason="Unavailable"):

        return {

            "trend": {
                "trend": "UNKNOWN",
                "confidence": 0,
            },

            "bos": {
                "bos": False,
                "direction": None,
            },

            "choch": {
                "choch": False,
                "direction": None,
            },

            "liquidity": {
                "sweep": False,
                "direction": None,
            },

            "momentum": {
                "strength": "UNKNOWN",
                "score": 0,
            },

            "structure": [],

            "swings": 0,

            "reason": reason,
        }

    ##############################################################

    def analyze(self, symbol):

        results = {}

        for timeframe in self.timeframes:

            try:

                candles = self.feed.get_candles(
                    symbol,
                    interval=timeframe,
                )

                if (
                    candles is None
                    or len(candles) < self.MINIMUM_CANDLES
                ):

                    results[timeframe] = self._empty_result(
                        "Not enough candles"
                    )

                    continue

                ##################################################
                # Market Structure
                ##################################################

                swings = self.swing_detector.find_swings(
                    candles
                )

                structure = self.classifier.classify(
                    swings
                )

                ##################################################
                # Analysis Modules
                ##################################################

                trend = self.trend_engine.detect_trend(
                    structure
                )

                bos = self.bos_detector.detect(
                    structure
                )

                choch = self.choch_detector.detect(
                    structure
                )

                liquidity = self.liquidity_detector.detect(
                    candles,
                    structure,
                )

                momentum = self.momentum_engine.calculate(
                    candles
                )

                ##################################################

                results[timeframe] = {

                    "trend": trend,

                    "bos": bos,

                    "choch": choch,

                    "liquidity": liquidity,

                    "momentum": momentum,

                    "structure": structure,

                    "swings": len(swings),
                }

            except Exception as e:

                results[timeframe] = self._empty_result(
                    str(e)
                )

        return results