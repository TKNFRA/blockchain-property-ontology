# IOF ↔ BPO Coverage Report

This report cross-walks the **Interoperability Framework for Digital Asset Securities (IOF)** — DTCC, Clearstream, Euroclear, in collaboration with BCG, February 2026 — to the **Blockchain Property Ontology (BPO)** catalogue. It is the consolidated view of `identifiers.external_refs.iof` arrays in the property records and the framework catalogue under [`iof.framework.json`](./iof.framework.json).

## Summary

The IOF organizes interoperability into **5 foundations and 29 building blocks** spanning legal, data, process, role, and infrastructure concerns. BPO catalogues *behavioural properties* — the things a smart-contract or ledger system can be proven to do across all executions — and so cross-walks only the building blocks whose content is behavioural. **9 of the 29 building blocks are behavioural; 20 are deliberately out-of-scope.** The framework's own principle — *same asset, same rights, same outcome* across infrastructures — is realized at the layer BPO occupies (provable behaviour) by these 9 cross-walks; the legal, data-standardization, governance, and SLA layers that surround them sit beside BPO rather than inside it, exactly as the FMIs' own framing organizes them.

That distribution — 9 behavioural, 20 not — is **the right shape for an interoperability framework**, not a coverage gap. A cross-walk that linked every IOF block to *some* BPO property would be the category error this catalogue exists to prevent: blocks that describe what an organization *does* (publish a standard, hold a licence, agree on a taxonomy, run a service level) are not blocks a formal property can mechanically discharge, and pretending otherwise manufactures false assurance.

|                                                                | Count                    |
| -------------------------------------------------------------- | -----------------------: |
| IOF foundations                                                | 5                        |
| IOF building blocks                                            | 29                       |
| Building blocks scoped `behavioural`                           | **9**                    |
| Building blocks scoped `out-of-scope` (by design)              | **20**                   |
| Properties with IOF cross-walks (`external_refs.iof`)          | 12                       |
| Total IOF cross-walk entries from property records             | 15                       |
| Cross-walks with `relation: supports`                          | 5                        |
| Cross-walks with `relation: partially-supports`                | 10                       |
| Cross-walks with `relation: establishes`                       | 0 (relation enum forbids it) |

The relation enum on IOF cross-walks deliberately excludes `establishes`. Every IOF building block bundles policy, data, infrastructure, and behavioural concerns whose multi-facet character means a single BPO property can at most materially support a block, never wholly discharge it. Every link is therefore `supports` or `partially-supports`, with its `note` field stating both **what the property covers** (the behavioural slice) and **what stays out-of-scope** (the surrounding policy / data / infrastructure dimension). The validator ([`schema/validate_refs.py`](../schema/validate_refs.py)) enforces this as **bidirectional scope-link consistency**: out-of-scope blocks must carry zero cross-walk links, and behavioural blocks must carry at least one. Neither half can drift out of sync with the actual links.

## What IS covered — the 9 behavioural building blocks

| IOF building block | Foundation | BPO link(s) | Residual (stays out-of-scope) |
|---|---|---|---|
| BB-contract-versioning-management | F1 Assets & liabilities | BPO:0030 `partially-supports` | Cross-chain version negotiation and harmonised version-record schema. |
| BB-on-chain-off-chain-protocols | F3 Asset lifecycle & movement | BPO:0091 `partially-supports` | Off-chain callbacks, SLA timing, idempotency conventions, data-level harmonisation of error semantics. |
| BB-cross-dlt-protocols | F3 Asset lifecycle & movement | BPO:0102 `supports`; BPO:0092 `partially-supports` | Wrapped-token lineage and entitlement-traceability metadata; protocol-upgrade / fork-survival governance; bridge-relay soundness assumption. |
| BB-asset-location-controls | F3 Asset lifecycle & movement | BPO:0102 `supports` | The authoritative-source-of-truth metadata layer and the common ruleset specifying which ledger holds authority. |
| BB-consensus-and-finality | F4 Ledgers | BPO:0090 `supports`; BPO:0080 `partially-supports` | Harmonised finality definitions and adapters between heterogeneous consensus mechanisms; cross-chain finality-recognition rules. |
| BB-smart-contracts-and-tokens-structure | F4 Ledgers | BPO:0030 `partially-supports`; BPO:0050 `partially-supports` | Chain-agnostic interface definitions, verifiable contract provenance, audited-code attestation, governed-upgrade ceremony. |
| BB-data-privacy | F4 Ledgers | BPO:0075 `supports`; BPO:0073 `partially-supports`; BPO:0003 `partially-supports` | Encryption in flight and at rest, key rotation, per-jurisdiction retention/deletion controls. |
| BB-roles-in-data-access | F4 Ledgers | BPO:0040 `supports`; BPO:0041 `partially-supports` | Dynamic ABAC constraints (jurisdiction, instrument class, time windows, amount thresholds); audit-log infrastructure. |
| BB-enforceability-of-transfers-and-finality-in-settlement | F5 Legal & regulatory compliance | BPO:0090 `partially-supports` | Statutes recognising electronic signatures, smart contracts, and ledger records as legally binding; settlement-finality rules under counterparty insolvency. |

