"""
A standard, deliberately simple transaction-cost & turnover layer.

Every replication can be scored *net of cost* with the same model, so the leaderboard compares
strategies on an honest footing — a recurring theme: a gross edge that turnover eats is not an edge.

``turnover`` is the average one-way fraction of the book traded per rebalance, inferred from a weight
matrix (rows = rebalance dates, columns = assets). ``net_returns`` deducts a per-unit-turnover cost
(in basis points) from the gross return stream.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def turnover_from_weights(weights: pd.DataFrame) -> float:
    """Average one-way turnover per rebalance from a (dates x assets) weight matrix."""
    w = weights.fillna(0.0)
    changes = w.diff().abs().sum(axis=1).iloc[1:]
    return float(changes.mean() / 2.0) if len(changes) else 0.0


def net_returns(gross: pd.Series, turnover: float, cost_bps: float = 10.0,
                rebalances_per_year: float = 12.0) -> pd.Series:
    """Subtract a flat cost: cost_bps per unit of one-way turnover, charged each rebalance.

    Spread evenly across the periods in a year so the drag shows up in the return stream.
    """
    per_year_cost = 2 * turnover * (cost_bps / 1e4) * rebalances_per_year
    ann_factor = 252.0 if _is_daily(gross.index) else 12.0
    per_period_drag = per_year_cost / ann_factor
    return gross - per_period_drag


def _is_daily(idx) -> bool:
    if len(idx) < 3:
        return True
    return np.median(np.diff(idx.values).astype("timedelta64[D]").astype(float)) <= 4
