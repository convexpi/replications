"""Investment (CMA) — reconstructed from the 6 size x investment portfolios.

Conservative-minus-aggressive: long low-investment (low asset-growth) firms, short high-investment
ones. The investment premium (Cooper-Gulen-Schill 2008 asset growth; the CMA factor of Fama-French
2015), rebuilt from the component portfolios.
"""
from ..base import Replication
from .. import data


class CooperGulenSchillInvestment(Replication):
    def __init__(self):
        super().__init__(
            name="cooper_gulen_schill_investment", title="Investment (CMA)",
            paper_title="Asset Growth and the Cross-Section of Stock Returns",
            paper_doi="10.1111/j.1540-6261.2008.01370.x", pub_year=2008,
            data_sources=["kenfrench:6_Portfolios_ME_INV_2x3_daily"],
            references=[
                "Cooper, M., Gulen, H. & Schill, M. (2008) — Asset Growth and the Cross-Section of Stock Returns — JF",
                "Fama, E. & French, K. (2015) — A Five-Factor Asset Pricing Model — JFE",
            ],
        )

    def build(self):
        p = data.kenfrench("6_Portfolios_ME_INV_2x3_daily")
        # CMA = (avg of the two LOW-investment corners) - (avg of the two HIGH-investment corners)
        return 0.5 * (p["SMALL LoINV"] + p["BIG LoINV"]) - 0.5 * (p["SMALL HiINV"] + p["BIG HiINV"])