The single `supports`-grade link on each of BB-cross-dlt-protocols, BB-asset-location-controls, BB-consensus-and-finality, BB-data-privacy, and BB-roles-in-data-access marks the block whose behavioural core the named BPO property *is* — not "discharges in full", but "materially carries". `partially-supports` is used everywhere else because the BPO property covers a facet of the block (replay-resistance within cross-DLT protocols; liveness within consensus-and-finality; selective disclosure within data-privacy; k-of-n threshold within roles-in-data-access; bounded pause within token-structure; storage-layout discipline within versioning and token-structure) rather than the block as a whole.

## Per-property inverse view

| Property | IOF building blocks linked |
|---|---|
| BPO:0003 zero-knowledge-witness-privacy           | BB-data-privacy (partial) |
| BPO:0030 storage-layout-isolation                 | BB-contract-versioning-management (partial); BB-smart-contracts-and-tokens-structure (partial) |
| BPO:0040 access-control-correctness               | BB-roles-in-data-access |
| BPO:0041 multiparty-transaction-validation        | BB-roles-in-data-access (partial) |
| BPO:0050 emergency-pause-safety-bounded           | BB-smart-contracts-and-tokens-structure (partial) |
| BPO:0073 circuit-public-signal-non-leakage        | BB-data-privacy (partial) |
| BPO:0075 private-data-confidentiality-hyperproperty | BB-data-privacy |
| BPO:0080 consensus-liveness                       | BB-consensus-and-finality (partial) |
| BPO:0090 settlement-finality-irrevocability       | BB-consensus-and-finality; BB-enforceability-of-transfers-and-finality-in-settlement (partial) |
| BPO:0091 fail-to-settle-reversal                  | BB-on-chain-off-chain-protocols (partial) |
| BPO:0092 transaction-sequencing-and-replay-resistance | BB-cross-dlt-protocols (partial) |
| BPO:0102 cross-ledger-inventory-consistency       | BB-cross-dlt-protocols; BB-asset-location-controls |

Twelve properties carry IOF links; twelve property records of the 24-record corpus have *no* IOF link, and that is the correct outcome — they describe behavioural properties (reentrancy, compiler arithmetic, knowledge soundness, public auditability, no-unauthorized-mint, eventual withdrawal, censorship resistance, L2 escape hatch, cryptographic-hardness assumption-node, conservation of value, encumbrance-pre-settlement, scoped-pause-safety) whose subject matter no IOF *behavioural* building block describes. They do not need IOF links to be coherent and adding stretched ones would be exactly the dilution this catalogue refuses to permit.

## What is deliberately *not* covered

This is the bulk of the IOF, and it is the correct bulk for an interoperability framework: the parts that move between infrastructures cleanly are mostly *agreements* (legal, taxonomic, role-based, operational) rather than *behaviours*. BPO catalogues behaviours. Every one of the 20 building blocks below is genuine and important — but it is the surrounding policy / data / role / infrastructure layer of any assurance argument that *uses* BPO, not BPO itself. The validator's bidirectional scope-link consistency check guarantees that the cross-walk layer cannot quietly drift into these blocks.

### Legal & regulatory (7) — *the legal scaffolding around interoperability*

| IOF building block | Foundation | Out-of-scope because… |
|---|---|---|
| BB-level-of-ownership-and-associated-rights | F1 | Harmonised definitions of legal ownership, contractual claim to restitution, and collateral-taker security interest are legal-taxonomy work, not behavioural property. |
| BB-ultimate-beneficial-owner-traceability | F2 | AML/travel-rule attestation models and beneficial-ownership query protocols are a regulatory and data-residency obligation, not a behavioural property of the ledger. |
| BB-assets-taxonomy-and-classification | F5 | Mapping assets to regulatory categories (security / commodity / payment token) across jurisdictions is legal taxonomy. |
| BB-custody-and-settlement-rules | F5 | Client-asset protection rules and the legal recognition of delivery-versus-payment are regulatory framework, not on-chain behaviour. |
| BB-aml-cft-sanctions | F5 | AML/CFT controls, sanctions screening, travel-rule data exchange, transaction monitoring are regulatory compliance processes. |
| BB-jurisdiction-in-dispute-resolution | F5 | Governing law, forum selection, and authority enforcement for cross-border disputes are legal arrangements. |
| BB-licensing-regime-of-market-institutions | F5 | Licensing and oversight frameworks for issuers, exchanges, brokers, custodians, bridge operators, oracles are regulatory authorisation. |

