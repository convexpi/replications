"""The operating-profitability premium (RMW) — Fama & French (2015).

More profitable firms earn higher average returns than less profitable ones, controlling for value.
Fama & French made operating profitability one of the two new factors (RMW, "robust minus weak") in
their five-factor model. It is the building block behind RMW and is closely related to — but distinct
from — Novy-Marx's gross-profitability premium (a different accounting numerator).

Reconstructed from Ken French's univariate quintile sorts on operating profitability, value-weighted,
monthly. Long the most profitable quintile, short the least; a positive return is the profitability
premium.
"""
from ..base import Replication
from .. import data


class FamaFrenchProfitability(Replication):
    def __init__(self):
        super().__init__(
            name="fama_french_op_profitability", title="Operating profitability (RMW)",
            paper_title="A five-factor asset pricing model",
            paper_doi="10.1016/j.jfineco.2014.10.010", pub_year=2015,
            data_sources=["kenfrench:Portfolios_Formed_on_OP"],
            references=[
                "Fama, E. & French, K. (2015) — A five-factor asset pricing model — JFE",
                "Novy-Marx, R. (2013) — The other side of value: The gross profitability premium — JFE "
                "(related gross-profitability variant)",
            ],
            caveat="Univariate operating-profitability sort (value-weighted quintiles). Related to "
                   "Novy-Marx gross profitability but a distinct accounting measure; overlaps the "
                   "quality complex. Gross of transaction costs.",
        )

    def build(self):
        p = data.kenfrench("Portfolios_Formed_on_OP")
        # long MOST profitable, short LEAST profitable
        return p["Hi 20"] - p["Lo 20"]
