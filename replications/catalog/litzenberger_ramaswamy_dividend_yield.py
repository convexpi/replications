"""The dividend-yield effect — Litzenberger & Ramaswamy (1979).

One of the original cross-sectional return predictors: high dividend-yield (D/P) stocks were found to
earn higher returns, which Litzenberger & Ramaswamy attributed to a tax effect (investors demanding
a premium to hold higher-taxed dividend income). It became a staple of the early anomaly literature.

Reconstructed from Ken French's univariate quintile sorts on dividend-to-price, value-weighted,
monthly. Long the highest-D/P quintile, short the lowest; a positive return is the dividend-yield
premium. The sort excludes non-payers (the "<= 0" bucket), so this is the premium *among payers*.
"""
from ..base import Replication
from .. import data


class LitzenbergerRamaswamyDividendYield(Replication):
    def __init__(self):
        super().__init__(
            name="litzenberger_ramaswamy_dividend_yield", title="Dividend yield (D/P effect)",
            paper_title="The effect of personal taxes and dividends on capital asset prices: "
                        "Theory and empirical evidence",
            paper_doi="10.1016/0304-405X(79)90012-6", pub_year=1979,
            data_sources=["kenfrench:Portfolios_Formed_on_D-P"],
            references=[
                "Litzenberger, R. & Ramaswamy, K. (1979) — The effect of personal taxes and "
                "dividends on capital asset prices — JFE",
            ],
            caveat="Univariate dividend-yield sort (value-weighted quintiles); non-payers are "
                   "excluded, so this is the premium among payers. Tax-driven and value-adjacent; "
                   "the premium has largely faded in modern data. Gross of transaction costs.",
        )

    def build(self):
        p = data.kenfrench("Portfolios_Formed_on_D-P")
        # long HIGH dividend yield, short LOW dividend yield
        return p["Hi 20"] - p["Lo 20"]
