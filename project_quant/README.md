## 1. problem statement
This project constructs a cross-sectional multi-factor stock selection 
model on S&P 500 constituents (2010–2024). Factor definitions follow 
the Fama-French academic tradition; data handling and validation 
methodology follow López de Prado (2018).

The system ingests daily OHLCV and fundamental data, generates monthly 
factor exposures, and outputs a ranked long-short signal evaluated on 
out-of-sample IC and risk-adjusted returns. The core challenge is 
preventing the common pitfalls of financial ML: look-ahead bias, low 
signal-to-noise ratio, and non-stationary factor returns.
## 2. Data

| Field              | Value                              | Notes                                                                 |
|--------------------|------------------------------------|-----------------------------------------------------------------------|
| Universe           | S&P 500 current constituents       | Survivorship bias acknowledged; point-in-time constituents deferred to v2 |
| Time range         | 2010-01-01 to 2024-12-31           | In-sample: 2010–2022; Out-of-sample: 2023–2024                       |
| Rebalance frequency| Monthly (end-of-month)             | Factors computed from daily data; signals applied monthly            |
| Price source       | yfinance (adjusted close)          |                                                                       |
| Fundamental source | yfinance quarterly financials      | 45-day publication lag applied to all fundamental data (known limitation) |
| Factor benchmark   | Ken French Data Library            | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html |

## 3. Success Criteria

Quantitative Targets (out-of-sample, 2023-2024):
- Monthly IC of ML composite signal: ≥ 0.03 (rank IC)
- Annualized Sharpe of equal-weight long-short decile portfolio: ≥ 1.0
  (net of 10 bps one-way transaction cost)
- Maximum drawdown: ≤ 20%
- Annual turnover: reported but not constrained (expected range: 200%–400%)

Validation Targets:
- FF3 factor reproduction: correlation ≥ 0.95 with Ken French series
  (monthly), ≥ 0.90 (daily)
- Backtest engine: passes look-ahead sanity test
  (perfect-foresight signal → Sharpe > 5)

## 4. Scope -- In and Out

In Scope:
- Cross-sectional ranking signal at monthly frequency
- 10-15 technical factors + 3 FF style factors
- LightGBM as primary model; linear baseline (OLS) for comparison
- Equal-weight long-short decile backtest
- Time-series cross-validation with embargo (purged k-fold)

Out of Scope (v1):
- Intraday or higher-frequency signals
- Chinese A-share market
- Deep learning models (LSTM, Transformer)
- Risk model (Barra-style factor risk decomposition)
- Portfolio optimization (mean-variance, risk parity)
- Live trading or paper trading infrastructure
- Alternative data (sentiment, satellite, etc.)

## 5. Technical Stack

Language: Python 3.11
Data: pandas, numpy, yfinance, pyarrow (parquet storage)
Modeling: scikit-learn, lightgbm
Validation: Custom purged k-fold (López de Prado, AFML Ch. 7)
Backtest: Custom vectorized engine (pandas-native)
Visualization: matplotlib
Environment: conda + pip, reproducibility via environment.yml
Versioning: git + GitHub

## 6. Risks & Go/No-Go Gates:
Mid-project Gate (2026-07-15) — 4 checks:

1. FF3 reproduction: monthly correlation ≥ 0.90 vs Ken French series
2. Backtest engine: passes look-ahead sanity test
3. Single-factor IC: at least 3 factors with monthly |IC| > 0.02
4. Cumulative effort: ≥ 50 hours logged

Decision rules:
- All 4 pass → Proceed to LightGBM v1 (target: 2026-08-15 full delivery)
- #3 fails only → Proceed with narrow factor set (no padding)
- #1 or #2 fails → Halt modeling; allocate 2 weeks to data/engine repair
- #4 fails → Honest reassessment of timeline and scope

Known Risks:
- R1: yfinance fundamental data quality may be insufficient
  → Mitigation: identify backup source by W2
- R2: Survivorship bias inflates backtest returns
  → Mitigation: acknowledged limitation; v2 may use point-in-time constituents
- R3: ML overfitting due to limited data
  → Mitigation: purged CV from W5; no test set access until final evaluation
- R4: Fundamental data timing: yfinance indexes financial data 
  by period-end date, not actual release date.
  → Mitigation: Apply uniform 45-day lag to all fundamental 
  inputs in v1; flagged as known limitation in Section 2.