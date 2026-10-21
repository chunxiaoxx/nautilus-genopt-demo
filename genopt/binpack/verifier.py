"""Independent verifier for binpack solver output.

Reads task.json + result.json, checks:
  - every item appears in exactly one bin (or in overflow)
  - no bin exceeds capacity
  - returns PASS/FAIL with details
"""
import json, sys

def verify(task_path="task.json", result_path="result.json"):
    task = json.load(open(task_path))
    result = json.load(open(result_path))
    bins = result.get("bins", [])
    overflow = result.get("overflow", [])
    cap = {b["id"]: b["capacity"] for b in task["bins"]}
    placed = set()
    load = {b["id"]: 0 for b in task["bins"]}
    for b in bins:
        for it in b.get("items", []):
            assert it not in placed, f"item {it} placed twice"
            placed.add(it)
        load[b["id"]] = sum(
            next(x["weight"] for x in task["items"] if x["id"] == i)
            for i in b.get("items", [])
        )
    overflow_ids = {o["id"] for o in overflow}
    task_ids = {x["id"] for x in task["items"]}
    missing = task_ids - placed - overflow_ids
    errs = []
    for b in bins:
        if load[b["id"]] > cap[b["id"]]:
            errs.append(f"bin {b['id']} overload: {load[b['id']]} > {cap[b['id']]}")
    if missing:
        errs.append(f"missing items: {sorted(missing)}")
    overlap = placed & overflow_ids
    if overlap:
        errs.append(f"items both placed and in overflow: {sorted(overlap)}")
    return {"verified": len(errs) == 0, "errors": errs,
            "n_bins_used": sum(1 for b in bins if b.get("items")),
            "utilization": round(sum(load.values()) / sum(cap.values()), 4)}

if __name__ == "__main__":
    print(json.dumps(verify(*(sys.argv[1:] if len(sys.argv) > 1 else [])), indent=2))