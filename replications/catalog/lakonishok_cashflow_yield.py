"""The cash-flow yield value effect — Lakonishok, Shleifer & Vishny (1994).

"Contrarian investment, extrapolation, and risk" argued that value strategies work because investors
naively extrapolate past growth, overpaying for "glamour" stocks and underpricing out-of-favour value
stocks — not because value is riskier. Cash-flow-to-price was one of their cleanest value signals:
high cash-flow yield earns higher subsequent returns than low cash-flow yield.

Reconstructed from Ken French's univariate quintile sorts on cash-flow-to-price, value-weighted,
monthly. Long the highest-CF/P quintile, short the lowest; a positive return is the value effect.
"""
from ..base import Replication
from .. import data


class LakonishokCashflowYield(Replication):
    def __init__(self):
        super().__init__(
            name="lakonishok_cashflow_yield", title="Cash-flow yield (value)",
            paper_title="Contrarian Investment, Extrapolation, and Risk",
            paper_doi="10.1111/j.1540-6261.1994.tb04772.x", pub_year=1994,
            data_sources=["kenfrench:Portfolios_Formed_on_CF-P"],
            references=[
                "Lakonishok, J., Shleifer, A. & Vishny, R. (1994) — Contrarian Investment, "
                "Extrapolation, and Risk — JF",
            ],
            caveat="Univariate cash-flow-to-price sort (value-weighted quintiles); firms with "
                   "negative cash flow are excluded. Highly correlated with book-to-market and "
                   "earnings-yield value; gross of transaction costs.",
        )

    def build(self):
        p = data.kenfrench("Portfolios_Formed_on_CF-P")
        # long HIGH cash-flow yield (value), short LOW (glamour)
        return p["Hi 20"] - p["Lo 20"]
