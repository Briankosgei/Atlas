import csv
import os


class PerformanceAnalyzer:

    FILE = "journal/trades.csv"

    def summary(self):

        if not os.path.exists(self.FILE):
            return None

        with open(self.FILE, newline="") as f:
            reader = csv.DictReader(f)
            trades = list(reader)

        if len(trades) == 0:
            return None

        total = len(trades)

        buy = 0
        sell = 0

        aligned_buy = 0
        aligned_sell = 0

        confidence_total = 0

        for trade in trades:

            confidence_total += float(trade["confidence"])

            if trade["signal"] == "BUY":
                buy += 1

                if trade["alignment"] == "BUY":
                    aligned_buy += 1

            elif trade["signal"] == "SELL":
                sell += 1

                if trade["alignment"] == "SELL":
                    aligned_sell += 1

        avg_confidence = round(confidence_total / total, 2)

        return {

            "total_trades": total,

            "buy_trades": buy,

            "sell_trades": sell,

            "aligned_buy": aligned_buy,

            "aligned_sell": aligned_sell,

            "average_confidence": avg_confidence,
        }