from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from data import load_sp500_data
from signals import build_signals
from regimes import build_benchmark, classify_regimes
from backtest import compute_strategy_returns, summarize_performance, summarize_by_regime

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sp500_stocks.csv"
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def main():
    df = load_sp500_data(DATA_PATH)
    df = build_signals(df)

    benchmark = build_benchmark(df)
    regimes = classify_regimes(benchmark)

    strategy_returns = compute_strategy_returns(df, transaction_cost_bps=5.0)
    benchmark_returns = benchmark.set_index("date")["benchmark_return"]

    summary = summarize_performance(strategy_returns, benchmark_returns=benchmark_returns)
    regime_summary = summarize_by_regime(strategy_returns, regimes)

    summary.to_csv(OUT_DIR / "strategy_performance_summary.csv", index=False)
    regime_summary.to_csv(OUT_DIR / "regime_performance_summary.csv", index=False)
    strategy_returns.to_csv(OUT_DIR / "daily_strategy_returns.csv")

    print("Overall performance:")
    print(summary.sort_values("sharpe_ratio", ascending=False))

    print("\nRegime performance:")
    print(regime_summary.sort_values("sharpe_ratio", ascending=False).head(20))

    cumulative = (1 + strategy_returns.fillna(0)).cumprod()
    plt.figure(figsize=(9, 5))
    for col in cumulative.columns:
        plt.plot(cumulative.index, cumulative[col], label=col)
    plt.title("Strategy Cumulative Returns")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "strategy_cumulative_returns.png", dpi=150)

    regime_pivot = regime_summary.pivot_table(
        index="strategy",
        columns="regime",
        values="sharpe_ratio",
        aggfunc="mean"
    )
    regime_pivot.to_csv(OUT_DIR / "regime_sharpe_pivot.csv")

if __name__ == "__main__":
    main()
