"""Net share issuance — Pontiff & Woodgate (2008).

Firms that issue shares subsequently under-perform, while firms that buy back stock out-perform —
share issuance predicts the cross-section of returns even after controlling for size, book-to-market
and momentum. It is a cleaner, more robust cousin of the investment/external-financing anomalies.

Reconstructed from Ken French's univariate quintile sorts on net share issuance, value-weighted,
monthly. Long the lowest-issuance quintile (net repurchasers), short the highest (net issuers); a
positive return is the issuance anomaly.
"""
from ..base import Replication
from .. import data


class PontiffWoodgateIssuance(Replication):
    def __init__(self):
        super().__init__(
            name="pontiff_woodgate_issuance", title="Net share issuance",
            paper_title="Share Issuance and Cross-Sectional Returns",
            paper_doi="10.1111/j.1540-6261.2008.01362.x", pub_year=2008,
            data_sources=["kenfrench:Portfolios_Formed_on_NI"],
            references=[
                "Pontiff, J. & Woodgate, A. (2008) — Share Issuance and Cross-Sectional Returns — JF",
                "Daniel, K. & Titman, S. (2006) — Market Reactions to Tangible and Intangible "
                "Information — JF",
            ],
            caveat="Univariate net-issuance sort (value-weighted quintiles). The effect is stronger "
                   "with equal weighting and among small caps; gross of transaction costs.",
        )

    def build(self):
        p = data.kenfrench("Portfolios_Formed_on_NI")
        # long LOW net issuance (repurchasers), short HIGH net issuance (issuers)
        return p["Lo 20"] - p["Hi 20"]
