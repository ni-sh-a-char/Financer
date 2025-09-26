# Financer  
**A Common Platform for Finance Analysis**  

---  

## Table of Contents
1. [Overview](#overview)  
2. [Installation](#installation)  
3. [Quick Start / Usage](#quick-start--usage)  
4. [API Documentation](#api-documentation)  
5. [Examples](#examples)  
6. [Contributing](#contributing)  
7. [License](#license)  

---  

## Overview  

Financer is a **modular, extensible, and open‑source** Python library that provides a unified interface for common finance‑related tasks such as:

* Market data ingestion (CSV, JSON, APIs, WebSocket streams)  
* Time‑series manipulation & resampling  
* Portfolio construction, back‑testing, and performance attribution  
* Risk metrics (VaR, CVaR, drawdown, Sharpe, Sortino, etc.)  
* Financial statement analysis & ratio calculation  
* Machine‑learning‑ready feature engineering  

The library follows a **plug‑and‑play** architecture: core objects (`Asset`, `Portfolio`, `MarketData`) are thin wrappers around pandas/NumPy, while optional extensions (e.g., `financer.ml`, `financer.algo`) can be installed separately.

> **Why Financer?**  
> * **Consistent API** – All data sources return the same `MarketData` object.  
> * **Zero‑dependency core** – Only pandas, numpy, and requests are required.  
> * **Extensible** – Add your own data adapters, risk models, or execution engines without touching the core.  

---  

## Installation  

Financer is published on PyPI and can be installed with `pip`.  

### 1. Core package (required)

```bash
pip install financer
```

### 2. Optional extras  

| Extra | Description | Install command |
|-------|-------------|-----------------|
| `ml` | Scikit‑learn, XGBoost, LightGBM wrappers for predictive finance models | `pip install "financer[ml]"` |
| `plot` | Interactive visualisations (Plotly, Bokeh) | `pip install "financer[plot]"` |
| `api` | Built‑in connectors for Alpha Vantage, Yahoo Finance, Polygon.io | `pip install "financer[api]"` |
| `all` | Everything above | `pip install "financer[all]"` |

> **Tip:** Use a virtual environment (e.g., `venv` or `conda`) to keep dependencies isolated.

### 3. From source (development)

```bash
git clone https://github.com/your-org/Financer.git
cd Financer
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .[all]       # editable install with all optional deps
```

---  

## Quick Start / Usage  

Below is a minimal end‑to‑end workflow that demonstrates how to:

1. Load market data (CSV or API)  
2. Build a portfolio  
3. Run a back‑test  
4. Compute risk metrics  

```python
# -------------------------------------------------
# 1️⃣  Imports
# -------------------------------------------------
from financer import MarketData, Portfolio, BacktestEngine
from financer.api import YahooFinance  # optional, requires the `api` extra

# -------------------------------------------------
# 2️⃣  Load data
# -------------------------------------------------
# Option A – CSV file
prices = MarketData.from_csv(
    "data/SP500_daily.csv",
    date_col="date",
    price_cols=["Adj Close"]
)

# Option B – Pull from Yahoo Finance (requires internet)
prices = YahooFinance().download(
    ticker="SPY",
    start="2015-01-01",
    end="2024-12-31",
    interval="1d"
)

# -------------------------------------------------
# 3️⃣  Build a simple equal‑weight portfolio
# -------------------------------------------------
portfolio = Portfolio(name="EqualWeight")
portfolio.add_asset(ticker="SPY", weight=1.0)   # 100% SPY

# -------------------------------------------------
# 4️⃣  Run a back‑test
# -------------------------------------------------
engine = BacktestEngine(
    market_data=prices,
    portfolio=portfolio,
    cash=100_000,               # initial capital
    commission=0.001            # 0.1% per trade
)

results = engine.run()
print(results.summary())
```

### Common CLI entry point  

Financer ships with a small command‑line interface for quick exploration:

```bash
# Show help
financer --help

# Download 5‑year daily data for AAPL and store as CSV
financer download --ticker AAPL --start 2019-01-01 --end 2024-12-31 --out aapl.csv

# Run a back‑test using a config file
financer backtest --config examples/backtest_config.yaml
```

---  

## API Documentation  

> **Note:** The documentation below reflects the latest stable release (v2.3.0). For the most up‑to‑date reference, see the generated docs at `docs/` or the online site: https://financer.readthedocs.io  

### Core Classes  

| Class | Description | Key Methods |
|-------|-------------|-------------|
| **`MarketData`** | Container for time‑series price/volume data. Internally a `pandas.DataFrame` with a `DateTimeIndex`. | `from_csv()`, `from_json()`, `from_api()`, `resample()`, `align()`, `as_returns()` |
| **`Asset`** | Light‑weight representation of a tradable instrument (ticker, currency, asset‑type). | `price_series()`, `metadata()`, `set_price_series()` |
| **`Portfolio`** | Holds a collection of `Asset` objects and their target weights. Supports rebalancing rules. | `add_asset()`, `remove_asset()`, `rebalance()`, `current_weights()`, `value_at(date)` |
| **`BacktestEngine`** | Orchestrates a historical simulation using a `Portfolio` and `MarketData`. | `run()`, `set_commission()`, `set_slippage()`, `add_event_handler()` |
| **`RiskModel`** (abstract) | Base class for risk calculations. Sub‑classes implement specific metrics. | `calculate()`, `report()` |
| **`VaR`**, **`CVaR`**, **`Drawdown`**, **`SharpeRatio`**, **`SortinoRatio`** | Concrete risk models derived from `RiskModel`. | `calculate(portfolio, window=252)` |
| **`FinancerAPI`** (abstract) | Base for all data‑source adapters (Alpha Vantage, Yahoo, Polygon, etc.). | `download(ticker, **kwargs)` |

### Selected Method Signatures  

#### `MarketData.from_csv(path, date_col='date', price_cols=None, **kwargs) → MarketData`  

* **Parameters**  
  * `path` – Path to CSV file.  
  * `date_col` – Column name containing dates (must be parseable).  
  * `price_cols` – List of columns to keep as price series; defaults to all numeric columns.  
  * `**kwargs` – Additional arguments passed to `pandas.read_csv`.  

* **Returns** a `MarketData` instance with a clean `DateTimeIndex`.  

#### `Portfolio.add_asset(ticker: str, weight: float, **kwargs) → None`  

* Adds a new asset to the portfolio.  
* `weight` is a **target** weight (not yet normalized).  
* Optional kwargs (`currency`, `price_series`) allow overriding defaults.  

#### `BacktestEngine.run() → BacktestResult`  

* Executes the simulation from the earliest to the latest date in the supplied `MarketData`.  
* Returns a `BacktestResult` object that contains:  
  * `equity_curve` (DataFrame)  
  * `trade_log` (DataFrame)  
  * `metrics` (dict) – e.g., total return, CAGR, max drawdown, Sharpe.  

#### `RiskModel.calculate(portfolio: Portfolio, market_data: MarketData, **kwargs) → float`  

* Abstract; each subclass implements its own logic.  

### Helper Functions  

| Function | Description |
|----------|-------------|
| `financer.utils.to_returns(series, method='log')` | Convert price series to simple or log returns. |
| `financer.utils.align_series(*series, fill_method='ffill')` | Align multiple time‑series on a common index. |
| `financer.plot.equity_curve(df, title='Equity Curve')` | Plot equity curve using Plotly (requires `plot` extra). |

---  

## Examples  

Below are a few ready‑to‑run notebooks / scripts that illustrate typical workflows. All examples live under the `examples/` directory of the repository.

### 1️⃣  **Basic Portfolio Back‑Test**  

File: `examples/basic_backtest.py`

```python
#!/usr/bin/env python
"""
Simple equal‑weight back‑test of SPY vs. VTI over the last 10 years.
"""

from financer import MarketData, Portfolio, BacktestEngine
from financer.api import YahooFinance
from financer.risk import SharpeRatio, MaxDrawdown

# -------------------------------------------------
# Load data
