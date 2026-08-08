# Changelog

## Collateralized-Lending Property Layer + Assurance-Case Contract — 2026-08-08

Added a protocol-agnostic layer of **13 property records** for collateralized lending (10 guarantees, 3 dependency contracts), **10 abstract operations**, and a published **assurance-case schema** — the contract a downstream verification project's cross-walk must satisfy — with a synthetic fixture and eight machine-enforced honesty gates. Two new build gates make the layer's central claims structural rather than editorial: a protocol-identity denylist over property records' normative fields, and evidence class-versus-claim consistency in the assurance-case layer. The corpus grows from 24 to 37 records and the operations catalogue from 22 to 32; no existing record changed meaning, no id was reused, and no relationship-edge type was invented. The validator reports `PASS`. **Not committed** — staged for maintainer review.

The work derives from an external proposal that also specified a Morpho Blue case-study cross-walk. That cross-walk is **deliberately excluded**; see the design decisions below.

### Design decisions recorded

- **No case study lands in this repository.** A cross-walk is an artifact of the verification project that produced the evidence: it points *up* at the catalogue and is indexed by two revisions (the subject's and BPO's). Hosting one here would invert the dependency and make a general catalogue carry one subject's evidence. BPO publishes `schema/assurance-case.schema.json` and a synthetic fixture; a real cross-walk lives in the project that cites it. *Rejected alternative:* a `case-studies/` directory with a populated 53-entry Morpho Blue cross-walk and a `build_crosswalk.py` generator, as the source proposal specified.
- **Everything lands in canonical directories, not an `upstream/` staging tree.** The source proposal was written as though submitting to a third party; there is no upstream. Repo precedent records staging status in this changelog ("*Not committed — staged for maintainer review*"), and files under `upstream/` would be invisible to the validator and CI.
- **`BPO:0021` for Atomic Failure Rollback, not `BPO:0119`.** The proposal placed it in the lending block. It is a platform-level execution guarantee that lending records *depend on* rather than a lending property, so it takes the execution decade beside `BPO:0020` reentrancy, matching the decade convention every existing record follows. It carries both `guarantee` and `environmental-assumption` deontic roles, because the same statement is an obligation for a system emulating rollback and an assumption for one running on a platform that provides it.
- **`BPO:0119` is permanently unallocated.** The nine remaining lending guarantees shifted down one slot to `BPO:0110`–`BPO:0118`. Per the authoring rules, a retired or skipped id is never reused.
- **The operations size guidance moved from 30 to 40 rather than the operations moving.** The lending layer admits 10 operations, taking the catalogue to 32. Under the old ceiling, two candidates that clear the inclusion bar on their merits — `OP:FLASH-LOAN` and `OP:CREATE-LENDING-MARKET` — would have been excluded for arithmetic reasons, which the source proposal acknowledged and accepted. An operation excluded by the count rather than by the test is evidence the count is wrong. The bar's *test* is unchanged; only the numeric guidance moved, and it now lives in the catalogue's new `size_guidance` field so the number and its rationale travel together.
- **The three dependency contracts are `assumption` nodes, not guarantees.** `BPO:0120`–`BPO:0122` describe what a lending system *relies on* from an external asset interface, valuation provider and rate provider. Their own assumptions carry `discharged_by: null` so they surface in the undischarged ledger. Labelling them guarantees would let a consuming system's proof appear to establish something about a dependency it never examined — the composition error `docs/ARCHITECTURE.md` warns about.
- **`BPO:0121` refuses to conflate interface well-formedness with economic correctness.** A valuation provider returning a well-formed, fresh, in-range value may still be manipulated, and no interface check excludes that. The boundary is stated four redundant ways — as a normative clause in the formalization, as an explicitly *non*-mitigated attack class, as a verification strategy with a deliberately empty tool list, and as an undischarged economic assumption — because collapsing it is the most common route by which a verified lending system acquires an unverified dependency nobody tracks.
- **`BPO:0115` is `k-safety` and kept separate from `BPO:0114`.** Liquidation-mode coherence relates two executions from a shared pre-state; liquidation safety is single-trace and applies to every design. Merging them would either impose a vacuous obligation on single-mode protocols or invite a per-mode single-trace result to be reported as covering a relational claim. `BPO:0115` also imposes no obligation where only one input mode exists, and says so.
- **`BPO:0117` is `guarantee-liveness-conditional`, and its LTL field states that no LTL formula covers it.** Bounded enabledness (`AG(Pre -> EX exit)`) is routinely produced by model checkers and routinely over-reported as withdrawal liveness. The `refinedBy` edge from `BPO:0002` says explicitly that `BPO:0117` is strictly weaker and is not evidence for it.
- **Five false equivalences are recorded as edge notes in the data**, not only in prose: state typing is not compiler arithmetic preservation (`BPO:0060`); within-system custody is not cross-ledger inventory consistency (`BPO:0102`); synchronous rollback is not delayed compensating settlement (`BPO:0091`); bounded enabledness is not eventual withdrawal (`BPO:0002`); and a post-callback storage cutoff covers only part of reentrancy safety (`BPO:0020`, now refined by `BPO:0021` for atomicity and `BPO:0116` for call-site consistency).
- **Protocol identity is barred from normative fields by a build gate, not by review.** With no case study here to absorb specifics, this lint is the only mechanism keeping the 13 records generic. Scope is `descriptions`, all of `formalization`, `assumptions[].statement`, `enforcement`, and the prose of `verification.strategies`. Deliberately excluded: `identifiers` and `attack_surface` (cross-walk and illustrative material — `BPO:0101` legitimately cites ERC-4626), `provenance` (attribution is scholarship), and `verification.strategies[].tools` (Certora and Echidna are prover names, not protocol identity). Terms are phrase-scoped where a bare token would false-positive: `compound finance` rather than `compound`, since "compound interest" is ordinary vocabulary in an accrual record; likewise `curve finance` and `euler finance`. All 24 pre-existing records pass with **zero allowlist entries**.
- **Evidence class is recorded separately from the claims made about it.** The source proposal's requirements 8–10 were review obligations; they are now schema fields the validator cross-checks, so `operation-local-cbc` cannot claim exhaustive reachability, `static-assertion` cannot claim transition preservation, and `curated-trace` cannot claim domain exhaustiveness.
- **Declared counts are recomputed rather than trusted.** The proposal hard-coded a requirement that a specific 17/28/8 alignment split stay reproducible. Generalized: a document declares its own `local_ledger` sizes and `alignment_summary` histogram, and the validator recomputes both from the data and fails on disagreement. This is project-independent and strictly stronger than checking one project's numbers.
- **The assurance-case local-id pattern is generic.** The proposal's schema baked in an `MB-` prefix from one project. A reusable contract cannot carry one subject's identifier scheme, so the pattern is `^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$` with uniqueness enforced in code.
- **Alignment is not a `relationships[]` edge type.** `refines`, `implies` and `equivalentTo` carry proof-theoretic meaning defined in `relationship.vocab.json`; a cross-walk earns none of it. The alignment enum offers no value meaning "equivalent to" or "proves", and `proof_transfer` is pinned to `none` by schema rather than by convention.
- **Assurance-case documents are optional.** Finding none is a skip, not a failure — the expected state for this repository, which hosts the contract and not a case study.
- **`defi-lending` gains its first users.** The slug has existed in `ontology/taxonomy.skos.ttl` since the seed and was used by no record. `classification.domains` has no enum and no closure check, so no schema or taxonomy change was needed.

