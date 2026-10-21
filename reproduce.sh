#!/usr/bin/env bash
# One command. Falsify our claims in under a minute. Pure stdlib Python 3.8+.
set -euo pipefail
cd "$(dirname "$0")"

echo "=============================================================="
echo " Nautilus GenOpt demo — independent re-verification"
echo "=============================================================="

echo
echo "[1/2] TSP-25 — verifying 100 submitted tours"
python3 genopt/tsp25/verifier.py genopt/tsp25/submission.jsonl

echo
echo "[2/2] Bin packing — running solver + independent verifier"
cd genopt/binpack
python3 solver.py >/dev/null
python3 verifier.py

cd ../..
echo
echo "=============================================================="
echo " Done. If anything above says FAIL, we are wrong."
echo " Fingerprints (sha256):"
find . -type f \( -name '*.jsonl' -o -name '*.json' -o -name '*.py' \) \
  | sort | xargs sha256sum
echo "=============================================================="