from pathlib import Path
import numpy as np
import pandas as pd

def generate_synthetic_prices(n_days: int = 3000, tickers: list[str] | None = None, seed: int = 7) -> pd.DataFrame:
    """Generate synthetic daily stock prices for testing."""
    rng = np.random.default_rng(seed)
    if tickers is None:
        tickers = ["AAA", "BBB", "CCC", "DDD", "EEE"]

    dates = pd.bdate_range("2012-01-01", periods=n_days)
    rows = []

    for ticker in tickers:
        drift = rng.normal(0.00025, 0.00008)
        vol = rng.uniform(0.012, 0.025)
        returns = rng.normal(drift, vol, size=n_days)
        close = 100 * np.exp(np.cumsum(returns))
        for date, price in zip(dates, close):
            rows.append({"date": date, "symbol": ticker, "close": price})

    return pd.DataFrame(rows)

def load_sp500_data(path: str | Path) -> pd.DataFrame:
    """
    Load Kaggle S&P 500 Stocks dataset.
    Expected columns are usually Date, Symbol, Adj Close/Close.
    """
    path = Path(path)
    if not path.exists():
        print(f"Kaggle file not found at {path}. Using synthetic dataset for pipeline test.")
        return generate_synthetic_prices()

    df = pd.read_csv(path)

    # Normalize common Kaggle column names.
    rename_map = {}
    for col in df.columns:
        low = col.lower().replace(" ", "_")
        if low in ["date"]:
            rename_map[col] = "date"
        elif low in ["symbol", "ticker"]:
            rename_map[col] = "symbol"
        elif low in ["adj_close", "adjusted_close", "close"]:
            rename_map[col] = "close"

    df = df.rename(columns=rename_map)

    required = {"date", "symbol", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns {missing}. Available columns: {df.columns.tolist()}")

    df["date"] = pd.to_datetime(df["date"])
    df = df[["date", "symbol", "close"]].dropna()
    return df.sort_values(["symbol", "date"])
