"""The illiquidity premium — Amihud (2002).

Illiquid stocks — where a given order pushes the price further — earn a **return premium** as
compensation for that price impact. Amihud's measure is beautifully simple: ILLIQ = the daily
absolute return divided by the daily dollar volume, averaged over a formation window. A big price
move on little volume means an illiquid, impactful stock. Each month we rank on last month's ILLIQ,
go long the most-illiquid quintile and short the most-liquid, equal-weighted, held the next month. A
positive long-short return is the illiquidity premium.

Data: Yahoo Finance daily prices + dollar volume (online), the same large-cap basket as the MAX
replication — which is exactly why the effect is muted here (see the caveat).
"""
import numpy as np
import pandas as pd

from ..base import Replication
from .. import data
from .bali_cakici_whitelaw_max import UNIVERSE   # shared liquid large-cap basket

QUANTILE = 0.20   # long most-illiquid 20%, short most-liquid 20%
MIN_DAYS = 10     # need enough daily obs in the month for a stable ILLIQ


class AmihudIlliquidity(Replication):
    def __init__(self):
        super().__init__(
            name="amihud_illiquidity",
            title="Amihud illiquidity",
            paper_title="Illiquidity and Stock Returns: Cross-Section and Time-Series Effects",
            paper_doi="10.1016/S1386-4181(01)00024-6",
            pub_year=2002,
            data_sources=[f"yfinance:{' '.join(UNIVERSE)}"],
            references=[
                "Amihud, Y. (2002) — Illiquidity and Stock Returns: Cross-Section and Time-Series "
                "Effects — Journal of Financial Markets",
            ],
            online=True,
            rebalances_per_year=12.0,
            caveat="Even in this fixed basket of large, liquid Yahoo survivors the premium shows up "
                   "(the relatively less-liquid large caps earn it) and then decays post-publication — "
                   "the McLean-Pontiff pattern. Two honest catches: it is survivorship-biased and "
                   "**gross of costs**, and the irony of this strategy is that its long leg holds the "
                   "least-liquid names, which are the most expensive to trade — the very impact the "
                   "premium compensates for — so net returns are materially lower than gross. The full "
                   "effect is larger in small/micro caps (the paper's CRSP universe), beyond free data.",
        )

    def _book(self):
        """Return (monthly long-short weights, monthly asset returns) aligned on month-end."""
        px = data.yfinance_prices(UNIVERSE, start="2000-01-01")
        dvol = data.yfinance_dollar_volume(UNIVERSE, start="2000-01-01").reindex_like(px)
        rets = px.pct_change()

        # Amihud ILLIQ per stock per month: mean of |daily return| / daily dollar volume.
        illiq_daily = rets.abs() / dvol.replace(0, np.nan)
        illiq = illiq_daily.resample("ME").mean()
        counts = rets.notna().resample("ME").sum()
        illiq = illiq.where(counts >= MIN_DAYS)
        mret = (1 + rets).resample("ME").prod() - 1

        # Trade on last month's illiquidity (no look-ahead); rank cross-sectionally.
        sig = illiq.shift(1)
        pr = sig.rank(axis=1, pct=True)
        enough = sig.notna().sum(axis=1) >= 10
        long = (pr > 1 - QUANTILE) & enough.values[:, None]           # most illiquid
        short = (pr <= QUANTILE) & enough.values[:, None]            # most liquid

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
