# Replication leaderboard — out-of-sample

Canonical strategies, each **recomputed from underlying building blocks** and scored out of
sample by splitting at the paper's publication year (the McLean & Pontiff test). The *OSAP*
column reports the correlation of our reconstruction with the Open Source Asset Pricing
single-name long-short returns (a different construction, so 0.4-0.8 is a genuine match).
Regenerate with `python tools/gen_benchmark.py`. Verdicts are honest, not editorial.

| Strategy | Paper | Pub. | IS Sharpe | OOS Sharpe | Decay | Verdict | OSAP |
|---|---|---:|---:|---:|---:|---|---|
| Idiosyncratic volatility puzzle [^1] | The Cross-Section of Volatility and Expected Returns | 2006 | 0.16 | 0.01 | 91% | dormant | clear (+0.93) |
| MAX effect (lottery stocks) [^2] | Maxing Out | 2011 | -0.11 | -0.29 | — | dormant | — |
| Investment (CMA) | Asset Growth and the Cross-Section of Stock Returns | 2008 | 0.71 | 0.03 | 95% | dormant | weak (+0.38) |
| Long-term reversal | Does the Stock Market Overreact? | 1985 | 0.20 | 0.07 | 66% | dormant | partial (+0.67) |
| Value (HML) | Common Risk Factors in the Returns on Stocks and Bonds | 1993 | 0.49 | 0.21 | 58% | decayed | partial (+0.55) |
| Size (SMB) | The Relationship Between Return and Market Value of Common Stocks | 1981 | 0.20 | -0.01 | 108% | dormant | partial (+0.63) |
| Betting against beta [^3] | Betting Against Beta | 2014 | 0.28 | 0.04 | 87% | dormant | partial (-0.41) |
| Short-term reversal [^4] | Evidence of Predictable Behavior of Security Returns | 1990 | 5.12 | 1.29 | 75% | decayed | partial (+0.44) |
| Momentum (WML) | Returns to Buying Winners and Selling Losers | 1993 | 0.63 | 0.38 | 40% | alive | clear (+0.74) |
| Industry momentum | Do Industries Explain Momentum? | 1999 | 0.47 | 0.31 | 35% | alive | partial (+0.45) |
| Trend (time-series momentum) [^5] | Time Series Momentum | 2012 | 0.34 | 0.42 | improved | alive | — |
| Profitability (RMW) | The Other Side of Value | 2013 | 0.58 | 0.24 | 59% | decayed | partial (+0.46) |
| Net share issuance [^6] | Share Issuance and Cross-Sectional Returns | 2008 | 0.45 | 0.03 | 94% | decayed | partial (+0.53) |
| Accruals anomaly [^7] | Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings? | 1996 | 0.63 | 0.23 | 63% | decayed | weak (+0.30) |

[^1]: **Idiosyncratic volatility puzzle** — Univariate residual-variance sort (value-weighted quintiles). The puzzle is stronger with equal weighting and among small, illiquid names; this is the value-weighted spread, gross of transaction costs.
[^2]: **MAX effect (lottery stocks)** — Uses a fixed basket of surviving Yahoo Finance large caps (history since ~2000), not the paper's full CRSP universe, so it is survivorship-biased and understates the effect, which is strongest in small, illiquid names. A faithful-but-limited proxy; gross of transaction costs.
[^3]: **Betting against beta** — Beta-rescaling uses a simple rolling 60-month market beta of each leg, not the paper's exact (1-year vol x 5-year correlation) estimator, and rescales the two quintile legs rather than every security. Gross of the (high) financing and turnover costs that leverage entails.
[^4]: **Short-term reversal** — Extremely high turnover and heavily driven by microstructure (bid-ask bounce). The gross Sharpe shown is not achievable net of realistic transaction costs.
[^5]: **Trend (time-series momentum)** — Uses Yahoo Finance continuous front-month futures, which begin ~2000 (vs the paper's 1985) and carry roll artifacts — a faithful but data-limited proxy for the paper's 58-instrument universe.
[^6]: **Net share issuance** — Univariate net-issuance sort (value-weighted quintiles). The effect is stronger with equal weighting and among small caps; gross of transaction costs.
[^7]: **Accruals anomaly** — Univariate accruals sort (value-weighted quintiles), available from 1963. The anomaly is concentrated in small, hard-to-arbitrage names and has weakened since publication; gross of transaction costs.

*Open replications maintained at [https://github.com/convexpi/replications](https://github.com/convexpi/replications) — fork, improve, and PR.*
