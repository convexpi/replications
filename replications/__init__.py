"""convexpi-replications — open, verified reference replications of canonical strategies."""
from .base import Replication, sharpe, max_drawdown
from .registry import all_replications
from . import data, portfolios, costs

__all__ = ["Replication", "sharpe", "max_drawdown", "all_replications", "data", "portfolios", "costs"]
__version__ = "0.1.0"
