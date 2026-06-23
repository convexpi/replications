"""Momentum (WML) — reconstructed from the 6 size x prior-return portfolios (winners minus losers)."""
from ..base import Replication
from .. import data


class JegadeeshTitmanMomentum(Replication):
    def __init__(self):
        super().__init__(
            name="jegadeesh_titman_momentum", title="Momentum (WML)",
            paper_title="Returns to Buying Winners and Selling Losers",
            paper_doi="10.1111/j.1540-6261.1993.tb04702.x", pub_year=1993,
            data_sources=["kenfrench:6_Portfolios_ME_Prior_12_2_daily"],
            references=["Jegadeesh, N. & Titman, S. (1993) — Returns to Buying Winners and Selling Losers — JF"],
        )

    def build(self):
        p = data.kenfrench("6_Portfolios_ME_Prior_12_2_daily")
        return 0.5 * (p["SMALL HiPRIOR"] + p["BIG HiPRIOR"]) - 0.5 * (p["SMALL LoPRIOR"] + p["BIG LoPRIOR"])
