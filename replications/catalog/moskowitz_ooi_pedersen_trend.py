"""Time-series (trend) momentum — the real strategy: a diversified, volatility-scaled trend follower
across a cross-asset futures universe (equities, bonds, commodities, FX), per Moskowitz, Ooi &
Pedersen (2012).

Each month, take a long/short position in every instrument equal to the SIGN of its own trailing
12-month return, scaled to a constant target volatility (so a calm bond future and a wild energy
future contribute equally), then average across instruments. This recovers the diversification and
"crisis alpha" that a single equity series cannot.

Data: Yahoo Finance continuous front-month futures (online). This is a live-data replication — see the
caveat about Yahoo's history (since ~2000) and continuous-contract roll artifacts.
"""
import numpy as np
import pandas as pd
from ..base import Replication
from .. import data

# ~18 liquid futures across asset classes (Yahoo continuous front-month tickers).
TICKERS = ("ES=F NQ=F YM=F "          # equity indices
           "ZN=F ZB=F ZF=F "          # US Treasury futures
           "GC=F SI=F HG=F "          # metals
           "CL=F NG=F "               # energy
           "ZC=F ZW=F ZS=F "          # agriculture
           "6E=F 6J=F 6B=F 6A=F")     # currencies
TARGET_VOL = 0.40                      # annualized vol each position is scaled to (MOP use ~40%)


class MoskowitzOoiPedersenTrend(Replication):
    def __init__(self):
        super().__init__(
            name="moskowitz_ooi_pedersen_trend", title="Trend (time-series momentum)",
            paper_title="Time Series Momentum",
            paper_doi="10.1016/j.jfineco.2011.11.003", pub_year=2012,
            data_sources=[f"yfinance:{TICKERS}"],
            references=["Moskowitz, T., Ooi, Y. H. & Pedersen, L. (2012) — Time Series Momentum — JFE"],
            online=True,
            caveat="Uses Yahoo Finance continuous front-month futures, which begin ~2000 (vs the "
                   "paper's 1985) and carry roll artifacts — a faithful but data-limited proxy for "
                   "the paper's 58-instrument universe.",
        )

    def build(self):
        px = data.yfinance_prices(TICKERS.split())
        rets = px.pct_change()

        # Monthly trailing 12-month signal (sign), per instrument.
        m = (1 + rets).resample("ME").prod() - 1
        sig = np.sign((1 + m).rolling(12).apply(np.prod, raw=True) - 1)

        # Ex-ante volatility (≈3-month, annualized), sampled monthly — for vol scaling.
        vol = (rets.rolling(63).std() * np.sqrt(252)).resample("ME").last()

        # Position per instrument: sign × (target vol / its vol), held the *following* month.
        weight = (sig * TARGET_VOL / vol).shift(1)

        wd = weight.reindex(rets.index, method="ffill")
        active = wd.notna().sum(axis=1).replace(0, np.nan)        # diversify across available instruments
        return ((rets * wd).sum(axis=1) / active).dropna()
