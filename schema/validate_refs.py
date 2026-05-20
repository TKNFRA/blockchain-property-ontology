#!/usr/bin/env python3
"""
BPO corpus validator.  Fails (exit 1) on:
  - any property not conforming to schema/property.schema.json
  - any relationship/discharged_by target in the BPO: namespace that does not resolve
ATK: targets are treated as an EXTERNAL namespace (the threat-class registry)
and are reported but not required to resolve yet.
Also prints the assumption-discharge ledger and basic graph stats.
"""
import json, glob, sys, collections
from jsonschema import Draft202012Validator

ROOT = __file__.rsplit("/", 2)[0] if "/" in __file__ else "."
schema = json.load(open(f"{ROOT}/schema/property.schema.json"))
validator = Draft202012Validator(schema)

props, ids = {}, set()
for f in sorted(glob.glob(f"{ROOT}/properties/*.json")):
    p = json.load(open(f)); props[f] = p; ids.add(p["id"])

fail = False

# 1) schema
print("== schema ==")
for f, p in props.items():
    errs = list(validator.iter_errors(p))
    print(f"  {'OK ' if not errs else 'FAIL'} {p['id']:9} {p['slug']}")
    for e in errs[:5]:
        fail = True; print("       ->", list(e.path), e.message)

# 2) reference resolution
print("\n== references ==")
edge_count = collections.Counter()
ext = set()
def check(src, kind, tgt):
    global fail
    if tgt.startswith("BPO:"):
        if tgt not in ids:
            fail = True; print(f"  DANGLING {src} --{kind}--> {tgt}  (no such BPO record)")
    elif tgt.startswith("ATK:"):
        ext.add(tgt)
    else:
        fail = True; print(f"  BADNS    {src} --{kind}--> {tgt}  (unknown namespace)")

for p in props.values():
    for r in p.get("relationships", []):
        edge_count[r["type"]] += 1
        check(p["id"], r["type"], r["target"])
    for a in p.get("assumptions", []):
        d = a.get("discharged_by")
        if d:
            check(p["id"], "dischargedBy", d)
print("  all BPO: targets resolve" if not fail else "  REFERENCE ERRORS ABOVE")

# 3) assumption ledger
print("\n== undischarged assumptions (accepted hypotheses) ==")
for p in props.values():
    for a in p.get("assumptions", []):
        if a.get("discharged_by") is None:
            print(f"  {p['id']:9} [{a['kind']}] {a['statement'][:80]}")

# 4) stats
print("\n== graph stats ==")
print(f"  properties: {len(ids)}")
print(f"  edges by type: {dict(edge_count)}")
print(f"  external ATK: targets referenced (Phase-2 registry): {len(ext)}")
for a in sorted(ext): print(f"    - {a}")

print("\nRESULT:", "FAIL" if fail else "PASS (DAG closed over BPO: namespace)")
sys.exit(1 if fail else 0)
