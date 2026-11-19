import numpy as np
import pandas as pd
import pytest
from replications.portfolios import long_short_from_signal


@pytest.mark.parametrize("signal_date,next_day", [("2024-01-31", "2024-02-01"), ("2024-03-31", "2024-04-01")])
def test_signal_applies_on_next_session_including_weekend_month_end(signal_date, next_day):
    dates = pd.bdate_range("2024-01-01", "2024-05-10")
    panel = pd.DataFrame({"A": .01, "B": -.01}, index=dates)
    signal = pd.DataFrame({"A": [1.], "B": [0.]}, index=pd.to_datetime([signal_date]))
    returns, weights = long_short_from_signal(panel, signal, k=1)
    assert returns.index[0] == pd.Timestamp(next_day)
    assert returns.iloc[0] == pytest.approx(.02)
    assert weights.index[0] == pd.Timestamp(signal_date)


def test_new_signal_does_not_earn_its_own_days_return():
    dates = pd.bdate_range("2024-01-30", "2024-03-04")
    panel = pd.DataFrame({"A": .01, "B": -.01}, index=dates)
    signal = pd.DataFrame({"A": [1., 0.], "B": [0., 1.]}, index=pd.to_datetime(["2024-01-31", "2024-02-29"]))
    returns, _ = long_short_from_signal(panel, signal, k=1)
    assert returns.loc["2024-02-29"] == pytest.approx(.02)
    assert returns.loc["2024-03-01"] == pytest.approx(-.02)
