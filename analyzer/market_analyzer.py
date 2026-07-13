from datafeed.yfinance_feed import YahooFinanceFeed

from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier
from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector
from analyzer.liquidity import LiquidityDetector
from analyzer.momentum import MomentumDetector
from analyzer.confidence import ConfidenceEngine
from analyzer.mtf_filter import MTFAlignment

from analyzer.session_manager import SessionManager

from signals.signal_engine import SignalEngine
from planner.trade_planner import TradePlanner
from risk.risk_manager import RiskManager

from timeframe.multi_timeframe import MultiTimeframeAnalyzer


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
        self.trade_planner = TradePlanner()
        self.risk_manager = RiskManager()
        self.session = SessionManager()
        self.mtf_filter = MTFAlignment()

        # NEW
        self.multi_timeframe = MultiTimeframeAnalyzer(self.feed)

    def analyze(self, symbol):

        # -----------------------
        # 1H Analysis
        # -----------------------

        candles = self.feed.get_candles(symbol)

        swings = self.swing_detector.find_swings(candles)

        classified = self.classifier.classify(swings)

        trend = self.trend.detect_trend(classified)

        bos = self.bos.detect(classified)

        choch = self.choch.detect(classified)

        liquidity = self.liquidity.detect(
            candles,
            classified,
        )

        momentum = self.momentum.detect(candles)

        confidence = self.confidence.calculate(
            trend,
            bos,
            choch,
            liquidity,
            momentum,
        )

        # -----------------------
        # Multi-Timeframe Analysis
        # -----------------------

        mtf = self.multi_timeframe.analyze(symbol)
        alignment = self.mtf_filter.check(mtf)

        # -----------------------
        # Signal
        # -----------------------

        signal = self.signal_engine.generate(
            trend,
            bos,
            choch,
            liquidity,
            momentum,
        )

        # -----------------------
        # Trade Plan
        # -----------------------

        trade = self.trade_planner.plan(
            symbol,
            candles[-1]["close"],
            signal,
        )

        # -----------------------
        # Risk
        # -----------------------

        risk = self.risk_manager.evaluate(
            symbol,
            trade,
        )

        # -----------------------
        # Session
        # -----------------------

        session = self.session.is_market_open(symbol)

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

            "trade": trade,

            "risk": risk,

            "session": session,

            "alignment": alignment,

            # NEW
            "mtf": mtf,
        }