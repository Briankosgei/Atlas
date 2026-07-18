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
from analyzer.mtf_filter import MTFAlignment

from signals.signal_engine import SignalEngine
from planner.trade_planner import TradePlanner
from risk.risk_manager import RiskManager

from timeframe.multi_timeframe import MultiTimeframeAnalyzer


class MarketAnalyzer:

    def __init__(self):

        self.feed = YahooFinanceFeed()

        # Structure Analysis
        self.swing_detector = SwingDetector()
        self.classifier = StructureClassifier()

        # Market Analysis
        self.trend = TrendEngine()
        self.bos = BOSDetector()
        self.choch = CHOCHDetector()
        self.liquidity = LiquidityDetector()
        self.momentum = MomentumDetector()
        self.confidence = ConfidenceEngine()

        # Session
        self.session = SessionManager()

        # Multi-Timeframe
        self.multi_timeframe = MultiTimeframeAnalyzer(self.feed)
        self.mtf_filter = MTFAlignment()

        # Trading
        self.signal_engine = SignalEngine()
        self.trade_planner = TradePlanner()
        self.risk_manager = RiskManager()

    def analyze(self, symbol):

        # Session Check
        session = self.session.is_market_open(symbol)

        try:

            # Load Market Data
            candles = self.feed.get_candles(symbol)

            if not candles:

                return {
                    "symbol": symbol,
                    "error": f"No market data available for {symbol}",
                    "session": session,
                }

            # Structure Analysis
            swings = self.swing_detector.find_swings(candles)
            structure = self.classifier.classify(swings)

            # Market Analysis
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

            # Multi-Timeframe
            mtf = self.multi_timeframe.analyze(symbol)

            alignment = self.mtf_filter.check(mtf)

            # Signal
            signal = self.signal_engine.generate(
                trend,
                bos,
                choch,
                liquidity,
                momentum,
                alignment,
            )

            # Trade Planning
            current_price = candles[-1]["close"]

            trade = self.trade_planner.plan_trade(
                direction=signal["signal"],
                entry=current_price,
                candles=candles,
            )

            # Risk Management
            risk = self.risk_manager.evaluate(
                symbol,
                trade,
            )

            # Return Full Report
            return {

                "symbol": symbol,

                "price": current_price,

                # Session
                "session": session,

                # Multi Timeframe
                "mtf": mtf,
                "alignment": alignment,

                # Analysis
                "trend": trend,
                "bos": bos,
                "choch": choch,
                "structure": structure,
                "liquidity": liquidity,
                "momentum": momentum,
                "confidence": confidence,

                # Trading
                "signal": signal,
                "trade": trade,
                "risk": risk,
            }

        except Exception as e:

            return {

                "symbol": symbol,

                "error": str(e),

                "session": session,
            }