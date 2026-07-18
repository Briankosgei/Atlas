import sys
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, PROJECT_ROOT)

from analyzer.atr import ATRCalculator
from datafeed.yfinance_feed import YahooFinanceFeed

feed = YahooFinanceFeed()

df = feed.get_candles(
    "XAUUSD",
    interval="1h",
    limit=500,
)

print(type(df))
print(df[:3])

atr = ATRCalculator()

value = atr.calculate(df)

print("\nATR")
print(value)