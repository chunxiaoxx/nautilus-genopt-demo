#!/usr/bin/env python3
"""Independent verifier for TSP-25 submissions."""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def total(path, cities):
    return sum(dist(cities[path[i]], cities[path[(i + 1) % len(path)]]) for i in range(len(path)))


def load(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def verify(submission_path: str, tolerance: float = 1.05) -> dict:
    """submission = jsonl: each line {id, path:[int...]}. pass if path ≤ baseline × 1.05."""
    instances = load(ROOT / "instances.jsonl")
    inst_map = {i["id"]: i for i in instances}
    subs = load(Path(submission_path))
    n = len(subs)
    passed = 0
    details = []
    for s in subs:
        iid = s["id"]
        if iid not in inst_map:
            details.append({"id": iid, "ok": False, "reason": "unknown_id"})
            continue
        inst = inst_map[iid]
        path = s["path"]
        if sorted(path) != list(range(25)):
            details.append({"id": iid, "ok": False, "reason": "invalid_permutation"})
            continue
        sl = total(path, inst["cities"])
        bl = inst["baseline_len"]
        ok = sl <= bl * tolerance
        if ok:
            passed += 1
        details.append({"id": iid, "ok": ok, "sub_len": round(sl, 4), "baseline": bl, "ratio": round(sl / bl, 4)})
    return {"total": n, "passed": passed, "pass_rate": passed / n if n else 0, "details": details[:10]}


if __name__ == "__main__":
    sub = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "submission.jsonl")
    res = verify(sub)
    print(json.dumps({"pass_rate": res["pass_rate"], "passed": res["passed"], "total": res["total"]}, indent=2))