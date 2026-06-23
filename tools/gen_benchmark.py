"""Build the leaderboard: BENCHMARK.md + results.json from live report cards (latest data)."""
import json, os
from replications import all_replications

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://github.com/convexpi/replications"

def main():
    rows = [r.report_card() for r in all_replications().values()]
    with open(os.path.join(ROOT, "results.json"), "w") as f:
        json.dump(rows, f, indent=2)
    L = ["# Replication leaderboard — out-of-sample",
         "",
         "Canonical strategies, each **recomputed from underlying building blocks** and scored out of",
         "sample by splitting at the paper's publication year (the McLean & Pontiff test). Regenerate",
         "with `python tools/gen_benchmark.py`. Verdicts are honest, not editorial.",
         "",
         "| Strategy | Paper | Pub. | IS Sharpe | OOS Sharpe | Net OOS | Decay | Verdict |",
         "|---|---|---:|---:|---:|---:|---:|---|"]
    caveats = []
    for r in sorted(rows, key=lambda x: x["name"]):
        is_s = "—" if r["in_sample_sharpe"] is None else f"{r['in_sample_sharpe']:.2f}"
        net = "—" if r["net_oos_sharpe"] is None else f"{r['net_oos_sharpe']:.2f}"
        d = r["sharpe_decay"]
        dec = "—" if d is None else ("improved" if d < 0 else f"{d:.0%}")
        mark = ""
        if r.get("caveat"):
            mark = f" [^{len(caveats) + 1}]"
            caveats.append((len(caveats) + 1, r["title"], r["caveat"]))
        L.append(f"| {r['title']}{mark} | {r['paper_title'].split(':')[0]} | {r['pub_year']} | {is_s} | "
                 f"{r['oos_sharpe']:.2f} | {net} | {dec} | {r['verdict']} |")
    L.append("")
    for n, title, text in caveats:
        L.append(f"[^{n}]: **{title}** — {text}")
    L += ["", f"*Open replications maintained at [{SITE}]({SITE}) — fork, improve, and PR.*", ""]
    with open(os.path.join(ROOT, "BENCHMARK.md"), "w") as f:
        f.write("\n".join(L))
    print(f"wrote BENCHMARK.md and results.json ({len(rows)} strategies)")

if __name__ == "__main__":
    main()
