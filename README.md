# AtlasTrader

Institutional-style multi-timeframe market scanner and trade-planning dashboard built in Python and Streamlit.

## Features

* Market structure detection (HH, HL, LH, LL)
* Trend engine
* Break of Structure (BOS)
* Change of Character (CHoCH)
* Liquidity sweep detection
* Momentum analysis
* Multi-timeframe alignment (1H, 4H, 1D, 1W)
* Confidence scoring
* Signal grading
* ATR-based trade planning
* Risk management and position sizing
* Streamlit dashboard

## Project Structure

```text
analyzer/        # Core market analysis
planner/         # Trade planning
risk/            # Position sizing and risk management
signals/         # Signal engine
timeframe/       # Multi-timeframe analysis
dashboard/       # Streamlit UI
journal/         # Trade logging
tests/           # Unit tests
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/Atlastrader.git
cd Atlastrader

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the Scanner

```bash
python scanner.py
```

## Run the Dashboard

```bash
streamlit run dashboard/app.py
```

Then open:

```text
http://localhost:8501
```

## Supported Symbols

* XAUUSD
* BTCUSD
* EURUSD
* USDJPY
* USDCAD
* AUDUSD

## Signal Logic

A signal is generated from:

* Trend
* Higher timeframe alignment
* BOS
* CHoCH
* Liquidity
* Momentum
* Volatility filter

## Confidence Score

| Score | Label     |
| ----- | --------- |
| 85+   | Excellent |
| 70-84 | Good      |
| 55-69 | Moderate  |
| <55   | Poor      |

## Dashboard

The dashboard displays:

* Scanner overview
* Trend
* BOS / CHoCH
* Liquidity sweeps
* Momentum
* HTF alignment
* Confidence breakdown
* Trade plan
* Risk metrics

## Disclaimer

This project is for educational and research purposes only. It is **not financial advice**. Always validate signals independently before trading real capital.

## Author

Brian Kipkosgei Kiplagat