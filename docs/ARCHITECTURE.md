# BPO — Architecture & Design Rationale

*Design notes for contributors. For the project overview, see the [README](../README.md); for the contribution standard, see [CONTRIBUTING](../CONTRIBUTING.md).*

A living, machine-readable, verification-oriented registry of safety, liveness, access-control, economic, temporal, cryptographic, governance, cross-chain, and agentic properties for blockchain systems. The intent is to become the **"CWE/CVE + formal-methods + ontology" layer** for provable blockchain infrastructure: each property carries not only a description but its formal semantics across multiple logics, its verification strategy, its attack mapping, and its typed relationships to every other property.

This is an early **seed**: the meta-architecture plus a set of fully-worked properties chosen to stress every part of the schema. It is designed to be extended to thousands of properties without structural change.

## Why this shape (the load-bearing decisions)

1. **Faceted, not a tree.** A property is a *point in five orthogonal axes* (modal class, deontic role, domain, abstraction level, verification modality) plus an open relationship DAG — never a leaf in one hierarchy. See `ontology/axes.md`. This is the difference between a reusable ontology and yet another flat vulnerability list.

2. **Hyperproperties are first-class.** The modal-class axis distinguishes Alpern–Schneider trace properties (safety/liveness) from Clarkson–Schneider **hyperproperties** (ZK, non-interference, MEV/ordering fairness, constant-time). Single-trace tools (symbolic execution, fuzzing) **cannot** verify hyperproperties; treating them as if they could is a category error that manufactures false assurance. `BPO:0003` exists to make this concrete.

3. **Assume–guarantee discipline.** Every guarantee exposes the `assumptions` it rests on, with a `discharged_by` ledger. `null` discharge is a *meaningful* state (an accepted-but-undischarged assumption). A property whose `dependsOn`-closure contains an undischarged assumption is **conditionally assured** — and the tooling must say so. This is how "we verified solvency" is forced to also say "…assuming the oracle is honest and the chain is live."

4. **Opaque IDs.** `BPO:NNNN` is immutable and semantically empty (cf. CWE-NNN, Wikidata Q-numbers): reclassification never breaks the ID join key. Human meaning lives in `slug` + classification.

5. **Dual serialization.** JSON + JSON Schema for *authoring/validation*; JSON-LD → RDF (SKOS/OWL) for *reasoning* (SPARQL queries, transitive-closure over `refines`/`implies`/`dependsOn`, SHACL shape validation). Same files, two consumers.

6. **Honest decidability.** Each property states what is *mechanically* achievable. Liveness needs fairness + model-checking/ITP, not fuzzing. Cryptographic indistinguishability needs reduction (EasyCrypt), not SMT. The registry never overstates what a tool can deliver.

## Layout

```
<repo root>/
  README.md                          public overview (vision + principles)
  docs/ARCHITECTURE.md               this file (design rationale + authoring rules)
  CONTRIBUTING.md                    quality bar, review lifecycle, provenance
  schema/
    property.schema.json             JSON Schema 2020-12 for one property record
    relationship.vocab.json          formal semantics of the typed DAG edges
    context.jsonld                   JSON-LD @context: JSON -> RDF (SKOS/OWL) projection
    validate_refs.py                 CI gate: schema + dangling-edge + assumption ledger
  ontology/
    axes.md                          the five orthogonal classification axes
    taxonomy.skos.ttl                SKOS poly-hierarchy of the domain axis (DAG)
  properties/                        16 records, DAG closed over the BPO: namespace
    BPO-0001-no-unauthorized-mint.json         safety / invariant      (SMT-tractable)
    BPO-0002-eventual-withdrawal.json          conditional liveness    (model-checking/ITP)
    BPO-0003-zero-knowledge.json               hyperproperty           (reduction/ITP)
    BPO-0020-reentrancy-safety.json            safety + 2-safety       (atomicity)
    BPO-0030-storage-layout-isolation.json     safety                  (separation logic)
    BPO-0040-access-control-correctness.json   safety                  (reference monitor)
    BPO-0050-emergency-pause-safety.json       safety + bounded-live   (pause tension host)
    BPO-0060-compiler-arithmetic-preservation  safety / observational  (translation validation)
    BPO-0070-knowledge-soundness.json          safety                  (extractor / under-constraint)
    BPO-0072-public-auditability.json          safety / transparency   (privacy-tension host)
    BPO-0073-circuit-public-signal-non-leakage hypersafety / NI        (self-composition)
    BPO-0074-crypto-hardness-setup-assumptions ASSUMPTION node         (null discharge)
    BPO-0080-consensus-liveness.json           conditional liveness    (FLP / partial synchrony)
    BPO-0081-censorship-resistance.json        liveness (strong-fair)  (forced inclusion)
    BPO-0082-l2-escape-hatch.json              liveness                (L1-only refinement)
    BPO-0101-conservation-of-value.json        economic root invariant (Certora/Echidna)
```

