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
  - the IOF framework file failing its own schema or internal integrity
    (duplicate ids across foundations ∪ building_blocks; building_block.foundation referencing
    a non-existent foundation id within the framework)
  - any identifiers.external_refs.iof[].id in a property not resolving to a building-block id in
    the IOF framework (IOF cross-walk closure)
  - bidirectional scope-link consistency between IOF building_blocks[].scope and the cross-walk
    links from property records: a block tagged `out-of-scope` must carry zero links and a block
    tagged `behavioural` must carry at least one, so the scope verdict cannot drift out of sync
    with the actual links
  - any protocol-identity token (protocol name, source revision, deployment address, local
    obligation id, fixed policy constant) appearing in a NORMATIVE field of a property record;
    the token list and the checked/excluded field scope live in
    schema/protocol-identity.denylist.json
  - any assurance-case cross-walk document failing schema/assurance-case.schema.json or one of
    the eight honesty gates: local-id uniqueness; declared-vs-recomputed ledger sizes; closure of
    bpo_targets into the corpus and of local_assumptions into the document's own ledger; scoped
    instantiations supplying clause + bindings + residual (and no-exact-match supplying no
    target); a passing result carrying machine/tool/bounds/assumptions/artifact; evidence CLASS
    consistent with the CLAIMS made about it (operation-local CBC is not exhaustive reachability,
    a static assertion is not transition preservation, a curated trace is not domain-exhaustive);
    no referenced property having been advanced to formally-verified; and the declared alignment
    histogram matching the recomputed one
ATK: targets are treated as an EXTERNAL namespace (the threat-class registry)
and are reported but not required to resolve yet.
Assurance-case documents are OPTIONAL: BPO publishes the contract and a synthetic fixture but
hosts no real case study, because a crosswalk is an artifact of the verification project that
produced the evidence. Closure runs one-directionally FROM a crosswalk INTO the corpus; no
property record ever points back at a verification project.
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
# Section 0d — IOF framework  (Interoperability Framework for Digital Asset
# Securities; DTCC / Clearstream / Euroclear / BCG, February 2026).  Loaded
# independently of the other frameworks because IOF cross-walks attach to
# property records (Step 3) but do not feed into the operations catalogue.
# Step 2 establishes intra-framework integrity only; the cross-walk closure
# and the bidirectional scope-link consistency check are added in Step 3.
# ---------------------------------------------------------------------------
print("\n== IOF framework ==")
iof_path        = f"{ROOT}/mappings/iof.framework.json"
iof_schema_path = f"{ROOT}/mappings/iof.framework.schema.json"
iof_ids = set()
iof_foundation_ids = set()
iof_bb_ids = set()
iof_bb_scope = {}
if not (os.path.exists(iof_path) and os.path.exists(iof_schema_path)):
    fail = True
    print(f"  FAIL  missing mappings/iof.framework.json or mappings/iof.framework.schema.json")
else:
    iof        = json.load(open(iof_path,        encoding="utf-8"))
    iof_schema = json.load(open(iof_schema_path, encoding="utf-8"))
    shape_errs = list(Draft202012Validator(iof_schema).iter_errors(iof))
    if shape_errs:
        fail = True
        print("  FAIL  iof.framework.json does not conform to iof.framework.schema.json:")
        for e in shape_errs[:10]:
            print("       ->", list(e.path), e.message)
    else:
        print("  OK   shape (matches mappings/iof.framework.schema.json)")

    seen, dupes = set(), []
    for grp in ("foundations", "building_blocks"):
        for item in iof.get(grp, []):
            i = item["id"]
            if i in seen: dupes.append(i)
            seen.add(i)
    iof_ids |= seen
    iof_foundation_ids = {f["id"] for f in iof.get("foundations",    [])}
    iof_bb_ids         = {b["id"] for b in iof.get("building_blocks", [])}
    iof_bb_scope       = {b["id"]: b["scope"] for b in iof.get("building_blocks", [])}
    if dupes:
        fail = True
        print(f"  FAIL  duplicate IOF ids: {sorted(set(dupes))}")
    else:
        n_beh = sum(1 for s in iof_bb_scope.values() if s == "behavioural")
        n_oos = sum(1 for s in iof_bb_scope.values() if s == "out-of-scope")
        print(f"  OK   {len(iof_ids)} IOF ids unique "
              f"(F={len(iof_foundation_ids)}, BB={len(iof_bb_ids)}; "
              f"behavioural={n_beh}, out-of-scope={n_oos})")

    bad_found = []
    for b in iof.get("building_blocks", []):
        if b.get("foundation") not in iof_foundation_ids:
            bad_found.append((b["id"], b.get("foundation")))
    if bad_found:
        fail = True
        for bid, fid in bad_found:
            print(f"  FAIL  building_block {bid} -> foundation {fid}  (no such foundation in framework)")
    else:
        print(f"  OK   internal closure (every building_block.foundation resolves)")


