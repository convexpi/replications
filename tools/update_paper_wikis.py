"""Inject a 'Reference replication' section into each replicated paper's wiki (DB wiki_markdown,
keyed by DOI). Closes the loop: a paper's wiki points to its runnable, OOS-scored replication +
Colab. Idempotent — replaces the section if already present.

    SUPABASE_URL=... SUPABASE_SERVICE_KEY=... python tools/update_paper_wikis.py [--dry-run]
"""
import argparse, datetime, json, os, sys, urllib.parse, urllib.request
from replications import all_replications

URL = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL") or ""
KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
REPO = "https://github.com/convexpi/replications"
MARK = "## Reference replication on ConvexPi"


def section(r) -> str:
    rc = r.report_card()
    name = r.name
    module = r.__class__.__module__.split(".")[-1]
    colab = f"https://colab.research.google.com/github/convexpi/replications/blob/main/notebooks/{name}.ipynb"
    code = f"{REPO}/blob/main/replications/catalog/{module}.py"
    is_s = "—" if rc["in_sample_sharpe"] is None else f"{rc['in_sample_sharpe']:+.2f}"
    rows = (f"| In-sample (pre-{r.pub_year}) | {is_s} |\n"
            f"| Out-of-sample (≥ {r.pub_year}) | {rc['oos_sharpe']:+.2f} |\n"
            f"| Last 10 years | {rc['recent_sharpe']:+.2f} |")
    return (f"{MARK}\n\n"
            f"An open, verified replication of this strategy is maintained at "
            f"[convexpi/replications]({REPO}). It recomputes the strategy from underlying building "
            f"blocks and scores it out of sample (the McLean & Pontiff test):\n\n"
            f"| Period | Annualized Sharpe |\n|---|---|\n{rows}\n\n"
            f"**Verdict: {rc['verdict']}.** "
            f"Run it on live data in [Colab]({colab}) · [view the code]({code})\n")


def get_wiki(doi):
    u = f"{URL}/rest/v1/papers?select=id,wiki_markdown,wiki_generated_at&doi=eq.{urllib.parse.quote(doi)}"
    req = urllib.request.Request(u, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    rows = json.loads(urllib.request.urlopen(req).read())
    return rows[0] if rows else None


def patch(pid, markdown):
    body = json.dumps({"wiki_markdown": markdown,
                       "wiki_generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}).encode()
    req = urllib.request.Request(f"{URL}/rest/v1/papers?id=eq.{pid}", data=body, method="PATCH",
        headers={"apikey": KEY, "Authorization": f"Bearer {KEY}",
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    urllib.request.urlopen(req).read()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not URL or not KEY:
        sys.exit("Set SUPABASE_URL and SUPABASE_SERVICE_KEY.")
    for name, r in all_replications().items():
        if not r.paper_doi:
            continue
        row = get_wiki(r.paper_doi)
        if not row:
            print(f"[skip] {name}: no paper with doi {r.paper_doi}")
            continue
        sec = section(r)
        existing = row.get("wiki_markdown") or ""
        if MARK in existing:                      # replace existing section
            existing = existing.split(MARK)[0].rstrip()
        merged = (existing.rstrip() + "\n\n" + sec) if existing else sec
        print(f"[{name}] -> doi {r.paper_doi}  ({'dry' if args.dry_run else 'write'}, {len(merged)} chars)")
        if not args.dry_run:
            patch(row["id"], merged)
    print("done" if not args.dry_run else "(dry run)")


if __name__ == "__main__":
    main()
