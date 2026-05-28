import numpy as np
import pandas as pd

def sharpe_ratio(returns: pd.Series, periods_per_year: int = 252) -> float:
    returns = returns.dropna()
    if returns.std() == 0:
        return np.nan
    return float(np.sqrt(periods_per_year) * returns.mean() / returns.std())

def max_drawdown(returns: pd.Series) -> float:
    cumulative = (1 + returns.fillna(0)).cumprod()
    running_max = cumulative.cummax()
    drawdown = cumulative / running_max - 1
    return float(drawdown.min())

def win_rate(returns: pd.Series) -> float:
    returns = returns.dropna()
    if len(returns) == 0:
        return np.nan
    return float((returns > 0).mean())

def cumulative_return(returns: pd.Series) -> float:
    return float((1 + returns.fillna(0)).prod() - 1)

def annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    return float(returns.std() * np.sqrt(periods_per_year))