# ---------------------------------------------------------------------------
# Section 0e — Assurance-case cross-walk documents.
#
# BPO publishes schema/assurance-case.schema.json as a contract for downstream
# verification projects and ships a synthetic fixture under examples/ so the
# honesty gates are exercised in CI.  It hosts no real case study: a crosswalk
# belongs to the project that produced the evidence, and carrying one here
# would invert the dependency.  Documents are therefore OPTIONAL — finding none
# is a skip, not a failure.  Shape is checked here; the eight gates run in
# Section 2d, after the property corpus has been indexed.
# ---------------------------------------------------------------------------
print("\n== assurance-case documents ==")
ac_schema_path = f"{ROOT}/schema/assurance-case.schema.json"
ac_docs = {}
if not os.path.exists(ac_schema_path):
    fail = True
    print("  FAIL  missing schema/assurance-case.schema.json")
else:
    ac_schema = json.load(open(ac_schema_path, encoding="utf-8"))
    candidates = sorted(
        glob.glob(f"{ROOT}/examples/*assurance-case*.json")
        + glob.glob(f"{ROOT}/case-studies/*.json")
    )
    if not candidates:
        print("  OK   schema present; no assurance-case documents in this repo (expected: "
              "crosswalks live in the verification projects that produce the evidence)")
    for f in candidates:
        doc = json.load(open(f, encoding="utf-8"))
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        shape_errs = list(Draft202012Validator(ac_schema).iter_errors(doc))
        if shape_errs:
            fail = True
            print(f"  FAIL  {rel} does not conform to assurance-case.schema.json:")
            for e in shape_errs[:10]:
                print("       ->", list(e.path), e.message)
        else:
            ac_docs[rel] = doc
            print(f"  OK   shape  {rel}  "
                  f"({len(doc.get('alignments', []))} alignments, "
                  f"{len(doc.get('assumptions', []))} assumptions)")


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
iof_xref_count = 0
# Reverse index: IOF building-block id -> list of (property id, relation) pairs.
# Populated alongside cross-walk closure and consumed by the bidirectional
# scope-link consistency check below.
iof_links_by_bb = collections.defaultdict(list)

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

    # NEW: IOF cross-walks (closure into building_blocks[]; foundation ids and unknown
    # ids are both rejected here. Reverse index feeds the scope-link consistency check.)
    for entry in p.get("identifiers", {}).get("external_refs", {}).get("iof", []):
        iof_xref_count += 1
        i_id = entry["id"]
        if i_id not in iof_bb_ids:
            fail = True
            print(f"  DANGLING {p['id']} --iof({entry.get('relation','?')})--> {i_id}  "
                  f"(no such IOF building-block id)")
        else:
            iof_links_by_bb[i_id].append((p["id"], entry.get("relation", "?")))

print("  all BPO: / DASCP: / ISO 20022: / IOF: targets resolve" if not fail else "  REFERENCE ERRORS ABOVE")


# ---------------------------------------------------------------------------
# Section 2b — IOF bidirectional scope-link consistency.
# Out-of-scope blocks must carry zero cross-walk links (otherwise the `scope`
# verdict in the framework file contradicts the actual links).  Behavioural
# blocks must carry at least one (otherwise the verdict claims a behavioural
# mapping that the corpus does not realize).  Both directions are FAIL.
# ---------------------------------------------------------------------------
print("\n== IOF scope-link consistency ==")
oos_with_links, beh_without_links = [], []
for bb_id, scope in iof_bb_scope.items():
    n_links = len(iof_links_by_bb.get(bb_id, []))
    if scope == "out-of-scope" and n_links > 0:
        oos_with_links.append((bb_id, n_links, iof_links_by_bb[bb_id]))
    if scope == "behavioural" and n_links == 0:
        beh_without_links.append(bb_id)
