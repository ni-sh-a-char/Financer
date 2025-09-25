# Financer  
**A Common Platform for Finance Analysis**  

> **Financer** is a modular, extensible Python library that provides a unified interface for financial data acquisition, cleaning, transformation, and analysis. It supports time‑series data, portfolio analytics, risk metrics, and a growing collection of quantitative models. The library can be used as a pure Python package, from the command‑line, or embedded in Jupyter notebooks and larger data‑science pipelines.

---  

## Table of Contents
1. [Installation](#installation)  
2. [Quick Start / Usage](#quick-start--usage)  
   - 2.1 [Command‑Line Interface (CLI)](#cli)  
   - 2.2 [Python API](#python-api)  
3. [API Documentation](#api-documentation)  
   - 3.1 [Core Modules](#core-modules)  
   - 3.2 [Data Sources](#data-sources)  
   - 3.3 [Analytics & Models](#analytics--models)  
   - 3.4 [Utilities](#utilities)  
4. [Examples](#examples)  
   - 4.1 [Fetching & Cleaning Data](#example-1-fetching--cleaning-data)  
   - 4.2 [Portfolio Construction & Back‑testing](#example-2-portfolio-construction--back‑testing)  
   - 4.3 [Risk Metrics & Reporting](#example-3-risk-metrics--reporting)  
   - 4.4 [Custom Indicator Development](#example-4-custom-indicator-development)  
5. [Contributing](#contributing)  
6. [License](#license)  

---  

## Installation <a name="installation"></a>

Financer is distributed on **PyPI** and can be installed with `pip`. It also supports optional extras for heavy‑weight data providers and GPU‑accelerated models.

```bash
# Core installation (minimum dependencies)
pip install financer

# Install with all optional dependencies (recommended for full feature set)
pip install "financer[all]"

# Install only specific optional groups
pip install "financer[db]"      # SQLAlchemy + PostgreSQL/MySQL drivers
pip install "financer[ml]"      # scikit‑learn, xgboost, lightgbm, pytorch
pip install "financer[plot]"    # matplotlib, seaborn, plotly
```

### Development / From Source

```bash
# Clone the repository
git clone https://github.com/yourorg/Financer.git
cd Financer

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

**Supported Python versions:** 3.9 – 3.12  

**System requirements:**  
- `numpy >= 1.23`  
- `pandas >= 2.0`  
- For optional GPU models: CUDA 11.8+ and `torch >= 2.0`  

---  

## Quick Start / Usage <a name="quick-start--usage"></a>

Financer can be used in three primary ways:

1. **Command‑Line Interface (CLI)** – quick one‑liners for data download, back‑testing, or report generation.  
2. **Python API** – full programmatic control inside scripts, notebooks, or larger applications.  
3. **Jupyter Widgets** – interactive dashboards (requires the `plot` extra).

### 2.1 Command‑Line Interface (CLI) <a name="cli"></a>

After installation, the `financer` command becomes available:

| Command | Description |
|---------|-------------|
| `financer fetch <ticker> --start 2020-01-01 --end 2024-12-31` | Download historical OHLCV data from the default source (Yahoo Finance). |
| `financer backtest config.yaml` | Run a back‑test using a YAML configuration file (see `examples/backtest_config.yaml`). |
| `financer report portfolio.csv --output report.pdf` | Generate a PDF risk‑report for a portfolio CSV. |
| `financer serve --port 8080` | Launch the optional web UI (requires `financer[web]`). |

**Help:** `financer --help` or `financer <subcommand> --help`.

### 2.2 Python API <a name="python-api"></a>

Below is a minimal “Hello‑World” example that fetches data, computes a simple moving average, and plots the result.

```python
>>> from financer import DataFetcher, Indicator, Plotter

# 1️⃣ Fetch data
df = DataFetcher.yahoo(
    ticker="AAPL",
    start="2022-01-01",
    end="2024-12-31"
)

# 2️⃣ Compute a 30‑day SMA
df["SMA_30"] = Indicator.sma(df["Close"], window=30)

# 3️⃣ Plot
Plotter.line(
    df[["Close", "SMA_30"]],
    title="AAPL Close vs 30‑Day SMA",
    ylabel="Price (USD)"
)
```

All high‑level objects are importable from the top‑level `financer` package for convenience, but you can also import sub‑modules directly (e.g., `from financer.sources import YahooFinance`).

---  

## API Documentation <a name="api-documentation"></a>

> The full API reference is also generated automatically by **Sphinx** and hosted at `https://financer.readthedocs.io`. The sections below give a concise overview of the most important classes and functions.

### 3.1 Core Modules <a name="core-modules"></a>

| Module | Primary Classes / Functions | Description |
|--------|-----------------------------|-------------|
| `financer.core.pipeline` | `Pipeline`, `Step` | Build reusable data‑processing pipelines (fetch → clean → transform → model). |
| `financer.core.config` | `Config`, `load_yaml` | Centralised configuration handling (YAML/JSON/TOML). |
| `financer.core.logging` | `get_logger` | Structured logging with JSON output for CI/CD pipelines. |

### 3.2 Data Sources <a name="data-sources"></a>

| Source | Class / Function | Notes |
|--------|------------------|-------|
| **Yahoo Finance** | `DataFetcher.yahoo(ticker, start, end, **kwargs)` | Free, no API key required. |
| **Alpha Vantage** | `DataFetcher.alpha_vantage(ticker, api_key, **kwargs)` | Requires free API key; supports intraday data. |
| **Polygon.io** | `DataFetcher.polygon(ticker, api_key, **kwargs)` | Premium data, optional `financer[db]` extra for bulk storage. |
| **SQL / CSV** | `DataLoader.from_sql(query, engine)`, `DataLoader.from_csv(path)` | Load pre‑existing datasets. |
| **Custom Provider** | Subclass `BaseProvider` | Implement `fetch(self, **kwargs)` to plug in any data source. |

All fetchers return a **pandas.DataFrame** with a standard column set: `["Open", "High", "Low", "Close", "Adj Close", "Volume"]` plus a `DateTimeIndex`.

### 3.3 Analytics & Models <a name="analytics--models"></a>

| Category | Class / Function | Typical Use‑Case |
|----------|------------------|------------------|
| **Indicators** | `Indicator.sma(series, window)`, `Indicator.ema(series, window)`, `Indicator.rsi(series, period=14)` | Technical analysis. |
| **Portfolio** | `Portfolio.from_positions(df)`, `Portfolio.optimize(method="mean_variance")` | Build & rebalance portfolios. |
| **Back‑testing** | `Backtester(pipeline, start, end, cash=1e6)` | Simulate strategies on historical data. |
| **Risk** | `RiskMetrics.annualized_volatility(series)`, `RiskMetrics.sharpe_ratio(ret, risk_free=0.02)` | Compute risk‑adjusted performance. |
| **Machine Learning** | `MLModel.fit(X, y)`, `MLModel.predict(X)` (wrappers for scikit‑learn, XGBoost, PyTorch) | Predictive finance models. |
| **Monte‑Carlo** | `MonteCarloSimulator(portfolio, n_paths=10_000, horizon=252)` | Scenario analysis. |

All analytics classes accept **numpy** or **pandas** objects and return results in the same type for seamless chaining.

### 3.4 Utilities <a name="utilities"></a>

| Utility | Function | Description |
|---------|----------|-------------|
| `financer.utils.time` | `to_utc(dt)`, `business_days(start, end)` | Date‑time helpers. |
| `financer.utils.validation` | `validate_ticker(ticker)`, `ensure_monotonic(series)` | Input validation. |
| `financer.utils