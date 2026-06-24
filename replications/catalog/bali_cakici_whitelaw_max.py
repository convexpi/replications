"""The MAX effect ("lottery" stocks) — Bali, Cakici & Whitelaw (2011).

Stocks with extreme *positive* daily returns in the recent past — lottery-like payoffs that attract
buyers willing to overpay — subsequently *under*-perform. Each month we rank stocks by MAX, the
average of their five largest daily returns over the prior month, then go long the lowest-MAX quintile
and short the highest-MAX quintile, equal-weighted, held the following month. A positive long-short
return is the MAX effect: avoiding lottery stocks pays.

Data: Yahoo Finance single-name daily prices (online). The paper uses the full CRSP universe; we use
a fixed basket of large, long-listed US stocks — a faithful-but-survivorship-limited proxy, exactly
as the trend replication proxies a futures universe. See the caveat.
"""
import numpy as np
import pandas as pd
from ..base import Replication
from .. import data

# A fixed basket of liquid, long-listed US large caps (Yahoo tickers). Survivorship-biased by
# construction (these are survivors) — see caveat. Breadth matters more than the exact names for
# demonstrating the cross-sectional effect.
UNIVERSE = (
    "AAPL MSFT JNJ JPM XOM PG KO PEP WMT HD MCD DIS CSCO INTC ORCL IBM "
    "CVX MRK PFE T VZ BA CAT GE MMM HON UNH ABT TXN QCOM AMGN GILD "
    "LOW COST TGT SBUX NKE MDT BMY LLY DUK SO NEE WFC BAC C GS USB AXP "
    "MO CL KMB GD LMT RTX ADP"
).split()

QUANTILE = 0.20   # long bottom 20% MAX, short top 20% MAX
N_MAX = 5         # MAX = mean of the 5 largest daily returns in the month


def _max_signal(daily: pd.Series) -> float:
    """Mean of the N largest daily returns in the group (NaN if too few observations)."""
    x = daily.dropna().values
    if x.size < 10:
        return np.nan
    return float(np.sort(x)[-N_MAX:].mean())


class BaliCakiciWhitelawMax(Replication):
    def __init__(self):
        super().__init__(
            name="bali_cakici_whitelaw_max", title="MAX effect (lottery stocks)",
            paper_title="Maxing Out: Stocks as Lotteries and the Cross-Section of Expected Returns",
            paper_doi="10.1016/j.jfineco.2010.08.014", pub_year=2011,
            data_sources=[f"yfinance:{' '.join(UNIVERSE)}"],
            references=[
                "Bali, T., Cakici, N. & Whitelaw, R. (2011) — Maxing Out: Stocks as Lotteries and "
                "the Cross-Section of Expected Returns — JFE",
            ],
            online=True,
            rebalances_per_year=12.0,
            caveat="Uses a fixed basket of surviving Yahoo Finance large caps (history since ~2000), "
                   "not the paper's full CRSP universe, so it is survivorship-biased and understates "
                   "the effect, which is strongest in small, illiquid names. A faithful-but-limited "
                   "proxy; gross of transaction costs.",
        )

    def _book(self):
        """Return (monthly long-short weights, monthly asset returns) aligned on month-end."""
        px = data.yfinance_prices(UNIVERSE, start="2000-01-01")
        rets = px.pct_change()

        # MAX signal and realized return, per stock per month.
        maxsig = rets.resample("ME").agg(_max_signal)
        mret = (1 + rets).resample("ME").prod() - 1

        # Trade on last month's signal (no look-ahead): form quintiles cross-sectionally.
        sig = maxsig.shift(1)
        pr = sig.rank(axis=1, pct=True)
        enough = sig.notna().sum(axis=1) >= 10            # need a cross-section to sort
        long = (pr <= QUANTILE) & enough.values[:, None]
        short = (pr > 1 - QUANTILE) & enough.values[:, None]

        wl = long.div(long.sum(axis=1).replace(0, np.nan), axis=0)
        ws = short.div(short.sum(axis=1).replace(0, np.nan), axis=0)
        w = wl.fillna(0) - ws.fillna(0)
        w = w[enough]
        return w, mret

    def build(self):
        w, mret = self._book()
        port = (w * mret.reindex(w.index)).sum(axis=1)
        return port[(w != 0).any(axis=1)].dropna()

    def weights(self):
        w, _ = self._book()
        return w[(w != 0).any(axis=1)]
