# ISO 20022 ↔ BPO Coverage Report

Consolidated view of the ISO 20022 reference subset in [`iso20022.framework.json`](./iso20022.framework.json) and how it connects to the BPO property corpus at two depths. The framework file mirrors only the 18 ISO 20022 ids (messages, components, elements) that the corpus or the operations catalogue actually points at; ISO 20022 publishes identifiers and structure free-of-use via [iso20022.org](https://www.iso20022.org/) so the references are unrestricted, and descriptions in the framework are paraphrased in our own words.

## Summary

| | Count |
|---|---:|
| ISO 20022 ids in framework (messages + components + elements) | 18 (7 + 5 + 6) |
| Properties with depth-1 cross-walks (`external_refs.iso20022`) | 11 |
| Total depth-1 cross-walk entries                              | 16 |
| Properties with depth-2 bindings (`formalization.bindings`)   |  8 |
| Total depth-2 binding entries                                 | 19 |
| Properties with declared `formalization.symbols` (Tier 1 lookup) |  8 |
| Operations with `iso20022_intents` (catalogue-side links)     |  8 |

Depth-2 closure runs *both* on the element side (the bound `element` must resolve in the framework) *and* on the symbol side (the bound `symbol` must appear in the property's `formalization.symbols` if declared, otherwise as a whole-token regex match against `formalization.signature`, case-sensitive). A binding that silently mis-resolves would be worse than no binding — every binding here passes Tier 1.

## Per-property coverage

| Property | Depth-1 cross-walks (relation) | Depth-2 bindings (symbol → element) |
|---|---|---|
| BPO:0001 | `setr.044` (constrains) | `Addr → cmp/PartyIdentification`<br>`hasRole_MINTER → elem/PartyRole` (partial — role-membership) |
| BPO:0002 | `setr.054` (relates-to) | — |
| BPO:0040 | — | `Principals → cmp/PartyIdentification`<br>`Authorities → elem/PartyRole` |
| BPO:0041 | `sese.023` (constrains) | `Validators → cmp/PartyIdentification` (identity aspect)<br>`Validators → elem/PartyRole` (role aspect) |
| BPO:0050 | `sese.023` (constrains) | — |
| BPO:0051 | `semt.013` (constrains) | — |
| BPO:0090 | `sese.023` (constrains)<br>`sese.024` (constrains)<br>`sese.025` (constrains) | `SettlementID → elem/SettlementTransactionIdentification`<br>`accountedOutcome → elem/SettlementAmount` (partial — monetary face)<br>`final → cmp/TransactionStatus` (selects SETTLED value) |
| BPO:0091 | `sese.024` (relates-to) | `parties → cmp/PartyIdentification`<br>`deadline → elem/SettlementDate` (partial — date granularity)<br>`status → cmp/TransactionStatus` |
| BPO:0092 | `elem/SettlementTransactionIdentification` (relates-to) | — |
| BPO:0093 | `semt.013` (constrains)<br>`cmp/SecuritiesAccount` (relates-to)<br>`cmp/FinancialInstrument` (relates-to) | `total → cmp/SecuritiesAccount` (partial — aggregate position)<br>`Holder → cmp/PartyIdentification` (account-owner role)<br>`Asset → cmp/FinancialInstrument`<br>`Obligation → elem/SettlementTransactionIdentification`<br>`obligationStatus → cmp/TransactionStatus` |
| BPO:0101 | `sese.023` (constrains)<br>`elem/SettlementAmount` (relates-to) | `V → elem/SettlementAmount` (partial — per-leg projection) |
| BPO:0102 | `cmp/FinancialInstrument` (relates-to) | `Asset → cmp/FinancialInstrument` |

## Properties without ISO 20022 links (12) — by design

| Property | Why no link |
|---|---|
| BPO:0003 zero-knowledge-witness-privacy | Pure cryptographic; no ISO 20022 message-level correspondence. |
| BPO:0020 reentrancy-safety               | Atomicity at call boundaries; no specific ISO 20022 message describes external-call atomicity. |
| BPO:0030 storage-layout-isolation        | Implementation-level invariant; not message-related. |
| BPO:0060 compiler-arithmetic-preservation | Compilation correctness; not message-related. |
| BPO:0070 knowledge-soundness             | Proof-system soundness; not message-related. |
| BPO:0072 public-auditability             | Broader than ISO 20022 messaging; auditability concerns any externally verifiable record. |
| BPO:0073 circuit-public-signal-non-leakage | Pure circuit / hypersafety. |
| BPO:0074 cryptographic-hardness-and-setup-assumptions | Assumption node; environmental, not message-related. |
| BPO:0075 private-data-confidentiality-hyperproperty | Hyperproperty over traces; not a message-level concern. |
| BPO:0080 consensus-liveness              | Consensus-layer property; ISO 20022 operates above consensus. |
| BPO:0081 censorship-resistance           | Same — consensus-layer mechanics. |
| BPO:0082 l2-escape-hatch                 | L2 protocol-specific mechanism; not standardized at the ISO 20022 layer. |

This is honest no-link rather than thematic stretch — adding a token reference for completeness would have been the category error the catalogue exists to prevent.

## Depth-2 worked examples

The fully worked example for **BPO:0090 settlement-finality-irrevocability** is in [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) under "Three-layer model: intent → operation → property" — that is the canonical demonstration of intent → operation → property → binding closing end-to-end. A second worked example follows.

### BPO:0091 fail-to-settle-reversal (end-to-end)

- **ISO 20022 message intents** (top): `sese.024` SecuritiesSettlementTransactionStatusAdvice (the message that surfaces a failed-attempt status that triggers compensation).
- **Operation** (middle): `OP:COMPENSATE` — `BPO:0091`'s `compensate(A)` is the named transition that takes an attempt to `reverted`. The operation has no `iso20022_intents` in the catalogue because the closest message-level analogue (modification / cancellation request) varies by attempt context and was deliberately omitted.
- **Property** (bottom): `BPO:0091` carries `external_refs.iso20022 = [{ sese.024, relates-to }]` — the property does not constrain `sese.024` directly; it constrains the system's *response* after failure surfaces through this message.
- **Depth-2 bindings**:
  - `parties → ISO20022:cmp/PartyIdentification` — per-party balance restoration `v(p, a, s_rev) = v(p, a, s_pre-A)` is per-PartyIdentification across the unwind.
  - `deadline → ISO20022:elem/SettlementDate` (partial) — `deadline d : Timestamp` is the cutoff after which compensation is reachable; SettlementDate is the same intent at date granularity.
  - `status → ISO20022:cmp/TransactionStatus` — `status(A, s) ∈ {pending, finalized, failed, reverted}` carries the same lifecycle ISO 20022's TransactionStatus expresses on the underlying settlement transaction.

End-to-end: a `sese.024` status advice signalling a failed transaction triggers `OP:COMPENSATE`, executed under `BPO:0091`'s correctness-and-bounded-time obligations, with the property's `parties / deadline / status` symbols binding back to the standard's `PartyIdentification / SettlementDate / TransactionStatus`.

### BPO:0093 encumbrance-pre-settlement (end-to-end)

- **ISO 20022 message intent** (top): `semt.013` IntraPositionMovementInstruction — the message that realizes an encumbrance as a beneficial-ownership-preserving hold on positions.
- **Operation** (middle): `OP:ENCUMBER` and `OP:RELEASE` — both governed by `BPO:0093`. Both list `semt.013` in their `iso20022_intents`.
- **Property** (bottom): `BPO:0093` carries `external_refs.iso20022 = [{ semt.013, constrains }, { cmp/SecuritiesAccount, relates-to }, { cmp/FinancialInstrument, relates-to }]`.
- **Depth-2 bindings**:
  - `total → ISO20022:cmp/SecuritiesAccount` (partial — aggregate position in the account; the (free, encumbered) partition is a refinement of positions inside it). *This binding is enabled by the Step 5 reviewable signature edit that surfaced `total` as a declared symbol.*
  - `Holder → ISO20022:cmp/PartyIdentification` (account-owner role).
  - `Asset → ISO20022:cmp/FinancialInstrument`.
  - `Obligation → ISO20022:elem/SettlementTransactionIdentification` — the obligation keys the encumbrance to the underlying settlement.
  - `obligationStatus → ISO20022:cmp/TransactionStatus` — gates RELEASE.

End-to-end: a `semt.013` instruction blocks `SettlementQuantity` of `FinancialInstrument` F in `SecuritiesAccount` of `AccountOwner` P against `SettlementTransactionIdentification` T — exactly `OP:ENCUMBER` under `BPO:0093` with `Holder=P`, `Asset=F`, `Obligation=T`. The property then enforces dispose-from-free-only and release-guarded-by-`obligationStatus`.

## Symbol-in-formalization check — how depth-2 stays honest

Every depth-2 binding has its `symbol` verified two ways simultaneously:

1. **Element-side closure**: the bound `element` must resolve in `iso20022.framework.json` (messages ∪ components ∪ elements). Dangling = FAIL.

2. **Symbol-side check** (tiered):
   - **Tier 1 (structured lookup, preferred)**: if the property has `formalization.symbols`, the bound `symbol` must appear in that list as an exact case-sensitive string equality.
   - **Tier 2 (fallback)**: otherwise, the bound `symbol` must match a whole-token regex against `formalization.signature` only — `(?<![A-Za-z0-9_]) <symbol> (?![A-Za-z0-9_])`, case-sensitive.

All 8 properties currently carrying bindings have `formalization.symbols` declared, so every binding currently uses Tier 1 — the trustworthy path. The Tier 2 fallback exists so new properties can be bound without retroactive symbols-list authoring, but the discipline strongly favours Tier 1.

A binding of `party` against a signature declaring `Principal` is REJECTED, not near-matched. A binding of `final` against `finalityCert` is REJECTED (the `i` after `final` is in the identifier alphabet, so the negative lookahead fires).

## Validator state

```
ISO 20022 framework: 18 ids unique (msg=7, cmp=5, elem=6)
Property → ISO 20022 depth-1 cross-walks: 16   (closure OK)
Property → ISO 20022 depth-2 bindings:    19   (element closure OK, symbol check OK on all)
Operation → ISO 20022 intents:            12   (closure OK)
```
