# convexpi-replications

**Open, verified reference replications of canonical quantitative-finance strategies.**

Every strategy here is *recomputed from underlying building blocks* — reconstructing the Fama-French
factors from their component portfolios, forming long-short books by ranking assets — never read off
a finished factor. Each is scored **honestly out of sample** by splitting its returns at the paper's
publication year (the McLean & Pontiff test), and ships a **committed reference result** that CI
re-checks on every change, so the library stays trustworthy as it grows.

It pairs with the [ConvexPi](https://convexpi.ai) research library: each replication links to the
paper's wiki, and each paper's wiki links back to its runnable replication.

## Install
```bash
pip install git+https://github.com/convexpi/replications.git
```

## Use
```python
from replications import all_replications

reps = all_replications()
r = reps["jegadeesh_titman_momentum"]
print(r.report_card())     # IS vs OOS Sharpe, decay, turnover, net-of-cost, verdict
series = r.build()         # the recomputed daily return series
```

Run any replication on **live data** in Colab — see the badge in each `notebooks/<name>.ipynb`, or
the *Open in Colab* link on the [playground](https://convexpi.ai/playground) and on each paper's wiki.

## What's inside
See [`BENCHMARK.md`](BENCHMARK.md) for the live leaderboard. Each row is recomputed and OOS-scored:

| Strategy | Paper | Recomputed from |
|---|---|---|
| Value (HML) | Fama & French 1993 | 6 size × book-to-market portfolios |
| Size (SMB) | Banz 1981 | 6 size × book-to-market portfolios |
| Momentum (WML) | Jegadeesh & Titman 1993 | 6 size × prior-return portfolios |
| Profitability (RMW) | Novy-Marx 2013 | 6 size × operating-profitability portfolios |
| Industry momentum | Moskowitz & Grinblatt 1999 | 12 industry portfolios (ranked & rebalanced) |
| Trend (TSMOM) | Moskowitz, Ooi & Pedersen 2012 | market excess return |
| Investment (CMA) | Cooper, Gulen & Schill 2008 | 6 size × investment portfolios |
| Short-term reversal | Jegadeesh 1990 | 6 size × prior-1-month portfolios |
| Long-term reversal | De Bondt & Thaler 1985 | 6 size × prior 13–60-month portfolios |

The leaderboard is re-run quarterly by CI and snapshotted to `history/leaderboard.jsonl`, so the
verdicts form a living time series. Some replications carry an honest `caveat` (e.g. short-term
reversal's gross Sharpe is unachievable net of costs).

## Cross-validation against OSAP
Each replication is cross-checked against the [Open Source Asset Pricing](https://www.openassetpricing.com)
(Chen & Zimmermann) gold-standard portfolio returns: `tools/validate_against_osap.py` correlates our
free, Ken-French-built *factor* series with OSAP's *single-name decile* long-short returns. Because
these are different constructions of the same anomaly, a genuine match lands around **0.4–0.8**, not
~1.0 — so the leaderboard reports a `clear` / `partial` / `weak` fidelity tier alongside the
correlation. This is an external check on top of the CI reference test; the result is committed to
`osap_validation.json` so CI and the website never touch OSAP at runtime. OSAP data © Chen &
Zimmermann, used under their open license.

## Contributing
We want replications of as many canonical strategies as possible — and **multiple takes** on the
same paper are welcome (replication is a choice; the disagreement is the lesson). Fork, add a module,
and open a PR; CI checks the contract and that your reference result reproduces. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Data & licensing
Code only, never bundled data. Replications declare free, redistributable sources (Ken-French via
`pandas-datareader`, prices via `yfinance`) that are fetched on demand and cached. MIT licensed.
