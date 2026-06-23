"""Generate committed reference results (references/<name>.json), pinned to a fixed as-of date so
they stay reproducible as upstream data is appended. CI re-runs each replication and checks it still
reproduces these within tolerance (see tests/test_reference.py). Run after adding/changing a replication."""
import json, os
from replications import all_replications

AS_OF = "2024-12-31"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "references")

def main():
    os.makedirs(OUT, exist_ok=True)
    for name, r in all_replications().items():
        rc = r.report_card(as_of=AS_OF)
        rc["as_of"] = AS_OF
        with open(os.path.join(OUT, f"{name}.json"), "w") as f:
            json.dump(rc, f, indent=2)
        print(f"wrote references/{name}.json  (OOS {rc['oos_sharpe']}, {rc['verdict']})")

if __name__ == "__main__":
    main()
