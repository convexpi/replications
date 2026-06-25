"""Build the leaderboard: BENCHMARK.md + results.json from live report cards (latest data)."""
import json, os
from replications import all_replications

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://github.com/convexpi/replications"

def main():
    rows = [r.report_card() for r in all_replications().values()]

    # Merge the OSAP cross-validation (refreshed separately by tools/validate_against_osap.py and
    # committed) so the leaderboard/site can show agreement with the gold-standard returns offline.
    osap_path = os.path.join(ROOT, "osap_validation.json")
    osap = json.load(open(osap_path)) if os.path.exists(osap_path) else {}
    for r in rows:
        v = osap.get(r["name"], {})
        r["osap_acronym"] = v.get("osap_acronym")
        r["osap_correlation"] = v.get("correlation")
        r["replication_quality"] = v.get("quality", "unverified")

    with open(os.path.join(ROOT, "results.json"), "w") as f:
        json.dump(rows, f, indent=2)
    L = ["# Replication leaderboard — out-of-sample",
         "",
         "Canonical strategies, each **recomputed from underlying building blocks** and scored out of",
         "sample by splitting at the paper's publication year (the McLean & Pontiff test). The *OSAP*",
         "column reports the correlation of our reconstruction with the Open Source Asset Pricing",
         "single-name long-short returns (a different construction, so 0.4-0.8 is a genuine match).",
         "Regenerate with `python tools/gen_benchmark.py`. Verdicts are honest, not editorial.",
         "",
         "| Strategy | Paper | Pub. | IS Sharpe | OOS Sharpe | Decay | Verdict | OSAP |",
         "|---|---|---:|---:|---:|---:|---|---|"]
    caveats = []
    for r in sorted(rows, key=lambda x: x["name"]):
        is_s = "—" if r["in_sample_sharpe"] is None else f"{r['in_sample_sharpe']:.2f}"
        d = r["sharpe_decay"]
        dec = "—" if d is None else ("improved" if d < 0 else f"{d:.0%}")
        corr, qual = r.get("osap_correlation"), r.get("replication_quality")
        # Display the *magnitude* of agreement: OSAP signs some predictors by their raw signal
        # (e.g. BetaFP is an ascending-beta sort), opposite to our economic-return orientation, so a
        # negative correlation is a sign convention, not a worse match. Tier is already abs-based.
        osap = "—" if corr is None else f"{qual} ({abs(corr):.2f})"
        mark = ""
        if r.get("caveat"):
            mark = f" [^{len(caveats) + 1}]"
            caveats.append((len(caveats) + 1, r["title"], r["caveat"]))
        L.append(f"| {r['title']}{mark} | {r['paper_title'].split(':')[0]} | {r['pub_year']} | {is_s} | "
                 f"{r['oos_sharpe']:.2f} | {dec} | {r['verdict']} | {osap} |")
    L.append("")
    for n, title, text in caveats:
        L.append(f"[^{n}]: **{title}** — {text}")
    L += ["", f"*Open replications maintained at [{SITE}]({SITE}) — fork, improve, and PR.*", ""]
    with open(os.path.join(ROOT, "BENCHMARK.md"), "w") as f:
        f.write("\n".join(L))
    print(f"wrote BENCHMARK.md and results.json ({len(rows)} strategies)")

if __name__ == "__main__":
    main()
