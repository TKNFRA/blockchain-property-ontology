#!/usr/bin/env python3
"""
BPO corpus validator.  Fails (exit 1) on:
  - any property not conforming to schema/property.schema.json
  - any relationship/discharged_by target in the BPO: namespace that does not resolve
  - the DASCP framework file failing its own schema or internal integrity
    (duplicate ids; mitigates_risks or risk.principle referencing a non-existent id within the framework)
  - any identifiers.external_refs.dascp[].id in a property not resolving in DASCP framework
  - the Operations catalogue failing its own schema or internal integrity
    (duplicate OP ids; iso20022_intents referencing a non-existent ISO 20022 id;
    governs_properties referencing a non-existent BPO record)
  - the ISO 20022 framework file failing its own schema or internal integrity
    (duplicate ids across messages ∪ components ∪ elements)
  - any identifiers.external_refs.iso20022[].id in a property not resolving in ISO 20022 framework
    (depth-1 cross-walk closure)
  - any formalization.bindings[].element in a property not resolving in ISO 20022 framework
    (depth-2 element closure)
  - any formalization.bindings[].symbol in a property not satisfying the symbol-in-formalization check
    (depth-2 symbol closure: structured lookup against formalization.symbols if present, else
    whole-token regex against formalization.signature, case-sensitive)
ATK: targets are treated as an EXTERNAL namespace (the threat-class registry)
and are reported but not required to resolve yet.
Also prints the assumption-discharge ledger and basic graph stats.
"""
import json, glob, sys, os, re, collections
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


# ---------------------------------------------------------------------------
# Helper: depth-2 symbol-in-formalization check.
# Tier 1 (preferred): structured lookup against formalization.symbols.
# Tier 2 (fallback): whole-token regex against formalization.signature only.
# Both tiers are case-sensitive; no near-match. A binding that silently
# mis-resolves is worse than no binding, so this check is strict by design.
# ---------------------------------------------------------------------------
def symbol_in_formalization(symbol, formalization):
    if not isinstance(formalization, dict):
        return False, "property has no formalization object"
    declared = formalization.get("symbols")
    if isinstance(declared, list) and declared:
        if symbol in declared:
            return True, "exact match in formalization.symbols"
        return False, (
            f"'{symbol}' not in formalization.symbols (the structured list is authoritative when present)"
        )
    signature = formalization.get("signature", "")
    if not signature:
        return False, "property has neither formalization.symbols nor formalization.signature"
    # Whole-token: bounded by non-identifier characters or string ends.
    pattern = r"(?<![A-Za-z0-9_])" + re.escape(symbol) + r"(?![A-Za-z0-9_])"
    if re.search(pattern, signature):
        return True, "whole-token match in formalization.signature"
    return False, (
        f"'{symbol}' is not a whole-token match in formalization.signature "
        "(near-matches like substrings inside other identifiers are intentionally rejected)"
    )


# ---------------------------------------------------------------------------
# Load property schema + records
# ---------------------------------------------------------------------------
schema    = json.load(open(f"{ROOT}/schema/property.schema.json", encoding="utf-8"))
validator = Draft202012Validator(schema)

props, ids = {}, set()
for f in sorted(glob.glob(f"{ROOT}/properties/*.json")):
    p = json.load(open(f, encoding="utf-8")); props[f] = p; ids.add(p["id"])

fail = False


# ---------------------------------------------------------------------------
# Section 0 — DASCP framework  (unchanged from the DASCP integration)
# ---------------------------------------------------------------------------
print("== DASCP framework ==")
dascp_path        = f"{ROOT}/mappings/dascp.framework.json"
dascp_schema_path = f"{ROOT}/mappings/dascp.framework.schema.json"
dascp_ids = set()
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


# ---------------------------------------------------------------------------
# Section 0b — ISO 20022 framework  (loaded BEFORE operations so that the
# operations catalogue's iso20022_intents closure can resolve against it).
# ---------------------------------------------------------------------------
print("\n== ISO 20022 framework ==")
iso_path        = f"{ROOT}/mappings/iso20022.framework.json"
iso_schema_path = f"{ROOT}/mappings/iso20022.framework.schema.json"
iso_ids = set()
if not (os.path.exists(iso_path) and os.path.exists(iso_schema_path)):
    fail = True
    print(f"  FAIL  missing mappings/iso20022.framework.json or mappings/iso20022.framework.schema.json")
