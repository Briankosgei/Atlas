from datafeed.yfinance_feed import YahooFinanceFeed

# Structure Analysis
from analyzer.market_structure.swings import SwingDetector
from analyzer.market_structure.classifier import StructureClassifier

# Core Analysis
from analyzer.trend import TrendEngine
from analyzer.bos import BOSDetector
from analyzer.choch import CHOCHDetector
from analyzer.liquidity import LiquidityDetector
from analyzer.momentum import MomentumDetector
from analyzer.confidence import ConfidenceEngine

# Advanced Analysis
from analyzer.trend_strength import TrendStrength
from analyzer.volatility_filter import VolatilityFilter
from analyzer.signal_grade import SignalGrade

# Session / MTF
from analyzer.session_manager import SessionManager
from analyzer.mtf_filter import MTFAlignment
from timeframe.multi_timeframe import MultiTimeframeAnalyzer

# Trading
from signals.signal_engine import SignalEngine
from planner.trade_planner import TradePlanner
from risk.risk_manager import RiskManager


class MarketAnalyzer:

    def __init__(self):

        self.feed = YahooFinanceFeed()

        ####################################################
        # MARKET STRUCTURE
        ####################################################

        self.swing_detector = SwingDetector()
        self.classifier = StructureClassifier()

        ####################################################
        # CORE ANALYSIS
        ####################################################

        self.trend = TrendEngine()
        self.bos = BOSDetector()
        self.choch = CHOCHDetector()
        self.liquidity = LiquidityDetector()
        self.momentum = MomentumDetector()
        self.confidence = ConfidenceEngine()

        ####################################################
        # ADVANCED ANALYSIS
        ####################################################

        self.trend_strength = TrendStrength()
        self.volatility = VolatilityFilter()
        self.grade = SignalGrade()

        ####################################################
        # SESSION
        ####################################################

        self.session = SessionManager()

        ####################################################
        # MULTI TIMEFRAME
        ####################################################

        self.multi_timeframe = MultiTimeframeAnalyzer(self.feed)
        self.mtf_filter = MTFAlignment()

        ####################################################
        # TRADING
        ####################################################

        self.signal_engine = SignalEngine()
        self.trade_planner = TradePlanner()
        self.risk_manager = RiskManager()

    def analyze(self, symbol):

        session = self.session.is_market_open(symbol)

        try:

            ####################################################
            # LOAD DATA
            ####################################################

            candles = self.feed.get_candles(symbol)

            if not candles:
                return {
                    "symbol": symbol,
                    "error": f"No market data available for {symbol}",
                    "session": session,
                }

            ####################################################
            # MARKET STRUCTURE
            ####################################################

            swings = self.swing_detector.find_swings(candles)
            structure = self.classifier.classify(swings)

            ####################################################
            # TREND
            ####################################################

            trend = self.trend.detect_trend(structure)

            ####################################################
            # BOS / CHOCH
            ####################################################

            bos = self.bos.detect(structure)
            choch = self.choch.detect(structure)

            ####################################################
            # LIQUIDITY
            ####################################################

            liquidity = self.liquidity.detect(
                candles,
                structure,
            )

            ####################################################
            # MOMENTUM
            ####################################################

            momentum = self.momentum.detect(candles)

            ####################################################
            # MULTI TIMEFRAME
            ####################################################

            mtf = self.multi_timeframe.analyze(symbol)

            alignment = self.mtf_filter.check(mtf)

            ####################################################
            # VOLATILITY
            ####################################################

            volatility = self.volatility.check(candles)

            ####################################################
            # CONFIDENCE
            ####################################################

            confidence = self.confidence.calculate(
                trend=trend,
                bos=bos,
                choch=choch,
                liquidity=liquidity,
                momentum=momentum,
                alignment=alignment,
                volatility=volatility,
            )

            ####################################################
            # TREND STRENGTH
            ####################################################

            trend_strength = self.trend_strength.calculate(
                trend=trend,
                bos=bos,
                choch=choch,
                momentum=momentum,
                alignment=alignment,
                liquidity=liquidity,
            )

            ####################################################
            # SIGNAL
            ####################################################

            signal = self.signal_engine.generate(
                trend=trend,
                bos=bos,
                choch=choch,
                liquidity=liquidity,
                momentum=momentum,
                alignment=alignment,
            )

            ####################################################
            # TRADE PLAN
            ####################################################

            current_price = candles[-1]["close"]

            trade = self.trade_planner.plan_trade(
                direction=signal["signal"],
                entry=current_price,
                candles=candles,
            )

            ####################################################
            # RISK
            ####################################################

            risk = self.risk_manager.evaluate(
                symbol=symbol,
                trade=trade,
            )

            ####################################################
            # GRADE
            ####################################################

            grade = self.grade.grade(confidence)

            ####################################################
            # REPORT
            ####################################################

            return {

                "symbol": symbol,

                "price": current_price,

                "session": session,

                "mtf": mtf,

                "alignment": alignment,

                "structure": structure,

                "trend": trend,

                "bos": bos,

                "choch": choch,

                "liquidity": liquidity,

                "momentum": momentum,

                "volatility": volatility,

                "confidence": confidence,

                "trend_strength": trend_strength,

                "grade": grade,
                
                "signal": signal,

                "trade": trade,

                "risk": risk,
            }

        except Exception as e:
            import traceback
            traceback.print_exc()

            return {

                "symbol": symbol,

                "error": str(e),

                "session": session,
            }