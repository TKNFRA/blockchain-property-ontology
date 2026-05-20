# BPO Classification Axes

The single most important architectural decision in BPO is that a property is **not a leaf in one tree**. It is a **point in a multi-axis faceted space**, plus a body of facets, plus typed edges to other properties. Single-tree taxonomies (the usual blockchain "vulnerability list") collapse under their own cross-cutting: "reentrancy" is simultaneously an EVM concern, a safety property, a control-flow property, and a mitigation target. Forcing it into one parent loses information and makes machine reasoning brittle.

BPO therefore uses **five orthogonal classification axes** (encoded in `classification` of each record) plus an open **relationship DAG** (encoded in `relationships`).

| Axis | Field | Vocabulary | What it captures | Why orthogonal |
|------|-------|-----------|------------------|----------------|
| **A. Modal class** | `modal_class` | safety, liveness, hypersafety, k-safety, observational-determinism, non-interference, conditional-liveness | The *logical shape* (Alpern–Schneider + Clarkson–Schneider). Determines which verification machinery can even apply. | A "DeFi" property may be safety *or* liveness *or* a hyperproperty; domain doesn't fix shape. |
| **B. Deontic role** | `deontic_role` | invariant, assumption, guarantee, obligation, constraint, policy, capability, permission, cryptographic-/trust-/environmental-assumption, temporal-commitment | The *assume–guarantee role*: does the property OFFER something or RELY ON something? | The same statement ("the sequencer posts within N blocks") is an *assumption* for the rollup contract and a *guarantee* for the sequencer. |
| **C. Domain** | `domains` | SKOS poly-hierarchy (`taxonomy.skos.ttl`) | Subject matter (EVM, ZK circuit, lending, bridge, agentic…). | Pure subject; says nothing about logical shape or proof method. |
| **D. Abstraction level** | `abstraction_levels` | bytecode, ir, contract, protocol, economic, systemic, governance, cryptographic | *Vertical* placement. Economic "solvency" REFINES into contract-level invariants. | Lets the same conceptual property exist at several levels linked by `refines` edges. |
| **E. Verification modality** | `verification_modalities` + `decidability` | smt, symbolic-execution, (bounded-)model-checking, abstract-interpretation, ITP, type-checking, runtime-verification, fuzzing, cryptographic-proof, static-dataflow | What can actually discharge it, and how completely. | Independent of all the above; honest about decidability limits. |

## The hyperproperty distinction (Axis A) — the most consequential subtlety

Most blockchain "security tooling" silently assumes every property is a **trace property** (a set of admissible individual executions), because that is what reachability-based symbolic execution and fuzzing can check. But several of the highest-value properties are **hyperproperties** (sets of *sets* of executions; they relate ≥2 traces):

- **Zero-knowledge / privacy** — defined by indistinguishability of *two systems* (real vs. simulator). A 2-execution / observational property.
- **Non-interference / confidentiality** — secret inputs do not affect public outputs across pairs of runs.
- **Observational determinism, MEV-fairness, ordering-fairness** — relate alternative orderings.
- **Constant-time / side-channel resistance** in client crypto.

A k-safety hyperproperty can be verified by *self-composition* + a safety checker; a hyperliveness property generally cannot be handled by single-trace tools at all. **Mislabeling a hyperproperty as safety and "verifying" it with a single-trace fuzzer is a category error that produces false assurance.** BPO makes the distinction load-bearing.

## The deontic / assume–guarantee discipline (Axis B)

Every `guarantee` carries a set of `assumptions` it rests on (the `assumptions` array + `dependsOn` edges). The corpus is only sound if, for any deployed system, the union of relied-upon assumptions is *discharged* — either by another property's guarantee (`discharged_by`) or by an explicit accepted trust assumption. A property whose `dependsOn`-closure contains an undischarged assumption is **conditionally assured**, and BPO query tooling is expected to surface that. This is the mechanism by which "we verified solvency" is forced to expose "…assuming the oracle is honest and the chain is live under synchrony."

## How the axes combine into queries

Because each axis is independent, the corpus supports faceted retrieval such as:

> *"All `safety` (A) `invariant` (B) properties in `evm` ∪ `token` (C) at `contract` level (D) that are `smt`-decidable (E) and `mitigate` attack-class X, together with the transitive `dependsOn`-closure of their assumptions."*

That query is answerable by SPARQL over the RDF projection (`context.jsonld`) using the transitive edges declared in `relationship.vocab.json`.
