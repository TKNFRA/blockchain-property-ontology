# Operations ↔ Properties Coverage Report

Consolidated view of the abstract-operations catalogue in [`operations.catalogue.json`](./operations.catalogue.json) and how its 32 operations connect to the BPO property corpus. The link is one-directional: each operation lists the BPO properties whose formalizations govern it (the property records themselves carry no operation references). Closure (every `BPO:` id in an operation's `governs_properties` resolves to a real property record) is enforced by [`schema/validate_refs.py`](../schema/validate_refs.py).

## Summary

| | Count |
|---|---:|
| Operations in catalogue                                       | 32 |
| Candidates pending grounding (held out of the catalogue)      |  7 |
| `governs_properties` link entries (operation → property)      | 70 |
| — of which primary (full) governors                           | 38 |
| — of which partial governors (`{property, note}` form)        | 32 |
| `iso20022_intents` link entries (operation → message)         | 12 |
| Operations with at least one primary (full) governor          | 29 |
| Operations covered only partially (no primary governor)       |  3 |
| Operations fully ungoverned                                   |  0 |

The 3 partial-only operations (`OP:TRANSFER`, `OP:BURN`, `OP:DEPOSIT`) are honest signal of where the property catalogue is thin — each is governed only via BPO:0101's sanctioned-flow conservation clause, with no dedicated primary governor. A symmetric `no-unauthorized-burn` property (mirroring BPO:0001's no-unauthorized-mint) is the obvious candidate; surfaced not papered over.

The candidate count previously read 6 in this table and "these six candidates" in the prose while `operations.catalogue.json` carried 7 entries — the table merged `OP:FORK` and `OP:REORG` into one row. Corrected to 7 here; the row is still merged, which is why the discrepancy went unnoticed. Nothing enforces this count, so it is worth re-deriving from the JSON on each edit.

### Size guidance raised from 30 to 40

The lending layer added 10 operations, taking the catalogue from 22 to 32. Under the previous guidance of 30, two candidates that clear the inclusion bar on their merits — `OP:FLASH-LOAN` and `OP:CREATE-LENDING-MARKET` — would have been excluded for arithmetic reasons alone. That is the wrong reason to exclude an operation, so the guidance moved rather than the operations. The bar's *test* is unchanged, and `size_guidance` now lives in the catalogue JSON alongside `inclusion_bar` so the number and its rationale travel together. It remains a smell threshold prompting review, not a quota enforced by code.

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

### Lending layer (added with `BPO:0021`, `BPO:0110`–`BPO:0118`, `BPO:0120`–`BPO:0122`)

| Operation | Primary governors (full) | Partial governors | ISO 20022 intents |
|---|---|---|---|
| OP:SUPPLY-LIQUIDITY      | BPO:0110 | BPO:0111 (issuance quotation), BPO:0120 (observed delta) | — |
| OP:WITHDRAW-LIQUIDITY    | BPO:0110, BPO:0117 | BPO:0111, BPO:0002 (liveness, strictly stronger than 0117) | — |
| OP:POST-COLLATERAL       | BPO:0110 | BPO:0113 (changes the capacity term), BPO:0120 | — |
| OP:WITHDRAW-COLLATERAL   | BPO:0113, BPO:0117 | BPO:0040 (delegated risk increase) | — |
| OP:BORROW                | BPO:0110, BPO:0113 | BPO:0111, BPO:0040 | — |
| OP:REPAY                 | BPO:0110, BPO:0117 | BPO:0111 (full-liability exactness) | — |
| OP:ACCRUE-INTEREST       | BPO:0112 | BPO:0110, BPO:0122 (rate call), BPO:0101 (issuance term) | — |
| OP:LIQUIDATE             | BPO:0114, BPO:0115 | BPO:0113 (boundary agreement), BPO:0110, BPO:0121 | — |
| OP:FLASH-LOAN            | BPO:0116 | BPO:0021, BPO:0020, BPO:0110 | — |
| OP:CREATE-LENDING-MARKET | BPO:0118 | BPO:0040 (where creation is permissioned) | — |

No ISO 20022 intents are claimed for the lending layer. The reference subset in [`iso20022.framework.json`](./iso20022.framework.json) covers securities settlement and transfer messaging; collateralized lending has no counterpart there, and inventing one would be a worse outcome than an empty column.

