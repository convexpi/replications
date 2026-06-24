import json, os, pytest
from replications import all_replications

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "references")
# Online (live-data) replications drift with the data, so they carry no committed reference.
REPS = {k: v for k, v in all_replications().items() if not v.online}
TOL = 0.04   # Sharpe tolerance vs the committed reference (source data is percent-rounded)

@pytest.mark.parametrize("name", list(REPS))
def test_reproduces_reference(name):
    path = os.path.join(REF, f"{name}.json")
    assert os.path.exists(path), f"missing reference for {name} (run tools/gen_references.py)"
    ref = json.load(open(path))
    rc = REPS[name].report_card(as_of=ref["as_of"])
    for k in ("in_sample_sharpe", "oos_sharpe"):
        if ref[k] is None:
            continue
        assert abs(rc[k] - ref[k]) <= TOL, f"{name}.{k} drifted: {ref[k]} -> {rc[k]}"
    assert rc["verdict"] == ref["verdict"], f"{name} verdict changed: {ref['verdict']} -> {rc['verdict']}"
