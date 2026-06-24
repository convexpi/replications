# Replication candidates

A running index of canonical strategies we *could* add to the library, with the **primary academic
paper** each traces to and whether it fits our free-data stack. This is a roadmap, not a backlog
commitment.

## Sourcing & licensing

We mine public strategy catalogs for *which* strategies are worth replicating and *which papers* they
trace to — then write **clean-room** implementations against our own free data
(`kenfrench:*`, `yfinance:*`) under the `Replication` contract. We do **not** copy third-party code.

- **OpenSourceAP / CrossSection (OSAP)** — used for the anomaly universe and as a validation target
  (`tools/validate_against_osap.py`). Cite the primary paper, not OSAP.
- **QuantConnect strategy library** — useful as a *candidate index*: ~83 articles, each tracing
  (often via Quantpedia) to a primary paper. Their code is LEAN-framework / platform-coupled and is
  their IP — we take only the *idea + primary citation*, never the code.

## Status legend

`done` shipped in `catalog/` · `next` clean fit, queued · `needs-data` requires data we don't have
yet (e.g. point-in-time fundamentals) · `technique` a method demo, not a single-paper strategy

| Strategy | Primary paper | DOI | Status | Data |
|---|---|---|---|---|
| Cross-sectional momentum | Jegadeesh & Titman (1993) | 10.1111/j.1540-6261.1993.tb04702.x | `done` | kenfrench |
| Short-term reversal | Jegadeesh (1990); Lehmann (1990) | 10.1111/j.1540-6261.1990.tb05110.x | `done` | kenfrench |
| Long-term reversal | De Bondt & Thaler (1985) | 10.1111/j.1540-6261.1985.tb05004.x | `done` | kenfrench |
| Industry momentum | Moskowitz & Grinblatt (1999) | 10.1111/0022-1082.00146 | `done` | kenfrench |
| Time-series (trend) momentum | Moskowitz, Ooi & Pedersen (2012) | 10.1016/j.jfineco.2011.11.003 | `done` | yfinance futures |
| Value (HML) | Fama & French (1993) | 10.1016/0304-405X(93)90023-5 | `done` | kenfrench |
| Size (SMB) | Fama & French (1993) | 10.1016/0304-405X(93)90023-5 | `done` | kenfrench |
| Profitability | Novy-Marx (2013) | 10.1016/j.jfineco.2013.01.003 | `done` | kenfrench |
| Investment / asset growth | Cooper, Gulen & Schill (2008) | 10.1111/j.1540-6261.2008.01370.x | `done` | kenfrench |
| **MAX effect (lottery stocks)** | **Bali, Cakici & Whitelaw (2011)** | **10.1016/j.jfineco.2010.08.014** | **`next` → shipping** | yfinance |
| Betting against beta | Frazzini & Pedersen (2014) | 10.1016/j.jfineco.2013.10.005 | `next` | yfinance (per-name beta) |
| Idiosyncratic volatility | Ang, Hodrick, Xing & Zhang (2006) | 10.1111/j.1540-6261.2006.00836.x | `next` | yfinance |
| Pairs trading (distance) | Gatev, Goetzmann & Rouwenhorst (2006) | 10.1093/rfs/hhj020 | `next` | yfinance |
| Asset-class momentum | Asness, Moskowitz & Pedersen (2013) | 10.1111/jofi.12021 | `next` | yfinance ETFs |
| Accruals | Sloan (1996) | (JSTOR 248290) | `needs-data` | fundamentals |
| Piotroski F-score | Piotroski (2000) | 10.2307/2672906 | `needs-data` | fundamentals |
| Mohanram G-score | Mohanram (2005) | 10.1007/s11142-005-1535-3 | `needs-data` | fundamentals |
| ML return forecasting (NB/GBM/CNN) | — | — | `technique` | — |

## Notes

- **Priority** is the `next` rows that run on data we already have: MAX, idiosyncratic vol, asset-class
  momentum, and distance pairs all work on `yfinance` single names/ETFs (a faithful-but-survivorship-
  limited proxy, flagged in each replication's `caveat`), exactly like the trend replication.
- **Fundamentals-dependent** strategies (accruals, F/G-score) are blocked until we add a free
  point-in-time fundamentals loader to `data.py`; sketched, not started.
- The QuantConnect article that prompted this index — "The MAX Effect with VIX-based Leverage
  Scaling" — cites **Bali, Cakici & Whitelaw (2011)**; we replicate that primary paper's plain MAX
  effect (their VIX leverage overlay is a platform-specific extension we don't copy).
