from datetime import datetime

from datafeed.yfinance_feed import YahooFinanceFeed

from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier

from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector
from analyzer.liquidity import LiquidityDetector
from analyzer.momentum import MomentumDetector
from analyzer.confidence import ConfidenceEngine

from analyzer.trend_strength import TrendStrength
from analyzer.volatility_filter import VolatilityFilter
from analyzer.signal_grade import SignalGrade

from analyzer.session_manager import SessionManager
from analyzer.mtf_filter import MTFAlignment
from timeframe.multi_timeframe import MultiTimeframeAnalyzer

from signals.signal_engine import SignalEngine
from planner.trade_planner import TradePlanner
from risk.risk_manager import RiskManager


class MarketAnalyzer:
    """
    AtlasTrader Master Analysis Engine

    Responsibilities

        • Load market data
        • Build market structure
        • Detect trend
        • Detect BOS / CHoCH
        • Detect liquidity sweeps
        • Calculate momentum
        • Run higher timeframe analysis
        • Calculate confidence
        • Generate trading signal
        • Build trade plan
        • Validate risk
        • Produce one standardized report
    """

    MIN_CANDLES = 120
    MIN_SWINGS = 4

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

        self.trend_strength = TrendStrength()
        self.volatility = VolatilityFilter()
        self.grade = SignalGrade()

        self.session = SessionManager()

        self.multi_timeframe = MultiTimeframeAnalyzer(self.feed)
        self.mtf_filter = MTFAlignment()

        self.signal_engine = SignalEngine()
        self.trade_planner = TradePlanner()
        self.risk_manager = RiskManager()

    ###########################################################

    def _error(self, symbol, session, message):

        return {

            "symbol": symbol,
            "timestamp": datetime.utcnow().isoformat(),

            "session": session,

            "error": message,
        }

    ###########################################################

    def analyze(self, symbol):

        session = self.session.is_market_open(symbol)

        try:

            candles = self.feed.get_candles(symbol)

            if candles is None:

                return self._error(
                    symbol,
                    session,
                    "No market data returned.",
                )

            if len(candles) < self.MIN_CANDLES:

                return self._error(
                    symbol,
                    session,
                    f"Only {len(candles)} candles available.",
                )

            current_price = candles[-1]["close"]

            swings = self.swing_detector.find_swings(candles)

            if len(swings) < self.MIN_SWINGS:

                return self._error(
                    symbol,
                    session,
                    "Insufficient swing points.",
                )

            structure = self.classifier.classify(swings)

            trend = self.trend.detect_trend(structure)

            bos = self.bos.detect(structure)

            choch = self.choch.detect(structure)

            liquidity = self.liquidity.detect(
                candles,
                structure,
            )

            momentum = self.momentum.detect(candles)

            mtf = self.multi_timeframe.analyze(symbol)

            alignment = self.mtf_filter.check(mtf)

            volatility = self.volatility.check(
                candles,
                symbol,
            )

            confidence = self.confidence.calculate(
                trend,
                bos,
                choch,
                liquidity,
                momentum,
                alignment,
                volatility,
            )

            strength = self.trend_strength.calculate(
                trend=trend,
                bos=bos,
                choch=choch,
                momentum=momentum,
                alignment=alignment,
                liquidity=liquidity,
                volatility=volatility,
            )

            signal = self.signal_engine.generate(
                trend=trend,
                bos=bos,
                choch=choch,
                liquidity=liquidity,
                momentum=momentum,
                alignment=alignment,
                volatility=volatility,
            )

            trade = self.trade_planner.plan_trade(
                direction=signal["signal"],
                entry=current_price,
                candles=candles,
                confidence=confidence,
            )

            risk = self.risk_manager.evaluate(
                symbol=symbol,
                trade=trade,
            )

            grade = self.grade.grade(confidence["score"])

            return {

                "symbol": symbol,

                "timestamp": datetime.utcnow().isoformat(),

                "price": current_price,

                "session": session,

                "candles": len(candles),

                "swings": len(swings),

                "structure": structure,

                "trend": trend,

                "bos": bos,

                "choch": choch,

                "liquidity": liquidity,

                "momentum": momentum,

                "mtf": mtf,

                "alignment": alignment,

                "volatility": volatility,

                "confidence": confidence,

                "trend_strength": strength,

                "grade": grade,

                "signal": signal,

                "trade": trade,

                "risk": risk,
            }

        except Exception as exc:

            import traceback

            traceback.print_exc()

            return self._error(
                symbol,
                session,
                str(exc),
            )