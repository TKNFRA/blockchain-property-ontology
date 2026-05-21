# DASCP ↔ BPO Coverage Report

This report cross-walks the **Digital Asset Securities Control Principles (DASCP)** — DTCC / Clearstream / Euroclear, May 2024 — to the **Blockchain Property Ontology (BPO)** catalogue, control by control. It is the consolidated view of the `identifiers.external_refs.dascp` arrays in the property records and the framework catalogue under [`dascp.framework.json`](./dascp.framework.json).

Per-control coverage classifies each of the 57 DASCP controls as:

- **Established** — at least one BPO property formally proves the control's behavioural content across all executions.
- **Partial** — at least one BPO property `supports` or `partially-supports` the control, but the property's scope is narrower than the control's full intent.
- **Gap** — no BPO property currently cross-walks to the control. Gaps in this catalogue are *deliberately* out-of-scope: legal, governance, process, infrastructure, standardization, education, or monitoring controls that describe what an organization *does* rather than what its system formally *guarantees*. BPO catalogues behavioural properties; the operational-control side of any assurance argument that *uses* BPO is a separate layer.

## Methodology

- **Relation qualifiers** are used conservatively. A link uses `establishes` *only* when proving the BPO property genuinely discharges the control across the control's full scope. When in doubt the link is downgraded to `supports` or `partially-supports`, and the limitation is recorded in the link's `note`. Under this discipline the catalogue currently has **zero** `establishes` links — even the cleanest fits (BPO:0041 → C16-S; BPO:0092 → C50-N) sit at `partially-supports` because the corresponding DASCP controls bundle operational clauses the new BPO properties do not formalize. This is the right outcome; see "Why no establishes yet" below.
- **Closure** is mechanically enforced. Every DASCP id in a BPO property's `external_refs.dascp[]` resolves against the framework file, the same way `BPO:` edges resolve against the property corpus. The validator (`schema/validate_refs.py`) fails on a dangling link.
- **Provenance** of the framework: ids, titles, category suffixes, and risk-to-control attributions are taken from the DASCP white paper (linked in `dascp.framework.json:source`); descriptions are paraphrased in our own words. The two appendix pages where multiple risks shared a Controls column (p. 26 R2/R3, p. 34 R20/R21) required a per-link subject-matter split that is documented inline on each affected `mitigates_risks` entry.

## Coverage summary

| | Count | % of 57 |
|---|---:|---:|
| Established        |  0 |   0% |
| Partial            | 25 |  44% |
| Gap                | 32 |  56% |
| — Step 3 candidates remaining as gaps | **0** | 0% |
| — out of scope (process / governance / infrastructure / standardization / education) | 32 | 56% |

**Headline of Step 4.** Every technical / behavioural gap identified in the Step 2 coverage report's Step 3 candidate list has now been answered by a newly-authored BPO property (8 new properties spanning the 11 candidate controls; see "Step 4 authored properties" below). The 32 remaining gaps are exclusively out-of-scope by design — they describe organizational practices, not system behaviour, and any attempt to formalize them in BPO would be the category error the catalogue exists to prevent.

## Control-by-control coverage

L = Legal · S = Smart Contract Governance · R = Resilience & Data Protection · N = Network Settlement

