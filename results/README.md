# Research results and audit artifacts

**Current stage (2026-11-12):** 198 stronger-test attempts and 83+115 raw audits complete; original v2 **153 PASS / 31 FAIL / 14 UNVERIFIED** unchanged. Step 8 versioned frozen indicators, Step 9 exact-match features (198/198) and Step 10 provisional task-aware univariate AUROCs are archived. These are not independently adjudicated semantic labels, a trained classifier or a generalization claim. **Step 11 technical reproduction, 45-run source crosswalk, 14 original result ZIPs and nine method-level coverage checks VERIFIED; human/maintainer semantic adjudication and controlled backend/exact-patch reruns remain NEXT.**

## Current version: Step 5, 83-run reconciliation

- [Current 198-row cumulative provisional CSV (v2)](2026-11-12/sweabs_full_198_cumulative_v2.csv)
- [Step 5 detailed 83-row historical re-audit evidence](2026-11-12/sweabs_historical_83_reaudit_evidence.csv)
- [Step 5 one-row correction ledger](2026-11-12/sweabs_historical_83_corrections.csv)
- [Step 5 report — correction justification and limitations](2026-11-12/STEP5_RECONCILIATION_REPORT.md)
- [Re-audit reproduction script](../scripts/reaudit_historical_83.py)

**Version control:** [v1 (198 runs)](2026-11-12/sweabs_full_198_cumulative_audited.csv) recorded 153 PASS, 32 FAIL, 13 UNVERIFIED. v2 corrects **Sample 1 offset 58: FAIL → UNVERIFIED** due to overlapping agent-modified/augmented test files. **Original v1 is preserved unchanged**. No other v1 rows were changed.

## Step 6: FAIL test-validity documentary review (completed, non-final)

- [Per-run semantic review ledger, 31 rows](2026-11-12/STEP6_FAIL_REVIEW_31.csv)
- [Issue-level summary, 15 tasks](2026-11-12/STEP6_TASK_SUMMARY_15.csv)
- [Detailed test-validity review: assertions, citations, counterarguments](2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md)
- [Review extraction and reasoning script](../scripts/review_step6_fail_cases.py)

**Disposition counts (among the same 31 raw FAILs):** 9 `valid_failure` (review-supported, still provisional), 4 `invalid_test`, 2 `environment_sensitive`, 16 `unresolved`. No v2 PASS/FAIL/UNVERIFIED labels were changed. The completed documentary review contains open semantic issues; independent human/maintainer adjudication remains pending.

## Step 7: provisional analysis-label and UNVERIFIED triage gate (completed)

- [Step 7 method/report: 14-case review, exclusions, competing interpretations, limitations](2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md)
- [Versioned 198-run analysis-label manifest v1](2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv): conservative primary **153 runner PASS / 9 review-supported FAIL / 36 excluded**; only 5 distinct FAIL task IDs
- [Triage ledger for all 14 UNVERIFIED](2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv): 9 coverage skips / 4 patch overlap / 1 large patch not fully verified
- [Deterministic label rebuild/check script](../scripts/build_step7_analysis_labels.py); source v2, audit tables and Step 6 review remain unchanged

Alternative target scenarios (0/1/excluded): noninvalid FAIL **153/27/18**, all runner FAIL **153/31/14**, hypothetical skipped-as-PASS **162/9/27**. These are sensitivity assumptions, **not new observed runner labels or semantic truth**. Actions artifact metadata was cross-checked but raw per-patch ZIPs were not newly re-audited in Step 7.

## Step 11: semantic validity/source artifact checks (2026-11-12)

