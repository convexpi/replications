# Replication leaderboard — out-of-sample

Canonical strategies, each **recomputed from underlying building blocks** and scored out of
sample by splitting at the paper's publication year (the McLean & Pontiff test). The *OSAP*
column reports the correlation of our reconstruction with the Open Source Asset Pricing
single-name long-short returns (a different construction, so 0.4-0.8 is a genuine match).
Regenerate with `python tools/gen_benchmark.py`. Verdicts are honest, not editorial.

| Strategy | Paper | Pub. | IS Sharpe | OOS Sharpe | Decay | Verdict | OSAP |
|---|---|---:|---:|---:|---:|---|---|
| Amihud illiquidity [^1] | Illiquidity and Stock Returns | 2002 | 1.55 | 0.65 | 58% | decayed | — |
| Idiosyncratic volatility puzzle [^2] | The Cross-Section of Volatility and Expected Returns | 2006 | 0.16 | -0.04 | 124% | dormant | clear (0.93) |
| Asset-class momentum [^3] | Value and Momentum Everywhere | 2013 | 0.28 | 0.63 | improved | alive | — |
| MAX effect (lottery stocks) [^4] | Maxing Out | 2011 | -0.11 | -0.30 | — | dormant | — |
| Earnings yield (P/E effect) [^5] | Investment Performance of Common Stocks in Relation to Their Price-Earnings Ratios | 1977 | 0.74 | 0.25 | 66% | dormant | partial (0.68) |
| Investment (CMA) | Asset Growth and the Cross-Section of Stock Returns | 2008 | 0.71 | 0.05 | 93% | dormant | weak (0.38) |
| Long-term reversal | Does the Stock Market Overreact? | 1985 | 0.20 | 0.07 | 66% | dormant | partial (0.67) |
| Value (HML) | Common Risk Factors in the Returns on Stocks and Bonds | 1993 | 0.49 | 0.20 | 58% | decayed | partial (0.55) |
| Operating profitability (RMW) [^6] | A five-factor asset pricing model | 2015 | 0.24 | 0.21 | 12% | weak | — |
| Size (SMB) | The Relationship Between Return and Market Value of Common Stocks | 1981 | 0.20 | -0.01 | 108% | dormant | partial (0.63) |
| Betting against beta [^7] | Betting Against Beta | 2014 | 0.29 | 0.08 | 74% | dormant | partial (0.41) |
| Pairs trading (distance) [^8] | Pairs Trading | 2006 | -0.05 | 0.10 | — | dormant | — |
| 52-week high momentum [^9] | The 52-Week High and Momentum Investing | 2004 | -0.40 | -0.27 | — | dormant | — |
| Short-term reversal [^10] | Evidence of Predictable Behavior of Security Returns | 1990 | 5.11 | 1.25 | 76% | decayed | partial (0.44) |
| Momentum (WML) | Returns to Buying Winners and Selling Losers | 1993 | 0.62 | 0.35 | 44% | alive | clear (0.74) |
| Cash-flow yield (value) [^11] | Contrarian Investment, Extrapolation, and Risk | 1994 | 0.58 | -0.05 | 109% | dormant | weak (0.34) |
| Dividend yield (D/P effect) [^12] | The effect of personal taxes and dividends on capital asset prices | 1979 | 0.13 | -0.01 | 106% | dormant | — |
| Industry momentum | Do Industries Explain Momentum? | 1999 | 0.47 | 0.33 | 31% | alive | partial (0.45) |
| Trend (time-series momentum) [^13] | Time Series Momentum | 2012 | 0.09 | 0.46 | improved | alive | — |
| Profitability (RMW) | The Other Side of Value | 2013 | 0.59 | 0.18 | 70% | decayed | partial (0.46) |
| Net share issuance [^14] | Share Issuance and Cross-Sectional Returns | 2008 | 0.45 | 0.05 | 89% | decayed | partial (0.53) |
| Accruals anomaly [^15] | Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings? | 1996 | 0.63 | 0.23 | 64% | decayed | weak (0.30) |