The seed properties are deliberately spread across the modal-class axis so the schema is exercised end-to-end: 1-safety invariants, fairness-dependent liveness guarantees (with genuine `conflictsWith` design tensions recorded, not hidden), and simulator-based hyperproperties (with the privacy claim cleanly separated from the soundness/under-constraint claim that automated tooling actually targets). The corpus forms a closed relationship DAG: every `BPO:` edge resolves to a record in the catalogue.

## Record facets ↔ the 20 requested dimensions

| Requested facet | Field |
|---|---|
| 1 Human semantic | `descriptions.semantic` |
| 2 Mathematical | `formalization.{first_order_logic, algebraic, signature}` |
| 3 System-theoretic | `descriptions.system_theoretic`, `formalization.state_machine` |
| 4 Security interp. | `descriptions.security` |
| 5 Execution semantics | `descriptions.execution_semantics` |
| 6 Formal-verification interp. | `descriptions.formal_verification` |
| 7 Machine-readable | the JSON record + `context.jsonld` |
| 8 Relationships | `relationships[]` (semantics in `relationship.vocab.json`) |
| 9 Attack surfaces | `attack_surface[]` + `mitigates` edges |
| 10 Observability | `observability` |
| 11 Monitoring | `observability.{metrics, telemetry, runtime_assertions}` |
| 12 Verification strategies | `verification.strategies[]` |
| 13 Testability | `verification.testability` |
| 14 Runtime enforcement | `enforcement.runtime` |
| 15 Static analysis | `enforcement.static` |
| 16 Symbolic execution | `verification.strategies` (modality tag) |
| 17 Model checking | `formalization.temporal_logic` + strategies |
| 18 SMT | strategies + `classification.verification_modalities` |
| 19 Type-theoretic | `formalization.type_theoretic` |
| 20 Taxonomy position | `classification` (5 axes) + `relationships` |

## Designed to be referenced, not just read

BPO is built so that other systems can point at it as a stable source of truth:

- **Specification and compiler toolchains** can cite BPO ids as `obligation`/`guarantee` clauses on modules and on a compiled system, so an emitted assurance argument links each guarantee to its formal semantics and verification strategy here. The `assumptions` ledger maps naturally onto cross-module rely/guarantee (assume–guarantee) contracts.
- **On-chain frameworks** (proxies, diamonds, modular/upgradeable systems) can attach a deployed artifact — a storage-layout hash, a selector set, a verification report — as a **proof artifact** discharging a specific BPO assumption (for example `BPO:0030` storage-layout-isolation under an EIP-2535 / ERC-7201 upgrade). Framework-specific error classes (e.g. storage-slot collisions, selector clashes, non-major schema changes) map onto BPO attack-classes and onto the invariants that mitigate them.

The opaque, immutable `BPO:NNNN` identifiers exist precisely so these references stay valid for years even as entries are reclassified or rewritten.

## Validation

```
pip install jsonschema --break-system-packages
python3 -c "import json,glob; from jsonschema import Draft202012Validator as V; \
s=json.load(open('schema/property.schema.json')); v=V(s); \
[print(f, 'OK' if not list(v.iter_errors(json.load(open(f)))) else 'FAIL') \
 for f in glob.glob('properties/*.json')]"
```
`schema/validate_refs.py` runs the full check and reports `PASS` when every record conforms to the schema and every `BPO:` reference resolves.

## Direction

This is an early seed. The catalogue is being actively expanded across domains, and the design is being refined together with early contributors and partners. The structural commitments above (faceted classification, first-class hyperproperties, assume–guarantee discipline, opaque IDs, dual serialization, honest decidability) are intended to be stable as the corpus grows; the set of properties, the threat-class layer the `mitigates` edges point at, and the reasoning/query layer over the RDF projection are all expected to grow over time. Contributions toward any of these are welcome — see [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for the quality bar and review process.

## Authoring rules (so the corpus stays sound as it grows)

- One property per file; never reuse a retired id.
- `modal_class` first — it gates which `verification_modalities` are even admissible.
- Label hyperproperties honestly; do not promise single-trace verification for them.
- Every `guarantee` must enumerate its `assumptions`; every `assumption` should eventually gain a `discharged_by` or be explicitly accepted (`null` + a provenance note).
- Mark unverified incident references `UNVERIFIED`/`VERIFY` and keep `provenance.confidence` honest; do not advance to `reviewed` with unverified attack citations.
