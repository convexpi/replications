"""The idiosyncratic-volatility puzzle — Ang, Hodrick, Xing & Zhang (2006).

Stocks with high idiosyncratic volatility — the part of return variance not explained by common
factors — earn abnormally *low* future returns. This is a puzzle: standard theory says diversifiable
risk shouldn't be priced at all, let alone negatively.

Reconstructed from Ken French's univariate quintile sorts on residual variance (the residual from the
market model — i.e. idiosyncratic variance), value-weighted, monthly, over the full CRSP universe.
Long the lowest-idio-vol quintile, short the highest; a positive return is the puzzle.
"""
from ..base import Replication
from .. import data


class AngIdiosyncraticVolatility(Replication):
    def __init__(self):
        super().__init__(
            name="ang_idiosyncratic_volatility", title="Idiosyncratic volatility puzzle",
            paper_title="The Cross-Section of Volatility and Expected Returns",
            paper_doi="10.1111/j.1540-6261.2006.00836.x", pub_year=2006,
            data_sources=["kenfrench:Portfolios_Formed_on_RESVAR"],
            references=[
                "Ang, A., Hodrick, R., Xing, Y. & Zhang, X. (2006) — The Cross-Section of "
                "Volatility and Expected Returns — JF",
            ],
            caveat="Univariate residual-variance sort (value-weighted quintiles). The puzzle is "
                   "stronger with equal weighting and among small, illiquid names; this is the "
                   "value-weighted spread, gross of transaction costs.",
        )

    def build(self):
        p = data.kenfrench("Portfolios_Formed_on_RESVAR")
        # long LOW idiosyncratic volatility, short HIGH
        return p["Lo 20"] - p["Hi 20"]
