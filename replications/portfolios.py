"""
Reusable portfolio-formation helpers.

These *form* long-short books from a panel of asset returns — rank on a signal each rebalance, go
long the top and short the bottom, hold to the next rebalance — returning both the daily strategy
return series and the rebalance-date weight matrix (so turnover / cost can be measured). This is the
"recompute, don't read a finished factor" machinery shared by several replications.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def trailing_signal(panel: pd.DataFrame, lookback: int, skip: int, freq: str = "ME") -> pd.DataFrame:
    """Trailing compounded return over [t-lookback, t-skip] periods, per asset, at frequency ``freq``."""
    m = (1 + panel).resample(freq).prod() - 1
    full = (1 + m).rolling(lookback).apply(np.prod, raw=True)
    base = (1 + m).rolling(skip).apply(np.prod, raw=True) if skip else 1.0
    return full / base - 1


def trailing_vol(panel: pd.DataFrame, lookback: int, freq: str = "ME") -> pd.DataFrame:
    """Trailing realized volatility per asset, sampled at ``freq`` over ``lookback`` periods of daily data."""
    daily_vol = panel.rolling(21 * lookback).std()
    return daily_vol.resample(freq).last()


def long_short_from_signal(panel: pd.DataFrame, signal: pd.DataFrame, k: int,
                           winners_high: bool = True):
    """Form an equal-weight long-short book: each rebalance, long the top-k / short the bottom-k.

    Returns (daily_returns, weights) where weights is indexed by rebalance date. ``winners_high``
    True longs the high-signal names (momentum); False longs the low-signal names (e.g. low-vol).
    """
    w = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)
    for dt, row in signal.dropna(how="all").iterrows():
        r = row.dropna()
        if len(r) < 2 * k:
            continue
        order = r.sort_values()
        lo, hi = order.index[:k], order.index[-k:]
        long_leg, short_leg = (hi, lo) if winners_high else (lo, hi)
        w.loc[dt, long_leg] = 1.0 / k
        w.loc[dt, short_leg] = -1.0 / k
    w = w.shift(1)                                          # hold last rebalance's book (no look-ahead)
    daily = panel.loc[panel.index >= w.dropna(how="all").index.min()]
    strat = (daily * w.reindex(daily.index, method="ffill")).sum(axis=1)
    return strat, w.dropna(how="all")