if oos_with_links:
    fail = True
    for bb_id, n, links in oos_with_links:
        srcs = ", ".join(f"{pid}({rel})" for pid, rel in links)
        print(f"  FAIL  out-of-scope {bb_id} carries {n} cross-walk link(s): {srcs}  "
              f"(downgrade the scope or remove the link)")
if beh_without_links:
    fail = True
    for bb_id in beh_without_links:
        print(f"  FAIL  behavioural {bb_id} carries 0 cross-walk links  "
              f"(downgrade the scope to out-of-scope or add a link)")
if not (oos_with_links or beh_without_links):
    n_beh = sum(1 for s in iof_bb_scope.values() if s == "behavioural")
    n_oos = sum(1 for s in iof_bb_scope.values() if s == "out-of-scope")
    print(f"  OK   all {n_beh} behavioural blocks carry ≥ 1 cross-walk link; "
          f"all {n_oos} out-of-scope blocks carry zero")


# ---------------------------------------------------------------------------
# Section 2c — protocol-identity denylist over NORMATIVE property fields.
#
# A BPO record states a behavioural truth over abstract sorts, functions and
# policy parameters; concrete protocol identity belongs to a downstream
# assurance-case crosswalk.  This gate makes that rule machine-checked.  The
# checked/excluded field scope is documented in the denylist file itself:
# cross-walk surfaces (identifiers.*), illustrative threat material
# (attack_surface[]), attribution (provenance.*) and prover names
# (verification.strategies[].tools) are all deliberately out of scope.
# ---------------------------------------------------------------------------
def normative_strings(p):
    """Yield (field_path, text) for every string in a property record's normative fields."""
    def walk(node, path):
        if isinstance(node, str):
            yield path, node
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from walk(v, f"{path}[{i}]")
        elif isinstance(node, dict):
            for k, v in sorted(node.items()):
                yield from walk(v, f"{path}.{k}")

    yield from walk(p.get("descriptions", {}), "descriptions")
    # formalization minus `bindings`: those are ISO 20022 cross-walk notes, an
    # excluded cross-walk surface like identifiers.*.
    yield from walk({k: v for k, v in p.get("formalization", {}).items() if k != "bindings"},
                    "formalization")
    for i, a in enumerate(p.get("assumptions", [])):
        if isinstance(a.get("statement"), str):
            yield f"assumptions[{i}].statement", a["statement"]
    yield from walk(p.get("enforcement", {}), "enforcement")
    ver = p.get("verification", {})
    for i, s in enumerate(ver.get("strategies", [])):
        for k in ("approach", "notes"):          # NOT `tools` — prover names are not protocol identity
            if isinstance(s.get(k), str):
                yield f"verification.strategies[{i}].{k}", s[k]
    yield from walk(ver.get("testability", []), "verification.testability")


def term_regex(term):
    """Whole-token, case-insensitive, whitespace-tolerant match for a denied term."""
    return re.compile(
        r"(?<![A-Za-z0-9])" + r"\s+".join(re.escape(w) for w in term.split()) + r"(?![A-Za-z0-9])",
        re.IGNORECASE,
    )


print("\n== protocol-identity denylist (normative fields) ==")
denylist_path = f"{ROOT}/schema/protocol-identity.denylist.json"
if not os.path.exists(denylist_path):
    fail = True
    print("  FAIL  missing schema/protocol-identity.denylist.json")
