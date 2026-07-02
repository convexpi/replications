"""
Data shim — declared, cached, free data sources.

Replications *declare* the data they need (by key) and call these loaders in ``build()``. We only
use free, redistributable sources, and we ship **code, not data**: each loader downloads on demand
and caches under ``~/.convexpi/replications-cache`` so repeated runs (and CI) are fast.

Keys (use these in a replication's ``data_sources``):
  kenfrench:F-F_Research_Data_Factors_daily   market, SMB, HML, RF
  kenfrench:F-F_Momentum_Factor_daily         the Mom (WML) factor
  kenfrench:6_Portfolios_2x3_daily            6 size x book-to-market building blocks
  kenfrench:6_Portfolios_ME_Prior_12_2_daily  6 size x prior-return building blocks
  kenfrench:12_Industry_Portfolios_daily      12 industry portfolios
  yfinance:<TICKERS>                          individual stock prices (Colab/online only)
"""
from __future__ import annotations
import os
import pandas as pd

CACHE = os.path.expanduser("~/.convexpi/replications-cache")
os.makedirs(CACHE, exist_ok=True)


def kenfrench(dataset: str, start: str = "1926-01-01") -> pd.DataFrame:
    """Load a Ken-French dataset as decimal returns (the source is in percent).

    Cached to parquet/CSV. Uses pandas-datareader; the first table in the dataset is returned with
    columns stripped of whitespace.
    """
    safe = dataset.replace("/", "_")
    path = os.path.join(CACHE, f"kf_{safe}.csv")
    if os.path.exists(path):
        df = pd.read_csv(path, index_col=0, parse_dates=True)
    else:
        from pandas_datareader import data as pdr
        raw = pdr.DataReader(dataset, "famafrench", start=start)[0]
        df = raw.copy()
        df.index = pd.to_datetime(df.index.astype(str))
        df.columns = [str(c).strip() for c in df.columns]
        df = df / 100.0                      # percent -> decimal
        df.to_csv(path)
    return df


def yfinance_prices(tickers: list[str] | str, start: str = "2005-01-01") -> pd.DataFrame:
    """Adjusted close prices for a list of tickers (online only; intended for Colab)."""
    import yfinance as yf
    if isinstance(tickers, str):
        tickers = tickers.split()
    px = yf.download(tickers, start=start, auto_adjust=True, progress=False)["Close"]
    return px


def yfinance_dollar_volume(tickers: list[str] | str, start: str = "2005-01-01") -> pd.DataFrame:
    """Daily dollar volume (adjusted close × share volume) for a list of tickers (online only)."""
    import yfinance as yf
    if isinstance(tickers, str):
        tickers = tickers.split()
    raw = yf.download(tickers, start=start, auto_adjust=True, progress=False)
    return raw["Close"] * raw["Volume"]