### Data harmonization (7) — *shared schemas and standard reference structures*

| IOF building block | Foundation | Out-of-scope because… |
|---|---|---|
| BB-security-and-contract-identification | F1 | Identifier conventions (ISIN, UTI, RWA↔digital-twin linkage) are standards harmonisation, not behavioural. |
| BB-terms-and-conditions | F1 | Shared schemas for economic terms, governing law, external-document references are data harmonisation. |
| BB-functions-and-corporate-actions | F1 | Common event types and calculation conventions for lifecycle events (issue, redeem, coupon, dividend) are data harmonisation; the *correctness* of any one action stays inside the BPO property layer. |
| BB-on-chain-data-portability | F1 | A portable on-chain asset-record schema readable across ledgers is data-format harmonisation. |
| BB-identity-recognition | F2 | LEI/BIC↔DID/VC mappings, supported signature suites, reusable onboarding decisions are credential-schema harmonisation. |
| BB-accounts-wallets-capabilities-harmonization | F2 | Harmonised on-chain account models mirroring traditional account types are schema harmonisation. |
| BB-message-purpose | F3 | ISO-20022-style standardisation of message types, attributes, and outcomes is exactly what the BPO ↔ ISO 20022 binding layer realizes; cross-walking it again at the IOF layer would double-count. |

### Roles & governance (4) — *who does what, with what authority*

| IOF building block | Foundation | Out-of-scope because… |
|---|---|---|
| BB-roles-in-contract-security-lifecycle | F1 | Common naming and permissions for issuer, guarantor, paying agent, registrar, transfer agent, CSD, regulator, tokenizer is a role taxonomy. |
| BB-role-responsibilities-in-accounts-wallets-management | F2 | Harmonised transaction-authorisation rules, RBAC administration with admin/operations separation, and audit-log requirements are governance design, not on-chain property — although BPO:0040 access-control correctness *does* discharge any specific instance. |
| BB-intermediary-responsibilities-and-obligations | F3 | Clear roles, SLAs, and liability for oracle providers, bridge relays, custodians, clearing houses, technology vendors are governance and contractual obligations. |
| BB-segregation-of-duties | F4 | The behavioural content (L1/L2 architectural separation with canonical proofs across layers) is already covered through BPO:0090 / BPO:0080 via BB-consensus-and-finality. Re-linking here would dual-link to the same property without adding coverage; the remaining content of the block is role / governance design. |

### Operational & SLA (2) — *service-level and infrastructure concerns*

| IOF building block | Foundation | Out-of-scope because… |
|---|---|---|
| BB-time-management | F3 | The primary content (synchronised cross-ledger clocks, trusted time oracles, central timekeeping services, coordinated snapshots) is governance and infrastructure. The one behavioural facet (no double-counting of an in-transit asset across chains) partially aligns with BPO:0102's joint-state invariant but would need a dedicated *temporal cross-ledger consistency* property to bind cleanly — a future BPO candidate, not a stretched current link. |
| BB-minimum-service-levels | F4 | Operational SLAs — high availability, predictable processing, throughput, recovery objectives aligned with CPMI-IOSCO — are infrastructure-quality targets, not behavioural properties. |

**Recap.** Legal & regulatory: 7. Data harmonization: 7. Roles & governance: 4. Operational & SLA: 2. Total deliberately not covered: **20** — the exact count the validator enforces against.

## Honest framing

The IOF is, by construction, dominated by non-behavioural concerns. An interoperability framework's job is to harmonize legal recognition, identifier schemas, role taxonomies, message conventions, time references, service levels, and licensing regimes — *agreements among institutions* — so that disparate infrastructures can carry the same asset with the same rights to the same outcome. Those agreements are loaded into the upper layers of the framework; the lower behavioural layer (does the ledger actually do what the agreement assumes it does?) is the BPO layer. Cross-walking the behavioural layer densely (9 blocks, 15 links, 12 properties) and cross-walking the agreement layer not at all (20 blocks, 0 links) is what *honest* coverage of an interoperability framework looks like.

When the BPO catalogue is referenced by an FMI's interoperability programme, the right reading of this report is: *BPO covers the behavioural layer of the IOF — the 9 building blocks an interoperable ledger can be proven to satisfy — and sits underneath the legal, data-standardization, governance, and SLA layers without competing with them.* That positioning realizes the FMIs' own "same asset, same rights, same outcome" principle at the level of provable behaviour while leaving every other layer of the framework intact.

## Validator state

```
IOF framework:        34 ids (5 foundations + 29 building blocks; behavioural=9, out-of-scope=20)
IOF cross-walk entries from properties:          15   (closure OK)
IOF scope-link consistency: all 9 behavioural blocks carry ≥ 1 cross-walk link;
                            all 20 out-of-scope blocks carry zero               (OK)
```
