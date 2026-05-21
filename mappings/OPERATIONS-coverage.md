# Operations ↔ Properties Coverage Report

Consolidated view of the abstract-operations catalogue in [`operations.catalogue.json`](./operations.catalogue.json) and how its 22 operations connect to the BPO property corpus. The link is one-directional: each operation lists the BPO properties whose formalizations govern it (the property records themselves carry no operation references). Closure (every `BPO:` id in an operation's `governs_properties` resolves to a real property record) is enforced by [`schema/validate_refs.py`](../schema/validate_refs.py).

## Summary

| | Count |
|---|---:|
| Operations in catalogue                                       | 22 |
| Candidates pending grounding (held out of the catalogue)      |  6 |
| `governs_properties` link entries (operation → property)      | 35 |
| `iso20022_intents` link entries (operation → message)         | 12 |
| Operations with at least one primary (full) governor          | 19 |
| Operations covered only partially (no primary governor)       |  3 |
| Operations fully ungoverned                                   |  0 |

The 3 partial-only operations (`OP:TRANSFER`, `OP:BURN`, `OP:DEPOSIT`) are honest signal of where the property catalogue is thin — each is governed only via BPO:0101's sanctioned-flow conservation clause, with no dedicated primary governor. A symmetric `no-unauthorized-burn` property (mirroring BPO:0001's no-unauthorized-mint) is the obvious candidate; surfaced not papered over.

## Per-operation coverage

| Operation | Primary governors (full) | Partial governors | ISO 20022 intents |
|---|---|---|---|
| OP:TRANSFER         | — | BPO:0020 (atomicity), BPO:0101 (Internal conservation) | sese.023, sese.024, sese.025 |
| OP:MINT             | BPO:0001 | BPO:0101 (sanctioned flow `m`) | setr.044 |
| OP:BURN             | — | BPO:0101 (sanctioned flow `b`) | setr.054 |
| OP:DEPOSIT          | — | BPO:0101 (sanctioned flow `d`) | setr.044 |
| OP:WITHDRAW         | BPO:0002 | BPO:0050, BPO:0082, BPO:0101 | setr.054 |
| OP:GRANT            | BPO:0040 | — | — |
| OP:REVOKE           | BPO:0040 | — | — |
| OP:PAUSE            | BPO:0050, BPO:0051 | — | — |
| OP:UNPAUSE          | BPO:0050, BPO:0051 | — | — |
| OP:ENCUMBER         | BPO:0093 | — | semt.013 |
| OP:RELEASE          | BPO:0093 | BPO:0091 (compensation cancel-disposition) | semt.013 |
| OP:SETTLE           | BPO:0090 | — | sese.023, sese.024, sese.025 |
| OP:COMPENSATE       | BPO:0091 | — | — |
| OP:FINALIZE-BLOCK   | BPO:0080 | BPO:0090 (settlement reparents finality) | — |
| OP:INCLUDE-TX       | BPO:0080, BPO:0081 | — | — |
| OP:EXECUTE-TX       | BPO:0020, BPO:0092 | BPO:0040 (privileged executions) | — |
| OP:APPROVE          | BPO:0041 | — | — |
| OP:BRIDGE-LOCK      | BPO:0102 | — | — |
| OP:BRIDGE-MINT      | BPO:0102 | — | — |
| OP:BRIDGE-BURN      | BPO:0102 | — | — |
| OP:BRIDGE-RELEASE   | BPO:0102 | — | — |
| OP:UPGRADE          | BPO:0030 | BPO:0040 (privileged) | — |

## Per-property inverse view: operations a property governs

| Property | Operations governed (full) | Operations governed (partial) |
|---|---|---|
| BPO:0001 | OP:MINT | — |
| BPO:0002 | OP:WITHDRAW | — |
| BPO:0020 | OP:EXECUTE-TX | OP:TRANSFER |
| BPO:0030 | OP:UPGRADE | — |
| BPO:0040 | OP:GRANT, OP:REVOKE | OP:EXECUTE-TX, OP:UPGRADE |
| BPO:0041 | OP:APPROVE | — |
| BPO:0050 | OP:PAUSE, OP:UNPAUSE | OP:WITHDRAW |
| BPO:0051 | OP:PAUSE, OP:UNPAUSE | — |
| BPO:0080 | OP:FINALIZE-BLOCK, OP:INCLUDE-TX | — |
| BPO:0081 | OP:INCLUDE-TX | — |
| BPO:0082 | — | OP:WITHDRAW |
| BPO:0090 | OP:SETTLE | OP:FINALIZE-BLOCK |
| BPO:0091 | OP:COMPENSATE | OP:RELEASE |
| BPO:0092 | OP:EXECUTE-TX | — |
| BPO:0093 | OP:ENCUMBER, OP:RELEASE | — |
| BPO:0101 | — | OP:TRANSFER, OP:MINT, OP:BURN, OP:DEPOSIT, OP:WITHDRAW |
| BPO:0102 | OP:BRIDGE-LOCK, OP:BRIDGE-MINT, OP:BRIDGE-BURN, OP:BRIDGE-RELEASE | — |
| BPO:0003, 0060, 0070, 0072, 0073, 0074, 0075 | — | — |

The seven properties with no operation links are pure-cryptographic / structural / hyperproperty / assumption-node properties (ZK, compilation, knowledge soundness, public auditability, circuit IFC, crypto hardness, data-confidentiality hyperproperty). Their formalizations quantify over proofs, executions-as-traces, or environmental conditions — not over named operations.

## Candidates pending grounding (held out of `operations[]`)

These six candidates were considered but did not meet the inclusion bar: clause (a) (distinct kind of state change) or clause (b) (at least one property's formalization treats it distinctly). Listed for transparency and as a roadmap.

| Candidate | Why held out |
|---|---|
| `OP:PROPOSE-BLOCK`  | BPO:0080 mentions block production only in `observability`; its formalization quantifies over outcomes (`ℓ` growing, submitted→finalized for txs), not a named `propose` transition. Promotes only if a future property's formalization names this as a distinct state change. Demoted from `operations[]` in Step 3 review. |
| `OP:EMIT-EVENT`     | BPO:0072 (public auditability) makes events load-bearing via the `Consequential ⊆ Op` set, but emission is a side effect of other operations, not a primary state change. |
| `OP:VERIFY-PROOF`   | The on-chain verifier call is a kind of OP:EXECUTE-TX; BPO:0070 is about proof-system soundness, not an op called VERIFY. |
| `OP:PROVE`          | Off-chain witness generation; not a state change in the modelled system. |
| `OP:FORK / OP:REORG` | No current property quantifies over a fork/reorg as a distinct state change. |
| `OP:SLASH`          | BPO:0080 mentions Byzantine bounds but does not model slashing as a transition. |

## Where the catalogue is thin (signal, not failure)

- **Burn / deposit have no primary governor.** Only BPO:0101's sanctioned-flow conservation reaches them. Candidates for symmetric properties: `no-unauthorized-burn` (mirroring BPO:0001) and a deposit-correctness property.
- **Transfer has no primary governor.** Atomicity (BPO:0020) and conservation (BPO:0101) reach it, but no single property is principally about transfer correctness. A dedicated transfer-correctness property is a future option.
- **No property governs `OP:PROPOSE-BLOCK`.** Held in `candidates_pending_grounding[]` per the inclusion bar.

## Validator state (cross-framework counts)

```
Operations catalogue:                                22 operations
Operations → ISO 20022 (iso20022_intents):           12 entries  (closure OK)
Operations → properties (governs_properties):        35 entries  (closure OK)
```
