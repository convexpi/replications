"""Generate one Colab notebook per replication (notebooks/<name>.ipynb). Each installs the package
from GitHub, runs the replication on live data, prints its report card, and plots the OOS split."""
import os
import nbformat as nbf
from replications import all_replications

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "notebooks")
REPO = "https://github.com/convexpi/replications"

def main():
    os.makedirs(OUT, exist_ok=True)
    for name, r in all_replications().items():
        module = r.__class__.__module__.split(".")[-1]
        colab = f"https://colab.research.google.com/github/convexpi/replications/blob/main/notebooks/{name}.ipynb"
        nb = nbf.v4.new_notebook(); c = []
        c.append(nbf.v4.new_markdown_cell(
            f"# {r.title} — reference replication\n\n"
            f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})\n\n"
            f"Replication of **{r.paper_title}** ({r.pub_year}). It recomputes the strategy from its "
            f"building blocks and runs the out-of-sample (McLean & Pontiff) test on live data.\n\n"
            f"Source: [`replications/catalog/{module}.py`]({REPO}/blob/main/replications/catalog/{module}.py)"))
        c.append(nbf.v4.new_code_cell(f"!pip -q install git+{REPO}.git"))
        c.append(nbf.v4.new_code_cell(
            "import pandas as pd, numpy as np, matplotlib.pyplot as plt\n"
            "from replications import all_replications\n"
            f"r = all_replications()[{name!r}]\n"
            "rc = r.report_card()\n"
            "print(rc['title'], '\\u2014 verdict:', rc['verdict'])\n"
            "print('IS Sharpe :', rc['in_sample_sharpe'])\n"
            "print('OOS Sharpe:', rc['oos_sharpe'], ' (decay:', rc['sharpe_decay'], ')')"))
        c.append(nbf.v4.new_code_cell(
            "s = r.build().dropna()\n"
            "(1 + s).cumprod().plot(logy=True, figsize=(9,4), title=rc['title'] + ' (recomputed)')\n"
            "plt.axvline(pd.Timestamp(f\"{r.pub_year}-01-01\"), color='crimson', ls='--', label='published')\n"
            "plt.legend(); plt.tight_layout(); plt.show()"))
        c.append(nbf.v4.new_markdown_cell(
            "## Your turn\nChange the split year, add costs, or fork the catalog module and improve "
            f"the replication — then open a PR at [{REPO}]({REPO})."))
        nb["cells"] = c
        nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
        nbf.write(nb, open(os.path.join(OUT, f"{name}.ipynb"), "w"))
        print(f"wrote notebooks/{name}.ipynb")

if __name__ == "__main__":
    main()
