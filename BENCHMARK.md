# Replication leaderboard — out-of-sample

Canonical strategies, each **recomputed from underlying building blocks** and scored out of
sample by splitting at the paper's publication year (the McLean & Pontiff test). Regenerate
with `python tools/gen_benchmark.py`. Verdicts are honest, not editorial.

| Strategy | Paper | Pub. | IS Sharpe | OOS Sharpe | Net OOS | Decay | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| Investment (CMA) | Asset Growth and the Cross-Section of Stock Returns | 2008 | 0.71 | 0.03 | — | 95% | dormant |
| Long-term reversal | Does the Stock Market Overreact? | 1985 | 0.20 | 0.07 | — | 66% | dormant |
| Value (HML) | Common Risk Factors in the Returns on Stocks and Bonds | 1993 | 0.49 | 0.21 | — | 58% | decayed |
| Size (SMB) | The Relationship Between Return and Market Value of Common Stocks | 1981 | 0.20 | -0.01 | — | 108% | dormant |
| Short-term reversal [^1] | Evidence of Predictable Behavior of Security Returns | 1990 | 5.12 | 1.29 | — | 75% | decayed |
| Momentum (WML) | Returns to Buying Winners and Selling Losers | 1993 | 0.63 | 0.38 | — | 40% | alive |
| Industry momentum | Do Industries Explain Momentum? | 1999 | 0.47 | 0.31 | 0.25 | 35% | alive |
| Trend (time-series momentum) | Time Series Momentum | 2012 | 0.17 | 0.48 | — | improved | alive |
| Profitability (RMW) | The Other Side of Value | 2013 | 0.58 | 0.24 | — | 59% | decayed |

[^1]: **Short-term reversal** — Extremely high turnover and heavily driven by microstructure (bid-ask bounce). The gross Sharpe shown is not achievable net of realistic transaction costs.

*Open replications maintained at [https://github.com/convexpi/replications](https://github.com/convexpi/replications) — fork, improve, and PR.*
