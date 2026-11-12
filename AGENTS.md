# Instructions for Research and Coding Agents

This repository supports a reproducible academic study of **originally successful Gemini 3 Flash coding-agent patches** re-evaluated against SWE-ABS strengthened tests.

## Read before acting (in this order)

1. [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) — **canonical snapshot, milestone checklist, next action, audit limitations and evidence digests**.
2. [docs/WORK_LOG.md](docs/WORK_LOG.md) — actual prior work and session chronology (newest first).
3. [README.md](README.md) — public research overview; do not confuse it with the operational handoff.
4. [Step 11 reproduction + robustness report](results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md), [successful pinned Python CI](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649), [12-case source recount](results/2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json), [post-hoc robustness JSON](results/2026-11-12/STEP11_EXPLORATORY_ROBUSTNESS_v1.json); then [Frozen Step 8 indicators](docs/STEP8_FROZEN_INDICATORS_v1.md), [Step 9 exact-match coverage/features](results/2026-11-12/STEP9_COVERAGE_v1.json), [Step 10 report](results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md), [corrected Step 10 v2 AUROCs](results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json), then [Step 7 eligibility policy](results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md), [Step 6 FAIL review](results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md), [current v2 and Step 5](results/2026-11-12/STEP5_RECONCILIATION_REPORT.md), and [evidence manifest](results/2026-11-12/MANIFEST.md).
5. [Pilot workflow](.github/workflows/sweabs-pilot.yml), [selection/collection script](scripts/pilot.py), and relevant exact source artifacts when the task involves evaluations.

**Last documented checkpoint:** 2026-11-12. Runner v2 unchanged: **198 originally successful attempts, 153 runner PASS / 31 provisional FAIL / 14 UNVERIFIED** across 73 task IDs. Step 7 primary retains **153 PASS / 9 documentary-review-supported FAIL / 36 excluded** (61 tasks, only 5 positive task IDs). Steps 8–10 frozen features/AUROCs DONE, primary duplicate-command AUROC **0.489** vs broader runner-only **0.708**. **Step 11 TECHNICAL GATES PASS:** full pinned Hugging Face Step 9 extraction, corrected Step 10 AUROC, Step 11 task-aware exploratory robustness, 5 synthetic unit tests and 12 independent original-trace event recounts (**168/168 feature comparisons**) passed in read-only [GitHub Actions #43260088649](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649), Python 3.11.18, `datasets==4.8.5`, `huggingface_hub==1.33.0`. [Report](results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md), [robustness](results/2026-11-12/STEP11_EXPLORATORY_ROBUSTNESS_v1.json), [raw-event recount](results/2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json). **Step 11 IN PROGRESS — independent semantic validity/coverage gate OPEN** (16 unresolved + 2 environment-sensitive FAIL, 4 invalid enhanced tests to interpret, 14 UNVERIFIED). No gold standard semantic oracle, task-disjoint prediction validation or journal-ready claim. Historical Step 10 v1 bootstrap intervals INVALID, use corrected v2. Next: adjudicate/qualify semantic validity in independently versioned evidence, then Step 12 case studies. Preserve source run outcomes, frozen indicator rules and full reproducibility provenance.

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
