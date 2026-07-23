from concurrent.futures import ThreadPoolExecutor, as_completed

from analyzer.market_analyzer import MarketAnalyzer
from journal.trade_journal import TradeJournal
from utils.logger import logger


SYMBOLS = [
    "XAUUSD",
    "BTCUSD",
    "EURUSD",
    "USDJPY",
    "USDCAD",
    "AUDUSD",
]


class Scanner:

    def __init__(self):
        self.analyzer = MarketAnalyzer()
        self.journal = TradeJournal()

    ###########################################################

    def analyze_symbol(self, symbol):

        logger.info(f"Scanning {symbol}")

        try:

            report = self.analyzer.analyze(symbol)

            if report is None:

                logger.error(
                    f"{symbol}: MarketAnalyzer returned None."
                )

                return symbol, {
                    "symbol": symbol,
                    "error": "MarketAnalyzer returned None.",
                }

            if not isinstance(report, dict):

                logger.error(
                    f"{symbol}: Invalid report type {type(report)}"
                )

                return symbol, {
                    "symbol": symbol,
                    "error": f"Invalid report type: {type(report)}",
                }

            return symbol, report

        except Exception as exc:

            logger.exception(exc)

            return symbol, {
                "symbol": symbol,
                "error": str(exc),
            }

    ###########################################################

    def display(self, symbol, report):

        print(f"\n{symbol}")
        print("-" * 70)

        #######################################################
        # Validate report
        #######################################################

        if report is None:

            print("ERROR: Analyzer returned None.")
            print("-" * 70)
            return

        if not isinstance(report, dict):

            print(f"ERROR: Invalid report type {type(report)}")
            print("-" * 70)
            return

        if report.get("error"):

            print(report["error"])
            print("-" * 70)
            return

        #######################################################
        # Session
        #######################################################

        session = report.get("session", {})

        print(
            f"Session          : "
            f"{'OPEN' if session.get('allowed', False) else 'CLOSED'}"
        )

        print(
            f"Reason           : "
            f"{session.get('reason','Unknown')}"
        )

        #######################################################
        # Price
        #######################################################

        print(f"Current Price    : {report.get('price')}")

        #######################################################
        # Trend
        #######################################################

        trend = report.get("trend", {})

        print(
            f"Trend            : "
            f"{trend.get('trend')} "
            f"({trend.get('confidence',0)}%)"
        )

        #######################################################
        # BOS
        #######################################################

        bos = report.get("bos", {})

        print(
            f"BOS              : "
            f"{bos.get('direction') if bos.get('bos') else 'None'}"
        )

        #######################################################
        # CHOCH
        #######################################################

        choch = report.get("choch", {})

        print(
            f"CHoCH            : "
            f"{choch.get('direction') if choch.get('choch') else 'None'}"
        )

        #######################################################
        # Liquidity
        #######################################################

        liquidity = report.get("liquidity", {})

        if liquidity.get("sweep"):

            print(
                f"Liquidity Sweep  : YES {liquidity.get('direction')}"
            )

        else:

            print("Liquidity Sweep  : NO")

        #######################################################
        # Momentum
        #######################################################

        momentum = report.get("momentum", {})

        print(
            f"Momentum         : "
            f"{momentum.get('strength')} "
            f"({momentum.get('score',0)}%)"
        )

        #######################################################
        # Volatility
        #######################################################

        volatility = report.get("volatility", {})

        print(f"ATR              : {volatility.get('atr')}")
        print(f"Volatility       : {volatility.get('reason')}")

        #######################################################
        # HTF
        #######################################################

        alignment = report.get("alignment", {})

        print(
            f"HTF Alignment    : "
            f"{alignment.get('direction')} "
            f"({alignment.get('confidence',0)}%)"
        )

        #######################################################
        # Trend Strength
        #######################################################

        strength = report.get("trend_strength", {})

        print(
            f"Trend Strength   : "
            f"{strength.get('score',0)}/100"
        )

        #######################################################
        # Confidence
        #######################################################

        confidence = report["confidence"]
        
        print("\nConfidence Breakdown")

        for name, value in confidence["breakdown"].items():
            print(f" {name:12}: {value}")
        #######################################################
        # Grade
        #######################################################

        grade = report.get("grade", {})

        print(
            f"Signal Grade     : "
            f"{grade.get('grade')} "
            f"({grade.get('quality')})"
        )

        #######################################################
        # Signal
        #######################################################

        signal = report.get("signal", {})

        print(f"Signal           : {signal.get('signal')}")
        print(f"Signal Score     : {signal.get('score')}")

        print("Reasons:")

        for reason in signal.get("reasons", []):

            print(f"   ✓ {reason}")

        #######################################################
        # Trade
        #######################################################

        trade = report.get("trade", {})

        print("\nTrade Plan")

        if trade.get("valid"):

            print(f"Direction        : {trade.get('direction')}")
            print(f"Entry            : {trade.get('entry')}")
            print(f"ATR              : {trade.get('atr')}")
            print(f"Stop Loss        : {trade.get('stop_loss')}")
            print(f"Take Profit      : {trade.get('take_profit')}")
            print(f"Risk Distance    : {trade.get('risk_distance')}")
            print(f"Risk Reward      : 1:{trade.get('rr')}")

        else:

            print("No valid setup.")

        #######################################################
        # Risk
        #######################################################

        risk = report.get("risk", {})

        print("\nRisk Management")

        if risk.get("approved"):

            position = risk.get("position", {})

            print(f"Balance          : ${position.get('balance')}")
            print(f"Risk             : {position.get('risk_percent')}%")
            print(f"Risk Amount      : ${position.get('risk_amount')}")
            print(f"Lot Size         : {position.get('lot_size')}")

            self.journal.save(report)

        else:

            print(
                f"Trade Rejected   : "
                f"{risk.get('reason')}"
            )

        logger.info(
            f"{symbol} | "
            f"{signal.get('signal')} | "
            f"Confidence={report.get('confidence')} | "
            f"Grade={grade.get('grade')}"
        )

        print("-" * 70)

    ###########################################################

    def run(self):

        print("\n" + "=" * 70)
        print("                ATLASTRADER MARKET SCANNER")
        print("=" * 70)

        with ThreadPoolExecutor(max_workers=4) as executor:

            futures = {
                executor.submit(
                    self.analyze_symbol,
                    symbol,
                ): symbol
                for symbol in SYMBOLS
            }

            for future in as_completed(futures):

                symbol = futures[future]

                try:

                    _, report = future.result()

                except Exception as exc:

                    report = {
                        "error": str(exc)
                    }

                self.display(symbol, report)

        print("\nScan Complete.\n")


if __name__ == "__main__":

    Scanner().run()