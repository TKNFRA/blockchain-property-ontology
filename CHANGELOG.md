# Changelog

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
