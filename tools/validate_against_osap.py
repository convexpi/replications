"""
validate_against_osap.py — cross-check our recomputed replications against the Open Source Asset
Pricing (Chen & Zimmermann) gold-standard long-short portfolio returns.

For each replication that maps to an OSAP predictor, we resample our (free, Ken-French-built) series
to monthly, align with OSAP's published single-name long-short returns, and report the correlation.
A high correlation means our cheap reconstruction tracks the canonical single-name anomaly — an
external check on top of CI. Writes osap_validation.json (committed); gen_benchmark.py merges it into
the leaderboard so /replications can show a "matches OSAP" stamp + a replication-quality tier.

OSAP data: PredictorLSretWide.csv from the public OSAP release (downloaded once, cached). Requires
`gdown`. Run occasionally; the result is committed so CI / the website never touch OSAP at runtime.

    python tools/validate_against_osap.py
"""
from __future__ import annotations
import json, os
import numpy as np
import pandas as pd
from replications import all_replications

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.expanduser("~/.convexpi/osap/PredictorLSretWide.csv")
OSAP_FILE_ID = "10sOryk_ddjkXagaajTKUk1nwJs2ZLRiI"   # Portfolios/Full Sets OP/PredictorLSretWide.csv

# our replication name -> OSAP predictor acronym (None = no cross-sectional OSAP equivalent)
OSAP_MAP = {
    "jegadeesh_titman_momentum":             "Mom12m",
    "fama_french_hml":                       "BM",
    "fama_french_smb":                       "Size",
    "novy_marx_profitability":               "GP",
    "cooper_gulen_schill_investment":        "AssetGrowth",
    "jegadeesh_short_term_reversal":         "STreversal",
    "debondt_thaler_long_term_reversal":     "LRreversal",
    "moskowitz_grinblatt_industry_momentum": "IndMom",
    "moskowitz_ooi_pedersen_trend":          None,   # time-series, not a cross-sectional sort
}


def _tier(corr: float | None) -> str:
    if corr is None:
        return "unverified"
    # Our free Ken-French *factor* series vs OSAP's *single-name decile* sorts are different
    # constructions of the same anomaly, so a genuine match lands around 0.4-0.8, not ~1.0.
    if abs(corr) >= 0.7:
        return "clear"
    if abs(corr) >= 0.4:
        return "partial"
    return "weak"


def _load_osap() -> pd.DataFrame:
    if not os.path.exists(CACHE):
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        import gdown
        gdown.download(id=OSAP_FILE_ID, output=CACHE, quiet=True)
    df = pd.read_csv(CACHE)
    df["date"] = pd.to_datetime(df["date"]).dt.to_period("M")
    return df.set_index("date")


def _monthly(series: pd.Series) -> pd.Series:
    s = series.dropna()
    s.index = pd.to_datetime(s.index)
    m = (1 + s).resample("ME").prod() - 1
    m.index = m.index.to_period("M")
    return m


def main():
    osap = _load_osap()
    out = {}
    for name, rep in all_replications().items():
        acr = OSAP_MAP.get(name)
        rec = {"osap_acronym": acr, "correlation": None, "n_months": 0, "quality": "unverified"}
        if acr and acr in osap.columns:
            ours = _monthly(rep.build())
            theirs = osap[acr].dropna()
            j = pd.concat([ours.rename("o"), theirs.rename("t")], axis=1).dropna()
            if len(j) >= 36:
                corr = float(j["o"].corr(j["t"]))
                rec.update(correlation=round(corr, 3), n_months=len(j), quality=_tier(corr))
        out[name] = rec
        print(f"{name:40} OSAP={str(acr):<12} corr={rec['correlation']}  n={rec['n_months']}  {rec['quality']}")

    with open(os.path.join(ROOT, "osap_validation.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote osap_validation.json")


if __name__ == "__main__":
    main()
