import pandas as pd, pytest
from replications import all_replications

REPS = all_replications()

@pytest.mark.parametrize("name", list(REPS))
def test_build_returns_series(name):
    r = REPS[name]
    s = r.build()
    assert isinstance(s, pd.Series), f"{name}.build() must return a Series"
    assert isinstance(s.index, pd.DatetimeIndex)
    assert s.dropna().shape[0] > 100
    assert r.paper_doi, f"{name} should link to a paper (paper_doi)"

@pytest.mark.parametrize("name", list(REPS))
def test_report_card_keys(name):
    rc = REPS[name].report_card()
    for k in ("oos_sharpe", "verdict", "paper_doi", "pub_year"):
        assert k in rc
    assert rc["verdict"] in ("alive", "decayed", "dormant", "weak")
