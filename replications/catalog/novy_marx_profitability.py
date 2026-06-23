"""Profitability (RMW) — reconstructed from the 6 size x operating-profitability portfolios.

Robust-minus-weak: long high-profitability firms, short low-profitability ones. This is the
profitability premium (Novy-Marx 2013; the RMW factor of Fama-French 2015), rebuilt from the
component portfolios exactly as the factor is constructed.
"""
from ..base import Replication
from .. import data


class NovyMarxProfitability(Replication):
    def __init__(self):
        super().__init__(
            name="novy_marx_profitability", title="Profitability (RMW)",
            paper_title="The Other Side of Value: The Gross Profitability Premium",
            paper_doi="10.1016/j.jfineco.2013.01.003", pub_year=2013,
            data_sources=["kenfrench:6_Portfolios_ME_OP_2x3_daily"],
            references=[
                "Novy-Marx, R. (2013) — The Other Side of Value: The Gross Profitability Premium — JFE",
                "Fama, E. & French, K. (2015) — A Five-Factor Asset Pricing Model — JFE",
            ],
        )

    def build(self):
        p = data.kenfrench("6_Portfolios_ME_OP_2x3_daily")
        # RMW = (avg of the two HIGH-profitability corners) - (avg of the two LOW corners)
        return 0.5 * (p["SMALL HiOP"] + p["BIG HiOP"]) - 0.5 * (p["SMALL LoOP"] + p["BIG LoOP"])
