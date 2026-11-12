# 2026-11-12 Evaluation Evidence Manifest

**Status:** Archival of provisional strengthened-test labels and audit provenance. Not a final semantic-correctness dataset. This manifest is a record of verified bytes and storage locations as of 2026-11-12.

## Step 11 original-base in-place coverage and missing Oracle method (2026-11-12)

**Pinned source & raw test-log validation:** [read-only CI #43267304895 SUCCESS](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43267304895) independently loaded original Django source at base commit `5e04e84d67da8163f365e9f5fcd169e2630e2873` (SHA-256 `70a046a812c17e7c8dbf0ec8d34cd6a4c5e3cd8bbcd0615c85460469769bfa5a`) and mapped the pinned SWE-ABS `django-14434` 10 insertion hunks to **one added plus nine modified existing tests**. Original test-output logs from **three** runs show the new method `ok`, **8/9 modified methods `ok`**, and **one modified method `skipped`** (`test_func_unique_constraint_covering`, backend lacks `supports_expression_indexes` and `supports_covering_indexes`). This proves incomplete enhanced test-method coverage but **not** semantic failure.

[Oracle source/log check](STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json), with [CI #43268521977 SUCCESS](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268521977) and [CI #43268574096 SUCCESS](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268574096), verified `django-15503` declares `test_oracle_json_path_final_key_is_quoted_for_numeric_strings` inside `JSONFieldNumericKeyLookupsTests` while the method is absent from each original SHA-identified verbose log. It reused previously independently audited original ZIP + method logs: **not a fresh raw ZIP download, not a runtime/semantic oracle**.

**Repository infrastructure caveat:** [intermediate workflow #43268071356 FAILED](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268071356) due to GitHub artifact storage **HTTP 503 egress limit** during redundant ZIP download; this was **not a coding-agent test failure**. Updated read-only [Step 11 CI workflow](../../.github/workflows/step11-reproduction.yml) makes raw ZIP redownloads **manual `workflow_dispatch` opt-in**, defaulting to already verified SHA-identified metadata; [later workflow #43268574096](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268574096) PASSED without rerunning ZIP downloads.

| Added versioned public artifact | Verified UTF-8 bytes | GitHub blob SHA-1 (NOT SHA-256) |
| --- | ---: | --- |
| [Django-14434 original-base in-place method audit script](../../scripts/step11_inplace_method_audit.py) | 9716 | `fdd276bf2886934686c8d81f5f95639018153f29` |
| [Django-15503 Oracle source/log method audit script](../../scripts/step11_missing_oracle_method_audit.py) | 9338 | `c66a1f49e2efb4291ee01ea95625e8431d512711` |
| [STEP11_INPLACE_METHOD_AUDIT_DJANGO14434_v1.json](STEP11_INPLACE_METHOD_AUDIT_DJANGO14434_v1.json) | 10965 | `8965cb43016ac0480a87ed792ad3c8def1129865` |
| [STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json](STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json) | 2990 | `3f63393b61edb0f92fa31de901efb39ec530aed2` |
| [STEP11_INPLACE_AND_ORACLE_COLLECTION_REVIEW_v1.md](STEP11_INPLACE_AND_ORACLE_COLLECTION_REVIEW_v1.md) | 7412 | `344ec8b9b397801ed234570736f62646b8b0a060` |
| [STEP11_SEMANTIC_VALIDITY_GATE_v1.md](STEP11_SEMANTIC_VALIDITY_GATE_v1.md) — updated | 19161 | `daf70d04484d3b0d930fe7c9cf3d44b82ec4591e` |
| [Read-only Step 11 CI workflow](../../.github/workflows/step11-reproduction.yml) — manual-raw-download default | 5599 | `892a80bcb3cd94f3e43d06b6333f8c7d30db45bf` |

**Research invariant:** Original runner v2 remains **153 PASS / 31 FAIL / 14 UNVERIFIED**; Step 7 conservative eligibility **153/9/36** unchanged; Step 8 frozen indicators and corrected v2 analysis unchanged. Controlled backend execution and human semantic label adjudication still **NOT verified**. Do not promote three Django-14434 or three Django-15503 UNVERIFIED records to PASS.

## Step 11 semantic/source, original ZIP and augmented-method evidence (2026-11-12)

**Evidence chain:** [CI #43262365929](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43262365929) independently matched original model/test SHA for **31 FAIL + 14 UNVERIFIED = 45 exact runs**, 20 distinct tasks. [CI #43263048387](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43263048387) freshly downloaded all **14** short-retention original Actions `sweabs-result-*` ZIPs from 11 evaluation runs, checked original model hash metadata, read **14 test output files**, and recorded SHA-256 digests. 14/14 original test patch hashes also match the independently pinned SWE-ABS structural crosswalk (verified from the two archived JSON records). [CI #43264326911](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43264326911) independently matched added Django test methods to original verbose test results in all nine skipped-coverage runs.

**Important audit distinction:** 9 skipped-coverage runs have **4 / 28 / 1** suite-level skipped counts in their Django task families, but newly added method coverage differs: Django-12039 **13 added: 9 passed + 4 skipped**, Django-14434 **1 added: 1 passed** (28 suite-level skipped), Django-15503 **10 added: 8 passed + 1 skipped + 1 not found in verbose log**. Modified pre-existing test methods and backend-dependent behavior are NOT exhaustively covered by this name-based check; no original UNVERIFIED outcome was promoted to PASS.

| Artifact | Verified UTF-8 bytes | Current GitHub blob SHA-1 (NOT SHA-256) |
| --- | ---: | --- |
| [scripts/step11_semantic_structural_audit.py](../../scripts/step11_semantic_structural_audit.py) | 8176 | `7e2739184b365062fc4fcacc8e42605ded2ad3e9` |
| [scripts/step11_raw_artifact_reaudit14.py](../../scripts/step11_raw_artifact_reaudit14.py) | 6260 | `374d02bf345147daf249fccdc3b84eb2ede773e4` |
| [scripts/step11_skip_attribution.py](../../scripts/step11_skip_attribution.py) | 5615 | `c72bb5b68b5fbe8fecc996c7d967a25f5092a2fb` |
| [STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json](STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json) | 75970 | `c88ba18ee0c12ddb41313b2e1e3f821bff20af92` |
| [STEP11_RAW_ARTIFACT_REAUDIT14_v1.json](STEP11_RAW_ARTIFACT_REAUDIT14_v1.json) | 36574 | `b3a5ea755bd12ecfd0a1bcd5516c2360b1e91ac5` |
| [STEP11_SKIP_ATTRIBUTION_9_v1.json](STEP11_SKIP_ATTRIBUTION_9_v1.json) | 21965 | `1421b2b7e4b5a93b8cb2593868468d71815f0683` |
| [STEP11_SEMANTIC_VALIDITY_GATE_v1.md](STEP11_SEMANTIC_VALIDITY_GATE_v1.md) | 19161 | `daf70d04484d3b0d930fe7c9cf3d44b82ec4591e` |
| [Read-only updated Step 11 reproduction workflow](../../.github/workflows/step11-reproduction.yml) | 5599 | `892a80bcb3cd94f3e43d06b6333f8c7d30db45bf` |

**Limitations:** GitHub artifact ZIPs have short retention; future `--check` reproduction depends on still-unexpired original artifacts and a token with Actions read permission. No private raw ZIP or full raw test log is published here. Source-level file collision is NOT a semantic failure verdict; skipped/backend and in-place modified existing test methods need controlled reruns or an independently defensible oracle. Four test-file overlaps, one huge generated Requests patch and 16 unresolved/2 environment-sensitive FAIL reviews remain open. Original runner v2 (153/31/14), Step 7 labels (153/9/36) and Step 8 feature formulas are **unchanged**.

## Step 11 — independent pinned reproduction, task-aware robustness and 12-trace recount (2026-11-12)

**Source integrity and execution:** [read-only CI workflow](../../.github/workflows/step11-reproduction.yml) triggered via GitHub and [successful job #43260088649](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649) confirmed from job status and raw logs. Python 3.11.18, pinned `datasets==4.8.5` and `huggingface_hub==1.33.0`. Five synthetic tests PASS; frozen Step 9 198/198 exact-HF `--check` PASS; corrected Step 10 AUROC `--check` PASS; exploratory Step 11 task-robustness `--check` PASS; 12 pinned raw trajectories independently recounted against 14 archived fields each (**168 comparisons, zero mismatches**); no original source evidence edited. The 12-case JSON below was obtained from the passing CI job's text logs, not inferred from workflow success alone. User data was not added; no raw full trajectory was committed to GitHub.

| Step 11 public artifact | UTF-8 bytes verified by GitHub read-back | GitHub blob SHA-1 (NOT SHA-256) |
| --- | ---: | --- |
| [Read-only CI workflow](../../.github/workflows/step11-reproduction.yml) | 4023 | `11bf436af68bd23d080378bd2f70daa35c25c8ff` |
| [Python post-hoc task robustness script](../../scripts/step11_robustness.py) | 7126 | `4d455fbb2237393601f88f2d072ecb247727c83f` |
| [Independent 12-trace raw-event recount script](../../scripts/step11_trace_spotcheck.py) | 7424 | `1fd07d922d97d5e69f686d51559405f2623d613a` |
| [Frozen indicator synthetic unit tests](../../tests/test_step9_indicators.py) | 2990 | `7ac5765cee52486055fe1ccee0cd5fd211f225c4` |
| [STEP11_EXPLORATORY_ROBUSTNESS_v1.json](STEP11_EXPLORATORY_ROBUSTNESS_v1.json) | 12492 | `b3af76ab18ec89aa0ef36b2c00678485e46e0c77` |
| [STEP11_TRACE_SPOTCHECK_12_v1.json](STEP11_TRACE_SPOTCHECK_12_v1.json) | 3948 | `a343315cba47faf5be6817ba45e3643e1497cd45` |
| [STEP11_REPRO_AND_ROBUSTNESS_v1.md](STEP11_REPRO_AND_ROBUSTNESS_v1.md) | 9643 | `067ddf83707f9ff179fe5208ed3cf0ef384db28c` |
| [Step 9 Python extractor after versioned Django regex implementation fix](../../scripts/step9_extract_trajectory_features.py) | 8360 | `3a45bc0d935427b2137835a7dce88d7ddf6d90e5` |

**Unchanged immutable data:** 198-run original provisional runner v2 (153 PASS / 31 FAIL / 14 UNVERIFIED); Step 7 198-run label/eligibility manifest (conservative 153/9/36); frozen Step 8 formulas; archived Step 9 feature CSV (198 rows); corrected Step 10 v2 AUROCs. The Django `runtests.py` parser fix is an implementation correction that enabled exact Python reproduction of the *same* original feature rows.

**Critical scope limit:** Step 11 technical reproduction/robustness is verified, but independent *semantic correctness* of all augmented test assertions and 16 unresolved, 2 environment-sensitive FAIL reviews plus 14 UNVERIFIED outcomes is not. This is not final gold-label proof or journal readiness. Step 11's human/maintainer semantic validity and coverage gate remains open; task-aware Step 11 analysis is post-hoc exploratory, not a trained task-disjoint predictor.

## Steps 8–10 — frozen trajectory features and provisional quantitative analysis (2026-11-12)

**Source:** [Step 8 frozen specification](../../docs/STEP8_FROZEN_INDICATORS_v1.md), [Step 9 exact-match features](STEP9_TRAJECTORY_FEATURES_v1.csv), [Step 9 coverage](STEP9_COVERAGE_v1.json), [Step 10 corrected AUROC v2](STEP10_AUROC_TASK_CLUSTER_v2.json) and [quantitative report](STEP10_QUANTITATIVE_REPORT_v1.md). The dataset's current HF revision was confirmed equal to the previously pinned `b5515d1dce40036633293b70477f0633b24593f7`; viewer returned 296 trajectories (198 original successful). Derived features matched 198/198 identities on sample/instance/SHA-256, 73 tasks and no matched-task patch hashes differed. The original 198-row v2 outcomes and Step 7 label manifest are unchanged.

| New public artifact | UTF-8 bytes from GitHub read-back | Current GitHub blob SHA-1 (NOT SHA-256) |
| --- | ---: | --- |
| [docs/STEP8_FROZEN_INDICATORS_v1.md](../../docs/STEP8_FROZEN_INDICATORS_v1.md) | 8102 | `7a825e1da9b172ca15c43e5267f5ebc0dd1e9fdd` |
| [scripts/step9_extract_trajectory_features.py](../../scripts/step9_extract_trajectory_features.py) | 8200 | `1e2eacc7bd5cb03afc2801163f03ea19153ec30f` |
| [STEP9_TRAJECTORY_FEATURES_v1.csv](STEP9_TRAJECTORY_FEATURES_v1.csv) | 37976 | `fac9cca283a4e0ae2f5a8f6f9684402354cac42b` |
| [STEP9_COVERAGE_v1.json](STEP9_COVERAGE_v1.json) | 462 | `18e745dff47e63e3c24d35c553afccf01d7af31d` |
| [scripts/step10_analyze_frozen_features.py](../../scripts/step10_analyze_frozen_features.py) | 5579 | `0d608dc5775600b86863b065edeebe9da6aa7ee4` |
| [STEP10_AUROC_TASK_CLUSTER_v1.json](STEP10_AUROC_TASK_CLUSTER_v1.json) — **INVALID bootstrap intervals, historical only** | 6724 | `f5dc1d575e8545e069e6cd8aa999f335829e504c` |
| [STEP10_AUROC_TASK_CLUSTER_v2.json](STEP10_AUROC_TASK_CLUSTER_v2.json) — **corrected task bootstrap** | 6916 | `c8dd764396f2bba06140a5e7340c9062ea747351` |
| [STEP10_QUANTITATIVE_REPORT_v1.md](STEP10_QUANTITATIVE_REPORT_v1.md) | 8750 | `1fee077212702052cb1d3f2a0d8976dba07415c9` |

**Status caution:** These are checked-in, connector-read-back files and calculated byte counts; no independent `sha256sum` was generated for this Step 8–10 group. The step 9–10 data pipeline was evaluated using browser-resident JavaScript transformations over the live dataset and GitHub-fetched CSVs. The checked-in Python scripts are intended reproducibility implementations, **but end-to-end Python execution and `--check` verification remain unverified**. Do not claim CI-tested reproduction, independent source-event spot check or semantic-oracle validation.

**Statistical caveat:** Conservative primary: 153 PASS, 9 documentary-supported FAIL (only five distinct FAIL task IDs), 36 excluded. Duplicate-terminal AUROC **0.489** (95% corrected task-cluster interval **0.270–0.706**). Runner-only sensitivity uses 31 provisional FAILs and yields **0.708** (0.562–0.834), a label-policy-dependent association. 500 task-ID-cluster bootstrap replicates with fixed seed; see [report](STEP10_QUANTITATIVE_REPORT_v1.md). The archived v1 bootstrap has a **low-bit LCG modulo bug** causing degenerate confidence intervals in a 64-task scenario; do NOT use those intervals. Corrected v2 uses high-bit scaled task sampling; point estimates and frozen indicators unchanged.

**Next stage:** Step 11 independent reproduction, feature spot-checks, task/project confounding, validation sensitivity and unresolved test semantic integrity. No external predictive performance is claimed.

## Step 7 — provisional analysis eligibility and UNVERIFIED triage (2026-11-12)

**Status:** The documentary review/eligibility gate is complete; not a rerun, independent oracle adjudication, or final semantic correctness dataset. Source inputs remain the archived [198-row v2](sweabs_full_198_cumulative_v2.csv), [historical 83 evidence](sweabs_historical_83_reaudit_evidence.csv), [recent 115 evidence](sweabs_samples2_3_full_audit_evidence_115.csv), and [Step 6 FAIL ledger](STEP6_FAIL_REVIEW_31.csv). All 198 exact identities were checked against their audit rows and the 31 FAIL reviews were joined. Raw runner v2 unchanged: **153 PASS / 31 FAIL / 14 UNVERIFIED**.

| New publicly archived Step 7 artifact | UTF-8 bytes | GitHub-fetched SHA-256 |
| --- | ---: | --- |
| [STEP7_ANALYSIS_LABELS_v1.csv](STEP7_ANALYSIS_LABELS_v1.csv) — 198 exact-run records, primary and sensitivity label screens | 51518 | `9f074e9a4a5d4caf8424bfa41bda18460c29d1c2ba72178587fc802c509cd8ec` |
| [STEP7_UNVERIFIED_TRIAGE_14.csv](STEP7_UNVERIFIED_TRIAGE_14.csv) — all 14 old UNVERIFIED, reasons and followups | 7965 | `e43e4abd92731386b23bd2d8ca7dcca0e6b5d49a89f40451b3b3abb7f1a49378` |
| [STEP7_TRIAGE_AND_LABEL_POLICY.md](STEP7_TRIAGE_AND_LABEL_POLICY.md) — documentary review, alternative interpretations, label rules | 9983 | `bf31e0087528187b20af3be266655ddd6a9f9b4bb17aa9a677e4d3f9a8320e55` |
| [scripts/build_step7_analysis_labels.py](../../scripts/build_step7_analysis_labels.py) — deterministic regeneration/check tool | 8354 | `defa44c2223551f438221180d4c2049c6315bf65ce2f25261694abc0a31bdaf7` |

The hashes and byte lengths above were recomputed from connector-fetched GitHub UTF-8 file contents, after the new files were committed. The SHA-256 routine passed a known `abc` digest self-check. **The Python rebuild/check command was not independently executed in a cloned checkout in this session** because the isolated local terminal could not resolve github.com; do not claim end-to-end reproduction was executed. A future environment with checkout access should run `python scripts/build_step7_analysis_labels.py --check` and log its result.

The 14 triaged cases are **9 partial coverage, 4 patch-overlap, and 1 whole-patch integrity gap**; all remained UNVERIFIED. GitHub Actions artifact metadata listed all 14 per-run artifacts as unexpired at the time of review, but individual ZIPs were not freshly re-audited. Conservative primary v1 screen: **153 audited PASS / 9 documentary-supported FAIL / 36 excluded** (162 rows, 61 tasks, only 5 distinct FAIL tasks). See report for alternative sensitivity definitions and unresolved human/oracle checks. Original archived audit CSV versions and private raw ZIPs have not been changed.

**Next stage:** Step 8 indicator specification freeze. Do not extract indicators or fit a predictive model before defining indicators and checking sources independent of observed outcome associations.

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

**Subsequent stage completed at documentary scope:** Step 7 now has a versioned, conservative provisional eligibility manifest (see section above). Independent semantic adjudication of unresolved FAILs remains open; do not silently promote them.

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
