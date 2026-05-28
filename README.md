# Quantitative Trading Signal Backtesting Project

## Overview

This project evaluates whether systematic trading signals generate persistent risk-adjusted returns across multiple market environments. A modular backtesting framework was developed to test signal robustness, evaluate strategy performance, and compare results across different market regimes.

The primary focus is not identifying a single profitable strategy, but understanding when and why particular signals perform well.

---

## Research Question

Do commonly used quantitative trading signals produce consistent excess returns, and how does their effectiveness change across different market environments?

---

## Dataset

**S&P 500 Historical Equity Data**

Source:
https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks

Historical equity prices are used to generate trading signals and evaluate performance through time.

---

## Project Architecture

1. Data Collection
2. Signal Construction
3. Backtesting Engine
4. Transaction Cost Modeling
5. Market Regime Classification
6. Performance Attribution
7. Strategy Comparison

---

## Trading Signals Evaluated

### Momentum

Identifies securities with strong recent performance and assumes trends may persist.

### Mean Reversion

Identifies securities that have experienced short-term price declines and may revert toward historical averages.

### Moving Average Crossover

Generates signals from interactions between short-term and long-term trend measures.

### Volatility Breakout

Attempts to capture significant price movements following periods of consolidation.

---

## Backtesting Framework

The project implements:

- Signal generation
- Position management
- Transaction cost assumptions
- Daily return calculation
- Benchmark comparison
- Performance aggregation

The framework is designed to minimize look-ahead bias and support repeatable quantitative research.

---

## Market Regime Analysis

Signals are evaluated across multiple market environments.

### Trend Regimes

- Bull Markets
- Bear Markets

### Volatility Regimes

- High Volatility Periods
- Low Volatility Periods

This analysis helps determine whether strategy performance is regime-dependent.

---

## Performance Metrics

The following metrics are calculated for each strategy:

### Return Metrics

- Cumulative Return
- Excess Return
- Average Daily Return

### Risk Metrics

- Maximum Drawdown
- Annualized Volatility

### Risk-Adjusted Metrics

- Sharpe Ratio

### Trading Metrics

- Win Rate
- Trade Frequency

---

## Outputs

### Strategy Summary

`outputs/strategy_performance_summary.csv`

Contains overall performance statistics for each signal.

### Regime Analysis

`outputs/regime_performance_summary.csv`

Compares strategy behavior across market regimes.

### Daily Returns

`outputs/daily_strategy_returns.csv`

Stores daily strategy return series.

### Visualization

`outputs/strategy_cumulative_returns.png`

Displays cumulative growth of each strategy through time.

---

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib

---

## Skills Demonstrated

- Quantitative Research
- Backtesting
- Time-Series Analysis
- Trading Signal Development
- Risk Analysis
- Performance Attribution
- Market Regime Analysis
- Portfolio Analytics

---

## Potential Extensions

- Multi-factor signals
- Portfolio optimization
- Machine learning signal integration
- Intraday data analysis
- Risk budgeting
- Alternative asset classes
