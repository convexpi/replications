"""The 52-week high momentum effect — George & Hwang (2004).

A stock's *nearness to its 52-week high* predicts its future return: names trading close to their
trailing one-year high keep winning, while those languishing far below keep lagging. George & Hwang
argue this dominates standard (Jegadeesh-Titman) momentum because traders **anchor** on the salient
52-week high and under-react to news that would push the price through it. Each month we rank stocks
by nearness = price / trailing-252-day high, go long the top quintile (nearest the high) and short
the bottom quintile (farthest below), equal-weighted, held the following month. A positive long-short
return is the 52-week-high effect.

Data: Yahoo Finance single-name daily prices (online), the same survivorship-limited large-cap basket
as the MAX replication — see the caveat.
"""
import numpy as np
import pandas as pd

from ..base import Replication
from .. import data
from .bali_cakici_whitelaw_max import UNIVERSE   # shared liquid large-cap basket

QUANTILE = 0.20    # long nearest-to-high 20%, short farthest 20%
WINDOW = 252       # trading days ≈ 52 weeks
MIN_OBS = 200      # need most of a year before a 52-week high is meaningful


class GeorgeHwang52WeekHigh(Replication):
    def __init__(self):
        super().__init__(
            name="george_hwang_52week_high",
            title="52-week high momentum",
            paper_title="The 52-Week High and Momentum Investing",
            paper_doi="10.1111/j.1540-6261.2004.00695.x",
            pub_year=2004,
            data_sources=[f"yfinance:{' '.join(UNIVERSE)}"],
            references=[
                "George, T. J. & Hwang, C.-Y. (2004) — The 52-Week High and Momentum Investing — "
                "Journal of Finance",
            ],
            online=True,
            rebalances_per_year=12.0,
            caveat="Comes out negative on this fixed large-cap Yahoo basket (survivors since ~2000): "
                   "cross-sectional momentum *reverses* here — plain 12-1 momentum is also negative on "
                   "this basket while 1-month reversal is positive — so a momentum-family effect like "
                   "the 52-week high does not replicate on a narrow large-cap universe. The effect "
                   "lives in the broad CRSP cross-section (especially smaller names); see the "
                   "Jegadeesh-Titman momentum replication (Ken French) for momentum on a full universe. "
                   "An honest data-access limitation, not a failed method. Survivorship-biased, gross "
                   "of transaction costs; nearness uses split/dividend-adjusted prices.",
        )

    def _book(self):
        """Return (monthly long-short weights, monthly asset returns) aligned on month-end."""
        px = data.yfinance_prices(UNIVERSE, start="2000-01-01")
        nearness = px / px.rolling(WINDOW, min_periods=MIN_OBS).max()   # daily, in (0, 1]

        # Trade on last month's nearness (no look-ahead); rank cross-sectionally into quintiles.
        sig = nearness.resample("ME").last().shift(1)
        mret = (1 + px.pct_change()).resample("ME").prod() - 1

        pr = sig.rank(axis=1, pct=True)
        enough = sig.notna().sum(axis=1) >= 10                          # need a cross-section to sort
        long = (pr > 1 - QUANTILE) & enough.values[:, None]            # nearest the 52-week high
        short = (pr <= QUANTILE) & enough.values[:, None]             # farthest below it

        wl = long.div(long.sum(axis=1).replace(0, np.nan), axis=0)
        ws = short.div(short.sum(axis=1).replace(0, np.nan), axis=0)
        w = (wl.fillna(0) - ws.fillna(0))[enough]
        return w, mret

    def build(self):
        w, mret = self._book()
        port = (w * mret.reindex(w.index)).sum(axis=1)
        return port[(w != 0).any(axis=1)].dropna()

    def weights(self):
        w, _ = self._book()
        return w[(w != 0).any(axis=1)]
