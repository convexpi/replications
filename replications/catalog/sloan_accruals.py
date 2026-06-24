"""The accruals anomaly — Sloan (1996).

Earnings have a cash-flow component and an accrual component. Investors fixate on headline earnings
and under-appreciate that the accrual part is less persistent, so firms with high accruals (earnings
flattered by accruals) subsequently *under*-perform, while low-accrual firms out-perform.

Reconstructed from Ken French's univariate quintile sorts on accruals, value-weighted, monthly. Long
the lowest-accrual quintile, short the highest; a positive return is the accruals anomaly.
"""
from ..base import Replication
from .. import data


class SloanAccruals(Replication):
    def __init__(self):
        super().__init__(
            name="sloan_accruals", title="Accruals anomaly",
            paper_title="Do Stock Prices Fully Reflect Information in Accruals and Cash Flows "
                        "about Future Earnings?",
            paper_doi="10.2307/248290", pub_year=1996,
            data_sources=["kenfrench:Portfolios_Formed_on_AC"],
            references=[
                "Sloan, R. (1996) — Do Stock Prices Fully Reflect Information in Accruals and "
                "Cash Flows about Future Earnings? — The Accounting Review",
            ],
            caveat="Univariate accruals sort (value-weighted quintiles), available from 1963. The "
                   "anomaly is concentrated in small, hard-to-arbitrage names and has weakened since "
                   "publication; gross of transaction costs.",
        )

    def build(self):
        p = data.kenfrench("Portfolios_Formed_on_AC")
        # long LOW accruals, short HIGH accruals
        return p["Lo 20"] - p["Hi 20"]