### Files added (16)

| File | What |
|---|---|
| `properties/BPO-0021-atomic-failure-rollback.json` | safety; failure edges are identity on the persistent projection |
| `properties/BPO-0110-lending-ledger-consistency.json` | safety; aggregate fold + backing relation — the lending root |
| `properties/BPO-0111-directed-position-unit-conversion-safety.json` | safety + k-safety; approximation contract + round-trip bound |
| `properties/BPO-0112-lending-accrual-and-fee-allocation-consistency.json` | safety; generated value bounds the fee |
| `properties/BPO-0113-collateralized-position-health-preservation.json` | safety; guarded post-condition on risk-increasing transitions |
| `properties/BPO-0114-liquidation-accounting-and-loss-allocation-safety.json` | safety; eligibility, bounds, settlement conservation, residual |
| `properties/BPO-0115-alternative-liquidation-mode-coherence.json` | k-safety; conditional on multiple input modes existing |
| `properties/BPO-0116-callback-settlement-integrity.json` | safety; pending claim consumed exactly once |
| `properties/BPO-0117-conditional-position-exit-enabledness.json` | conditional enabledness; explicitly weaker than `BPO:0002` |
| `properties/BPO-0118-protocol-instance-configuration-integrity.json` | safety; admission, immutability, monotone registries, bounds |
| `properties/BPO-0120-asset-interface-accounting-semantics.json` | ASSUMPTION node; declared movement profile |
| `properties/BPO-0121-valuation-provider-interface-integrity.json` | ASSUMPTION node; well-formedness, *not* economic correctness |
| `properties/BPO-0122-rate-provider-call-integrity.json` | ASSUMPTION node; termination, range, input fidelity, frame |
| `schema/assurance-case.schema.json` | the cross-walk contract, instantiated downstream |
| `schema/protocol-identity.denylist.json` | tokens barred from normative fields, with scope and rationale |
| `examples/assurance-case.example.json` | synthetic fixture covering every alignment value and evidence class |

### Files modified (9)

| File | Change |
|---|---|
| `schema/validate_refs.py` | new Sections 0e (document shape), 2c (denylist lint), 2d (eight gates); extended stats and docstring |
| `mappings/operations.catalogue.json` | +10 operations (22 → 32); new `size_guidance` field; version 0.1.0 → 0.2.0 |
| `mappings/operations.catalogue.schema.json` | `size_guidance` added to the top-level shape |
| `mappings/OPERATIONS-coverage.md` | regenerated: 32 ops, 70 links; lending sub-tables; candidate-count drift corrected |
| `properties/BPO-0101-conservation-of-value.json` | +4 `refinedBy` edges, making good on its own provenance note about future lending children |
| `properties/BPO-0020-reentrancy-safety.json` | +2 `refinedBy` edges splitting the atomicity and call-site-consistency readings |
| `properties/BPO-0040-access-control-correctness.json` | +2 `refinedBy` edges (configuration integrity; guard completeness) |
| `properties/BPO-0002-eventual-withdrawal.json` | +1 `refinedBy` edge stating that `BPO:0117` is strictly weaker and not evidence for it |
| `properties/BPO-0060-compiler-arithmetic-preservation.json` | +1 `composesWith` edge recording the state-typing false equivalence |

`schema/context.jsonld` was **not** modified — see below.

### New id schemes introduced

| Namespace | Pattern | Examples | Permanence |
|---|---|---|---|
| (none) | — | — | The layer introduces **no new id namespace**. Property ids continue `BPO:NNNN`; operation ids continue `OP:*`. Local obligation and assumption identifiers in an assurance-case document belong to the verification project, are namespaced by that project, and are never minted here. |

### Deliberately *not* changed

- **`schema/context.jsonld`.** `external_refs` is not RDF-projected today, and this layer is not projected either. Emitting a non-entailing alignment link into the same graph as entailing `refines`/`implies` edges is the one way this integration could become unsound. Deferred until the projection can mark the distinction (a `bpo:alignsWith` term with no transitive semantics, or equivalent) — documented in `docs/ARCHITECTURE.md`, not silent.
- **`ontology/taxonomy.skos.ttl`.** `defi-lending` already existed; no new concept was needed.
- **`.github/workflows/validate.yml`.** No new dependency: the gates use only `json`, `re`, `glob` and the existing `jsonschema`.
- **The meaning of any pre-existing record.** The nine edges added to five existing records are additive relationship links; no `descriptions`, `formalization`, or `classification` field of an existing record was touched.
- **Any ISO 20022 intents for the lending operations.** The reference subset covers securities settlement and transfer messaging and has no collateralized-lending counterpart. Inventing one would be worse than an empty column; the gap is recorded in `OPERATIONS-coverage.md`.

### Empirical grounding

The abstraction derives from a collateralized-lending B-method verification study with 53 local obligations and 30 named assumptions. Against the 24-record baseline, that study's obligations aligned as 17 scoped instantiations, 28 partial overlaps, and 8 with no exact match. All eight gaps are now closed:

