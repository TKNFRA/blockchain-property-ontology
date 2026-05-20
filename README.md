# Blockchain Property Ontology (BPO)

**A living, machine-readable catalogue of the properties blockchain systems are supposed to have — and a precise account, for each one, of what it means, why it matters, how it can fail, and how it can actually be verified.**

---

## Why this exists

Every few months, a blockchain system loses an enormous sum to a failure the field already understood. The reason this keeps happening is structural: we have built powerful machinery for *checking* code — analyzers, fuzzers, theorem provers — and almost nothing for *agreeing on what correctness means in the first place.*

Today, that knowledge is scattered across audit reports, blog posts, war stories, and the tacit expertise of a few specialists. Every audit re-derives its requirements from intuition. Every tool encodes its own private notion of "a problem." Every team writes its safety goals, if at all, in prose no one else can reuse and no machine can read.

BPO is an attempt to fix the missing layer — not with another tool, but with a **shared map.** Think of it as a periodic table for correctness: each property given a stable identity, a structured description, and a position relative to every other property, so that everyone's work can finally add up.

## What this is

A catalogue of the properties blockchain systems should satisfy — safety, liveness, access control, economic soundness, cryptographic and zero-knowledge guarantees, governance, cross-chain integrity, and the behaviour of autonomous on-chain agents.

Each entry describes one property from every angle that matters at once:

- in **plain language** anyone can read,
- in **precise mathematics**,
- and in a **structured, machine-readable form** that verification tools and automated auditors can consume directly.

It records the property's relationships to others — which properties imply it, depend on it, strengthen it, or conflict with it. It maps the attack patterns that exploit its absence, often with references to real historical incidents. It lists what you would need to *observe* and *monitor* to know it's holding in production. And it cross-references the established industry registries of weaknesses and standards, so the new structure sits *beside* existing knowledge rather than asking anyone to abandon it.

The result is that the same entry serves a smart-contract developer wanting a checklist, a security auditor choosing a verification strategy, a formal-methods researcher needing a precise specification, and an automated tool consuming the whole thing as data. One source of truth, many doors in.

## Principles

**Honest about verification.** Each entry states what is *mechanically* achievable. Liveness needs fairness assumptions and model-checking or interactive proof, not fuzzing. Cryptographic indistinguishability needs a reduction, not an SMT solver. Hyperproperties (zero-knowledge, non-interference, ordering fairness) relate *multiple* executions and cannot be established by single-trace tools at all — treating them as if they could is a category error that manufactures false assurance. BPO never overstates what a tool can deliver.

**Assumptions are first-class.** Every guarantee exposes the assumptions it rests on, and whether each is discharged by another property or simply *accepted*. This is how "we verified solvency" is forced to also say "…assuming the oracle is honest and the chain is live." Conditional assurance is labelled as conditional.

**Conflicts are recorded, not hidden.** Some properties pull against each other — an emergency pause versus a guarantee of eventual withdrawal, transparency versus privacy. BPO records such conflicts explicitly, so designers confront the trade-off with their eyes open.

**It sits beside existing knowledge, not on top of it.** Entries cross-reference the established weakness registries and engineering standards, so prior knowledge flows in rather than being thrown away.

**Stable identity.** Every property has a permanent, meaningless identifier that never changes even when the property is reclassified or rewritten — so other systems can safely point to it for years.

## What's in this repository today

This is an early, deliberately small **seed**: the underlying structure and schema, the classification scheme and relationship vocabulary, a set of fully-worked exemplar properties chosen to stress every part of the design, and an automated validator that checks the whole catalogue for internal consistency. The seed is intentionally compact so the design can be refined cheaply before it scales.

If you want the design rationale behind the schema — the five classification axes, the treatment of hyperproperties, the assume–guarantee discipline, and the authoring rules — see [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md).

The catalogue is being actively expanded across domains. Direction is emerging, and is being shaped together with early contributors and partners.

### Checking the catalogue

```bash
pip install jsonschema
python3 schema/validate_refs.py
```

The validator schema-checks every record, fails on any dangling relationship, prints the ledger of accepted (undischarged) assumptions, and reports `PASS` when the catalogue is internally consistent.

## How to contribute

Contributions of properties, verification strategies, attack patterns, and corrections are welcome — held to an explicit quality bar, because the entire value of this work rests on its rigor. Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) before opening a contribution.

## License and provenance

This project is dual-licensed to keep it open while protecting authorship and attribution: the ontology content under **CC BY-SA 4.0**, and the code (schema, validator, scripts) under **Apache-2.0**. See [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE). To cite this work, see [`CITATION.cff`](./CITATION.cff).

## Authorship

Created and maintained by **&lt;AUTHOR NAME&gt;**. This project began as the work of a single author and remains under that author's stewardship; attribution is required for any reuse or derivative.

---

*BPO is foundational infrastructure: closer to a standard than a product. Its value compounds with adoption — the more teams, auditors, and tools reference the same map, the more valuable the map becomes.*
