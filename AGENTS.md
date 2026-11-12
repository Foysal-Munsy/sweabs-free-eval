# Instructions for Research and Coding Agents

This repository supports a reproducible academic study of **originally successful Gemini 3 Flash coding-agent patches** re-evaluated against SWE-ABS strengthened tests.

## Read before acting (in this order)

1. [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) — **canonical snapshot, milestone checklist, next action, audit limitations and evidence digests**.
2. [docs/WORK_LOG.md](docs/WORK_LOG.md) — actual prior work and session chronology (newest first).
3. [README.md](README.md) — public research overview; do not confuse it with the operational handoff.
4. [Frozen Step 8 indicators](docs/STEP8_FROZEN_INDICATORS_v1.md), [Step 9 exact-match coverage/features](results/2026-11-12/STEP9_COVERAGE_v1.json), [Step 10 report](results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md), [corrected Step 10 v2 AUROCs](results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json), then [Step 7 eligibility policy](results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md), [Step 6 FAIL review](results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md), [current v2 and Step 5](results/2026-11-12/STEP5_RECONCILIATION_REPORT.md), and [evidence manifest](results/2026-11-12/MANIFEST.md).
5. [Pilot workflow](.github/workflows/sweabs-pilot.yml), [selection/collection script](scripts/pilot.py), and relevant exact source artifacts when the task involves evaluations.

**Last documented checkpoint:** 2026-11-12. Original evaluation v2 unchanged: **198 attempted, 153 PASS / 31 provisional FAIL / 14 UNVERIFIED** across 73 tasks. Steps 6–7 documentary validity and analysis eligibility documented (primary **153/9/36**). **Step 8 DONE:** versioned feature specification and extractor committed before feature extraction. **Step 9 DONE:** 198/198 originally successful trajectories match exact sample/instance/patch SHA at pinned dataset revision among 296 source rows; 73 distinct task IDs, 191 recognized verification-command runs; [features](results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv). **Step 10 DONE for preliminary univariate association:** primary duplicate-command AUROC **0.489** (task-cluster interval **0.270–0.706**); runner-only sensitivity **0.708** (**0.562–0.834**). These conflict under label policy; only **5 positive task IDs** in primary, not a validated predictor. The initial [Step 10 v1 JSON](results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v1.json) has INVALID bootstrap intervals due to low-bit PRNG modulo; use [corrected v2](results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json). Independent execution of the checked-in Python `--check` commands remains **UNVERIFIED**. **NEXT: Step 11 independent reproduction, task-aware robustness, feature checks and semantic oracle/coverage followup.** Cross-check newest repo files and do not silently change frozen signals or source labels.

## Research safety and evidence rules

- Keep `(sample, instance_id, patch_sha256)` as exact run identity. Some tasks repeat across samples.
- Distinguish *workflow success*, *observed augmented-runner PASS/FAIL*, and *independent test semantic correctness*. They are not interchangeable.
- UNVERIFIED is not FAIL. No old verdict, patch, or dataset revision may be silently relabeled or replaced. **Step 6 semantic review statuses are separate from raw runner outcomes** and never imply that a discarded failure is an agent PASS.
- Do not tune trajectory messiness indicators to observed outcomes; Step 8 indicator specification must be versioned/frozen before feature extraction or association analysis.
- Preserve all raw logs and provenance. Any rerun must retain the previous result and explain what changed.
- Base every factual research claim on verified files, GitHub Actions runs, dataset revisions, papers, or logs. Mark missing support **unverified**; do not invent citations or numerical claims.
- Do not alter the push-trigger manifests `.github/sweabs-sample2-batch.json` and `.github/sweabs-sample3-batch.json` without intentionally launching an evaluation.
- This repository is public. Do not commit secrets, credentials, personal data, or unreviewed private traces.

## After every substantive change

1. Update [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) to reflect verified current status, blockers, and next action.
2. Append a factual, source-linked entry to [docs/WORK_LOG.md](docs/WORK_LOG.md) (newest first).
3. Reconcile the public [README.md](README.md) when project progress, method, or results change.
4. Fetch/read back GitHub content to verify writes. Do not claim archival or completion based only on a tool invocation.
5. Finish with a short handoff: **what was done; what is still unverified; exact next step; links**.

These instructions are for agents working in the repository. A chat assistant must still be given access to the repo and instructed to read these files; the repo does not grant a background autonomous research process.
