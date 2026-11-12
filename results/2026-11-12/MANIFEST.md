# 2026-11-12 Evaluation Evidence Manifest

**Status:** Archival of provisional strengthened-test labels and audit provenance. Not a final semantic-correctness dataset. This manifest is a record of verified bytes and storage locations as of 2026-11-12.

## Step 6 — semantic review of 31 provisional FAIL records

**Status:** Completed an **AI-assisted documentary review** against verified upstream merged PR descriptions, source issue text in the SWE-ABS record, augmented test assertions, and original per-run raw test outputs. **This was not a fresh benchmark rerun, independent human adjudication, or final correctness-label freeze.** The current **v2 runner dataset is unchanged**: 198 total, 153 PASS, 31 provisional FAIL, 14 UNVERIFIED.

| Step 6 artifact (public GitHub) | Bytes | Original SHA-256 |
| --- | ---: | --- |
| [STEP6_FAIL_REVIEW_31.csv](STEP6_FAIL_REVIEW_31.csv) — all 31 per-run opinions and evidence links | 47562 | `c1a394dccdb2a331539423f760c2b97b8fee784dcb53de3641c60e80c3a87262` |
| [STEP6_TASK_SUMMARY_15.csv](STEP6_TASK_SUMMARY_15.csv) — 15 issue-level groups | 4634 | `76e427ffe91f1f50cdd2a38fc74313ac875d5c42af869eacbca8295fecf2a13b` |
| [STEP6_FAIL_VALIDITY_REVIEW.md](STEP6_FAIL_VALIDITY_REVIEW.md) — full assertion-by-assertion rationale, counterviews, standards | 34498 | `efd61275248f440abf9d2bf7a20bb96d1bc94cd539f9aa007053a8831cb6d6b7` |
| [scripts/review_step6_fail_cases.py](../../scripts/review_step6_fail_cases.py) — deterministic extraction and documented review rules | 29666 | `6df72830f20869fbecb77f0dca7bf13a46ebb181752152eac77ef76587c62aa5` |

Each file was uploaded from the exact local source text/CSV and fetched back from GitHub with exact content comparison. **Disposition counts among the 31 raw FAILs**: 9 `valid_failure` (documentary support, still provisional); 4 `invalid_test` (specific enhanced-assertion defect / issue-scope mismatch); 2 `environment_sensitive` (Python 3.9 staticmethod behavior); 16 `unresolved` (specification or scope ambiguous). **Do not reinterpret these as revised PASS/FAIL labels.**

