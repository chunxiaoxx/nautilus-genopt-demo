import json, hashlib, time

def solve(task):
    items = sorted(task["items"], key=lambda x: -x["weight"])
    bins = [{"id": b["id"], "capacity": b["capacity"], "load": 0, "items": []} for b in task["bins"]]
    overflow = []
    for it in items:
        placed = False
        for b in bins:
            if b["load"] + it["weight"] <= b["capacity"]:
                b["load"] += it["weight"]
                b["items"].append(it["id"])
                placed = True
                break
        if not placed:
            overflow.append(it)
    return bins, overflow

if __name__ == "__main__":
    task = json.load(open("task.json"))
    t0 = time.time()
    bins, overflow = solve(task)
    dt = (time.time() - t0) * 1000
    total_load = sum(b["load"] for b in bins)
    util = total_load / sum(b["capacity"] for b in bins)
    sig = hashlib.sha256(json.dumps(task, sort_keys=True).encode()).hexdigest()[:12]
    result = {
        "task_sig": sig,
        "solver": "first-fit-decreasing",
        "n_bins_used": sum(1 for b in bins if b["items"]),
        "utilization": round(util, 4),
        "elapsed_ms": round(dt, 3),
        "bins": bins,
        "overflow": overflow,
        "verifier": "pending_independent_check"
    }
    with open("result.json", "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: result[k] for k in ["task_sig","n_bins_used","utilization","elapsed_ms","verifier"]}, indent=2))
