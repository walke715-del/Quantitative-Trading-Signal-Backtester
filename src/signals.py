import numpy as np
import pandas as pd

def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["return"] = df.groupby("symbol")["close"].pct_change()
    return df

def momentum_signal(df: pd.DataFrame, lookback: int = 126) -> pd.Series:
    past_return = df.groupby("symbol")["close"].pct_change(lookback)
    return (past_return > 0).astype(int)

def mean_reversion_signal(df: pd.DataFrame, lookback: int = 5) -> pd.Series:
    short_return = df.groupby("symbol")["close"].pct_change(lookback)
    return (short_return < -0.03).astype(int)

def moving_average_signal(df: pd.DataFrame, short: int = 50, long: int = 200) -> pd.Series:
    short_ma = df.groupby("symbol")["close"].transform(lambda x: x.rolling(short).mean())
    long_ma = df.groupby("symbol")["close"].transform(lambda x: x.rolling(long).mean())
    return (short_ma > long_ma).astype(int)

def volatility_breakout_signal(df: pd.DataFrame, lookback: int = 20) -> pd.Series:
    rolling_high = df.groupby("symbol")["close"].transform(lambda x: x.rolling(lookback).max())
    prev_high = rolling_high.groupby(df["symbol"]).shift(1)
    return (df["close"] > prev_high).astype(int)

def build_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = add_returns(df)
    df["momentum"] = momentum_signal(df)
    df["mean_reversion"] = mean_reversion_signal(df)
    df["moving_average"] = moving_average_signal(df)
    df["volatility_breakout"] = volatility_breakout_signal(df)

    # Shift signals by one day to avoid look-ahead bias.
    signal_cols = ["momentum", "mean_reversion", "moving_average", "volatility_breakout"]
    for col in signal_cols:
        df[col] = df.groupby("symbol")[col].shift(1)

    return df.dropna(subset=["return"] + signal_cols)
