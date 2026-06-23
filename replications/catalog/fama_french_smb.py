"""Size (SMB) — reconstructed from the 6 size x book-to-market portfolios (small minus big)."""
from ..base import Replication
from .. import data


class FamaFrenchSMB(Replication):
    def __init__(self):
        super().__init__(
            name="fama_french_smb", title="Size (SMB)",
            paper_title="The Relationship Between Return and Market Value of Common Stocks",
            paper_doi="10.1016/0304-405x(81)90018-0", pub_year=1981,
            data_sources=["kenfrench:6_Portfolios_2x3_daily"],
            references=["Banz, R. (1981) — The Relationship Between Return and Market Value of Common Stocks — JFE"],
        )

    def build(self):
        p = data.kenfrench("6_Portfolios_2x3_daily")
        small = p[["SMALL LoBM", "ME1 BM2", "SMALL HiBM"]].mean(axis=1)
        big = p[["BIG LoBM", "ME2 BM2", "BIG HiBM"]].mean(axis=1)
        return small - big