else:
    denylist  = json.load(open(denylist_path, encoding="utf-8"))
    allowed   = {(a.get("property"), a.get("term")) for a in denylist.get("allowlist", [])}
    terms     = [(t["term"], t.get("kind", "?"), term_regex(t["term"]))
                 for t in denylist.get("denied_terms", [])]
    patterns  = [(pt.get("kind", "?"), re.compile(pt["pattern"]))
                 for pt in denylist.get("denied_patterns", [])]
    deny_hits = 0
    for p in props.values():
        for path, text in normative_strings(p):
            for term, kind, rx in terms:
                if rx.search(text) and (p["id"], term) not in allowed:
                    fail = True; deny_hits += 1
                    print(f"  FAIL  {p['id']} {path}: denied {kind} '{term}'")
            for kind, rx in patterns:
                m = rx.search(text)
                if m and (p["id"], m.group(0)) not in allowed:
                    fail = True; deny_hits += 1
                    print(f"  FAIL  {p['id']} {path}: denied {kind} '{m.group(0)}'")
    if not deny_hits:
        print(f"  OK   {len(props)} records clean over {len(terms)} denied terms + "
              f"{len(patterns)} denied patterns ({len(allowed)} allowlisted exception(s))")


# ---------------------------------------------------------------------------
# Section 2d — assurance-case honesty gates.
#
# Closure runs one-directionally FROM a crosswalk INTO the corpus.  The gates
# exist so that a local, bounded, tool-specific result cannot be reported as
# something stronger than it is, and so that an alignment cannot quietly
# promote itself into a proof about a generic record.
# ---------------------------------------------------------------------------
print("\n== assurance-case gates ==")
by_id = {p["id"]: p for p in props.values()}
if not ac_docs:
    print("  OK   no assurance-case documents to gate")
