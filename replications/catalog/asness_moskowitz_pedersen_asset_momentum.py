"""Asset-class momentum — Asness, Moskowitz & Pedersen (2013), "Value and Momentum Everywhere".

Momentum isn't just a stock-picking anomaly — it works *across* asset classes too. Here we run
cross-sectional momentum over a basket of liquid asset-class ETFs (equities, bonds, credit,
commodities, gold, real estate, currencies): each month rank them by their trailing 12-month return
(skipping the most recent month, the standard 12–1 signal), go long the top third and short the
bottom third, equal-weighted, held the following month.

Data: Yahoo Finance ETF prices (online). A practical proxy for the paper's broad cross-asset universe;
ETF histories start in the mid-2000s, so the sample is shorter than the paper's. See the caveat.
"""
import numpy as np
import pandas as pd
from ..base import Replication
from .. import data

# Liquid ETFs spanning asset classes (Yahoo tickers).
ETFS = ("SPY EFA EEM "        # US / developed / EM equities
        "TLT IEF "            # long / intermediate US Treasuries
        "LQD HYG "            # investment-grade / high-yield credit
        "GLD DBC "            # gold / broad commodities
        "VNQ "                # US real estate
        "UUP FXE")           # USD / EUR currency
LOOKBACK = 252 - 21          # ~12 months minus the most recent ~1 month (12-1 momentum)


class AsnessMoskowitzPedersenAssetMomentum(Replication):
    def __init__(self):
        super().__init__(
            name="asness_moskowitz_pedersen_asset_momentum", title="Asset-class momentum",
            paper_title="Value and Momentum Everywhere",
            paper_doi="10.1111/jofi.12021", pub_year=2013,
            data_sources=[f"yfinance:{ETFS}"],
            references=[
                "Asness, C., Moskowitz, T. & Pedersen, L. (2013) — Value and Momentum Everywhere — JF",
            ],
            online=True,
            rebalances_per_year=12.0,
            caveat="Cross-sectional 12-1 momentum across a fixed ETF basket (histories begin mid-2000s, "
                   "so the sample is short), a practical proxy for the paper's broad cross-asset "
                   "universe; gross of transaction costs.",
        )

    def build(self):
        px = data.yfinance_prices(ETFS.split(), start="2004-01-01")
        rets = px.pct_change()
        mom = px.pct_change(LOOKBACK)                       # 12-1 momentum signal
        sig = mom.resample("ME").last().shift(1)            # trade on last month's signal
        mret = (1 + rets).resample("ME").prod() - 1

        pr = sig.rank(axis=1, pct=True)
        enough = sig.notna().sum(axis=1) >= 6
        long = (pr > 2 / 3) & enough.values[:, None]
        short = (pr <= 1 / 3) & enough.values[:, None]
        wl = long.div(long.sum(axis=1).replace(0, np.nan), axis=0)
        ws = short.div(short.sum(axis=1).replace(0, np.nan), axis=0)
        w = (wl.fillna(0) - ws.fillna(0))[enough]

        port = (w * mret.reindex(w.index)).sum(axis=1)
        return port[(w != 0).any(axis=1)].dropna()
