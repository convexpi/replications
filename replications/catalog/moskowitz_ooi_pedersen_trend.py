"""Trend / time-series momentum — hold the market long/short on the sign of its trailing 12-month return."""
import numpy as np
from ..base import Replication
from .. import data


class MoskowitzOoiPedersenTrend(Replication):
    def __init__(self):
        super().__init__(
            name="moskowitz_ooi_pedersen_trend", title="Trend (time-series momentum)",
            paper_title="Time Series Momentum",
            paper_doi="10.1016/j.jfineco.2011.11.003", pub_year=2012,
            data_sources=["kenfrench:F-F_Research_Data_Factors_daily"],
            references=["Moskowitz, T., Ooi, Y. H. & Pedersen, L. (2012) — Time Series Momentum — JFE"],
        )

    def build(self):
        mkt = data.kenfrench("F-F_Research_Data_Factors_daily")["Mkt-RF"].dropna()
        m = (1 + mkt).resample("ME").prod() - 1
        trail = (1 + m).rolling(12).apply(np.prod, raw=True) - 1
        pos = np.sign(trail).shift(1)                         # last month's signal, held this month
        daily = mkt.loc[mkt.index >= pos.dropna().index.min()]
        return pos.reindex(daily.index, method="ffill") * daily
