"""Industry momentum — FORM a long-short book by ranking the 12 industries each month."""
from ..base import Replication
from .. import data
from ..portfolios import trailing_signal, long_short_from_signal


class MoskowitzGrinblattIndustryMomentum(Replication):
    def __init__(self):
        super().__init__(
            name="moskowitz_grinblatt_industry_momentum", title="Industry momentum",
            paper_title="Do Industries Explain Momentum?",
            paper_doi="10.1111/0022-1082.00146", pub_year=1999,
            data_sources=["kenfrench:12_Industry_Portfolios_daily"],
            references=["Moskowitz, T. & Grinblatt, M. (1999) — Do Industries Explain Momentum? — JF"],
        )

    def _form(self):
        ind = data.kenfrench("12_Industry_Portfolios_daily").dropna()
        sig = trailing_signal(ind, lookback=12, skip=1)      # trailing 12-1 month return
        return long_short_from_signal(ind, sig, k=3, winners_high=True)

    def build(self):
        return self._form()[0]

    def weights(self):
        return self._form()[1]
