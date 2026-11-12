# Instructions for Research and Coding Agents

This repository supports a reproducible academic study of **originally successful Gemini 3 Flash coding-agent patches** re-evaluated against SWE-ABS strengthened tests.

## Read before acting (in this order)

1. [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) — **canonical snapshot, milestone checklist, next action, audit limitations and evidence digests**.
2. [docs/WORK_LOG.md](docs/WORK_LOG.md) — actual prior work and session chronology (newest first).
3. [README.md](README.md) — public research overview; do not confuse it with the operational handoff.
4. [Step 7 provisional label policy/14-case triage](results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md), [198-row analysis manifest](results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv), [Step 6 full FAIL validity review](results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md), [current v2 and Step 5 reconciliation](results/2026-11-12/STEP5_RECONCILIATION_REPORT.md), then [archived evidence manifest](results/2026-11-12/MANIFEST.md) — evidence boundaries and policies.
5. [Pilot workflow](.github/workflows/sweabs-pilot.yml), [selection/collection script](scripts/pilot.py), and relevant exact source artifacts when the task involves evaluations.

**Last documented checkpoint:** 2026-11-12. Original evidence unchanged: **198 attempts, 153 v2 provisional PASS, 31 provisional FAIL, 14 UNVERIFIED** (73 distinct task IDs), with 83 historical + 115 recent raw audits. Step 6 review of 31 FAILs: 9 review-supported, 4 invalid-test, 2 environment-sensitive, 16 unresolved. **Step 7 DONE for documentary UNVERIFIED triage and provisional analysis-label policy freeze**: 9 skipped coverage, 4 patch overlaps, 1 large-patch integrity gap; a versioned 198-row manifest has 153 PASS / 9 review-supported FAIL / 36 excluded in its conservative primary screen, plus sensitivity alternatives. Neither final semantic validity nor human oracle proof is established. **NEXT: Step 8 — define and freeze trajectory indicator formulas, parsing rules, missingness and leakage safeguards BEFORE feature extraction or association checks.** Cross-check current repository/evidence before resuming. Raw logs remain private per archive manifest.

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