else:
    iso        = json.load(open(iso_path,        encoding="utf-8"))
    iso_schema = json.load(open(iso_schema_path, encoding="utf-8"))
    shape_errs = list(Draft202012Validator(iso_schema).iter_errors(iso))
    if shape_errs:
        fail = True
        print("  FAIL  iso20022.framework.json does not conform to iso20022.framework.schema.json:")
        for e in shape_errs[:10]:
            print("       ->", list(e.path), e.message)
    else:
        print("  OK   shape (matches mappings/iso20022.framework.schema.json)")

    seen, dupes = set(), []
    for grp in ("messages", "components", "elements"):
        for item in iso.get(grp, []):
            i = item["id"]
            if i in seen: dupes.append(i)
            seen.add(i)
    iso_ids |= seen
    if dupes:
        fail = True
        print(f"  FAIL  duplicate ISO 20022 ids: {sorted(set(dupes))}")
    else:
        print(f"  OK   {len(iso_ids)} ISO 20022 ids unique "
              f"(msg={len(iso.get('messages',[]))}, "
              f"cmp={len(iso.get('components',[]))}, "
              f"elem={len(iso.get('elements',[]))})")


# ---------------------------------------------------------------------------
# Section 0a — Operations catalogue  (loaded AFTER ISO 20022 and after the
# property corpus so its cross-framework closures can resolve).
# ---------------------------------------------------------------------------
print("\n== Operations catalogue ==")
ops_path        = f"{ROOT}/mappings/operations.catalogue.json"
ops_schema_path = f"{ROOT}/mappings/operations.catalogue.schema.json"
op_ids = set()
if not (os.path.exists(ops_path) and os.path.exists(ops_schema_path)):
    fail = True
    print(f"  FAIL  missing mappings/operations.catalogue.json or mappings/operations.catalogue.schema.json")
else:
    ops        = json.load(open(ops_path,        encoding="utf-8"))
    ops_schema = json.load(open(ops_schema_path, encoding="utf-8"))
    shape_errs = list(Draft202012Validator(ops_schema).iter_errors(ops))
    if shape_errs:
        fail = True
        print("  FAIL  operations.catalogue.json does not conform to operations.catalogue.schema.json:")
        for e in shape_errs[:10]:
            print("       ->", list(e.path), e.message)
    else:
        print("  OK   shape (matches mappings/operations.catalogue.schema.json)")

    seen, dupes = set(), []
    for o in ops.get("operations", []):
        if o["id"] in seen: dupes.append(o["id"])
        seen.add(o["id"])
    op_ids |= seen
    if dupes:
        fail = True
        print(f"  FAIL  duplicate OP ids: {sorted(set(dupes))}")
    else:
        print(f"  OK   {len(op_ids)} OP ids unique")

    # Cross-framework closure: operations.iso20022_intents -> ISO 20022 framework
    bad_intents, intent_count = [], 0
    for o in ops.get("operations", []):
        for intent in o.get("iso20022_intents", []):
            intent_count += 1
            if intent not in iso_ids:
                bad_intents.append((o["id"], intent))
    if bad_intents:
        fail = True
        for oid, intent in bad_intents:
            print(f"  FAIL  operation {oid} -> iso20022_intents {intent}  (no such id in ISO 20022 framework)")
    else:
        print(f"  OK   operations -> ISO 20022 closure ({intent_count} iso20022_intents entries all resolve)")

    # Operations -> BPO corpus closure: governs_properties[] (string or {property})
    bad_gov, gov_count = [], 0
    for o in ops.get("operations", []):
        for g in o.get("governs_properties", []):
            gov_count += 1
            pid = g["property"] if isinstance(g, dict) else g
            if pid not in ids:
                bad_gov.append((o["id"], pid))
    if bad_gov:
        fail = True
        for oid, pid in bad_gov:
            print(f"  FAIL  operation {oid} -> governs_properties {pid}  (no such BPO record)")
    else:
        print(f"  OK   operations -> properties closure ({gov_count} governs_properties entries all resolve)")


