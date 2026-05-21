#!/usr/bin/env python3
"""
BPO corpus validator.  Fails (exit 1) on:
  - any property not conforming to schema/property.schema.json
  - any relationship/discharged_by target in the BPO: namespace that does not resolve
  - the DASCP framework file failing its own schema (mappings/dascp.framework.schema.json)
  - the DASCP framework failing internal integrity (duplicate ids; mitigates_risks or
    risk.principle referencing a non-existent id within the framework)
  - any identifiers.external_refs.dascp[].id in a property not resolving to a real
    DASCP principle / risk / control id in the framework
ATK: targets are treated as an EXTERNAL namespace (the threat-class registry)
and are reported but not required to resolve yet.
Also prints the assumption-discharge ledger and basic graph stats.
"""
import json, glob, sys, os, collections
from jsonschema import Draft202012Validator

# Ensure UTF-8 stdout so assumption-ledger and reference output containing
# JSON-legal Unicode (math symbols, dashes, etc.) prints cleanly on Windows
# consoles whose default codec is cp1252.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

schema = json.load(open(f"{ROOT}/schema/property.schema.json", encoding="utf-8"))
validator = Draft202012Validator(schema)

props, ids = {}, set()
for f in sorted(glob.glob(f"{ROOT}/properties/*.json")):
    p = json.load(open(f, encoding="utf-8")); props[f] = p; ids.add(p["id"])

fail = False

# 0) DASCP framework: own schema, then internal integrity
print("== DASCP framework ==")
dascp_path        = f"{ROOT}/mappings/dascp.framework.json"
dascp_schema_path = f"{ROOT}/mappings/dascp.framework.schema.json"
dascp_ids = set()  # all P/R/C ids; used by reference closure below
if not (os.path.exists(dascp_path) and os.path.exists(dascp_schema_path)):
    fail = True
    print(f"  FAIL  missing mappings/dascp.framework.json or mappings/dascp.framework.schema.json")
else:
    dascp        = json.load(open(dascp_path,        encoding="utf-8"))
    dascp_schema = json.load(open(dascp_schema_path, encoding="utf-8"))
    shape_errs = list(Draft202012Validator(dascp_schema).iter_errors(dascp))
    if shape_errs:
        fail = True
        print("  FAIL  dascp.framework.json does not conform to dascp.framework.schema.json:")
        for e in shape_errs[:10]:
            print("       ->", list(e.path), e.message)
    else:
        print("  OK   shape (matches mappings/dascp.framework.schema.json)")

    # Internal integrity: id uniqueness across P/R/C
    seen, dupes = set(), []
    for grp in ("principles", "risks", "controls"):
        for item in dascp.get(grp, []):
            i = item["id"]
            if i in seen: dupes.append(i)
            seen.add(i)
    dascp_ids |= seen
    if dupes:
        fail = True
        print(f"  FAIL  duplicate DASCP ids: {sorted(set(dupes))}")
    else:
        print(f"  OK   {len(dascp_ids)} DASCP ids unique (P={len(dascp.get('principles',[]))}, "
              f"R={len(dascp.get('risks',[]))}, C={len(dascp.get('controls',[]))})")

    # Internal closure: risk.principle resolves; control.mitigates_risks each resolves
    principle_ids = {p["id"] for p in dascp.get("principles", [])}
    risk_ids      = {r["id"] for r in dascp.get("risks",      [])}
    bad_pr, bad_mr = [], []
    for r in dascp.get("risks", []):
        if r.get("principle") not in principle_ids:
            bad_pr.append((r["id"], r.get("principle")))
    for c in dascp.get("controls", []):
        for entry in c.get("mitigates_risks", []):
            rid = entry["risk"] if isinstance(entry, dict) else entry
            if rid not in risk_ids:
                bad_mr.append((c["id"], rid))
    if bad_pr:
        fail = True
        for rid, pid in bad_pr:
            print(f"  FAIL  risk {rid} -> principle {pid}  (no such principle in framework)")
    if bad_mr:
        fail = True
        for cid, rid in bad_mr:
            print(f"  FAIL  control {cid} -> mitigates_risks {rid}  (no such risk in framework)")
    if not (bad_pr or bad_mr):
        print(f"  OK   internal closure (every risk.principle and control.mitigates_risks resolves)")

# 1) schema
print("\n== schema ==")
for f, p in props.items():
    errs = list(validator.iter_errors(p))
    print(f"  {'OK ' if not errs else 'FAIL'} {p['id']:9} {p['slug']}")
    for e in errs[:5]:
        fail = True; print("       ->", list(e.path), e.message)

# 2) reference resolution
print("\n== references ==")
edge_count = collections.Counter()
ext = set()
dascp_xref_count = 0
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
    # DASCP cross-walk closure: every dascp[].id resolves to a real DASCP P/R/C
    for entry in p.get("identifiers", {}).get("external_refs", {}).get("dascp", []):
        dascp_xref_count += 1
        d_id = entry["id"]
        if d_id not in dascp_ids:
            fail = True
            print(f"  DANGLING {p['id']} --dascp({entry.get('relation','?')})--> {d_id}  (no such DASCP id)")
print("  all BPO: / DASCP: targets resolve" if not fail else "  REFERENCE ERRORS ABOVE")

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
print(f"  DASCP cross-walk entries from properties: {dascp_xref_count}")

print("\nRESULT:", "FAIL" if fail else "PASS (DAG closed over BPO: namespace; DASCP framework integral and closed)")
sys.exit(1 if fail else 0)
