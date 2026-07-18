import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, PROJECT_ROOT)

from datafeed.yfinance_feed import YahooFinanceFeed
from planner.trade_planner import TradePlanner

feed = YahooFinanceFeed()

candles = feed.get_candles(
    "XAUUSD",
    interval="1h",
    limit=500,
)

entry = candles[-1]["close"]

planner = TradePlanner()

trade = planner.plan_trade(
    direction="BUY",
    entry=entry,
    candles=candles,
)

print()

print(trade)