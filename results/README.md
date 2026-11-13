# Experimental Results and Audit Artifacts

This directory contains the archived evidence for the study of originally successful Gemini 3 Flash coding-agent trajectories under SWE-ABS strengthened tests. The original frozen data and versioned audits are retained; runner labels are not independent semantic ground truth.

## Main evidence

| Artifact | Description |
| --- | --- |
| [198-run cumulative v2](2026-11-12/sweabs_full_198_cumulative_v2.csv) | Original **153 PASS / 31 provisional FAIL / 14 UNVERIFIED** runner statuses |
| [Historical evidence manifest](2026-11-12/MANIFEST.md) | Recorded evaluations, audit coverage and original execution evidence |
| [Step 6 validity review](2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md) | Issue/test documentary review of all 31 FAILs: 9 issue-aligned, 4 invalid-test, 2 environment-sensitive, 16 unresolved |
| [Step 7 label policy](2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md) | Conservative 153 PASS / 9 documentary-supported FAIL / 36 excluded and alternative screens |
| [Step 9 exact features](2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv) | Four frozen process proxies for 198 exact patch identities |
| [Step 10 corrected task-cluster results](2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) | Feature AUROCs, corrected bootstrap intervals and sensitivity policies |
| [Step 10 report](2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md) | Descriptive quantitative interpretation, sample-size and label limitations |
| [Step 11 reproduction](2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md) | Independent software checks, task-cluster robustness and provenance |
| [Step 11 scientific scope decision](2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md) | Explicit limits on semantic correctness and generalization claims |
| [Step 12 qualitative cases](2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md) | Eight deterministic illustrative cases and counterexamples |
| [Step 12 independent recount](2026-11-13/STEP12_SOURCE_RECOUNT_8_v1.json) | Eight pinned source runs; 112 audited feature comparisons, zero mismatches |

Additional dated files document raw-evidence reconciliation, supported-backend probes, patch-preservation investigations and retrospective technical audit steps. Historical intermediate v1 artifacts remain available for provenance; **Step 10 v2** is the corrected primary quantitative result.

For scientific context see [Methodology](../docs/METHODOLOGY.md) and [Reproducibility](../docs/REPRODUCIBILITY.md). The original `UNVERIFIED` runner outcomes have not been silently changed after later controlled checks.
