"""Short-term reversal — reconstructed from the 6 size x prior-1-month portfolios.

Long last month's losers, short last month's winners. The classic short-horizon reversal effect
(Jegadeesh 1990; Lehmann 1990) — built from the *correct* building blocks (single sorts on the prior
one-month return), not from aggregated industries.
"""
from ..base import Replication
from .. import data


class JegadeeshShortTermReversal(Replication):
    def __init__(self):
        super().__init__(
            name="jegadeesh_short_term_reversal", title="Short-term reversal",
            paper_title="Evidence of Predictable Behavior of Security Returns",
            paper_doi="10.1111/j.1540-6261.1990.tb05110.x", pub_year=1990,
            data_sources=["kenfrench:6_Portfolios_ME_Prior_1_0_daily"],
            references=[
                "Jegadeesh, N. (1990) — Evidence of Predictable Behavior of Security Returns — JF",
                "Lehmann, B. (1990) — Fads, Martingales, and Market Efficiency — QJE",
            ],
            caveat="Extremely high turnover and heavily driven by microstructure (bid-ask bounce). "
                   "The gross Sharpe shown is not achievable net of realistic transaction costs.",
        )

    def build(self):
        p = data.kenfrench("6_Portfolios_ME_Prior_1_0_daily")
        # long prior-month LOSERS, short prior-month WINNERS
        return 0.5 * (p["SMALL LoPRIOR"] + p["BIG LoPRIOR"]) - 0.5 * (p["SMALL HiPRIOR"] + p["BIG HiPRIOR"])
