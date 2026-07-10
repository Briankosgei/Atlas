from datafeed.yfinance_feed import YahooFinanceFeed

from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier

from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector
from analyzer.liquidity import LiquidityDetector
from analyzer.momentum import MomentumDetector
from analyzer.confidence import ConfidenceEngine
from analyzer.session_manager import SessionManager

from signals.signal_engine import SignalEngine
from planner.trade_planner import TradePlanner
from risk.risk_manager import RiskManager


class MarketAnalyzer:

    def __init__(self):

        # Data Feed
        self.feed = YahooFinanceFeed()

        # Market Structure
        self.swing_detector = SwingDetector()
        self.classifier = StructureClassifier()

        # Analysis Engines
        self.trend = TrendEngine()
        self.bos = BOSDetector()
        self.choch = CHOCHDetector()
        self.liquidity = LiquidityDetector()
        self.momentum = MomentumDetector()
        self.confidence = ConfidenceEngine()

        # Trading Engines
        self.signal_engine = SignalEngine()
        self.trade_planner = TradePlanner()
        self.risk_manager = RiskManager()

        # Session Filter
        self.session = SessionManager()

    def analyze(self, symbol):

        # --------------------------------------------------
        # Market Data
        # --------------------------------------------------

        candles = self.feed.get_candles(symbol)
        current_price = candles[-1]["close"]

        # --------------------------------------------------
        # Market Structure
        # --------------------------------------------------

        swings = self.swing_detector.find_swings(candles)
        structure = self.classifier.classify(swings)

        # --------------------------------------------------
        # Analysis
        # --------------------------------------------------

        trend = self.trend.detect_trend(structure)
        bos = self.bos.detect(structure)
        choch = self.choch.detect(structure)

        liquidity = self.liquidity.detect(
            candles,
            structure,
        )

        momentum = self.momentum.detect(candles)

        confidence = self.confidence.calculate(
            trend,
            bos,
            choch,
            liquidity,
            momentum,
        )

        # --------------------------------------------------
        # Signal Generation
        # --------------------------------------------------

        signal = self.signal_engine.generate(
            trend,
            bos,
            choch,
            liquidity,
            momentum,
        )

        # --------------------------------------------------
        # Trade Planning
        # --------------------------------------------------

        trade = self.trade_planner.plan(
            symbol,
            current_price,
            signal,
        )

        # --------------------------------------------------
        # Risk Management
        # --------------------------------------------------

        risk = self.risk_manager.evaluate(
            symbol,
            trade,
        )

        # --------------------------------------------------
        # Session Filter
        # --------------------------------------------------

        session = self.session.is_market_open(symbol)

        # --------------------------------------------------
        # Final Report
        # --------------------------------------------------

        return {
            "symbol": symbol,
            "price": current_price,
            "session": session,
            "trend": trend,
            "bos": bos,
            "choch": choch,
            "structure": structure,
            "liquidity": liquidity,
            "momentum": momentum,
            "confidence": confidence,
            "signal": signal,
            "trade": trade,
            "risk": risk,
        }