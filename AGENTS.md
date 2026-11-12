# Instructions for Research and Coding Agents

This repository supports a reproducible academic study of **originally successful Gemini 3 Flash coding-agent patches** re-evaluated against SWE-ABS strengthened tests.

## Read before acting (in this order)

1. [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) — **canonical snapshot, milestone checklist, next action, audit limitations and evidence digests**.
2. [docs/WORK_LOG.md](docs/WORK_LOG.md) — actual prior work and session chronology (newest first).
3. [README.md](README.md) — public research overview; do not confuse it with the operational handoff.
4. [In-place enhanced assertion and Oracle collection review](results/2026-11-12/STEP11_INPLACE_AND_ORACLE_COLLECTION_REVIEW_v1.md), [Django-14434 original-base method check](results/2026-11-12/STEP11_INPLACE_METHOD_AUDIT_DJANGO14434_v1.json), [Django-15503 declared-but-unobserved method check](results/2026-11-12/STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json), then [Step 11 semantic gate report](results/2026-11-12/STEP11_SEMANTIC_VALIDITY_GATE_v1.md), [45-case source test crosswalk](results/2026-11-12/STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json), [14 original result ZIP audit](results/2026-11-12/STEP11_RAW_ARTIFACT_REAUDIT14_v1.json), [9-case augmented method attribution](results/2026-11-12/STEP11_SKIP_ATTRIBUTION_9_v1.json), then [Step 11 reproduction + robustness report](results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md), [successful pinned Python CI](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649), [12-case source recount](results/2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json), [post-hoc robustness JSON](results/2026-11-12/STEP11_EXPLORATORY_ROBUSTNESS_v1.json); then [Frozen Step 8 indicators](docs/STEP8_FROZEN_INDICATORS_v1.md), [Step 9 exact-match coverage/features](results/2026-11-12/STEP9_COVERAGE_v1.json), [Step 10 report](results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md), [corrected Step 10 v2 AUROCs](results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json), then [Step 7 eligibility policy](results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md), [Step 6 FAIL review](results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md), [current v2 and Step 5](results/2026-11-12/STEP5_RECONCILIATION_REPORT.md), and [evidence manifest](results/2026-11-12/MANIFEST.md).
5. [Pilot workflow](.github/workflows/sweabs-pilot.yml), [selection/collection script](scripts/pilot.py), and relevant exact source artifacts when the task involves evaluations.

**Last documented checkpoint:** 2026-11-12. Original runner v2 **153 PASS / 31 provisional FAIL / 14 UNVERIFIED**, 198 exact originally successful agent patches across 73 tasks; frozen Step 7 conservative screen **153/9/36**, Step 8 indicators unchanged. Step 9 pinned extraction, Step 10 AUROC and Step 11 technical/12-trace checks PASS. Step 11 semantic source/ZIP/method audits: 45 pinned agent/test case pairs (CI #43262365929), 14 original ZIPs SHA verified (CI #43263048387), 9 newly added method-to-log checks (CI #43264326911). **NEW: `django-14434` 1 new test method passed, but 9 existing methods contained enhanced inserted assertions; 8 passed, `test_func_unique_constraint_covering` SKIPPED in all three samples** due unsupported `supports_expression_indexes` and `supports_covering_indexes` (original-base [10-hunk/3-run audit](results/2026-11-12/STEP11_INPLACE_METHOD_AUDIT_DJANGO14434_v1.json), [CI #43267304895](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43267304895)). **`django-15503` newly declared Oracle-named method is absent from all three original verbose logs**; no cause/semantic verdict established ([source/archived-log check](results/2026-11-12/STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json)). One intermediate GitHub Actions #43268071356 FAILED due **HTTP 503 artifact-storage egress**, not an original agent failure. Read-only Step 11 workflow now defaults to archived SHA-verified ZIP metadata and repeat raw ZIP downloads are manual opt-in; [new workflow CI #43268574096 SUCCESS](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268574096). See [full Step 11 in-place/collection report](results/2026-11-12/STEP11_INPLACE_AND_ORACLE_COLLECTION_REVIEW_v1.md) and [updated semantic gate](results/2026-11-12/STEP11_SEMANTIC_VALIDITY_GATE_v1.md). **Step 11 still IN PROGRESS**: needs controlled compatible-backend/exact-agent-patch tests and independent human/maintainer semantic oracles. Never silently relabel, post-hoc select indicators or claim a validated predictor. Steps 12–14 TODO.

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