| DASCP id | Title | BPO link(s) | Coverage |
|---|---|---|---|
| C1-L  | Participation Guidelines                             | — | Gap (out of scope: legal) |
| C2-L  | Product Eligibility                                  | — | Gap (out of scope: legal) |
| C3-L  | Network and Oracle Vetting                           | — | Gap (out of scope: legal) |
| C4-L  | Participant Roles, Responsibilities, and Obligations | — | Gap (out of scope: legal) |
| C5-L  | Service Providers' Responsibilities                  | — | Gap (out of scope: legal) |
| C6-L  | Terms and Conditions                                 | — | Gap (out of scope: legal) |
| C7-L  | Governance                                           | — | Gap (out of scope: governance) |
| C8-L  | Rule Enforcement and Arrangements                    | — | Gap (out of scope: governance) |
| C9-L  | Regulatory Approval and Oversight                    | — | Gap (out of scope: legal) |
| C10-L | Asset Safeguarding and Segregation                   | — | Gap (out of scope: legal/operational) |
| C11-L | Policies and Procedures                              | — | Gap (out of scope: process) |
| C12-L | Education and Training                               | — | Gap (out of scope: education) |
| C13-S | Smart Contract Auditing Guidelines                   | — | Gap (out of scope: process) |
| C14-S | Certification                                        | — | Gap (out of scope: process) |
| C15-S | Investor Compliance and Access Control               | BPO:0040 `partially-supports` | **Partial** — access-control mediation; not the KYC/sanctions binding |
| C16-S | Multiparty Transaction Validation                    | BPO:0041 `partially-supports` | **Partial** — formalizes the behavioural k-of-n core; the "periodic updates" process clause stays out of scope |
| C17-S | Dispute Resolution Mechanism                         | — | Gap (out of scope: process) |
| C18-S | Code Auditing                                        | — | Gap (out of scope: process) |
| C19-S | Smart Contract Entitlements                          | BPO:0040 `partially-supports`; BPO:0001 `partially-supports` | **Partial** — correctness framework + mint slice; not the fine-grained mechanism mandate |
| C20-S | Quantum-Resistant Signature Algorithms               | BPO:0074 `supports` | **Partial** — hardness-assumption framework; does not specify the algorithm |
| C21-S | Intraoperability between DLT Networks                | BPO:0082 `partially-supports` | **Partial** — one L2→L1 forced-withdrawal protocol; broader cross-network surface uncovered |
| C22-S | Token Specification Model                            | — | Gap (out of scope: standardization) |
| C23-S | Data / Properties                                    | — | Gap (out of scope: standardization) |
| C24-S | Functions / Behaviors                                | BPO:0001 `partially-supports` | **Partial** — one formalized function (mint); meta-control over conformance |
| C25-S | Bookkeeping                                          | BPO:0101 `partially-supports` | **Partial** — accounting invariant present; private/public model not fixed |
| C26-S | Account Structure                                    | BPO:0101 `partially-supports` | **Partial** — accounting invariant; customer/proprietary delineation uncovered |
| C27-S | Key Life Cycle Management                            | — | Gap (out of scope: operational/process) |
| C28-S | Smart Contract Roles                                 | BPO:0040 `partially-supports`; BPO:0001 `partially-supports` | **Partial** — role-admin soundness + MINTER instance; not the full role catalogue |
| C29-S | Emergency Stop                                       | BPO:0050 `partially-supports` | **Partial** — BPO:0050 strengthens C29-S to BOUNDED form with always-available exit |
| C30-S | Account Pause                                        | BPO:0050 `partially-supports`; BPO:0051 `partially-supports` | **Partial** — system-level (0050) plus per-account scoped umbrella (0051); same bounded-with-exit strengthening |
| C31-S | Token Pause                                          | BPO:0050 `partially-supports`; BPO:0051 `partially-supports` | **Partial** — system-level (0050) plus per-token scoped umbrella (0051); same bounded-with-exit strengthening |
| C32-R | Audit Trail                                          | BPO:0072 `partially-supports`; BPO:0070 `supports` | **Partial** — public-verifiability content; timestamps + external-activity binding uncovered |
| C33-R | Data Life Cycle Management                           | — | Gap (out of scope: process) |
| C34-R | Data Subject Access Rights Enforcement               | — | Gap (out of scope: process) |
| C35-R | Event Monitoring and Alerts                          | — | Gap (out of scope: monitoring/observability) |
| C36-R | Redundancy and Concurrency                           | BPO:0080 `partially-supports` | **Partial** — formal liveness goal; redundancy is the operational mitigation |
| C37-R | Backups                                              | — | Gap (out of scope: infrastructure) |
| C38-R | Failure Prevention, Detection, and Recovery          | BPO:0080 `partially-supports` | **Partial** — formal liveness goal; recovery is operational |
| C39-R | Recovery Testing                                     | — | Gap (out of scope: process) |
| C40-R | Private Data Segregation                             | BPO:0003 `partially-supports`; BPO:0073 `partially-supports`; BPO:0075 `partially-supports` | **Partial** — proof-layer + circuit-layer + network-observer hyperproperty; data-life-cycle aspects uncovered |
| C41-R | Anonymization and Pseudonymization                   | BPO:0003 `partially-supports`; BPO:0073 `partially-supports`; BPO:0075 `partially-supports` | **Partial** — proof-layer + circuit-layer + network-observer hyperproperty; identifier-level pseudonymization process uncovered |
| C42-R | Identity Verification                                | — | Gap (out of scope: process) |
| C43-R | Geographical Distribution                            | — | Gap (out of scope: infrastructure) |
| C44-R | Feature Deployment Process                           | BPO:0030 `partially-supports` | **Partial** — layout-preservation is one necessary condition for safe upgrades |
| C45-R | Data Integrity Correction                            | BPO:0040 `partially-supports` | **Partial** — correctness of privileged roles; correction mechanism itself uncovered |
| C46-N | Data Lineage                                         | BPO:0072 `supports` | **Partial** — auditability is the precondition; lineage mechanism is operational |
| C47-N | Encumbrance Mechanism                                | BPO:0020 `partially-supports`; BPO:0093 `partially-supports` | **Partial** — reentrancy slice (0020) + single-ledger encumbrance (0093); cross-network encumbrance uncovered |
| C48-N | Settlement Proofs                                    | BPO:0070 `supports`; BPO:0090 `partially-supports` | **Partial** — knowledge-soundness as precondition (0070) + finality-as-invariant (0090); cross-network synchronized timestamps uncovered |
| C49-N | Fail to Settle Process                               | BPO:0091 `partially-supports` | **Partial** — formal reversibility content; organizational procedures stay out of scope |
| C50-N | Transaction Sequencing                               | BPO:0092 `partially-supports` | **Partial** — per-issuer monotone-nonce / at-most-once core; consensus-level global ordering uncovered |
| C51-N | Cross Ledger Data and Inventory Balances             | BPO:0101 `partially-supports`; BPO:0102 `partially-supports` | **Partial** — within-ledger conservation (0101) + cross-ledger supply consistency (0102); non-supply shared-data reconciliation uncovered |
| C52-N | Compliance and Policy Management                     | — | Gap (out of scope: process) |
| C53-N | Continuous Management Education                      | — | Gap (out of scope: education) |
| C54-N | Legacy Infrastructure Integration                    | — | Gap (out of scope: process) |
| C55-N | Third-Party Integration Guidelines                   | — | Gap (out of scope: process) |
| C56-N | Community Engagement Framework                       | — | Gap (out of scope: process) |
| C57-N | Liquidity Management Strategies                      | — | Gap (out of scope: economic strategy) |

