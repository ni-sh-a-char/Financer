# Financer  
**A Common Platform for Finance Analysis**  

Welcome to **Financer** – a unified, extensible toolkit for financial data ingestion, transformation, analysis, and reporting. Whether you’re building a back‑testing engine, a risk‑management dashboard, or a simple portfolio‑tracker, Financer provides a clean, Pythonic API and a set of ready‑to‑use components that let you focus on the finance logic instead of plumbing.

---  

## Table of Contents
1. [Installation](#installation)  
2. [Quick Start / Usage](#quick-start)  
3. [Core Concepts](#core-concepts)  
4. [API Documentation](#api-documentation)  
5. [Examples](#examples)  
6. [Configuration & Environment Variables](#configuration)  
7. [Testing](#testing)  
8. [Contributing](#contributing)  
9. [License](#license)  

---  

## Installation <a name="installation"></a>

Financer is published on PyPI and can be installed with `pip`. It also supports optional extras for data‑source integrations, GPU‑accelerated calculations, and Jupyter notebooks.

```bash
# Core package (required)
pip install financer

# Optional extras (choose what you need)
pip install financer[all]          # everything (data sources, notebooks, GPU)
pip install financer[data]         # data source adapters (Yahoo, Alpha Vantage, Bloomberg)
pip install financer[notebook]     # Jupyter/IPython extensions
pip install financer[gpu]          # CuPy‑based vectorised calculations
```

### System Requirements
| Requirement | Minimum Version |
|-------------|-----------------|
| Python      | 3.9+            |
| NumPy       | 1.23+           |
| pandas      | 2.0+            |
| scikit‑learn| 1.2+            |
| optional: CuPy (GPU) | 12.0+ (CUDA) |

> **Tip:** For a reproducible environment, we recommend using a virtual environment or Conda:

```bash
# Using venv
python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install financer[all]

# Using Conda
conda create -n financer python=3.11
conda activate financer
pip install financer[all]
```

### Installing from source

If you want the latest development version:

```bash
git clone https://github.com/your-org/Financer.git
cd Financer
pip install -e .[all]   # editable install with all optional deps
```

---  

## Quick Start / Usage <a name="quick-start"></a>

Below is a minimal end‑to‑end example that:

1. Pulls historical price data for a list of tickers.  
2. Calculates daily returns and a simple moving‑average (SMA) indicator.  
3. Runs a basic mean‑variance portfolio optimisation.  
4. Plots the results.

```python
# demo.py
import pandas as pd
import matplotlib.pyplot as plt
from financer import DataLoader, Indicators, PortfolioOptimizer, Plotter

# ----------------------------------------------------------------------
# 1️⃣ Load data
# ----------------------------------------------------------------------
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
loader = DataLoader(source="yahoo")          # built‑in Yahoo Finance adapter
prices = loader.get_price_history(
    tickers=tickers,
    start="2022-01-01",
    end="2024-12-31",
    freq="B"                                   # business‑day frequency
)

# ----------------------------------------------------------------------
# 2️⃣ Compute indicators
# ----------------------------------------------------------------------
returns = Indicators.daily_returns(prices)
sma_20 = Indicators.sma(prices, window=20)

# ----------------------------------------------------------------------
# 3️⃣ Optimise a portfolio (Mean‑Variance)
# ----------------------------------------------------------------------
optimizer = PortfolioOptimizer(method="mean_variance")
weights = optimizer.optimize(returns)

# ----------------------------------------------------------------------
# 4️⃣ Visualise
# ----------------------------------------------------------------------
Plotter.plot_price_series(prices, sma_20, title="Price + 20‑day SMA")
Plotter.plot_weights(weights, tickers, title="Optimised Portfolio Weights")
plt.show()
```

Run the script:

```bash
python demo.py
```

You should see two plots: a price chart with a 20‑day SMA overlay, and a bar chart of the optimal weights.

---  

## Core Concepts <a name="core-concepts"></a>

| Concept | Description | Typical Classes |
|---------|-------------|-----------------|
| **DataLoader** | Abstracts data‑source handling (Yahoo, Alpha Vantage, CSV, DB, etc.) | `DataLoader`, `CSVLoader`, `SQLLoader` |
| **Indicators** | Vectorised financial indicators (returns, moving averages, volatility, etc.) | `Indicators` (static methods) |
| **PortfolioOptimizer** | Implements classic and modern optimisation algorithms (Mean‑Variance, Black‑Litterman, Risk Parity, CVaR) | `PortfolioOptimizer`, `RiskParityOptimizer` |
| **Backtester** | Event‑driven back‑testing engine with transaction cost modelling | `Backtester`, `StrategyBase` |
| **Plotter** | Helper functions for quick visualisation (price series, heatmaps, performance) | `Plotter` |
| **Config** | Centralised configuration (API keys, cache directories, logging) | `Config` |

All core objects are **stateless** (except for caching) and can be safely reused across threads.

---  

## API Documentation <a name="api-documentation"></a>

> The full API reference is generated automatically with **Sphinx** and hosted on GitHub Pages at `https://your-org.github.io/Financer/`. Below is a concise overview of the most important modules.

### `financer.loader`

```python
class DataLoader:
    """Base class for data ingestion."""
    def __init__(self, source: str = "yahoo", **kwargs):
        ...

    def get_price_history(
        self,
        tickers: List[str],
        start: str | pd.Timestamp,
        end: str | pd.Timestamp,
        freq: str = "B",
        adjust: bool = True,
    ) -> pd.DataFrame:
        """Return a DataFrame indexed by date with columns = tickers."""
        ...

    def get_fundamentals(self, tickers: List[str]) -> pd.DataFrame:
        """Optional: fetch balance‑sheet / income‑statement data."""
        ...
```

**Supported sources** (via optional extras):
- `"yahoo"` – Yahoo Finance (default)
- `"alpha_vantage"` – Alpha Vantage (requires `FINANCER_AV_API_KEY`)
- `"bloomberg"` – Bloomberg (requires Bloomberg API libraries)
- `"csv"` – local CSV files (use `CSVLoader` subclass)

---

### `financer.indicators`

All methods are **vectorised** and return `pandas.DataFrame` objects aligned with the input.

| Method | Signature | Description |
|--------|-----------|-------------|
| `daily_returns` | `daily_returns(prices: pd.DataFrame) -> pd.DataFrame` | Simple arithmetic returns. |
| `log_returns` | `log_returns(prices: pd.DataFrame) -> pd.DataFrame` | Logarithmic returns. |
| `sma` | `sma(series: pd.DataFrame, window: int) -> pd.DataFrame` | Simple moving average. |
| `ema` | `ema(series: pd.DataFrame, span: int) -> pd.DataFrame` | Exponential moving average. |
| `volatility` | `volatility(returns: pd.DataFrame, window: int, method: str = "std") -> pd.DataFrame` | Rolling volatility (std or EWMA). |
| `drawdown` | `drawdown(prices: pd.DataFrame) -> pd.DataFrame` | Peak‑to‑trough drawdown series. |
| `beta` | `beta(returns: pd.DataFrame, benchmark: pd.Series) -> pd.Series` | Asset beta vs benchmark. |

---

### `financer.optimisation`

```python
class PortfolioOptimizer:
    """Mean‑Variance, Black‑Litterman, Risk‑Parity, etc."""
    def __init__(self,
                 method: str = "mean_variance",
                 target_return: float | None = None,
                 risk_aversion: float = 1.0,
                 bounds: Tuple[float, float] = (0.0, 1.0),
                 **kwargs):
        ...

    def optimize(self,
                 returns: pd.DataFrame,
                 cov: pd.DataFrame | None = None) -> pd.Series:
        """Return optimal weights indexed by asset name."""
        ...

    # Convenience static methods
    @staticmethod
    def efficient_frontier(returns: pd.DataFrame,
                           points: int = 50) -> pd.DataFrame:
        """Generate the efficient frontier (return, volatility)."""
        ...
```

Supported `method` values:

| Method | Description |
|--------|-------------|
| `"mean_variance"` | Classic Markowitz optimisation (quadratic programming). |
| `"black_litterman"` | Incorporates analyst views via the Black‑Litterman model. |
| `"risk_parity"` | Equal‑risk contribution optimisation. |
