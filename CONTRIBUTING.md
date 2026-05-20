# Contributing to BPO

Thank you for considering a contribution. This project's entire credibility rests on **rigor**, so contributions are held to an explicit standard and reviewed before they are accepted. Please read this guide in full before opening one.

This document covers what you can contribute, the quality bar every entry must meet, how entries move from draft to accepted, and the provenance terms that protect both you and the project.

---

## What you can contribute

- **New properties** — well-formed entries for properties not yet in the catalogue.
- **Verification strategies** — additional or improved ways to establish an existing property, with an honest statement of what each one actually proves.
- **Attack patterns** — failure modes that exploit the absence of a property, ideally tied to a real, verifiable incident.
- **Corrections** — fixes to formalizations, classifications, relationships, or references.

If you are unsure whether something fits, open an issue describing it before writing the entry.

## The quality bar

Every entry must meet all of the following before it can be accepted. These are not stylistic preferences; they are what keeps the catalogue trustworthy.

1. **Honest classification.** A property's modal class must be correct: safety, liveness, or a hyperproperty. This is load-bearing because it determines which verification methods are even admissible. In particular, a hyperproperty (e.g. zero-knowledge, non-interference, ordering fairness) **must not** be presented as something a single-trace tool can verify.

2. **Explicit assumptions.** Every guarantee must enumerate the assumptions it depends on. Each assumption is either *discharged* by another property (cite its identifier) or *accepted* — in which case it must be marked as accepted with a short justification, never left implicit. An entry that hides its assumptions will be sent back.

3. **Decidability honesty.** State what is *mechanically* achievable, and by what kind of tool. Do not claim a proof where only evidence (testing, bounded checking, heuristics) is available. Do not promise that fuzzing establishes liveness, or that an SMT solver settles a cryptographic reduction.

4. **Grounded incidents.** When an attack pattern references a real-world incident, the reference must be verifiable. Unverified or anecdotal incidents must be explicitly marked as unverified and may not be used to justify a non-draft status.

5. **Passes the validator.** Every contribution must pass `schema/validate_refs.py` with no schema errors and no dangling references. A contribution that does not validate cannot be reviewed.

6. **Stable identifiers.** Never reuse a retired identifier, and never repurpose an existing one. Identifiers are permanent and meaningless by design.

## Review lifecycle

Entries carry a `status` field and move through a deliberate lifecycle. Nothing arrives authoritative.

- **`draft`** — submitted, validates structurally, not yet reviewed. May contain unverified incident references (clearly marked).
- **`reviewed`** — checked by a maintainer for correctness of classification, formalization, assumptions, and references. All incident references must be verified at this stage.
- **`stable`** — settled, widely referenced, changed only with strong justification and never in a way that breaks the meaning other systems rely on.

A maintainer reviews each contribution against the quality bar above. Expect questions, especially on classification and assumptions — these are where rigor is won or lost.

## Provenance and inbound contribution terms

By submitting a contribution, you agree that:

1. You have the right to submit it, and it is your original work (or you have the right to contribute it).
2. Your contribution to the **ontology content** is licensed under **CC BY-SA 4.0**, and your contribution to **code** is licensed under **Apache-2.0**, consistent with the repository's [`LICENSE`](./LICENSE).
3. You additionally grant the project maintainer a perpetual, irrevocable, non-exclusive right to relicense your contribution — including as part of a larger combined work — under other terms. This lets the project, as a whole, be offered under alternative or commercial terms in the future without having to track down every contributor, while keeping the public catalogue open under the licenses above.

This grant governs only contributions made after it is in place; it is not retroactive. Attribution to contributors is preserved regardless of relicensing.

> **Note:** this is a common, deliberately lightweight structure (no signing bot, no separate CLA document), but it is a legal arrangement and not legal advice. If you are contributing on behalf of an employer, make sure you are authorized to grant these terms.

## Mechanics

- One property per file, under `properties/`, named `BPO-NNNN-slug.json`.
- Run `python3 schema/validate_refs.py` locally and make sure it reports `PASS` before opening a pull request.
- Keep formal notation consistent with existing entries; Unicode logical symbols are fine and parse correctly.
- In your pull request, state plainly what the entry claims, what it assumes, and what can honestly be verified about it.