[^1]: **Amihud illiquidity** — Even in this fixed basket of large, liquid Yahoo survivors the premium shows up (the relatively less-liquid large caps earn it) and then decays post-publication — the McLean-Pontiff pattern. Two honest catches: it is survivorship-biased and **gross of costs**, and the irony of this strategy is that its long leg holds the least-liquid names, which are the most expensive to trade — the very impact the premium compensates for — so net returns are materially lower than gross. The full effect is larger in small/micro caps (the paper's CRSP universe), beyond free data.
[^2]: **Idiosyncratic volatility puzzle** — Univariate residual-variance sort (value-weighted quintiles). The puzzle is stronger with equal weighting and among small, illiquid names; this is the value-weighted spread, gross of transaction costs.
[^3]: **Asset-class momentum** — Cross-sectional 12-1 momentum across a fixed ETF basket (histories begin mid-2000s, so the sample is short), a practical proxy for the paper's broad cross-asset universe; gross of transaction costs.
[^4]: **MAX effect (lottery stocks)** — Uses a fixed basket of surviving Yahoo Finance large caps (history since ~2000), not the paper's full CRSP universe, so it is survivorship-biased and understates the effect, which is strongest in small, illiquid names. A faithful-but-limited proxy; gross of transaction costs.
[^5]: **Earnings yield (P/E effect)** — Univariate earnings-yield sort (value-weighted quintiles); firms with negative earnings are excluded from the sort. Overlaps with the book-to-market value factor; gross of transaction costs.
[^6]: **Operating profitability (RMW)** — Univariate operating-profitability sort (value-weighted quintiles). Related to Novy-Marx gross profitability but a distinct accounting measure; overlaps the quality complex. Gross of transaction costs.
[^7]: **Betting against beta** — Beta-rescaling uses a simple rolling 60-month market beta of each leg, not the paper's exact (1-year vol x 5-year correlation) estimator, and rescales the two quintile legs rather than every security. Gross of the (high) financing and turnover costs that leverage entails.
[^8]: **Pairs trading (distance)** — Distance method on a fixed large-cap Yahoo basket (history since ~2000), not the paper's full CRSP universe, so it is survivorship-biased and understates an effect that lives in smaller names; equal-weight long/short per pair, gross of the high transaction costs pairs trading incurs.
[^9]: **52-week high momentum** — Comes out negative on this fixed large-cap Yahoo basket (survivors since ~2000): cross-sectional momentum *reverses* here — plain 12-1 momentum is also negative on this basket while 1-month reversal is positive — so a momentum-family effect like the 52-week high does not replicate on a narrow large-cap universe. The effect lives in the broad CRSP cross-section (especially smaller names); see the Jegadeesh-Titman momentum replication (Ken French) for momentum on a full universe. An honest data-access limitation, not a failed method. Survivorship-biased, gross of transaction costs; nearness uses split/dividend-adjusted prices.
[^10]: **Short-term reversal** — Extremely high turnover and heavily driven by microstructure (bid-ask bounce). The gross Sharpe shown is not achievable net of realistic transaction costs.
[^11]: **Cash-flow yield (value)** — Univariate cash-flow-to-price sort (value-weighted quintiles); firms with negative cash flow are excluded. Highly correlated with book-to-market and earnings-yield value; gross of transaction costs.
[^12]: **Dividend yield (D/P effect)** — Univariate dividend-yield sort (value-weighted quintiles); non-payers are excluded, so this is the premium among payers. Tax-driven and value-adjacent; the premium has largely faded in modern data. Gross of transaction costs.
[^13]: **Trend (time-series momentum)** — Uses Yahoo Finance continuous front-month futures, which begin ~2000 (vs the paper's 1985) and carry roll artifacts — a faithful but data-limited proxy for the paper's 58-instrument universe.
[^14]: **Net share issuance** — Univariate net-issuance sort (value-weighted quintiles). The effect is stronger with equal weighting and among small caps; gross of transaction costs.
[^15]: **Accruals anomaly** — Univariate accruals sort (value-weighted quintiles), available from 1963. The anomaly is concentrated in small, hard-to-arbitrage names and has weakened since publication; gross of transaction costs.

*Open replications maintained at [https://github.com/convexpi/replications](https://github.com/convexpi/replications) — fork, improve, and PR.*
