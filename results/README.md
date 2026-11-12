# Research results and audit artifacts

**Current stage (2026-11-12):** 198 stronger-test attempts and 83+115 raw audits complete; original v2 **153 PASS / 31 FAIL / 14 UNVERIFIED** unchanged. Step 8 versioned frozen indicators, Step 9 exact-match features (198/198) and Step 10 provisional task-aware univariate AUROCs are archived. These are not independently adjudicated semantic labels, a trained classifier or a generalization claim. **Step 11 reproduction and robustness NEXT.**

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

**Next milestone: Step 11** — independently reproduce pinned extraction and task-bootstrap results; audit a trace subset, task/project confounding and label-policy sensitivity; pursue outstanding human/oracle and controlled rerun validity work before claiming reliability prediction.

For current research state: [PROJECT_STATE.md](../docs/PROJECT_STATE.md) · [WORK_LOG.md](../docs/WORK_LOG.md).
