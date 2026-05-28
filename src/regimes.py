import pandas as pd
import numpy as np

def build_benchmark(df: pd.DataFrame) -> pd.DataFrame:
    """Equal-weight all available stocks to create benchmark return series."""
    bench = df.groupby("date")["return"].mean().rename("benchmark_return").to_frame()
    bench["benchmark_index"] = (1 + bench["benchmark_return"].fillna(0)).cumprod()
    bench["ma_200"] = bench["benchmark_index"].rolling(200).mean()
    bench["rolling_vol_60"] = bench["benchmark_return"].rolling(60).std() * np.sqrt(252)
    return bench.reset_index()

def classify_regimes(benchmark: pd.DataFrame) -> pd.DataFrame:
    """Classify bull/bear and high/low volatility regimes."""
    b = benchmark.copy()
    median_vol = b["rolling_vol_60"].median()

    b["trend_regime"] = "unknown"
    b.loc[b["benchmark_index"] >= b["ma_200"], "trend_regime"] = "bull"
    b.loc[b["benchmark_index"] < b["ma_200"], "trend_regime"] = "bear"

    b["vol_regime"] = "unknown"
    b.loc[b["rolling_vol_60"] >= median_vol, "vol_regime"] = "high_vol"
    b.loc[b["rolling_vol_60"] < median_vol, "vol_regime"] = "low_vol"

    b["combined_regime"] = b["trend_regime"] + "_" + b["vol_regime"]
    return b[["date", "benchmark_return", "trend_regime", "vol_regime", "combined_regime"]]