- [45-run pinned original agent/test structural crosswalk](2026-11-12/STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json) and [independent checker](../scripts/step11_semantic_structural_audit.py) — [CI #43262365929 success](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43262365929). Matched 31 reviewed FAIL + 14 UNVERIFIED across 20 tasks on original model SHA; confirmed all Step 6 test hashes, 4 source-level model/test file collisions, and 65 generated Requests `build/` paths.
- [Original 14 ZIP fresh metadata/log re-audit](2026-11-12/STEP11_RAW_ARTIFACT_REAUDIT14_v1.json) and [read-only downloader](../scripts/step11_raw_artifact_reaudit14.py) — [CI #43263048387 success](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43263048387): downloaded 14 original result ZIPs, checked 14 exact patch identities, independently matched 14 pinned augmented-test SHA values and recorded 14 raw-test-log digests. Private raw ZIPs/full logs **not published**.
- [Nine-run newly-added augmented test-method attribution](2026-11-12/STEP11_SKIP_ATTRIBUTION_9_v1.json) and [method matcher](../scripts/step11_skip_attribution.py) — [CI #43264326911 success](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43264326911). Each sample: `django-12039`: 13 added methods, 9 passed/4 skipped; `django-14434`: 1 added method passed despite 28 total suite skips; `django-15503`: 10 added, 8 passed/1 skipped/1 unobserved in verbose test log. Only **new definitions** counted, not extra assertions injected into existing tests. No original outcomes changed.
- [Complete evidence hierarchy, opposing interpretations, controlled-rerun prerequisites and semantic limitations](2026-11-12/STEP11_SEMANTIC_VALIDITY_GATE_v1.md). All remain *documentary/structural* findings; semantic labels require separate validated evidence. Original v2 **153/31/14** and Step 7 frozen primary **153/9/36** unchanged.

## Step 11: in-place enhanced assertions and missing Oracle test collection

- [Source-aware Django-14434 method mapping](2026-11-12/STEP11_INPLACE_METHOD_AUDIT_DJANGO14434_v1.json), [reproduction script](../scripts/step11_inplace_method_audit.py), [successful CI #43267304895](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43267304895). Pinned Django base `tests/schema/tests.py` at `5e04e84d67da8163f365e9f5fcd169e2630e2873`: one newly defined method and nine enhanced in-place modified pre-existing methods. In each of samples 1/2/3, **new method `ok`, eight modified methods `ok`, one modified method `skipped`** (`test_func_unique_constraint_covering`, backend does not support expression and covering indexes). The 28 suite-level skips did indeed include **at least one enhanced assertion-bearing method**.
- [Pinned Django-15503 Oracle method/source-log gap](2026-11-12/STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json), [reproduction script](../scripts/step11_missing_oracle_method_audit.py). The source `JSONFieldNumericKeyLookupsTests` declares `test_oracle_json_path_final_key_is_quoted_for_numeric_strings`; **none of three original verbose logs show it**. Cause not established, no runner outcome promoted; [successful CI #43268574096](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268574096) reuses independently SHA-verified original ZIP and method logs.
- [Full source-level review and methodological limits](2026-11-12/STEP11_INPLACE_AND_ORACLE_COLLECTION_REVIEW_v1.md). A redundant artifact download in [CI #43268071356](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268071356) temporarily failed with **HTTP 503 egress-limit**; now repeat original ZIP downloads are **manual opt-in** and do not run on ordinary pushes. Successful CI #43268574096 confirms revised workflow integrity. All original v2/Step 7 outcomes and frozen Step 8 signals unchanged.
- **Next:** controlled backend-matched test `test_func_unique_constraint_covering` and Oracle test collection checks under pinned exact original agent patch, plus independent unresolved FAIL semantic oracles. Step 11 remains **IN PROGRESS**.

## Step 11: pinned independent reproduction and exploratory task-aware robustness

- [Step 11 full report, methodological cautions and remaining validity gate](2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md), [post-hoc robustness JSON](2026-11-12/STEP11_EXPLORATORY_ROBUSTNESS_v1.json), [12-trajectory source recount JSON](2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json).
- [Reproducibility workflow](../.github/workflows/step11-reproduction.yml) — **[GitHub Actions #43260088649: success](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649)** using Python 3.11.18, `datasets==4.8.5`, `huggingface_hub==1.33.0`. Five synthetic tests, pinned full HF Step 9 extraction and Step 10–11 `--check` comparisons, independent 12-trace tool event recount (**168 comparisons / 0 mismatch**) and read-only source integrity all pass.
- [Task-robustness implementation](../scripts/step11_robustness.py), [independent raw-message recounter](../scripts/step11_trace_spotcheck.py) and [synthetic indicator tests](../tests/test_step9_indicators.py). Primary duplicate rate run-level AUROC **0.489**, task-macro **0.522**, within-project **0.390**, one-positive-task omission **0.382–0.620**. Broader runner-only target **0.708**, task-macro **0.741**. **Post-hoc sensitivity, not held-out predictive validation.**
- **Still open:** Independent semantics of unresolved/environment-sensitive enhanced-test FAILs, and 14 UNVERIFIED. No original outcome labels changed and no final semantic correctness established.

## Steps 8–10: frozen signals, exact-match extraction, preliminary AUROCs

- [Step 8 preregistered feature specifications](../docs/STEP8_FROZEN_INDICATORS_v1.md) and [reproduction extractor](../scripts/step9_extract_trajectory_features.py) — committed before inspecting feature-label associations.
- [Step 9 198-run feature CSV](2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv) and [exact-match/parse coverage](2026-11-12/STEP9_COVERAGE_v1.json) — 296 original source rows, 198 originally successful runs, 198/198 exact identities, 73 tasks, 191 recognized verification-command runs.
- [Step 10 full report](2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md), [corrected v2 task-cluster AUROC JSON](2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json), [analysis script](../scripts/step10_analyze_frozen_features.py). Conservative primary (153/9/36): duplicate-command AUROC **0.489** (95% task-cluster interval 0.270–0.706), explicit error rate **0.599** (0.420–0.790). All runner FAIL sensitivity (153/31/14): duplicate-command AUROC **0.708** (0.562–0.834). **No validated predictive conclusion.**
- [Historical Step 10 v1 JSON](2026-11-12/STEP10_AUROC_TASK_CLUSTER_v1.json) — **do not use its confidence intervals**; a low-bit cluster-bootstrap sampling bug produced degenerate results at 64 clusters. v2 fixes the draw only and retains point estimates and original data.

**Open verification:** The pinned Python extractor/analysis `--check` commands have not been independently executed end-to-end. Semantic oracles, original strengthened-test test-validity disputes, repeated-task confounding, and only five primary FAIL tasks remain major limitations. Step 11 addresses reproducibility and robustness.

## Other archived evidence

- [Detailed 115-run raw-audit evidence](2026-11-12/sweabs_samples2_3_full_audit_evidence_115.csv) and [original audit report](2026-11-12/sweabs_full_198_audit_report.md).
- [Historical first83 input](2026-11-12/sweabs_samples1_2_first83_cumulative.csv) and [original audit script](2026-11-12/sweabs_full_audit.py).
- [Full file manifest, sizes, SHA-256 checksums and raw-archive access limitations](2026-11-12/MANIFEST.md).

**Private raw data:** Two checksum-verified ZIP archives are backed up in the owner's ChatGPT Library (historical 83 and Sample 2/3 combined). They contain raw logs/test fixtures and **are not publicly hosted here**. The public GitHub files are audit tables, scripts, and reports only.

**Next milestone: Step 11 controlled backend/exact-patch and independent semantic oracle gate** — technical reproduction/spot-check/robustness PASSED, but outstanding human/oracle assessment of disputed enhanced tests and 14 UNVERIFIED remains open. Do not promote provisional broadened-label associations to a verified prediction until independently adjudicated or explicitly constrained as limitations.

For current research state: [PROJECT_STATE.md](../docs/PROJECT_STATE.md) · [WORK_LOG.md](../docs/WORK_LOG.md).
