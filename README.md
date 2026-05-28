# Quantitative Trading Signal Backtesting Project

## Purpose
Determine whether trading signals perform differently across bull, bear, high-volatility, and low-volatility market regimes.

## Dataset
Use the S&P 500 Stocks dataset from Kaggle:

https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks

Expected input file after download:

```text
project_2_signal_backtester/data/sp500_stocks.csv
```

If the Kaggle file is not present, the project generates synthetic equity-price data so the full pipeline can still be tested.

## What the Code Does
1. Loads historical stock prices.
2. Constructs daily returns.
3. Builds momentum, mean-reversion, moving-average, and volatility-breakout signals.
4. Applies transaction costs.
5. Creates bull, bear, high-volatility, and low-volatility regimes using benchmark trend and volatility.
6. Evaluates performance by Sharpe ratio, max drawdown, win rate, cumulative return, excess return, and volatility.
7. Saves summary tables and charts.

## Resume Bullets
- Built a backtesting engine evaluating momentum, mean-reversion, moving-average, and volatility-breakout signals across historical equity data.
- Compared signal performance across bull, bear, high-volatility, and low-volatility regimes using Sharpe ratio, drawdown, excess return, and win-rate metrics.
