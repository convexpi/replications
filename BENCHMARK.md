# Replication leaderboard — out-of-sample

Canonical strategies, each **recomputed from underlying building blocks** and scored out of
sample by splitting at the paper's publication year (the McLean & Pontiff test). The *OSAP*
column reports the correlation of our reconstruction with the Open Source Asset Pricing
single-name long-short returns (a different construction, so 0.4-0.8 is a genuine match).
Regenerate with `python tools/gen_benchmark.py`. Verdicts are honest, not editorial.

| Strategy | Paper | Pub. | IS Sharpe | OOS Sharpe | Decay | Verdict | OSAP |
|---|---|---:|---:|---:|---:|---|---|
| Investment (CMA) | Asset Growth and the Cross-Section of Stock Returns | 2008 | 0.71 | 0.03 | 95% | dormant | weak (+0.38) |
| Long-term reversal | Does the Stock Market Overreact? | 1985 | 0.20 | 0.07 | 66% | dormant | partial (+0.67) |
| Value (HML) | Common Risk Factors in the Returns on Stocks and Bonds | 1993 | 0.49 | 0.21 | 58% | decayed | partial (+0.55) |
| Size (SMB) | The Relationship Between Return and Market Value of Common Stocks | 1981 | 0.20 | -0.01 | 108% | dormant | partial (+0.63) |
| Short-term reversal [^1] | Evidence of Predictable Behavior of Security Returns | 1990 | 5.12 | 1.29 | 75% | decayed | partial (+0.44) |
| Momentum (WML) | Returns to Buying Winners and Selling Losers | 1993 | 0.63 | 0.38 | 40% | alive | clear (+0.74) |
| Industry momentum | Do Industries Explain Momentum? | 1999 | 0.47 | 0.31 | 35% | alive | partial (+0.45) |
| Trend (time-series momentum) [^2] | Time Series Momentum | 2012 | 0.34 | 0.42 | improved | alive | — |
| Profitability (RMW) | The Other Side of Value | 2013 | 0.58 | 0.24 | 59% | decayed | partial (+0.46) |

[^1]: **Short-term reversal** — Extremely high turnover and heavily driven by microstructure (bid-ask bounce). The gross Sharpe shown is not achievable net of realistic transaction costs.
[^2]: **Trend (time-series momentum)** — Uses Yahoo Finance continuous front-month futures, which begin ~2000 (vs the paper's 1985) and carry roll artifacts — a faithful but data-limited proxy for the paper's 58-instrument universe.

*Open replications maintained at [https://github.com/convexpi/replications](https://github.com/convexpi/replications) — fork, improve, and PR.*
