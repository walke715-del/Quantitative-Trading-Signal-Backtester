import pandas as pd
import numpy as np

from metrics import sharpe_ratio, max_drawdown, win_rate, cumulative_return, annualized_volatility

SIGNAL_COLS = ["momentum", "mean_reversion", "moving_average", "volatility_breakout"]

def compute_strategy_returns(df: pd.DataFrame, transaction_cost_bps: float = 5.0) -> pd.DataFrame:
    """
    Convert signals into equal-weight daily strategy returns.
    Transaction costs are applied when position changes.
    """
    data = df.copy()
    cost = transaction_cost_bps / 10000

    output = []
    for signal in SIGNAL_COLS:
        temp = data[["date", "symbol", "return", signal]].copy()
        temp["position"] = temp[signal].fillna(0)
        temp["position_change"] = temp.groupby("symbol")["position"].diff().abs().fillna(0)
        temp["strategy_return_stock"] = temp["position"] * temp["return"] - temp["position_change"] * cost

        daily = temp.groupby("date")["strategy_return_stock"].mean().rename(signal).to_frame()
        output.append(daily)

    strategy_returns = pd.concat(output, axis=1).sort_index()
    return strategy_returns

def summarize_performance(strategy_returns: pd.DataFrame, benchmark_returns: pd.Series | None = None) -> pd.DataFrame:
    rows = []

    for col in strategy_returns.columns:
        ret = strategy_returns[col].dropna()
        row = {
            "strategy": col,
            "cumulative_return": cumulative_return(ret),
            "sharpe_ratio": sharpe_ratio(ret),
            "max_drawdown": max_drawdown(ret),
            "win_rate": win_rate(ret),
            "annualized_volatility": annualized_volatility(ret)
        }

        if benchmark_returns is not None:
            aligned = pd.concat([ret, benchmark_returns], axis=1).dropna()
            if not aligned.empty:
                row["excess_return"] = cumulative_return(aligned.iloc[:, 0]) - cumulative_return(aligned.iloc[:, 1])
            else:
                row["excess_return"] = np.nan

        rows.append(row)

    return pd.DataFrame(rows)

def summarize_by_regime(strategy_returns: pd.DataFrame, regimes: pd.DataFrame) -> pd.DataFrame:
    merged = strategy_returns.reset_index().merge(regimes, on="date", how="left")
    rows = []

    for regime_type in ["trend_regime", "vol_regime", "combined_regime"]:
        for regime_value, group in merged.groupby(regime_type):
            if regime_value == "unknown":
                continue
            for signal in SIGNAL_COLS:
                ret = group[signal].dropna()
                if len(ret) < 30:
                    continue
                rows.append({
                    "regime_type": regime_type,
                    "regime": regime_value,
                    "strategy": signal,
                    "cumulative_return": cumulative_return(ret),
                    "sharpe_ratio": sharpe_ratio(ret),
                    "max_drawdown": max_drawdown(ret),
                    "win_rate": win_rate(ret),
                    "annualized_volatility": annualized_volatility(ret)
                })

    return pd.DataFrame(rows)
