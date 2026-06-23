"""
The Replication contract.

Every reference replication subclasses ``Replication`` and implements ``build()``, which returns a
daily (or monthly) decimal return series for the strategy. Everything else — the out-of-sample
report card, the Colab notebook, the leaderboard row, the link to the paper's wiki — is derived
automatically from this contract, so a contributor only has to write ``build()`` and declare a little
metadata.

A replication is *honest by construction*: it recomputes the strategy from underlying building
blocks (portfolios, prices) rather than reading a finished factor off the shelf, and it is scored
out of sample by splitting at the paper's publication year (the McLean & Pontiff test).
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np
import pandas as pd


def _ann_factor(idx: pd.DatetimeIndex) -> float:
    """Periods per year, inferred from the median spacing of the index."""
    if len(idx) < 3:
        return 252.0
    days = np.median(np.diff(idx.values).astype("timedelta64[D]").astype(float))
    if days <= 4:
        return 252.0      # daily
    if days <= 10:
        return 52.0       # weekly
    return 12.0           # monthly


def sharpe(returns: pd.Series) -> float:
    r = returns.dropna()
    if r.std() == 0 or len(r) < 2:
        return float("nan")
    return float(np.sqrt(_ann_factor(r.index)) * r.mean() / r.std())


def max_drawdown(returns: pd.Series) -> float:
    eq = (1 + returns.dropna()).cumprod()
    return float((eq / eq.cummax() - 1).min())


@dataclass
class Replication(ABC):
    """Subclass this; set the class attributes and implement ``build()``.

    Attributes
    ----------
    name        : stable slug, e.g. "jegadeesh_titman_momentum".
    title       : human title of the strategy.
    paper_title : the paper being replicated.
    paper_doi   : DOI (links the replication to the paper's wiki). None if no single paper.
    pub_year    : publication year — the in-sample / out-of-sample split point.
    data_sources: declared data dependencies (see ``data.py`` keys), for transparency + caching.
    references  : a few key citations.
    authors     : replication contributors (provenance / attribution).
    """
    name: str = ""
    title: str = ""
    paper_title: str = ""
    paper_doi: str | None = None
    pub_year: int = 0
    data_sources: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    authors: list[str] = field(default_factory=lambda: ["ConvexPi"])
    caveat: str = ""                       # honest health warning (e.g. cost/turnover/microstructure)
    recent_years: int = 10
    cost_bps: float = 10.0                 # per unit of one-way turnover, for the net-of-cost score
    rebalances_per_year: float = 12.0

    @abstractmethod
    def build(self) -> pd.Series:
        """Return the strategy's periodic decimal return series with a DatetimeIndex."""

    def weights(self) -> pd.DataFrame | None:
        """Optional: the (rebalance-date x asset) weight matrix, enabling turnover / net-of-cost.

        Replications that form a long-short book should return it here; factor reconstructions that
        don't trade an explicit book can leave this as None.
        """
        return None

    # --- derived, identical for every replication --------------------------------------------
    def report_card(self, as_of: str | None = None) -> dict:
        """In-sample vs out-of-sample stats + the verdict (the McLean & Pontiff test).

        Pass ``as_of`` (e.g. "2024-12-31") to truncate the series to a fixed end date — used for
        committed reference results so they stay reproducible as new data is appended upstream.
        """
        r = self.build().dropna()
        r.index = pd.to_datetime(r.index)
        if as_of is not None:
            r = r[r.index <= pd.Timestamp(as_of)]
        yrs = r.index.year
        ins = r[yrs < self.pub_year]
        oos = r[yrs >= self.pub_year]
        recent = r[yrs >= yrs.max() - self.recent_years]
        is_s = sharpe(ins) if len(ins) else None
        oos_s = sharpe(oos)
        decay = None
        if is_s and is_s > 0 and not np.isnan(is_s):
            decay = round(1 - oos_s / is_s, 3)

        # Optional net-of-cost out-of-sample Sharpe, when the replication exposes a weight book.
        turnover = net_oos_sharpe = None
        try:
            from .costs import turnover_from_weights, net_returns
            w = self.weights()
            if w is not None and len(w):
                turnover = round(turnover_from_weights(w), 3)
                net = net_returns(oos, turnover, self.cost_bps, self.rebalances_per_year)
                net_oos_sharpe = round(sharpe(net), 3)
        except Exception:
            pass

        return {
            "name": self.name,
            "title": self.title,
            "paper_title": self.paper_title,
            "paper_doi": self.paper_doi,
            "pub_year": self.pub_year,
            "authors": self.authors,
            "start": str(r.index.min().date()),
            "end": str(r.index.max().date()),
            "in_sample_sharpe": None if is_s is None else round(is_s, 3),
            "oos_sharpe": round(oos_s, 3),
            "recent_sharpe": round(sharpe(recent), 3),
            "oos_max_drawdown": round(max_drawdown(oos), 3),
            "sharpe_decay": decay,
            "turnover": turnover,
            "net_oos_sharpe": net_oos_sharpe,
            "caveat": self.caveat or None,
            "verdict": _verdict(oos_s, sharpe(recent), decay),
        }


def _verdict(oos_sharpe, recent_sharpe, decay) -> str:
    if recent_sharpe is not None and not np.isnan(recent_sharpe) and recent_sharpe < 0:
        return "dormant"
    if decay is not None and decay > 0.5:
        return "decayed"
    if oos_sharpe is not None and not np.isnan(oos_sharpe) and oos_sharpe > 0.3:
        return "alive"
    return "weak"