## Step 4 authored properties

The eight properties newly authored in Step 4, with the DASCP controls each answers and the honest target relation. All targets are `partially-supports`; none claim discharge of the control's full scope.

| BPO id | Slug | Modal class | Hyperproperty? | DASCP answered |
|---|---|---|---|---|
| BPO:0041 | multiparty-transaction-validation                       | safety                                      | no  | C16-S |
| BPO:0051 | scoped-pause-safety-bounded                             | safety + guarantee-liveness-conditional     | no  | C30-S, C31-S |
| BPO:0075 | private-data-confidentiality-hyperproperty              | **hypersafety, non-interference (2-safety)** | **yes** | C40-R, C41-R |
| BPO:0090 | settlement-finality-irrevocability                      | safety                                      | no  | C48-N |
| BPO:0091 | fail-to-settle-reversal                                 | safety + guarantee-liveness-conditional     | no  | C49-N |
| BPO:0092 | transaction-sequencing-and-replay-resistance            | safety                                      | no  | C50-N |
| BPO:0093 | encumbrance-pre-settlement                              | safety                                      | no  | C47-N |
| BPO:0102 | cross-ledger-inventory-consistency                      | safety (joint-state)                        | no  | C51-N |

BPO:0075's hypersafety classification is load-bearing: the `verification.strategies` list explicitly marks single-trace tools (SMT on individual reachable states, single-execution symbolic, single-trace fuzzing) as `heuristic-evidence` with a note that they *cannot* establish the property — that entry exists in the record to record their inadmissibility, not to license them.