# ---------------------------------------------------------------------------
# Section 1 — schema validation of property records
# ---------------------------------------------------------------------------
print("\n== schema ==")
for f, p in props.items():
    errs = list(validator.iter_errors(p))
    print(f"  {'OK ' if not errs else 'FAIL'} {p['id']:9} {p['slug']}")
    for e in errs[:5]:
        fail = True; print("       ->", list(e.path), e.message)


# ---------------------------------------------------------------------------
# Section 2 — reference resolution (relationships, assumptions, cross-walks)
# ---------------------------------------------------------------------------
print("\n== references ==")
edge_count = collections.Counter()
ext = set()
dascp_xref_count = 0
iso_d1_count = 0
iso_d2_count = 0

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
    # Existing: typed relationship edges
    for r in p.get("relationships", []):
        edge_count[r["type"]] += 1
        check(p["id"], r["type"], r["target"])

    # Existing: assumption-discharge edges
    for a in p.get("assumptions", []):
        d = a.get("discharged_by")
        if d:
            check(p["id"], "dischargedBy", d)

    # Existing: DASCP cross-walks
    for entry in p.get("identifiers", {}).get("external_refs", {}).get("dascp", []):
        dascp_xref_count += 1
        d_id = entry["id"]
        if d_id not in dascp_ids:
            fail = True
            print(f"  DANGLING {p['id']} --dascp({entry.get('relation','?')})--> {d_id}  (no such DASCP id)")

    # NEW: ISO 20022 depth-1 cross-walks
    for entry in p.get("identifiers", {}).get("external_refs", {}).get("iso20022", []):
        iso_d1_count += 1
        i_id = entry["id"]
        if i_id not in iso_ids:
            fail = True
            print(f"  DANGLING {p['id']} --iso20022({entry.get('relation','?')})--> {i_id}  (no such ISO 20022 id)")

    # NEW: ISO 20022 depth-2 bindings
    formalization = p.get("formalization", {})
    for b in formalization.get("bindings", []):
        iso_d2_count += 1
        element = b["element"]
        symbol  = b["symbol"]
        # (a) element resolves in the ISO 20022 framework
        if element not in iso_ids:
            fail = True
            print(f"  DANGLING {p['id']} --binding({symbol})--> {element}  (no such ISO 20022 id)")
        # (b) symbol satisfies the symbol-in-formalization check
        ok, reason = symbol_in_formalization(symbol, formalization)
        if not ok:
            fail = True
            print(f"  BINDING-SYMBOL FAIL  {p['id']} symbol '{symbol}' ({reason})")

print("  all BPO: / DASCP: / ISO 20022: targets resolve" if not fail else "  REFERENCE ERRORS ABOVE")


# ---------------------------------------------------------------------------
# Section 3 — undischarged assumptions ledger  (unchanged)
# ---------------------------------------------------------------------------
print("\n== undischarged assumptions (accepted hypotheses) ==")
for p in props.values():
    for a in p.get("assumptions", []):
        if a.get("discharged_by") is None:
            print(f"  {p['id']:9} [{a['kind']}] {a['statement'][:80]}")


# ---------------------------------------------------------------------------
# Section 4 — graph stats  (extended with operations + ISO 20022 counts)
# ---------------------------------------------------------------------------
print("\n== graph stats ==")
print(f"  properties: {len(ids)}")
print(f"  edges by type: {dict(edge_count)}")
print(f"  external ATK: targets referenced (Phase-2 registry): {len(ext)}")
for a in sorted(ext):
    print(f"    - {a}")
print(f"  DASCP cross-walk entries from properties:        {dascp_xref_count}")
print(f"  ISO 20022 depth-1 cross-walk entries:            {iso_d1_count}")
print(f"  ISO 20022 depth-2 binding entries:               {iso_d2_count}")
print(f"  Operations catalogue: {len(op_ids)} operations")
print(f"  ISO 20022 framework:  {len(iso_ids)} ids (msg+cmp+elem combined)")


print("\nRESULT:", "FAIL" if fail else "PASS (DAG closed over BPO: namespace; DASCP / Operations / ISO 20022 frameworks integral and closed)")
sys.exit(1 if fail else 0)
