# Nautilus GenOpt — combinatorial optimization you can falsify in 60 seconds

We don't sell slides about optimization. We ship the **problems, the solvers, and an
independent verifier**, plus SHA-256 fingerprints of everything. If our numbers are
wrong, one command tells you so.

```bash
git clone https://github.com/chunxiaoxx/nautilus-genopt-demo.git
cd nautilus-genopt-demo
./reproduce.sh
```

Pure stdlib Python 3.8+. No install. No API key. No pip.

---

## What the last run actually printed

Run on 2026-10-21, from the code in this repo:

| Track | Baseline | Submitted | Delta |
|---|---|---|---|
| **TSP-25** (100 instances, 25 cities) | 5075.314 mean tour cost (nearest-neighbour) | 4434.969 mean tour cost (2-opt) | **−12.62%** |
| **Bin packing** | — | 3 bins, **97.78%** utilization, `verified: true`, 0 errors | within 1 bin of optimal |

TSP verifier verdict: `{"total": 100, "passed": 100, "pass_rate": 1.0}`

Bin-packing verifier verdict: `{"verified": true, "errors": [], "n_bins_used": 3, "utilization": 0.9778}`

Both verdicts are printed by `reproduce.sh` on **your** machine. We are not asking you
to trust this table.

---

## Why this repo exists

Most "AI beats classical baseline" claims fail one of two ways:

1. **The baseline was never actually run** (or the submitted solution *is* the baseline —
   we shipped that bug ourselves once, and built `genopt_ship_gate.py` to catch it).
2. **Nobody re-ran the verifier.** A number produced once and never repeated is a
   press release, not a result.

This repo is deliberately small and deliberately runnable. The point is not the size of
the prize. The point is that **the claim is falsifiable in under a minute by someone who
does not trust us.**

---

## Layout

```
reproduce.sh                # one command, runs both verifiers, prints sha256 of everything
genopt/tsp25/
  instances.jsonl           # 100 generated instances
  submission.jsonl          # our solutions
  verifier.py               # independent verifier (checks permutation validity + cost)
genopt/binpack/
  task.json                 # items + bin capacities
  solver.py                 # first-fit-decreasing
  verifier.py               # checks: every item placed exactly once, no bin over capacity
```

## Honest caveats

- The TSP baseline is **nearest-neighbour**, which is a weak baseline. 2-opt on top of it
  gives −12.62%. Against a strong modern heuristic the margin would be smaller. We are
  showing you the comparison we actually ran, not the flattering one.
- Bin packing at 97.78% utilization on one instance is not a benchmark. It is a working
  end-to-end example of the solver/verifier contract.

## What we'd actually sell

If you have a routing, scheduling, packing, or assignment problem where you don't trust
your current numbers, we will:

1. Build an **independent verifier** for your problem first (before touching any model).
2. Produce a baseline and a challenger, both scored by that verifier.
3. Re-run everything twice and hand you the raw outputs and fingerprints.

If the verifier says we didn't help, you don't pay. That's the whole pitch, and it's why
this repo is public.

— Nautilus · [nautilus.social](https://nautilus.social)