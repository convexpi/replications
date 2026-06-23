"""Long-term reversal — reconstructed from the 6 size x prior 13-60 month portfolios.

Long multi-year losers, short multi-year winners. The long-horizon overreaction / reversal effect
(De Bondt & Thaler 1985), built from single sorts on the prior 13-to-60-month return.
"""
from ..base import Replication
from .. import data


class DeBondtThalerLongTermReversal(Replication):
    def __init__(self):
        super().__init__(
            name="debondt_thaler_long_term_reversal", title="Long-term reversal",
            paper_title="Does the Stock Market Overreact?",
            paper_doi="10.1111/j.1540-6261.1985.tb05004.x", pub_year=1985,
            data_sources=["kenfrench:6_Portfolios_ME_Prior_60_13_daily"],
            references=[
                "De Bondt, W. & Thaler, R. (1985) — Does the Stock Market Overreact? — JF",
            ],
        )

    def build(self):
        p = data.kenfrench("6_Portfolios_ME_Prior_60_13_daily")
        # long long-term LOSERS, short long-term WINNERS
        return 0.5 * (p["SMALL LoPRIOR"] + p["BIG LoPRIOR"]) - 0.5 * (p["SMALL HiPRIOR"] + p["BIG HiPRIOR"])
