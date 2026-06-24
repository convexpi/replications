"""Betting against beta — Frazzini & Pedersen (2014).

The security market line is too flat: high-beta assets earn less than CAPM predicts and low-beta
assets earn more, because constrained, leverage-averse investors bid up high-beta stocks. The BAB
factor exploits this by going long low-beta assets *levered up* to a beta of one and short high-beta
assets *deleveraged* to a beta of one — so the book is (ex-ante) market-neutral and isolates the
flatness of the security market line.

Reconstructed from Ken French's beta-sorted quintiles: we rescale each leg by its own ex-ante beta
(rolling 60-month market beta), exactly in the spirit of the paper's construction:

    BAB_t = (r_Lo,t - rf_t) / beta_Lo  -  (r_Hi,t - rf_t) / beta_Hi

rather than the raw low-minus-high spread (whose Sharpe is weak precisely because it is *not*
beta-neutral). Monthly, full CRSP universe.
"""
import numpy as np
from ..base import Replication
from .. import data

WINDOW, MIN_OBS = 60, 36       # rolling-beta estimation window (months)


class FrazziniPedersenBAB(Replication):
    def __init__(self):
        super().__init__(
            name="frazzini_pedersen_bab", title="Betting against beta",
            paper_title="Betting Against Beta",
            paper_doi="10.1016/j.jfineco.2013.10.005", pub_year=2014,
            data_sources=["kenfrench:Portfolios_Formed_on_BETA",
                          "kenfrench:F-F_Research_Data_Factors"],
            references=[
                "Frazzini, A. & Pedersen, L. (2014) — Betting Against Beta — JFE",
                "Black, F., Jensen, M. & Scholes, M. (1972) — The Capital Asset Pricing Model: "
                "Some Empirical Tests",
            ],
            caveat="Beta-rescaling uses a simple rolling 60-month market beta of each leg, not the "
                   "paper's exact (1-year vol x 5-year correlation) estimator, and rescales the two "
                   "quintile legs rather than every security. Gross of the (high) financing and "
                   "turnover costs that leverage entails.",
        )

    def _beta(self, excess, mkt):
        cov = excess.rolling(WINDOW, min_periods=MIN_OBS).cov(mkt)
        var = mkt.rolling(WINDOW, min_periods=MIN_OBS).var()
        return (cov / var).shift(1)            # ex-ante (no look-ahead)

    def build(self):
        p = data.kenfrench("Portfolios_Formed_on_BETA")
        ff = data.kenfrench("F-F_Research_Data_Factors")
        mkt, rf = ff["Mkt-RF"], ff["RF"]
        idx = p.index.intersection(ff.index)
        lo, hi, mkt, rf = p["Lo 20"][idx], p["Hi 20"][idx], mkt[idx], rf[idx]

        ex_lo, ex_hi = lo - rf, hi - rf
        b_lo = self._beta(ex_lo, mkt).replace(0, np.nan)
        b_hi = self._beta(ex_hi, mkt).replace(0, np.nan)
        # long low-beta levered to beta 1, short high-beta deleveraged to beta 1
        return (ex_lo / b_lo - ex_hi / b_hi).dropna()