| Baseline gap | Closed by |
|---|---|
| Instance lifecycle / creation admission | `BPO:0118` admission clause |
| Exact interest accrual | `BPO:0112` exactness clause — post-state equals a declared relation |
| Monotone instance time | `BPO:0112` time-monotonicity and no-repeated-interval clauses |
| Valuation-shock reachability | `BPO:0113` non-vacuity obligation — the profile must admit reachable unhealthy states |
| Liquidation input-mode coherence | `BPO:0115`, k-safety and conditional on the modes existing |
| Instance-parameter immutability | `BPO:0118` immutability clause |
| Fee cap | `BPO:0118` bounded-parameter clause (the domain bound) **and** `BPO:0112` fee bound (generated value bounds the fee) — two distinct clauses, neither implying the other |
| Synchronous transaction rollback | `BPO:0021` |

That grounding is recorded **here and nowhere else**. No property record names the study, its subject, or its revision: `provenance.sources` cites "a collateralized-lending B-method verification study" and the denylist gate would fail the build on anything more specific.

### Final state (validator output)

```
== Operations catalogue ==
  OK   32 OP ids unique
  OK   operations -> ISO 20022 closure (12 iso20022_intents entries all resolve)
  OK   operations -> properties closure (70 governs_properties entries all resolve)

== assurance-case documents ==
  OK   shape  examples/assurance-case.example.json  (8 alignments, 4 assumptions)

== references ==
  all BPO: / DASCP: / ISO 20022: / IOF: targets resolve

== IOF scope-link consistency ==
  OK   all 9 behavioural blocks carry >= 1 cross-walk link; all 20 out-of-scope blocks carry zero

== protocol-identity denylist (normative fields) ==
  OK   37 records clean over 17 denied terms + 3 denied patterns (0 allowlisted exception(s))

== assurance-case gates ==
  OK   examples/assurance-case.example.json  all 8 gates pass (3 scoped / 3 partial / 2 unmatched)

== graph stats ==
  properties: 37
  edges by type: {'refines': 12, 'dependsOn': 48, 'composesWith': 45, 'mitigates': 97,
                  'conflictsWith': 11, 'refinedBy': 13}
  external ATK: targets referenced (Phase-2 registry): 88
  Operations catalogue: 32 operations
  Assurance-case documents:  1
    - examples/assurance-case.example.json: 8 alignments (3 scoped, 3 partial, 2 unmatched),
      4 local assumptions

RESULT: PASS (DAG closed over BPO: namespace; DASCP / Operations / ISO 20022 / IOF frameworks
        integral and closed; normative fields free of protocol identity; assurance-case gates
        satisfied)
```

Baseline for comparison: 24 properties, 22 operations, 35 `governs_properties` entries, 18 undischarged assumptions, 134 relationship edges. Now: 37 properties, 32 operations, 70 `governs_properties` entries, 40 undischarged assumptions, 226 edges. The undischarged ledger grew by 22, of which 9 belong to the three dependency contracts (`BPO:0120` ×2, `BPO:0121` ×3, `BPO:0122` ×4). That growth is the intended result of making external reliance explicit, not a regression: a lending layer that added no undischarged assumptions would be claiming its dependencies come for free.

### Gate verification

Every gate was negative-tested: each was mutated to violate its clause, the validator confirmed to exit 1 with the specific message, and the fixture restored. All 8 assurance-case gates fire (13 mutation cases including the schema-pinned `proof_transfer`), and the denylist was checked against both false negatives (protocol names, revisions, addresses, local ids, fixed constants) and false positives ("compound interest", "capacity curve", "Euler-Maclaurin", prover names). A gate that has never been seen to fail is not known to work.

### Not committed

Staged for maintainer review. No branch pushed, no pull request opened.

## IOF Interoperability Framework Cross-Walk — 2026-05-22

Cross-walked the **Interoperability Framework for Digital Asset Securities (IOF)** — DTCC, Clearstream, Euroclear, in collaboration with BCG, February 2026 — to the BPO catalogue. The IOF organizes interoperability into 5 foundations and 29 building blocks; BPO catalogues *behavioural* properties, so the cross-walk is dense exactly where the IOF describes provable on-chain behaviour (9 blocks) and empty everywhere else (20 blocks — legal/regulatory, data-harmonization, role/governance, operational/SLA — out-of-scope by design). The validator reports `PASS` on the final corpus (24 property records unchanged in meaning; IOF framework integral and closed; bidirectional scope-link consistency green). **Not committed** — staged for maintainer review.

### Design decisions recorded

- **Scope verdict lives in the data, not the prose.** Each IOF building block carries a `scope` field with the enum `{behavioural, out-of-scope}` in [`mappings/iof.framework.json`](mappings/iof.framework.json). The validator enforces **bidirectional scope-link consistency** as a build-time gate: out-of-scope blocks must carry zero cross-walk links from property records, and behavioural blocks must carry at least one. Either direction's violation fails the build, so the verdict cannot drift out of sync with the actual links.
- **Conservative relation enum on IOF cross-walks: no `establishes`.** Every IOF building block bundles policy, infrastructure, and behavioural concerns whose multi-facet character means a single BPO property can at most materially support a block, never wholly discharge it. The `external_refs.iof[].relation` enum is therefore `{supports, partially-supports}` only — tighter than the DASCP enum on purpose.
- **Each link's note states both sides.** Every cross-walk note follows a *behavioural slice covered, X stays out-of-scope* shape so the residual is visible at the link site, not buried in the framework prose. This makes the conservatism of the link auditable per-entry.
- **9 honest behavioural blocks beats 10 with a stretched one.** The behavioural test was applied rigorously; marginal blocks were downgraded rather than stretched. Three illustrative resolutions:
  - **BB-message-purpose** → out-of-scope. Its behavioural intent is "adopt an ISO-20022-style standard for instructions" — already realized by BPO via the ISO 20022 binding layer; cross-walking it again at the IOF layer would double-count.
  - **BB-time-management** → out-of-scope. Primary content (synchronised clocks, trusted time oracles, central timekeeping services) is governance/infrastructure. The one behavioural facet (no double-counting of an in-transit asset across chains) only partially aligns with BPO:0102's joint-state invariant and would need a dedicated *temporal cross-ledger consistency* property to bind cleanly — recorded as a future BPO candidate, not a stretched current link.
  - **BB-segregation-of-duties** → out-of-scope. Its appendix content is L1/L2 architectural separation, already covered through BPO:0090 / BPO:0080 via BB-consensus-and-finality; relinking here would dual-link to the same properties without adding coverage.
