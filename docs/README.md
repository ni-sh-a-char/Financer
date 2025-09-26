# Financer  
**A Common Platform for Finance Analysis**  

> Financer is a modular, extensible Python library (and optional CLI/REST service) that provides a unified interface for financial data ingestion, transformation, modeling, and reporting. It supports equities, fixed‑income, crypto, and alternative data sources, and ships with a suite of ready‑to‑use analytics (time‑series, risk metrics, portfolio optimisation, etc.).  

---  

## Table of Contents  

| Section | Description |
|---------|-------------|
| **[Installation](#installation)** | How to get Financer up and running (pip, conda, Docker, dev mode). |
| **[Quick Start / Usage](#quick-start-usage)** | Minimal example that shows the typical workflow. |
| **[API Documentation](#api-documentation)** | Overview of the public Python API (core modules, classes, functions). |
| **[Examples](#examples)** | Ready‑to‑run notebooks & scripts for common finance tasks. |
| **[Configuration](#configuration)** | Environment variables, config files, and credential handling. |
| **[Testing & CI](#testing--ci)** | Running the test suite and linting. |
| **[Contributing](#contributing)** | How to submit bugs, feature requests, or pull requests. |
| **[License](#license)** | Open‑source license information. |

---  

## Installation  

Financer can be installed in several ways depending on your workflow.

### 1. Install via **pip** (recommended for most users)

```bash
# Create a clean virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the latest stable release from PyPI
pip install financer
```

> **Note**: Financer requires Python 3.9 – 3.12.  

### 2. Install via **conda** (if you prefer the conda ecosystem)

```bash
conda create -n financer python=3.11
conda activate financer
pip install financer   # conda does not host the package yet
```

### 3. Install the **latest development version** from GitHub

```bash
# Clone the repo
git clone https://github.com/your-org/Financer.git
cd Financer

# Install in editable mode with all optional dependencies
pip install -e ".[dev,all]"
```

The `dev` extra pulls in testing and linting tools, while `all` adds optional data‑provider SDKs (e.g., `yfinance`, `alpha_vantage`, `ccxt`, `pandas-datareader`).

### 4. Run with **Docker** (ideal for reproducible environments)

```bash
docker pull your-org/financer:latest
docker run -it --rm \
    -v $(pwd)/data:/app/data \
    -e FINANCER_CONFIG=/app/config.yaml \
    your-org/financer:latest
```

> The Docker image bundles the library, a Jupyter server, and a tiny API gateway (see the *Dockerfile* in the repo for details).

### 5. System‑level dependencies  

| Dependency | Reason | Install (Ubuntu) |
|------------|--------|------------------|
| `libpq-dev` | PostgreSQL driver for `psycopg2-binary` | `sudo apt-get install libpq-dev` |
| `gfortran` | Required by `numpy`/`scipy` compiled wheels | `sudo apt-get install gfortran` |
| `ffmpeg` | For handling audio‑based alternative data | `sudo apt-get install ffmpeg` |

If you encounter compilation errors, make sure the above packages are present or use the pre‑built wheels from PyPI.

---  

## Quick Start / Usage  

Below is a minimal end‑to‑end example that demonstrates the typical Financer workflow:

```python
# -------------------------------------------------
# 1️⃣  Import the high‑level API
# -------------------------------------------------
from financer import DataLoader, Analyzer, Portfolio, Report

# -------------------------------------------------
# 2️⃣  Load market data (Yahoo! Finance, CSV, or DB)
# -------------------------------------------------
loader = DataLoader(
    source="yahoo",               # other options: "csv", "postgres", "alpha_vantage"
    symbols=["AAPL", "MSFT", "GOOG"],
    start="2022-01-01",
    end="2023-12-31",
)

prices = loader.fetch_prices()
# `prices` is a pandas.DataFrame with a MultiIndex (date, symbol)

# -------------------------------------------------
# 3️⃣  Run analytics (returns, volatility, Sharpe)
# -------------------------------------------------
analysis = Analyzer(prices)
returns = analysis.compute_returns()
vol = analysis.compute_annualized_volatility()
sharpe = analysis.compute_sharpe_ratio(risk_free_rate=0.02)

print("Annualised Sharpe:", sharpe)

# -------------------------------------------------
# 4️⃣  Build a simple mean‑variance portfolio
# -------------------------------------------------
port = Portfolio(returns)
weights = port.optimize_mean_variance(target_return=0.12)
print("Optimised weights:", weights)

# -------------------------------------------------
# 5️⃣  Generate a PDF report
# -------------------------------------------------
report = Report(
    title="Financer Quick‑Start Report",
    author="Your Name",
    data=dict(
        returns=returns,
        volatility=vol,
        sharpe=sharpe,
        weights=weights,
    ),
)
report.to_pdf("quick_start_report.pdf")
```

### Running the example as a script  

```bash
python examples/quick_start.py
```

### Running the example as a Jupyter notebook  

```bash
jupyter notebook examples/quick_start.ipynb
```

---  

## API Documentation  

Financer follows a **modular, layered architecture**. The public API is split into four top‑level namespaces:

| Namespace | Purpose | Most important classes / functions |
|-----------|---------|--------------------------------------|
| `financer.loader` | Data ingestion from many sources | `DataLoader`, `CSVLoader`, `PostgresLoader`, `AlphaVantageLoader` |
| `financer.analysis` | Time‑series and statistical analytics | `Analyzer`, `ReturnsCalculator`, `RiskMetrics`, `FactorModel` |
| `financer.portfolio` | Portfolio construction & optimisation | `Portfolio`, `EfficientFrontier`, `RiskParity`, `BlackLitterman` |
| `financer.report` | Reporting & visualisation utilities | `Report`, `ChartFactory`, `PDFExporter`, `HTMLExporter` |

Below is a concise reference for the most frequently used objects. Full docstrings are available in the code and via `help()`.

### 1. `financer.loader.DataLoader`

```python
class DataLoader:
    """
    Unified interface to fetch price/quote data.

    Parameters
    ----------
    source : str
        One of {"yahoo", "csv", "postgres", "alpha_vantage", "ccxt"}.
    symbols : List[str] | str
        Ticker symbols (or a single ticker).
    start : str | datetime
        Start date (inclusive).
    end : str | datetime
        End date (inclusive).
    **kwargs
        Provider‑specific arguments (e.g., `api_key`, `db_uri`, `path`).

    Methods
    -------
    fetch_prices() -> pd.DataFrame
        Returns a DataFrame indexed by date with columns for each symbol.
    fetch_fundamentals() -> pd.DataFrame
        Optional: pull balance‑sheet / income‑statement data.
    """
```

**Typical usage**

```python
loader = DataLoader(source="csv", path="data/market.csv")
prices = loader.fetch_prices()
```

### 2. `financer.analysis.Analyzer`

```python
class Analyzer:
    """
    High‑level analytics wrapper around a price DataFrame.

    Parameters
    ----------
    price_df : pd.DataFrame
        Must be indexed by date with symbols as columns.

    Methods
    -------
    compute_returns(method="log") -> pd.DataFrame
    compute_annualized_volatility(window=252) -> pd.Series
    compute_sharpe_ratio(risk_free_rate=0.0) -> pd.Series
    compute_drawdowns() -> pd.DataFrame
    factor_exposure(factors: pd.DataFrame) -> pd.DataFrame
    """
```

### 3. `financer.portfolio.Portfolio`

```python
class Portfolio:
    """
    Portfolio optimisation utilities.

    Parameters
    ----------
    returns : pd.DataFrame
        Periodic returns (e.g., daily) with symbols as columns.

    Methods
    -------
    optimize_mean_variance(target_return=None, bounds=(0,1)) -> pd.Series
    optimise_risk_parity() -> pd.Series
    optimise_black_litterman(views, tau=0.05) -> pd.Series
    backtest(weights, rebalance='monthly') -> BacktestResult
    """
```

### 4. `financer.report.Report`

```python
class Report:
    """
    Assemble a multi‑page PDF