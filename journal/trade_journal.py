import csv
import os
from datetime import datetime


class TradeJournal:

    FILE = "journal/trades.csv"

    def __init__(self):

        if not os.path.exists("journal"):
            os.makedirs("journal")

        if not os.path.exists(self.FILE):

            with open(self.FILE, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "time",
                    "symbol",
                    "signal",
                    "entry",
                    "stop_loss",
                    "take_profit",
                    "confidence",
                    "alignment",
                    "status"
                ])

    def save(self, report):

        trade = report["trade"]

        if not trade["valid"]:
            return

        with open(self.FILE, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                report["symbol"],
                trade["direction"],
                trade["entry"],
                trade["stop_loss"],
                trade["take_profit"],
                report["confidence"],
                report["alignment"]["direction"],
                "OPEN"
            ])