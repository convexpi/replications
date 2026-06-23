"""Append a dated snapshot of the leaderboard to history/leaderboard.jsonl — turning the verdicts
into a living time series. Run on a schedule by .github/workflows/leaderboard.yml (quarterly)."""
import json, os, datetime
from replications import all_replications

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "history")

def main():
    os.makedirs(HIST, exist_ok=True)
    rows = [r.report_card() for r in all_replications().values()]
    snap = {
        "date": datetime.date.today().isoformat(),
        "strategies": [
            {"name": r["name"], "oos_sharpe": r["oos_sharpe"],
             "recent_sharpe": r["recent_sharpe"], "verdict": r["verdict"]}
            for r in sorted(rows, key=lambda x: x["name"])
        ],
    }
    path = os.path.join(HIST, "leaderboard.jsonl")
    with open(path, "a") as f:
        f.write(json.dumps(snap) + "\n")
    print(f"appended snapshot {snap['date']} ({len(rows)} strategies) -> {path}")

if __name__ == "__main__":
    main()
