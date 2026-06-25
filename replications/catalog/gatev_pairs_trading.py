"""Distance pairs trading — Gatev, Goetzmann & Rouwenhorst (2006).

The original statistical-arbitrage strategy: find pairs of stocks whose normalized prices have moved
together historically, then bet on convergence whenever they diverge. During a 12-month *formation*
window we pick the pairs with the smallest sum of squared distance between their normalized price
paths; over the following 6-month *trading* window we open a position when a pair's spread diverges by
more than 2 historical standard deviations (long the laggard, short the leader) and close it when the
spread converges back to its mean.

Data: Yahoo Finance single-name daily prices (online). The paper uses the full CRSP universe; we use a
fixed large-cap basket — a faithful-but-survivorship-limited proxy (the effect is strongest in
smaller, less-followed names). See the caveat.
"""
import numpy as np
import pandas as pd
from ..base import Replication
from .. import data
from .bali_cakici_whitelaw_max import UNIVERSE   # reuse the liquid large-cap basket

FORMATION = 252      # ~12 months to select pairs and estimate the spread distribution
TRADING = 126        # ~6 months to trade the selected pairs
N_PAIRS = 20         # number of closest pairs to trade each period
ENTRY = 2.0          # open when |z| exceeds this many formation std devs; close at z = 0


class GatevPairsTrading(Replication):
    def __init__(self):
        super().__init__(
            name="gatev_pairs_trading", title="Pairs trading (distance)",
            paper_title="Pairs Trading: Performance of a Relative-Value Arbitrage Rule",
            paper_doi="10.1093/rfs/hhj020", pub_year=2006,
            data_sources=[f"yfinance:{' '.join(UNIVERSE)}"],
            references=[
                "Gatev, E., Goetzmann, W. & Rouwenhorst, K. G. (2006) — Pairs Trading: Performance "
                "of a Relative-Value Arbitrage Rule — RFS",
            ],
            online=True,
            rebalances_per_year=2.0,
            caveat="Distance method on a fixed large-cap Yahoo basket (history since ~2000), not the "
                   "paper's full CRSP universe, so it is survivorship-biased and understates an effect "
                   "that lives in smaller names; equal-weight long/short per pair, gross of the high "
                   "transaction costs pairs trading incurs.",
        )

    def build(self):
        px = data.yfinance_prices(UNIVERSE, start="2000-01-01")
        rets = px.pct_change()
        port = pd.Series(0.0, index=rets.index)
        active = pd.Series(0, index=rets.index)

        for s in range(FORMATION, len(px) - 1, TRADING):
            form = px.iloc[s - FORMATION:s].dropna(axis=1)
            if form.shape[1] < 4:
                continue
            trade_idx = px.index[s:s + TRADING]
            if len(trade_idx) < 5:
                break

            # Normalize formation prices to a cumulative index starting at 1, then rank pairs by
            # sum of squared distance between the two normalized paths.
            norm = form / form.iloc[0]
            cols = list(norm.columns)
            arr = norm.values
            ssd = []
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    ssd.append((float(np.sum((arr[:, i] - arr[:, j]) ** 2)), cols[i], cols[j]))
            ssd.sort(key=lambda x: x[0])

            for _, a, b in ssd[:N_PAIRS]:
                spread_form = norm[a] - norm[b]
                mu, sd = spread_form.mean(), spread_form.std()
                if not sd or np.isnan(sd):
                    continue
                # Continue the same normalization into the trading window.
                na = px[a].loc[trade_idx] / form[a].iloc[0]
                nb = px[b].loc[trade_idx] / form[b].iloc[0]
                z = ((na - nb) - mu) / sd

                # Position: +1 = long a / short b (spread too low), -1 = short a / long b. Hold until
                # the spread reverts through its mean (z crosses 0).
                pos = np.zeros(len(trade_idx))
                cur = 0
                for k in range(len(trade_idx)):
                    zk = z.iloc[k]
                    if cur == 0:
                        if zk > ENTRY:
                            cur = -1
                        elif zk < -ENTRY:
                            cur = 1
                    elif (cur == 1 and zk >= 0) or (cur == -1 and zk <= 0):
                        cur = 0
                    pos[k] = cur

                pos_lag = np.concatenate([[0.0], pos[:-1]])     # trade on yesterday's signal
                ra = rets[a].loc[trade_idx].values
                rb = rets[b].loc[trade_idx].values
                pair_ret = pos_lag * (np.nan_to_num(ra) - np.nan_to_num(rb))
                port.loc[trade_idx] = port.loc[trade_idx].values + pair_ret
                active.loc[trade_idx] = active.loc[trade_idx].values + (pos_lag != 0).astype(int)

        # Average across the pairs that were actually open each day.
        return (port / active.replace(0, np.nan)).dropna()
