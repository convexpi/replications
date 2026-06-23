"""Value (HML) — reconstructed from the 6 size x book-to-market portfolios, as Fama-French build it."""
from ..base import Replication
from .. import data


class FamaFrenchHML(Replication):
    def __init__(self):
        super().__init__(
            name="fama_french_hml", title="Value (HML)",
            paper_title="Common Risk Factors in the Returns on Stocks and Bonds",
            paper_doi="10.1016/0304-405x(93)90023-5", pub_year=1993,
            data_sources=["kenfrench:6_Portfolios_2x3_daily"],
            references=["Fama, E. & French, K. (1993) — Common Risk Factors in the Returns on Stocks and Bonds — JFE"],
        )

    def build(self):
        p = data.kenfrench("6_Portfolios_2x3_daily")
        # long the two value corners, short the two growth corners
        return 0.5 * (p["SMALL HiBM"] + p["BIG HiBM"]) - 0.5 * (p["SMALL LoBM"] + p["BIG LoBM"])
