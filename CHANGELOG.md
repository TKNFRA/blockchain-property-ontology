# Changelog

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