- **Inverted-emphasis coverage report.** [`mappings/IOF-coverage.md`](mappings/IOF-coverage.md) leads with the "same asset, same rights, same outcome" framing and then makes "What is deliberately not covered" the largest section — all 20 out-of-scope blocks named and categorized into legal/regulatory (7), data harmonization (7), roles/governance (4), operational/SLA (2). The majority-out-of-scope distribution is stated explicitly as the correct, expected outcome for an interoperability framework — not a coverage gap.
- **Additive-only.** Every schema edit is a new *optional* key under an existing `additionalProperties: false` container. Every one of the 24 pre-existing property records continues to validate without edit. No `BPO:` id is reused or renumbered. No relationship-edge type is invented.

### Files added (3)

- **[`mappings/iof.framework.json`](mappings/iof.framework.json)** — 5 foundations (IOF:F1–F5) and 29 building blocks (`IOF:BB-…`), each carrying official title (verbatim from Exhibits 2–3 of the white paper), paraphrased description in our own words, `enablers ⊆ {data, processes, roles}`, and `scope ∈ {behavioural, out-of-scope}`. Tally: 9 behavioural / 20 out-of-scope.
- **[`mappings/iof.framework.schema.json`](mappings/iof.framework.schema.json)** — JSON Schema fixing the file shape; id patterns `^IOF:F[0-9]+$` and `^IOF:BB-[a-z0-9]+(-[a-z0-9]+)*$`; internal-integrity checks (id uniqueness across foundations ∪ building_blocks; `building_block.foundation` closure) live in `schema/validate_refs.py`.
- **[`mappings/IOF-coverage.md`](mappings/IOF-coverage.md)** — coverage report with inverted emphasis; small "What is covered" section (the 9 behavioural blocks with their property links and residuals) plus the largest "What is deliberately *not* covered" section (the 20 out-of-scope blocks categorized into legal/regulatory, data harmonization, roles/governance, operational/SLA), with an honest-framing closing paragraph for FMI-facing conversations.

### Files modified (15)

#### Schema and validator (2)

- **[`schema/property.schema.json`](schema/property.schema.json)** — One additive optional field:
  - `identifiers.external_refs.iof[]` of `{id, relation, note?}` entries; id pattern `^IOF:BB-[a-z0-9]+(-[a-z0-9]+)*$` (foundation ids deliberately not admitted — only building blocks can carry cross-walks); `relation ∈ {supports, partially-supports}` (no `establishes`).
  - Every pre-existing record continues to validate without change.
- **[`schema/validate_refs.py`](schema/validate_refs.py)** — Extended with:
  - **Section 0d — IOF framework loader.** Own JSON Schema validation; id uniqueness across foundations ∪ building_blocks; internal closure (every `building_block.foundation` resolves to a foundation id).
  - **IOF cross-walk closure** inside Section 2. Every `external_refs.iof[].id` referenced from any BPO property must resolve to a *building-block* id; foundation ids and unknown ids both fail.
  - **Section 2b — bidirectional scope-link consistency.** A reverse index `building_block_id → [(property, relation), …]` is built while traversing properties; out-of-scope blocks carrying ≥ 1 link FAIL, behavioural blocks carrying 0 links FAIL. Both halves must hold.
  - Final RESULT line and Section 4 stats output extended with IOF counts.

#### Documentation (1)

- **[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)** — New section "IOF cross-walk: behavioural layer of an interoperability framework" after the three-layer-model section. Explains the *same asset, same rights, same outcome* positioning, the structural rather than editorial honesty enforced by the `scope` field + bidirectional check, the relation enum's exclusion of `establishes`, and points at [`mappings/IOF-coverage.md`](mappings/IOF-coverage.md) for the full coverage report. The layout listing under `mappings/` is updated to include the three new IOF files. The Validation paragraph is extended to mention IOF closure, IOF behavioural-id restriction on cross-walks, and the bidirectional scope-link consistency check.

#### Property records — IOF cross-walks added (12)

Each record had a new `iof` array added inside `identifiers.external_refs`. 15 entries total; honest `supports` for the 5 blocks a property materially carries, `partially-supports` for the 10 facet-only links. Every note records the behavioural slice covered AND the surrounding dimension that stays out-of-scope.

- [`BPO:0003`](properties/BPO-0003-zero-knowledge.json) — BB-data-privacy (partial).
- [`BPO:0030`](properties/BPO-0030-storage-layout-isolation.json) — BB-contract-versioning-management (partial); BB-smart-contracts-and-tokens-structure (partial).
- [`BPO:0040`](properties/BPO-0040-access-control-correctness.json) — BB-roles-in-data-access.
- [`BPO:0041`](properties/BPO-0041-multiparty-transaction-validation.json) — BB-roles-in-data-access (partial).
- [`BPO:0050`](properties/BPO-0050-emergency-pause-safety.json) — BB-smart-contracts-and-tokens-structure (partial).
- [`BPO:0073`](properties/BPO-0073-circuit-public-signal-non-leakage.json) — BB-data-privacy (partial).
- [`BPO:0075`](properties/BPO-0075-private-data-confidentiality-hyperproperty.json) — BB-data-privacy.
- [`BPO:0080`](properties/BPO-0080-consensus-liveness.json) — BB-consensus-and-finality (partial).
- [`BPO:0090`](properties/BPO-0090-settlement-finality-irrevocability.json) — BB-consensus-and-finality; BB-enforceability-of-transfers-and-finality-in-settlement (partial).
- [`BPO:0091`](properties/BPO-0091-fail-to-settle-reversal.json) — BB-on-chain-off-chain-protocols (partial).
- [`BPO:0092`](properties/BPO-0092-transaction-sequencing-and-replay-resistance.json) — BB-cross-dlt-protocols (partial).
- [`BPO:0102`](properties/BPO-0102-cross-ledger-inventory-consistency.json) — BB-cross-dlt-protocols; BB-asset-location-controls.

### New id scheme introduced

| Namespace | Pattern | Examples | Permanence |
|---|---|---|---|
| `IOF:F` (foundations) | `^IOF:F[0-9]+$` | `IOF:F1`, `IOF:F4` | Mirrors the IOF white paper's foundation numbering. |
| `IOF:BB-` (building blocks) | `^IOF:BB-[a-z0-9]+(-[a-z0-9]+)*$` | `IOF:BB-cross-dlt-protocols`, `IOF:BB-data-privacy` | Kebab-case rendering of the white paper's official building-block titles. |

### Deliberately *not* changed

