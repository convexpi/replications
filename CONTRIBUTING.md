# Contributing a replication

Thank you for helping build an open, trustworthy library of strategy replications! The bar is simple:
**recompute the strategy from building blocks, score it honestly out of sample, and prove it
reproduces.**

## The contract
Add one module under `replications/catalog/<your_strategy>.py` with a subclass of `Replication`:

```python
from ..base import Replication
from .. import data

class MyStrategy(Replication):
    def __init__(self):
        super().__init__(
            name="author_year_strategy",          # stable slug
            title="Human Title",
            paper_title="The paper being replicated",
            paper_doi="10.xxxx/...",               # links to the paper's wiki
            pub_year=1993,                          # the in-sample / out-of-sample split
            data_sources=["kenfrench:..."],         # declared, free data
            references=["Author (year) — Title — Journal"],
            authors=["Your Name"],                  # attribution / provenance
        )

    def build(self):
        # Recompute the strategy from underlying data and return a daily/monthly return Series.
        ...

    # Optional: return the (rebalance x asset) weight matrix to enable turnover / net-of-cost.
    # def weights(self): ...
```

Reuse `replications.data` (loaders), `replications.portfolios` (long-short formation), and
`replications.costs` (turnover / net-of-cost). See the existing catalog modules as templates.

## Rules
- **Recompute, don't read a finished factor.** Reconstruct from portfolios/prices.
- **Free, redistributable data only**, declared in `data_sources`. Ship code, not data.
- **Be honest.** If a strategy can't be faithfully reproduced from the available data (e.g. a
  single-name effect from aggregated portfolios), don't dress it up — say so or omit it.
- **Multiple variants welcome.** A different lookback, universe, or weighting is a *new* module with
  its own name and attribution, benchmarked side by side.

## Before you open a PR
```bash
pip install -e ".[dev]"
python tools/gen_references.py     # writes references/<name>.json (your committed reference result)
python tools/gen_benchmark.py      # refresh the leaderboard
python tools/gen_notebooks.py      # generate your Colab notebook
pytest -q                          # contract + reference reproduction must pass
```
Commit the new module, its `references/<name>.json`, its `notebooks/<name>.ipynb`, and the refreshed
`BENCHMARK.md` / `results.json`. CI runs the same checks on your PR; a maintainer reviews and merges
to `main`.