Key external sources checked directly: [RFC 7231 §7.1.1.1](https://www.rfc-editor.org/rfc/rfc7231.html#section-7.1.1.1), [RFC 3986 §3.2.1](https://www.rfc-editor.org/rfc/rfc3986.html#section-3.2.1), [Python staticmethod documentation](https://docs.python.org/3/library/functions.html#staticmethod), and the 15 verified upstream merged PR links in the per-run CSV.

**Next stage:** Step 7 — triage 14 UNVERIFIED, choose and document exclusion/sensitivity policies that distinguish raw runner outcomes from semantic review, and freeze a versioned analysis label manifest. Any additional human/maintainer validation of unresolved FAILs remains a research limitation or separate check; do not silently promote them.

## Current provisional dataset — Step 5 historical reconciliation (v2)

**Current research labels (after the 83-run raw-log re-audit): 153 PASS, 31 FAIL, 14 UNVERIFIED among 198 attempts.** The files in the table immediately below were created on 2026-11-12 and GitHub content was read back after commit. The original v1 CSV and its historical counts (153/32/13) remain unchanged below for reproducibility; **use v2 for subsequent reviewed-label work**.

| Step 5 artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| [sweabs_full_198_cumulative_v2.csv](sweabs_full_198_cumulative_v2.csv) — current versioned provisional labels | 93933 | `e8cca12033e7666dcb14133d619ddac00297bd2a6fbc8c03e1801944da78c214` |
| [sweabs_historical_83_reaudit_evidence.csv](sweabs_historical_83_reaudit_evidence.csv) — 83 raw runner / identity audit records | 35131 | `3fe8b9f4de0df30d96c44825d361a51f85f9df6315ecb97b9602bca2137f33be` |
| [sweabs_historical_83_corrections.csv](sweabs_historical_83_corrections.csv) — 1 append-only correction | 521 | `1c66f4e0c819a67e7f727154e110a3f3cfc05a4996077325b60c12a7060d01c1` |
| [STEP5_RECONCILIATION_REPORT.md](STEP5_RECONCILIATION_REPORT.md) — method, justification, unresolved cases | 8071 | `93759c073a4cff4387b816702c3da7b84d3cac1e77f904752da00c37946bfc55` |
| [scripts/reaudit_historical_83.py](../../scripts/reaudit_historical_83.py) — offline audit reproduction | 13024 | `f1b8f7bc4b50b65a49ddeaa94a9410c3fbd34c314c721c0ee47e81321939a7f1` |

**Single correction:** Sample 1 offset 58, `sympy__sympy-23413`, **FAIL → UNVERIFIED**. Model patch's modified test file disappeared from post-test repository diff, so exact-patch persistence was not established. The raw 7-pass/1-exception observation remains recorded. `psf__requests-1142` remains UNVERIFIED despite 15 passing tests because its large generated/build patch was not fully repository-diff-verified. See [Step 5 report](STEP5_RECONCILIATION_REPORT.md).

**Private historical raw evidence:** `sweabs_historical_83_raw_evidence_private.zip` (2,790,331 bytes; 86 ZIP entries; SHA-256 `cc7c5f4280c3dd7e4ccfb34f55ea151f472435e33d1e7465fb73cf9c75c586e4`). It contains 83 original selected per-patch ZIPs and the earlier failed Sample 1 offset-5 attempt. Stored only in the owner's private ChatGPT Library at `/Research/SWE-ABS/2026-11-12/sweabs_historical_83_raw_evidence_private.zip`; materialized back and ZIP+checksum verified. **Not publicly available on GitHub.** The earlier 5.1 MB raw ZIP for Samples 2–3 is preserved separately below.

**Step 5 completion:** Historical 83-row v1-to-v2 identity and all 83 artifact audits reviewed, one correction versioned. Semantic validity of the remaining 31 FAIL cases is **not** established; this is Step 6. No new evaluation runs or trajectory features were created in Step 5.

## GitHub-archived, byte-verified files

| File | Records / role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| [sweabs_full_198_cumulative_audited.csv](sweabs_full_198_cumulative_audited.csv) | 198 provisional attempts across Samples 1–3 | 93852 | `7a848f2dfbbad224ea110a9d090ba4f2194ed157df7fd49d1946ae88743c6da8` |
| [sweabs_samples2_3_full_audit_evidence_115.csv](sweabs_samples2_3_full_audit_evidence_115.csv) | 115 newly raw-audited per-patch attempts (48 Sample 2, 67 Sample 3) | 132150 | `3e4218862ac500872b2645ad766835579e146e58b004e394031e8c9c707cb18f` |
| [sweabs_full_198_audit_report.md](sweabs_full_198_audit_report.md) | Audit scope, corrections, limitations, unresolved cases | 11814 | `76559162321d9cab1e5fee4f9ad7bdba999a4379a0e38f651819f1571201ea07` |
| [sweabs_samples1_2_first83_cumulative.csv](sweabs_samples1_2_first83_cumulative.csv) | Historical input snapshot; first 83 rows retained by the 198-row audit | 23453 | `919c137b315fbe8ba6e9cdbe9491222304a36f17e920ae05aa15f405ab08aea4` |
| [sweabs_full_audit.py](sweabs_full_audit.py) | Historical offline audit script used in the original audit session | 15509 | `8f9061760eda1c8f4f6188a66bce4b6d6da24e75c7977be05a95ad0f719f74f9` |

**Verification:** The above GitHub file contents were read back after commit; the first three files were independently SHA-256 verified against the original local files using an SHA-256 implementation tested against the `abc` reference digest. The historical CSV/script were verified by exact content and expected original byte sizes; their SHA-256 hashes above were generated from the local source files. Original CSV CRLF line endings and terminal newlines were preserved; an earlier transient text-normalized commit of the first three files was superseded by corrected commits.

**Interpretation:** 153 provisional PASS, 32 provisional FAIL (independent test semantic-validity review outstanding), 13 UNVERIFIED (not failures). These describe 198 agent runs with repeated task IDs, not 198 unique tasks. Earlier 83 rows were not independently re-audited in the 115-run pass.

## Raw ZIP — privately preserved, not public on GitHub

| Artifact | Original bytes | SHA-256 |
| --- | ---: | --- |
| `sweabs_full_audit_evidence_bundle.zip` | 5136675 | `b7f5fd76f747a23a83fb5b2d5e2c355d6123c2e2c9ddfe6fea974b3ac3c73d99` |

- Saved to the repository owner's **private ChatGPT Library** at `/Research/SWE-ABS/2026-11-12/sweabs_full_audit_evidence_bundle.zip`.
- Independently materialized back from the Library; digest matched the original ZIP; `zipfile.testzip()` passed and 140 archive entries were visible.
- Contents: 135 per-patch ZIPs for Samples 2 and 3, plus the historical 83-row CSV, 198-row CSV, 115-row audit evidence CSV, audit report and audit script. **Sample 1 raw per-patch ZIPs are not in this bundle**; consult the corresponding GitHub Actions history and the older audit checkpoint.
- **Private limitation:** The Library archive is accessible via the owner's ChatGPT file Library, **not to a public reader or an arbitrary unauthenticated AI**. The GitHub repository does **not** host this ZIP. An external long-term/public distribution decision remains a separate consideration.
- Public-release suitability review: a recursive scan found email-address-like strings and password-like assignment patterns inside nested test files and logs. No obvious GitHub PAT, GitHub fine-grained PAT, AWS access-key pattern, or private-key block matched the limited detector set. **This is not a guarantee of no secrets**; the ZIP was intentionally **not publicly committed or shared** pending stronger review.

## Integrity / usage instructions

Verify each downloaded GitHub artifact with, for example:

```bash
sha256sum results/2026-11-12/sweabs_full_198_cumulative_audited.csv
sha256sum results/2026-11-12/sweabs_samples2_3_full_audit_evidence_115.csv
sha256sum results/2026-11-12/sweabs_full_198_audit_report.md
```

To retrieve the private ZIP in a future authorized chat, inspect the **Library**, look under `/Research/SWE-ABS/2026-11-12`, materialize the file, and verify SHA-256 before using it. Do not assume the path is available to other users, public GitHub readers, or unconnected assistants.

**Historical audit script caveat:** `sweabs_full_audit.py` was archived verbatim as an audit provenance artifact and has session-specific paths (`ROOT=/mnt/data`). It was **not** refactored or rerun in this archival step; use with its original input folder layout and review before adapting.

## GitHub source runs

[All GitHub Actions evaluation runs](https://github.com/Foysal-Munsy/sweabs-free-eval/actions) · [Full audit and known issues](sweabs_full_198_audit_report.md) · [Current milestone state](../../docs/PROJECT_STATE.md)

**Next research milestone:** Step 7 — triage 14 UNVERIFIED, define inclusion/exclusion and uncertainty policies for Step 6 reviewed FAILs, and freeze versioned analysis labels. Any independent human/maintainer adjudication remains outstanding.