- **No new BPO:NNNN ids minted.** This integration adds a layer beside the property records; no new property was authored. The "temporal cross-ledger consistency" candidate surfaced by BB-time-management is recorded for future authoring, not minted now.
- **No relationship-edge type invented.** IOF cross-walks live in `identifiers.external_refs.iof`, not in property records' `relationships` (which remain confined to the 13 legal property-to-property edge types).
- **No silent rewrite of any property's formalization.** All 12 affected records had only the `external_refs.iof[]` array appended; no other field of any record was edited.
- **DASCP, ISO 20022, and operations layers untouched.** The IOF integration is additive over the three existing cross-walks; no entries in [`mappings/dascp.framework.json`](mappings/dascp.framework.json), [`mappings/iso20022.framework.json`](mappings/iso20022.framework.json), [`mappings/operations.catalogue.json`](mappings/operations.catalogue.json), or their schemas/coverage reports were modified.
- **Provenance / authorship conventions** — Preserved verbatim. No identifying authorship was added to any record, header, or commit field.

### Final state (validator output)

```
properties: 24                                       (unchanged in meaning)
IOF framework:        34 ids (5 foundations + 29 building blocks; behavioural=9, out-of-scope=20)
IOF cross-walk entries from properties:          15  (closure OK)
IOF scope-link consistency: all 9 behavioural blocks carry ≥ 1 cross-walk link;
                            all 20 out-of-scope blocks carry zero               (OK)
DASCP cross-walk entries from properties:        37  (unchanged)
ISO 20022 depth-1 cross-walk entries:            16  (unchanged)
ISO 20022 depth-2 binding entries:               19  (unchanged)
Operations → properties (governs_properties):    35  (unchanged)
Operations → ISO 20022 (iso20022_intents):       12  (unchanged)
undischarged-assumption ledger entries:          18  (unchanged)
edges by type: refines 5, refinedBy 4, composesWith 34, dependsOn 24, conflictsWith 6, mitigates 61  (unchanged)

RESULT: PASS (DAG closed over BPO: namespace; DASCP / Operations / ISO 20022 / IOF frameworks integral and closed)
```

### Not committed

These changes are staged for maintainer review. No `git commit`, `git push`, or branch creation was executed.

## Operations Catalogue + ISO 20022 Binding — 2026-05-22

Added two additive layers to the catalogue under `mappings/` — an **Abstract Operations** catalogue and an **ISO 20022 reference binding** at two depths — closing a three-layer model that runs **ISO 20022 message intent → abstract operation → governing BPO property → ISO 20022 element binding**. The validator reports `PASS` on the final corpus (24 property records still unchanged in meaning; both new frameworks integral and closed). **Not committed** — staged for maintainer review.

### Design decisions recorded

- **Operations are not functions.** An operation is an abstract *kind of state change* (TRANSFER, MINT, BURN, PAUSE, SETTLE, ENCUMBER, …). Function signatures like `transferFrom(address,address,uint256)` appear only under each operation's `examples` field and are explicitly *non-normative*. A hard inclusion bar gates entries: a candidate qualifies only if it is (a) a distinct kind of state change and (b) at least one current BPO property's formalization treats it differently from its neighbours. Six candidates that failed the bar are held in `candidates_pending_grounding[]`, not silently elevated. Result: 22 operations (well under the ≤30 ceiling), all corpus-grounded.
- **ISO 20022 binding is by reference, not by replication.** ISO 20022 publishes identifiers and structure free-of-use via iso20022.org; the framework file mirrors only the 18 ids the corpus or operations catalogue actually points at, with paraphrased descriptions in our own words and a top-level `license_note` citing the source. No bulk replication of the data dictionary.
- **Additive-only.** Every schema edit is a new *optional* key under an existing `additionalProperties: false` container. Every one of the 24 pre-existing property records continues to validate without edit. No `BPO:` id is reused or renumbered. No relationship-edge type is invented (the operation↔property link lives in the catalogue, not in property records' `relationships`).
- **Depth-2 binding integrity is strict.** A symbol-binding is admitted only when (i) the bound `element` resolves in the ISO 20022 framework AND (ii) the bound `symbol` passes the symbol-in-formalization check — Tier 1 structured lookup against `formalization.symbols` when present, Tier 2 whole-token regex against `formalization.signature` only as fallback, case-sensitive throughout, no near-match. A binding that silently mis-resolves would be worse than no binding.
- **Three-layer model documented.** A new section in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) walks the chain end-to-end using `BPO:0090` settlement-finality as the worked example.

### Files added (6)

#### Operations framework (3)

- **[`mappings/operations.catalogue.json`](mappings/operations.catalogue.json)** — 22 operations with definitions, state-change semantics, non-normative `examples`, `iso20022_intents`, and `governs_properties` (35 link entries) — plus 6 `candidates_pending_grounding` with rationale for each held-out candidate.
- **[`mappings/operations.catalogue.schema.json`](mappings/operations.catalogue.schema.json)** — JSON Schema fixing the file shape; internal-integrity checks (id uniqueness; cross-framework closure of `iso20022_intents`; closure of `governs_properties` into the BPO corpus) live in `schema/validate_refs.py`.
- **[`mappings/OPERATIONS-coverage.md`](mappings/OPERATIONS-coverage.md)** — per-operation and per-property coverage tables; lists the 3 partial-only-coverage operations (TRANSFER, BURN, DEPOSIT) as honest signal that the property catalogue is thin in those slices; lists the 6 candidates pending grounding.

#### ISO 20022 framework (3)

- **[`mappings/iso20022.framework.json`](mappings/iso20022.framework.json)** — 18 ISO 20022 ids in three groups: 7 messages (`sese.020`, `sese.023–025`, `semt.013`, `setr.044`, `setr.054`), 5 components (`PartyIdentification`, `SecuritiesAccount`, `FinancialInstrument`, `SettlementDetails`, `TransactionStatus`), 6 elements (`SettlementTransactionIdentification`, `SettlementDate`, `TradeDate`, `SettlementAmount`, `SettlementQuantity`, `PartyRole`). All paraphrased; `license_note` cites the iso20022.org Financial Repository as the authoritative source.
- **[`mappings/iso20022.framework.schema.json`](mappings/iso20022.framework.schema.json)** — JSON Schema fixing the file shape; internal-integrity check (id uniqueness across messages ∪ components ∪ elements) lives in `schema/validate_refs.py`.
- **[`mappings/ISO20022-coverage.md`](mappings/ISO20022-coverage.md)** — per-property depth-1 and depth-2 view; documents the symbol-in-formalization check; includes a second worked example (BPO:0091 fail-to-settle) to complement the BPO:0090 trace in `ARCHITECTURE.md`.

