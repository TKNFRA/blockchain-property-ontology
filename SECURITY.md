# Security & Responsible Use

BPO is a **catalogue of properties and their failure modes**, not deployed software. It does not custody funds or execute on-chain. Still, a few things are worth stating clearly.

## What this project is (and isn't)

- BPO describes what blockchain systems *should* satisfy and how those guarantees can fail and be verified. It is reference material.
- An entry's presence does **not** certify that any particular deployed system satisfies that property. Verification is a separate act, performed against a specific system with specific assumptions.
- The `verification` strategies in an entry state honestly what each method can establish. Do not read "this can be model-checked" as "this is proven."

## Reporting an issue with the catalogue

If you find an entry that is **wrong in a way that could mislead someone into a false sense of assurance** — a misclassification (e.g. a hyperproperty presented as single-trace verifiable), a hidden assumption, an overstated verification claim, or an incorrect/unverifiable incident reference — please report it.

- For ordinary corrections, open a public issue.
- For anything you believe is sensitive (for example, an entry whose error could be weaponized against live systems before it is fixed), contact the maintainer privately at **&lt;SECURITY CONTACT&gt;** rather than opening a public issue.

We aim to acknowledge reports promptly and to correct misleading entries with priority, since the project's value rests entirely on not overstating assurance.