The seven new accepted-undischarged assumptions added by Step 4 — every one of them surfaced verbatim by the validator's ledger output. The Step 4 directives explicitly named four of these as required visible open dependencies (re-org primitive on BPO:0090, replay separation on BPO:0092, bridge-relay soundness on BPO:0102, information-flow labelling soundness on BPO:0075); the other three are load-bearing dependencies that surfaced during authoring and are kept honest rather than buried in prose.

**Ledger arithmetic.** 11 entries in the seed corpus (the state prior to Step 4) + 7 added by Step 4 authoring = **18 total in the current corpus** (= validator's ledger count).

| Property | Kind | Assumption (null discharge) | Source |
|---|---|---|---|
| BPO:0041 | environmental | Approval messages carry sufficient domain separation (chain-id, contract address, nonce) to prevent cross-context replay. | surfaced during authoring |
| BPO:0051 | environmental | The effect-set `effects(o)` of every value-moving operation is precisely modelled, so per-scope coverage is decidable. | surfaced during authoring |
| BPO:0075 | tooling       | Information-flow labelling is sound and complete across the audited code surface; every High → Low flow is either annotated `declassify(Δ)` or rejected by the type-checker. | named-honesty (Step 4 directives) |
| BPO:0075 | environmental | The Low (public-observer) model is precisely specified — which storage slots, events, call returns, gas signals, and timing signals are in scope. | surfaced during authoring |
| BPO:0090 | environmental | No protocol-level reorg primitive bypasses the finality gadget; the consensus protocol's finalized prefix is the boundary at which this property bottoms out. | named-honesty (Step 4 directives) |
| BPO:0092 | environmental | Cross-chain and cross-context replay is prevented by sufficient domain separation in the signed payload — chain-id, contract address, function-type-hash. | named-honesty (Step 4 directives) |
| BPO:0102 | cryptographic | The bridge relay is sound: the destination ledger accepts a relay evidence only when that evidence genuinely attests a finalized event on the source ledger (ZK validity proof, light-client header verification, or honest-majority committee per the relay design). | named-honesty (Step 4 directives) |

## Why there are still no `establishes` links

The conservative discipline of Step 2 carried through Step 4 unchanged. Every DASCP control bundles a behavioural core with operational, procedural, or organizational clauses; the new BPO properties formalize the behavioural cores but explicitly do not address the rest. The two cleanest cases were considered and deliberately left at `partially-supports`:

- **BPO:0041 → C16-S.** The k-of-n approval invariant is fully formalized. But C16-S also says the mechanism "includes provisions for periodic updates to address emerging security challenges and maintain compliance with industry standards." That clause is process; the BPO property does not establish it.
- **BPO:0092 → C50-N.** Per-issuer monotone-nonce / at-most-once execution is fully formalized. But C50-N also says transactions are "processed in the appropriate order" — a consensus-level global-ordering aspect that the property explicitly delegates to BPO:0080 territory and does not itself cover.

In both cases the link is `partially-supports` with a note spelling out the covered slice and the residual. Either link could be upgraded by a future maintainer-led review once the property has stabilized and the residuals are explicitly judged out-of-scope-by-design rather than uncovered-as-yet, but the default at authoring time stays conservative.

## What is deliberately *not* covered

The 32 out-of-scope gaps — C1-L through C12-L, C13-S / C14-S / C17-S / C18-S, C22-S / C23-S / C27-S, C33-R / C34-R / C35-R / C37-R / C39-R / C42-R / C43-R, and C52-N through C57-N — describe organizational practice, not system behaviour: legal arrangements, regulatory engagement, governance structures, audit programs, identity-verification procedures, infrastructure deployment, monitoring runbooks, training programs, third-party integration policy, community engagement, and liquidity management strategy. These are real DASCP controls and belong in any complete assurance argument, but the assurance argument's *behavioural-property* layer is what BPO catalogues — the operational-control layer above it is a separate concern. Sweeping these into BPO to inflate coverage would be the exact category error the catalogue exists to prevent.