### Files modified (15)

#### Schema and validator (2)

- **[`schema/property.schema.json`](schema/property.schema.json)** — Three additive optional fields:
  - `identifiers.external_refs.iso20022[]` (depth-1 cross-walks; `relation ∈ {relates-to, constrains}`).
  - `formalization.symbols[]` (declarative list enabling Tier-1 structured lookup for depth-2 bindings).
  - `formalization.bindings[]` (depth-2 symbol→element mappings).
  All optional; every pre-existing record continues to validate without change.
- **[`schema/validate_refs.py`](schema/validate_refs.py)** — Extended with:
  - Operations catalogue loader + shape validation; id uniqueness; cross-framework closure of `iso20022_intents` into ISO 20022; cross-corpus closure of `governs_properties` into the BPO property corpus.
  - ISO 20022 framework loader + shape validation; id uniqueness across messages, components, elements.
  - Depth-1 cross-walk closure (property's `external_refs.iso20022[].id` → ISO 20022 framework).
  - Depth-2 binding closure (property's `formalization.bindings[].element` → ISO 20022 framework) plus the `symbol_in_formalization` Tier-1/Tier-2 check.
  - Cross-framework load order: independent frameworks (DASCP, ISO 20022) first, then operations (which references both ISO 20022 and the property corpus), then property cross-walks last.
  - Stats output extended with `governs_properties`, `iso20022_intents`, depth-1, and depth-2 counts.

#### Documentation (1)

- **[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)** — New section "Three-layer model: intent → operation → property" between "Designed to be referenced, not just read" and "Validation". Walks the BPO:0090 example end-to-end and records the additive-only / operations-not-functions / binding-by-reference disciplines.

#### Property records — depth-1 ISO 20022 cross-walks added (11)

Each carries `identifiers.external_refs.iso20022[]` of `{id, relation, note}` entries; 16 entries total; honest `relates-to` (general relevance) and `constrains` (behavioural bound) qualifiers per entry.

[`BPO:0001`](properties/BPO-0001-no-unauthorized-mint.json) → setr.044 (constrains).
[`BPO:0002`](properties/BPO-0002-eventual-withdrawal.json) → setr.054 (relates-to).
[`BPO:0041`](properties/BPO-0041-multiparty-transaction-validation.json) → sese.023 (constrains).
[`BPO:0050`](properties/BPO-0050-emergency-pause-safety.json) → sese.023 (constrains).
[`BPO:0051`](properties/BPO-0051-scoped-pause-safety-bounded.json) → semt.013 (constrains).
[`BPO:0090`](properties/BPO-0090-settlement-finality-irrevocability.json) → sese.023, sese.024, sese.025 (all constrains).
[`BPO:0091`](properties/BPO-0091-fail-to-settle-reversal.json) → sese.024 (relates-to).
[`BPO:0092`](properties/BPO-0092-transaction-sequencing-and-replay-resistance.json) → elem/SettlementTransactionIdentification (relates-to).
[`BPO:0093`](properties/BPO-0093-encumbrance-pre-settlement.json) → semt.013 (constrains), cmp/SecuritiesAccount (relates-to), cmp/FinancialInstrument (relates-to).
[`BPO:0101`](properties/BPO-0101-conservation-of-value.json) → sese.023 (constrains), elem/SettlementAmount (relates-to).
[`BPO:0102`](properties/BPO-0102-cross-ledger-inventory-consistency.json) → cmp/FinancialInstrument (relates-to).

#### Property records — depth-2 bindings added (8), with `formalization.symbols` enabling Tier-1 structured lookup

19 binding entries total; each binding has its `element` resolve in the ISO 20022 framework AND its `symbol` pass the structured-lookup check (Tier 1 used throughout — every property with a binding has a `formalization.symbols` list declared).

- [`BPO:0001`](properties/BPO-0001-no-unauthorized-mint.json): `Addr → cmp/PartyIdentification`; `hasRole_MINTER → elem/PartyRole` (partial — role-membership).
- [`BPO:0040`](properties/BPO-0040-access-control-correctness.json): `Principals → cmp/PartyIdentification`; `Authorities → elem/PartyRole`.
- [`BPO:0041`](properties/BPO-0041-multiparty-transaction-validation.json): `Validators → cmp/PartyIdentification` (identity); `Validators → elem/PartyRole` (role aspect).
- [`BPO:0090`](properties/BPO-0090-settlement-finality-irrevocability.json): `SettlementID → elem/SettlementTransactionIdentification`; `accountedOutcome → elem/SettlementAmount` (partial — monetary face); `final → cmp/TransactionStatus` (selects SETTLED value).
- [`BPO:0091`](properties/BPO-0091-fail-to-settle-reversal.json): `parties → cmp/PartyIdentification`; `deadline → elem/SettlementDate` (partial — date granularity); `status → cmp/TransactionStatus`.
- [`BPO:0093`](properties/BPO-0093-encumbrance-pre-settlement.json): `total → cmp/SecuritiesAccount` (partial — aggregate position); `Holder → cmp/PartyIdentification` (account-owner role); `Asset → cmp/FinancialInstrument`; `Obligation → elem/SettlementTransactionIdentification`; `obligationStatus → cmp/TransactionStatus`.
- [`BPO:0101`](properties/BPO-0101-conservation-of-value.json): `V → elem/SettlementAmount` (partial — per-leg projection).
- [`BPO:0102`](properties/BPO-0102-cross-ledger-inventory-consistency.json): `Asset → cmp/FinancialInstrument`.

#### One reviewable signature edit (BPO:0093 only)

- [`BPO:0093`](properties/BPO-0093-encumbrance-pre-settlement.json) `formalization.signature`: the opening clause `Holder × Asset → ℕ;` was a type signature with no name, while the FOL already referenced `total(h, a, s)`. Renamed to `total : Holder × Asset × State → ℕ;` — a minor surface change that closes a genuine internal-consistency gap in the formalization. The enabled `total → cmp/SecuritiesAccount` depth-2 binding is a welcome byproduct, not the reason. Surfaced as a proposed reviewable edit in Step 5 before being applied; no other property's formalization was touched.

### New id schemes introduced

| Namespace | Pattern | Examples | Permanence |
|---|---|---|---|
| `OP:` (operations) | `^OP:[A-Z][A-Z0-9]*(-[A-Z0-9]+)*$` | `OP:TRANSFER`, `OP:BRIDGE-LOCK`, `OP:UPGRADE` | Permanent; retired ids stay retired, never reused. |
| `ISO20022:` (reference subset) | `^ISO20022:(?:[a-z]+\.[0-9]{3}\|cmp/[A-Za-z][A-Za-z0-9]*\|elem/[A-Za-z][A-Za-z0-9]*)$` | `ISO20022:sese.023`, `ISO20022:cmp/PartyIdentification`, `ISO20022:elem/SettlementDate` | Mirrors ISO 20022's own identifier conventions. |

### Deliberately *not* changed

- **No new BPO:NNNN ids minted.** This integration adds layers above and beside the property records; no new property was authored.
- **No relationship-edge type invented.** Operations↔properties links live in the operations catalogue, not in property records' `relationships` (which remain confined to the 13 legal property-to-property edge types).
- **No silent rewrite of any property's formalization.** The one signature edit (BPO:0093 `total` declaration) was surfaced as a proposed reviewable change in Step 5 and applied only after explicit approval.
- **Operations and ISO 20022 frameworks kept thin.** 22 operations (≤30 inclusion ceiling); 18 ISO 20022 ids (only what the corpus or operations catalogue references). Six candidate operations held in `candidates_pending_grounding[]`; ISO 20022 `elem/PartyRole` added in Step 5 only because medium-fit bindings explicitly needed it.
- **No authorship / provenance / commit-convention changes.** Property records' `provenance.authors` left intact.

### Final state (validator output)

```
properties: 24                                       (unchanged in meaning)
Operations catalogue: 22 operations                  (+ 6 candidates pending grounding)
ISO 20022 framework:  18 ids (msg=7, cmp=5, elem=6)
DASCP cross-walk entries from properties:        37  (unchanged)
ISO 20022 depth-1 cross-walk entries:            16
ISO 20022 depth-2 binding entries:               19
Operations → properties (governs_properties):    35  (closure OK)
Operations → ISO 20022 (iso20022_intents):       12  (closure OK)
undischarged-assumption ledger entries:          18  (unchanged)
edges by type: refines 5, refinedBy 4, composesWith 34, dependsOn 24, conflictsWith 6, mitigates 61  (unchanged)

RESULT: PASS (DAG closed over BPO: namespace; DASCP / Operations / ISO 20022 frameworks integral and closed)
```

### Not committed

These changes are staged for maintainer review. No `git commit`, `git push`, or branch creation was executed.

## DASCP Integration — 2026-05-21

Cross-walked the **Digital Asset Securities Control Principles (DASCP)** — DTCC / Clearstream / Euroclear, May 2024 — to the BPO catalogue, and authored eight new BPO property records to address the technical gaps the cross-walk surfaced. The validator reports `PASS` on the final corpus (24 properties; DASCP framework integral and closed). **Not committed** — staged for maintainer review.

### Files added (12)

#### Framework (new top-level `mappings/` directory)

- **`mappings/dascp.framework.schema.json`** — JSON Schema 2020-12 for the catalogue file. `mitigates_risks` items use `oneOf [string, {risk, note?}]` so verbatim links stay plain and judgment-call links carry inline provenance notes.
- **`mappings/dascp.framework.json`** — Full DASCP catalogue: 6 principles (P1–P6), 36 risks (R1–R36 with principle assignment), 57 controls (C1–C57 with category suffix and `mitigates_risks`). Sourced from the DTCC white paper (https://www.dtcc.com/-/media/DASCPWhitePaper.pdf); titles and risk↔control attributions taken from the appendix and cross-checked against the consolidated control-card figure on p. 14; descriptions paraphrased in our own words. The 16 interpretive links from the two appendix pages where multiple risks shared a Controls column (p. 26 R2/R3 split; p. 34 R20/R21 split) carry inline `note` fields documenting the subject-matter judgment and the p. 14 cross-check.
- **`mappings/DASCP-coverage.md`** — Control-by-control coverage report. Step 2 introduced; Step 5 refreshed to reflect the ten newly-linked controls.

#### New BPO property records (8 ids minted in sequence within thematic decades; no retired number reused)

| Id | Slug | Modal class | DASCP answered | File |
|---|---|---|---|---|
| **BPO:0041** | multiparty-transaction-validation                       | safety                                      | C16-S         | [`properties/BPO-0041-multiparty-transaction-validation.json`](properties/BPO-0041-multiparty-transaction-validation.json) |
| **BPO:0051** | scoped-pause-safety-bounded                             | safety + guarantee-liveness-conditional     | C30-S, C31-S  | [`properties/BPO-0051-scoped-pause-safety-bounded.json`](properties/BPO-0051-scoped-pause-safety-bounded.json) |
| **BPO:0075** | private-data-confidentiality-hyperproperty              | **hypersafety, non-interference (2-safety)** | C40-R, C41-R  | [`properties/BPO-0075-private-data-confidentiality-hyperproperty.json`](properties/BPO-0075-private-data-confidentiality-hyperproperty.json) |
| **BPO:0090** | settlement-finality-irrevocability                      | safety                                      | C48-N         | [`properties/BPO-0090-settlement-finality-irrevocability.json`](properties/BPO-0090-settlement-finality-irrevocability.json) — opens new 90s settlement decade |
| **BPO:0091** | fail-to-settle-reversal                                 | safety + guarantee-liveness-conditional     | C49-N         | [`properties/BPO-0091-fail-to-settle-reversal.json`](properties/BPO-0091-fail-to-settle-reversal.json) |
| **BPO:0092** | transaction-sequencing-and-replay-resistance            | safety                                      | C50-N         | [`properties/BPO-0092-transaction-sequencing-and-replay-resistance.json`](properties/BPO-0092-transaction-sequencing-and-replay-resistance.json) |
| **BPO:0093** | encumbrance-pre-settlement                              | safety                                      | C47-N         | [`properties/BPO-0093-encumbrance-pre-settlement.json`](properties/BPO-0093-encumbrance-pre-settlement.json) |
| **BPO:0102** | cross-ledger-inventory-consistency                      | safety (joint-state)                        | C51-N         | [`properties/BPO-0102-cross-ledger-inventory-consistency.json`](properties/BPO-0102-cross-ledger-inventory-consistency.json) |

All eight enter at `status: draft` per `CONTRIBUTING.md`. All DASCP cross-walk targets are `partially-supports` — none claim discharge of a control's full scope; the cleanest candidates (BPO:0041 → C16-S; BPO:0092 → C50-N) were deliberately not upgraded to `establishes`, with `note` fields recording the operational residual that justifies the conservative qualifier.

### Files modified (15)

#### Schema and validator (2)

- **`schema/property.schema.json`** — Additive, backward-compatible: new `dascp` key under `identifiers.external_refs` (array of `{id, relation, note?}` objects with `relation ∈ {establishes, supports, partially-supports}`; id pattern is a loose `^(P[0-9]+|R[0-9]+|C[0-9]+-[LSRN])$` shape check, with closure against the framework file as the authoritative gate). Every pre-existing record continues to validate without change.
- **`schema/validate_refs.py`** — Four extensions, each labelled at the top of the file:
  1. *DASCP framework loading* — own JSON Schema validation, then internal-integrity checks (id uniqueness across P/R/C; `risk.principle` closure to a real principle; `control.mitigates_risks` closure to a real risk — handling both string-form and `{risk, note}` object-form items).
  2. *Cross-walk closure* — every `dascp[].id` referenced from any BPO property record must resolve in the framework file; dangling DASCP ids fail the build the same way dangling `BPO:` edges do.
  3. *Cross-platform `ROOT` path* — via `os.path.dirname(os.path.abspath(__file__))` instead of the previous slash-based heuristic.
  4. **Robustness fix: UTF-8 stdout** — `sys.stdout.reconfigure(encoding="utf-8")` at startup, so the assumption-ledger and reference output containing JSON-legal Unicode (math symbols, em-dashes, arrows) prints cleanly on Windows consoles whose default codec is cp1252. *Deliberate.* The alternative — banning Unicode from formal and ledger fields to suit a legacy codepage — would be a worse constraint on the catalogue than a five-line encoding guard at the output layer. Reverting this would force editorial restrictions on formal content; keeping it means the data layer stays expressive and the validator stays robust.

#### Property records — DASCP cross-walks added (13)

Each of these records had a `dascp` array added inside `identifiers.external_refs`. All entries carry `relation: partially-supports` or `relation: supports` and a `note` spelling out the covered slice vs. the residual the DASCP control still demands. 27 cross-walk entries in total from Step 2; 10 additional entries from the Step 4 new records (per their own `dascp` arrays).

- [`properties/BPO-0001-no-unauthorized-mint.json`](properties/BPO-0001-no-unauthorized-mint.json) — added 3 entries (C19-S, C24-S, C28-S)
- [`properties/BPO-0003-zero-knowledge.json`](properties/BPO-0003-zero-knowledge.json) — added 2 entries (C40-R, C41-R)
- [`properties/BPO-0020-reentrancy-safety.json`](properties/BPO-0020-reentrancy-safety.json) — added 1 entry (C47-N)
- [`properties/BPO-0030-storage-layout-isolation.json`](properties/BPO-0030-storage-layout-isolation.json) — added 1 entry (C44-R)
- [`properties/BPO-0040-access-control-correctness.json`](properties/BPO-0040-access-control-correctness.json) — added 4 entries (C19-S, C28-S, C15-S, C45-R)
- [`properties/BPO-0050-emergency-pause-safety.json`](properties/BPO-0050-emergency-pause-safety.json) — added 3 entries (C29-S, C30-S, C31-S)
- [`properties/BPO-0070-knowledge-soundness.json`](properties/BPO-0070-knowledge-soundness.json) — added 2 entries (C48-N, C32-R)
- [`properties/BPO-0072-public-auditability.json`](properties/BPO-0072-public-auditability.json) — added 2 entries (C32-R, C46-N)
- [`properties/BPO-0073-circuit-public-signal-non-leakage.json`](properties/BPO-0073-circuit-public-signal-non-leakage.json) — added 2 entries (C40-R, C41-R)
- [`properties/BPO-0074-crypto-hardness-setup-assumptions.json`](properties/BPO-0074-crypto-hardness-setup-assumptions.json) — added 1 entry (C20-S)
- [`properties/BPO-0080-consensus-liveness.json`](properties/BPO-0080-consensus-liveness.json) — added 2 entries (C36-R, C38-R)
- [`properties/BPO-0082-l2-escape-hatch.json`](properties/BPO-0082-l2-escape-hatch.json) — added 1 entry (C21-S)
- [`properties/BPO-0101-conservation-of-value.json`](properties/BPO-0101-conservation-of-value.json) — added 3 entries (C25-S, C26-S, C51-N)

### Files deliberately *not* touched

- **No DASCP link on BPO:0002, BPO:0060, BPO:0081.** Recorded as deliberate non-mappings. BPO:0002's relationship to the pause-control family is *tension*, not establishment — encoded as `conflictsWith` on BPO:0050 and BPO:0051. BPO:0060 (compilation correctness) has no behaviourally-aligned DASCP control. BPO:0081 (censorship resistance) addresses risk content that no specific DASCP control covers.
- **`README.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `ontology/axes.md`, `ontology/taxonomy.skos.ttl`, `schema/context.jsonld`** — Unchanged. The DASCP integration is additive and required no documentation or ontology restructure.
- **Provenance / authorship conventions** — Preserved verbatim. No identifying authorship was added to any record, header, or commit field.

### Final state (validator output)

```
properties: 24                                       (16 seed + 8 new)
DASCP framework ids: 99                              (P=6, R=36, C=57)
DASCP cross-walk entries from properties: 37         (27 Step 2 + 10 Step 4)
DASCP coverage: 0 established / 25 partial / 32 gap
  — Step 3 candidates remaining as gaps: 0          (all 11 now at least partial)
  — out-of-scope gaps: 32                            (process / governance / infrastructure / standardization / education)
undischarged-assumption ledger entries: 18           (11 prior + 7 new in Step 4; of the 7, 4 are the named-honesty entries from the Step 4 directives and 3 are additional load-bearing dependencies surfaced during authoring)
external ATK: targets referenced (Phase-2 registry): 56
edges by type: refines 5, refinedBy 4, composesWith 34, dependsOn 24, conflictsWith 6, mitigates 61

RESULT: PASS (DAG closed over BPO: namespace; DASCP framework integral and closed)
```

### Not committed

These changes are staged for maintainer review. No `git commit`, `git push`, or branch creation was executed. When committed, the maintainer's existing commit conventions apply.