`OP:LIQUIDATE` carries `BPO:0115` as a primary governor, but that record is *conditional*: it imposes no obligation on a protocol exposing a single liquidation input mode. The link records that the record governs the operation where it applies, not that every design must satisfy it.

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
| BPO:0021 | — | OP:FLASH-LOAN |
| BPO:0110 | OP:BORROW, OP:POST-COLLATERAL, OP:REPAY, OP:SUPPLY-LIQUIDITY, OP:WITHDRAW-LIQUIDITY | OP:ACCRUE-INTEREST, OP:FLASH-LOAN, OP:LIQUIDATE |
| BPO:0111 | — | OP:BORROW, OP:REPAY, OP:SUPPLY-LIQUIDITY, OP:WITHDRAW-LIQUIDITY |
| BPO:0112 | OP:ACCRUE-INTEREST | — |
| BPO:0113 | OP:BORROW, OP:WITHDRAW-COLLATERAL | OP:LIQUIDATE, OP:POST-COLLATERAL |
| BPO:0114 | OP:LIQUIDATE | — |
| BPO:0115 | OP:LIQUIDATE | — |
| BPO:0116 | OP:FLASH-LOAN | — |
| BPO:0117 | OP:REPAY, OP:WITHDRAW-COLLATERAL, OP:WITHDRAW-LIQUIDITY | — |
| BPO:0118 | OP:CREATE-LENDING-MARKET | — |
| BPO:0120 | — | OP:POST-COLLATERAL, OP:SUPPLY-LIQUIDITY |
| BPO:0121 | — | OP:LIQUIDATE |
| BPO:0122 | — | OP:ACCRUE-INTEREST |
| BPO:0003, 0060, 0070, 0072, 0073, 0074, 0075 | — | — |

The seven properties with no operation links are pure-cryptographic / structural / hyperproperty / assumption-node properties (ZK, compilation, knowledge soundness, public auditability, circuit IFC, crypto hardness, data-confidentiality hyperproperty). Their formalizations quantify over proofs, executions-as-traces, or environmental conditions — not over named operations.

Three lending records (`BPO:0111`, `BPO:0120`, `BPO:0121`, `BPO:0122`) appear only as partial governors, and this is the right shape rather than thin coverage. `BPO:0111` is a constraint on the *conversions inside* other operations, not on an operation of its own — no catalogue entry is principally "convert". The three dependency contracts are assumption nodes describing external modules; an operation of the consuming system can only ever consume them partially, and a primary link would misrepresent an assumption as something the system's own transitions establish.

`BPO:0021` likewise appears only as a partial governor of `OP:FLASH-LOAN`. It is a platform-level guarantee that every operation depends on and none is principally about, which is why it sits in the execution decade beside `BPO:0020` rather than in the lending block.

## Candidates pending grounding (held out of `operations[]`)

These seven candidates (shown in six rows — `OP:FORK` and `OP:REORG` share one) were considered but did not meet the inclusion bar: clause (a) (distinct kind of state change) or clause (b) (at least one property's formalization treats it distinctly). Listed for transparency and as a roadmap.

The lending layer promoted nothing from this list — all ten of its operations are new. `OP:FLASH-LOAN` and `OP:CREATE-LENDING-MARKET` were never held here; they became admissible the moment `BPO:0116` and `BPO:0118` gave them a distinct guard and effect.

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
- **The lending layer claims no ISO 20022 intents.** The reference subset has no collateralized-lending counterpart, and 10 of 32 operations now carry an empty intents column. Extending the ISO 20022 subset — or concluding that lending has no natural message intent there — is open work.
- **Eight operations remain without a primary governor for their *own* correctness**, in the sense that the record governing them is about a broader invariant. This is most visible in the lending block, where `OP:SUPPLY-LIQUIDITY` and `OP:POST-COLLATERAL` are governed primarily by `BPO:0110`'s ledger fold rather than by any record principally about supplying or posting.

## Validator state (cross-framework counts)

```
Operations catalogue:                                32 operations
Operations → ISO 20022 (iso20022_intents):           12 entries  (closure OK)
Operations → properties (governs_properties):        70 entries  (closure OK)
```