for rel, doc in ac_docs.items():
    errs = []
    alignments = doc.get("alignments", [])
    local_assumption_ids = [a["id"] for a in doc.get("assumptions", [])]

    # Gate 1 — local identifiers unique within the document.
    dupes = [i for i, n in collections.Counter(
        a["local_id"] for a in alignments).items() if n > 1]
    if dupes:
        errs.append(f"duplicate local_id(s): {sorted(dupes)}")
    dupe_asm = [i for i, n in collections.Counter(local_assumption_ids).items() if n > 1]
    if dupe_asm:
        errs.append(f"duplicate assumption id(s): {sorted(dupe_asm)}")

    # Gate 2 — declared ledger sizes match the data.
    ledger = doc.get("local_ledger", {})
    if ledger.get("property_count") != len(alignments):
        errs.append(f"local_ledger.property_count={ledger.get('property_count')} "
                    f"but {len(alignments)} alignments present")
    if ledger.get("assumption_count") != len(local_assumption_ids):
        errs.append(f"local_ledger.assumption_count={ledger.get('assumption_count')} "
                    f"but {len(local_assumption_ids)} assumptions present")

    known_assumptions = set(local_assumption_ids)
    for a in alignments:
        lid   = a["local_id"]
        kind  = a["alignment"]
        tgts  = a.get("bpo_targets", [])
        ev    = a.get("evidence", {})

        # Gate 3 — closure, both directions of reference.
        for t in tgts:
            if t["property"] not in ids:
                errs.append(f"{lid}: bpo_target {t['property']} does not resolve in the corpus")
        for aid in a.get("local_assumptions", []):
            if aid not in known_assumptions:
                errs.append(f"{lid}: local_assumption {aid} not in this document's ledger")

        # Gate 4 — the alignment class must be backed by the structure it claims.
        if kind == "scoped-instantiation":
            if not tgts:
                errs.append(f"{lid}: scoped-instantiation with no bpo_targets")
            if not all(t.get("clause") for t in tgts):
                errs.append(f"{lid}: scoped-instantiation without an identified clause on every target")
            if not a.get("symbol_bindings"):
                errs.append(f"{lid}: scoped-instantiation without symbol_bindings")
            if not a.get("residual_scope"):
                errs.append(f"{lid}: scoped-instantiation without residual_scope")
        elif kind == "partial-overlap":
            if not tgts:
                errs.append(f"{lid}: partial-overlap with no bpo_targets")
        elif kind == "no-exact-match" and tgts:
            errs.append(f"{lid}: no-exact-match must carry zero bpo_targets, found {len(tgts)}")

        # Gate 5 — a reported pass must be reproducible on its face.
        if ev.get("result") == "pass":
            for field in ("machine", "bounds", "artifact"):
                if not ev.get(field):
                    errs.append(f"{lid}: evidence.result=pass without evidence.{field}")
            if not ev.get("tool", {}).get("name"):
                errs.append(f"{lid}: evidence.result=pass without evidence.tool.name")
            if not a.get("local_assumptions"):
                errs.append(f"{lid}: evidence.result=pass without local_assumptions")

        # Gate 6 — evidence CLASS must be consistent with the CLAIMS made about it.
        cls = ev.get("class")
        if cls == "operation-local-cbc" and ev.get("reachability_claim") == "exhaustive":
            errs.append(f"{lid}: operation-local CBC claims exhaustive reachability "
                        f"(constraint-checking one operation says nothing about reachability)")
        if cls == "static-assertion" and ev.get("transition_preservation"):
            errs.append(f"{lid}: static assertion claims transition preservation "
                        f"(an assertion over a state enumeration is not an inductive step)")
        if cls == "curated-trace" and ev.get("domain_exhaustive"):
            errs.append(f"{lid}: curated trace claims domain exhaustiveness "
                        f"(a hand-built trace shows one behaviour is reachable, never that others are absent)")
        if cls == "none" and ev.get("result") == "pass":
            errs.append(f"{lid}: evidence.class=none reported as a pass")

        # Gate 7 — no referenced property may have been advanced to verified.
        for t in tgts:
            target = by_id.get(t["property"])
            if target and target.get("provenance", {}).get("confidence") == "formally-verified":
                errs.append(f"{lid}: target {t['property']} is marked formally-verified; "
                            f"an alignment must not promote a generic record")

    # Gate 8 — declared alignment histogram matches the recomputed one.
    computed = collections.Counter(a["alignment"] for a in alignments)
    declared = doc.get("alignment_summary", {})
    for key, field in (("scoped-instantiation", "scoped_instantiation"),
                       ("partial-overlap",      "partial_overlap"),
                       ("no-exact-match",       "no_exact_match")):
        if declared.get(field) != computed.get(key, 0):
            errs.append(f"alignment_summary.{field}={declared.get(field)} "
                        f"but {computed.get(key, 0)} entries are '{key}'")

    if errs:
        fail = True
        print(f"  FAIL  {rel}")
        for e in errs[:20]:
            print(f"       -> {e}")
        if len(errs) > 20:
            print(f"       -> ... and {len(errs) - 20} more")
    else:
        print(f"  OK   {rel}  all 8 gates pass "
              f"({computed.get('scoped-instantiation', 0)} scoped / "
              f"{computed.get('partial-overlap', 0)} partial / "
              f"{computed.get('no-exact-match', 0)} unmatched)")


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
print(f"  IOF cross-walk entries from properties:          {iof_xref_count}")
print(f"  Operations catalogue: {len(op_ids)} operations")
print(f"  ISO 20022 framework:  {len(iso_ids)} ids (msg+cmp+elem combined)")
print(f"  IOF framework:        {len(iof_ids)} ids "
      f"({len(iof_foundation_ids)} foundations + {len(iof_bb_ids)} building blocks; "
      f"behavioural={sum(1 for s in iof_bb_scope.values() if s == 'behavioural')}, "
      f"out-of-scope={sum(1 for s in iof_bb_scope.values() if s == 'out-of-scope')})")


print(f"  Assurance-case documents:  {len(ac_docs)}")
for rel, doc in ac_docs.items():
    hist = collections.Counter(a["alignment"] for a in doc.get("alignments", []))
    print(f"    - {rel}: {len(doc.get('alignments', []))} alignments "
          f"({hist.get('scoped-instantiation', 0)} scoped, "
          f"{hist.get('partial-overlap', 0)} partial, "
          f"{hist.get('no-exact-match', 0)} unmatched), "
          f"{len(doc.get('assumptions', []))} local assumptions")


print("\nRESULT:", "FAIL" if fail else "PASS (DAG closed over BPO: namespace; DASCP / Operations / ISO 20022 / IOF frameworks integral and closed; normative fields free of protocol identity; assurance-case gates satisfied)")
sys.exit(1 if fail else 0)
