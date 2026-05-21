# BPO — Architecture & Design Rationale

*Design notes for contributors. For the project overview, see the [README](../README.md); for the contribution standard, see [CONTRIBUTING](../CONTRIBUTING.md).*

A living, machine-readable, verification-oriented registry of safety, liveness, access-control, economic, temporal, cryptographic, governance, cross-chain, and emerging agentic properties for blockchain systems. The intent is to become the **"CWE/CVE + formal-methods + ontology" layer** for provable blockchain infrastructure: each property carries not only a description but its formal semantics across multiple logics, its verification strategy, its attack mapping, and its typed relationships to every other property.

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
  CHANGELOG.md                       integration changelog
  docs/ARCHITECTURE.md               this file (design rationale + authoring rules)
  CONTRIBUTING.md                    quality bar, review lifecycle, provenance
  schema/
    property.schema.json             JSON Schema 2020-12 for one property record
    relationship.vocab.json          formal semantics of the typed DAG edges
    context.jsonld                   JSON-LD @context: JSON -> RDF (SKOS/OWL) projection
    validate_refs.py                 CI gate: schema + cross-framework closure + ledger
  ontology/
    axes.md                          the five orthogonal classification axes
    taxonomy.skos.ttl                SKOS poly-hierarchy of the domain axis (DAG)
  properties/                        24 records, DAG closed over the BPO: namespace
    BPO-0001-no-unauthorized-mint.json         safety / invariant      (SMT-tractable)
    BPO-0002-eventual-withdrawal.json          conditional liveness    (model-checking/ITP)
    BPO-0003-zero-knowledge.json               hyperproperty           (reduction/ITP)
    BPO-0020-reentrancy-safety.json            safety + 2-safety       (atomicity)
    BPO-0030-storage-layout-isolation.json     safety                  (separation logic)
    BPO-0040-access-control-correctness.json   safety                  (reference monitor)
    BPO-0041-multiparty-transaction-validation safety                  (k-of-n threshold)
    BPO-0050-emergency-pause-safety.json       safety + bounded-live   (pause tension host)
    BPO-0051-scoped-pause-safety-bounded.json  safety + bounded-live   (per-scope pause)
    BPO-0060-compiler-arithmetic-preservation  safety / observational  (translation validation)
    BPO-0070-knowledge-soundness.json          safety                  (extractor / under-constraint)
    BPO-0072-public-auditability.json          safety / transparency   (privacy-tension host)
    BPO-0073-circuit-public-signal-non-leakage hypersafety / NI        (self-composition)
    BPO-0074-crypto-hardness-setup-assumptions ASSUMPTION node         (null discharge)
    BPO-0075-private-data-confidentiality      hypersafety / NI        (network-observer)
    BPO-0080-consensus-liveness.json           conditional liveness    (FLP / partial synchrony)
    BPO-0081-censorship-resistance.json        liveness (strong-fair)  (forced inclusion)
    BPO-0082-l2-escape-hatch.json              liveness                (L1-only refinement)
    BPO-0090-settlement-finality-irrevocability safety / persistence   (final = absorbing)
    BPO-0091-fail-to-settle-reversal.json      safety + bounded-live   (compensating action)
    BPO-0092-sequencing-and-replay-resistance  safety                  (monotone nonce)
    BPO-0093-encumbrance-pre-settlement.json   safety                  (encumbrance partition)
    BPO-0101-conservation-of-value.json        economic root invariant (Certora/Echidna)
    BPO-0102-cross-ledger-inventory-consistency safety (joint-state)   (Σ_L supply_L)
  mappings/
    dascp.framework.json             DTCC/Clearstream/Euroclear control framework (P/R/C)
    dascp.framework.schema.json      JSON Schema for the DASCP catalogue
    DASCP-coverage.md                per-control coverage report
    operations.catalogue.json        abstract-operations catalogue (≤30, corpus-grounded)
    operations.catalogue.schema.json JSON Schema for the operations catalogue
    OPERATIONS-coverage.md           per-operation / per-property coverage report
    iso20022.framework.json          ISO 20022 reference subset (msg / cmp / elem)
    iso20022.framework.schema.json   JSON Schema for the ISO 20022 framework
    ISO20022-coverage.md             depth-1 + depth-2 coverage report
