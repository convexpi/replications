"""The earnings-yield (P/E) effect — Basu (1977).

One of the original value anomalies: stocks with high earnings-to-price (low P/E) earn higher
risk-adjusted returns than low earnings-to-price (high P/E, "glamour") stocks. Basu's evidence that
P/E predicts returns was an early challenge to the efficient-market hypothesis.

Reconstructed from Ken French's univariate quintile sorts on earnings-to-price, value-weighted,
monthly. Long the highest-E/P quintile (cheap), short the lowest (expensive); a positive return is
the earnings-yield effect.
"""
from ..base import Replication
from .. import data


class BasuEarningsYield(Replication):
    def __init__(self):
        super().__init__(
            name="basu_earnings_yield", title="Earnings yield (P/E effect)",
            paper_title="Investment Performance of Common Stocks in Relation to Their "
                        "Price-Earnings Ratios",
            paper_doi="10.1111/j.1540-6261.1977.tb01979.x", pub_year=1977,
            data_sources=["kenfrench:Portfolios_Formed_on_E-P"],
            references=[
                "Basu, S. (1977) — Investment Performance of Common Stocks in Relation to Their "
                "Price-Earnings Ratios — JF",
            ],
            caveat="Univariate earnings-yield sort (value-weighted quintiles); firms with negative "
                   "earnings are excluded from the sort. Overlaps with the book-to-market value "
                   "factor; gross of transaction costs.",
        )

    def build(self):
        p = data.kenfrench("Portfolios_Formed_on_E-P")
        # long HIGH earnings yield (cheap), short LOW earnings yield (expensive)
        return p["Hi 20"] - p["Lo 20"]