```

The seed properties are deliberately spread across the modal-class axis so the schema is exercised end-to-end: 1-safety invariants, fairness-dependent liveness guarantees (with genuine `conflictsWith` design tensions recorded, not hidden), and simulator-based hyperproperties (with the privacy claim cleanly separated from the soundness/under-constraint claim that automated tooling actually targets). The corpus forms a closed relationship DAG: every `BPO:` edge resolves to a record in the catalogue.

## Record facets ↔ the 20 facets each record carries

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

## Three-layer model: intent → operation → property

Beyond the property layer itself, the catalogue carries two additive layers under `mappings/` that close it to the standards world without diluting the property-level core:

- **Operations** (`mappings/operations.catalogue.json`) — a small (≤30), bounded set of *abstract operations*: TRANSFER, MINT, BURN, PAUSE, SETTLE, COMPENSATE, ENCUMBER, … Each operation is one *kind of state change*, grounded in at least one BPO property's formalization. The inclusion bar gates entries: a candidate qualifies only if it is a distinct kind of state change *and* at least one current property's formalization treats it differently from its neighbours. Function signatures appear only as *non-normative* examples; the ontology does not commit to maintaining function-level coverage. Each operation carries optional `iso20022_intents` (ISO 20022 message ids whose business intent the operation realizes) and `governs_properties` (BPO ids whose formalizations govern it). The operations↔properties link lives one-directionally inside the catalogue file — closure runs from `mappings/` into the property corpus — so adding or removing an operation touches one file, not all 24 property records.

- **ISO 20022 binding, two depths** (`mappings/iso20022.framework.json`) — a minimal subset of ISO 20022 messages, components, and elements that BPO properties or operations actually reference, with paraphrased descriptions in our own words. ISO 20022 publishes identifiers and structure free-of-use via iso20022.org, so the catalogue mirrors only what it needs and cites the source. **Depth 1**: `identifiers.external_refs.iso20022` on a property points at a message / business component, qualified `relates-to` (general relevance) or `constrains` (the property places a behavioural constraint on operations of that type). **Depth 2**: `formalization.bindings` maps a *named symbol from the property's formalization* (declared in `formalization.symbols` when present, otherwise whole-token-matched against `formalization.signature`) to an ISO 20022 element. The depth-2 symbol check is structured-lookup-when-available, regex-on-`signature`-only as fallback, case-sensitive throughout — a binding that silently mis-resolves would be worse than no binding.

The three layers chain end-to-end:

```
ISO 20022 message intent          (top: business intent, standards interop)
        │
        │ operation's `iso20022_intents`
        ▼
Abstract operation                (middle: catalogue of state changes)
        │
        │ operation's `governs_properties`
        ▼
BPO property                      (bottom: formal behavioural truth)
        │
        │ property's `formalization.bindings`
        ▼
ISO 20022 element / component      (back to standards at variable granularity)
```

**Worked example — settlement finality (`BPO:0090`).**

- ISO 20022 message intents: `sese.023` SecuritiesSettlementTransactionInstruction, `sese.024` StatusAdvice, `sese.025` Confirmation.
- These ids appear under `OP:SETTLE`'s `iso20022_intents` in the operations catalogue.
- `OP:SETTLE`'s `governs_properties` points to `BPO:0090`, the property whose formalization names `final(t, s')` as the sole effect of the operation.
- `BPO:0090`'s `formalization.bindings` map the property's symbols back to ISO 20022 elements:
  - `SettlementID` → `ISO20022:elem/SettlementTransactionIdentification` (direct)
  - `accountedOutcome` → `ISO20022:elem/SettlementAmount` (partial — monetary face only; the property's accountedOutcome also encompasses ownership changes)
  - `final` → `ISO20022:cmp/TransactionStatus` (the predicate selects the SETTLED value of the status component)

End-to-end: a `sese.023` instruction is an instance of `OP:SETTLE`, which is the operation `BPO:0090`'s persistence invariant governs, with the instruction's SettlementTransactionIdentification = the property's `t`, the SettlementAmount projecting from `accountedOutcome(t, s')`, and TransactionStatus advancing to settled = the predicate `final` becoming TRUE — which `BPO:0090` then guarantees persists in every reachable successor.

The whole addition is purely additive: no property record's meaning changed, no `BPO:` id was reused or renumbered, no relationship-edge type was invented. Both new framework files mirror the DASCP integration pattern — shape fixed by JSON Schema, internal integrity (id uniqueness, cross-framework closure, the depth-2 symbol-in-formalization check) enforced in code by `schema/validate_refs.py`. Function-level details and full ISO 20022 message bodies stay out of scope by design.

## Validation

```
pip install jsonschema --break-system-packages
python3 -c "import json,glob; from jsonschema import Draft202012Validator as V; \
s=json.load(open('schema/property.schema.json')); v=V(s); \
[print(f, 'OK' if not list(v.iter_errors(json.load(open(f)))) else 'FAIL') \
 for f in glob.glob('properties/*.json')]"
```
`schema/validate_refs.py` runs the full check and reports `PASS` when every property conforms to the schema; every `BPO:` reference resolves to a record; the DASCP, operations, and ISO 20022 framework files each pass their own shape and internal-integrity checks (id uniqueness, intra-framework closure); every cross-framework reference resolves (`external_refs.dascp[].id`, `external_refs.iso20022[].id`, operations' `iso20022_intents`, operations' `governs_properties`); and every depth-2 ISO 20022 binding satisfies both the element-side closure and the symbol-in-formalization check (Tier 1 structured lookup against `formalization.symbols` when present, Tier 2 whole-token regex against `formalization.signature` as fallback, case-sensitive).

## Direction

This is an early seed. The catalogue is being actively expanded across domains, and the design is being refined together with early contributors and partners. The structural commitments above (faceted classification, first-class hyperproperties, assume–guarantee discipline, opaque IDs, dual serialization, honest decidability) are intended to be stable as the corpus grows; the set of properties, the threat-class layer the `mitigates` edges point at, and the reasoning/query layer over the RDF projection are all expected to grow over time. Contributions toward any of these are welcome — see [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for the quality bar and review process.

## Authoring rules (so the corpus stays sound as it grows)

- One property per file; never reuse a retired id.
- `modal_class` first — it gates which `verification_modalities` are even admissible.
- Label hyperproperties honestly; do not promise single-trace verification for them.
- Every `guarantee` must enumerate its `assumptions`; every `assumption` should eventually gain a `discharged_by` or be explicitly accepted (`null` + a provenance note).
- Mark unverified incident references `UNVERIFIED`/`VERIFY` and keep `provenance.confidence` honest; do not advance to `reviewed` with unverified attack citations.
