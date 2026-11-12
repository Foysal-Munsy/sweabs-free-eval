# Instructions for Research and Coding Agents

This repository supports a reproducible academic study of **originally successful Gemini 3 Flash coding-agent patches** re-evaluated against SWE-ABS strengthened tests.

## Read before acting (in this order)

1. [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) — **canonical snapshot, milestone checklist, next action, audit limitations and evidence digests**.
2. [docs/WORK_LOG.md](docs/WORK_LOG.md) — actual prior work and session chronology (newest first).
3. [README.md](README.md) — public research overview; do not confuse it with the operational handoff.
4. [Step 6 full FAIL test-validity review](results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md), [31-row review ledger](results/2026-11-12/STEP6_FAIL_REVIEW_31.csv), and [current v2 results and Step 5 reconciliation](results/2026-11-12/STEP5_RECONCILIATION_REPORT.md), then [archived evidence and SHA-256 manifest](results/2026-11-12/MANIFEST.md) — verified public files and private raw-evidence boundary.
5. [Pilot workflow](.github/workflows/sweabs-pilot.yml), [selection/collection script](scripts/pilot.py), and relevant exact source artifacts when the task involves evaluations.

**Last documented checkpoint:** 2026-11-12. All **198** strengthened-test attempts completed. Raw per-patch logs have been audited in two stages (115 recent and 83 historical); [current v2](results/2026-11-12/sweabs_full_198_cumulative_v2.csv) reports **153 provisional PASS, 31 provisional FAIL, 14 UNVERIFIED** (73 distinct task IDs). Step 5 corrected one old FAIL to UNVERIFIED due to an agent-modified test file reset; original v1 was preserved. GitHub contains audit tables, reports, manifests, scripts; raw evidence is privately preserved in two ZIP archives. **Step 6 AI-assisted FAIL-test documentary review is DONE (not final human/oracle validation)**: the same 31 FAILs have 9 review-supported, 4 invalid-test, 2 environment-sensitive, and 16 unresolved dispositions. The **NEXT milestone is Step 7: triage 14 UNVERIFIED and freeze explicit analysis eligibility/exclusion/sensitivity labels** before trajectory feature extraction. Cross-check the latest repository evidence before treating this snapshot as live. Cross-check current repository/evidence rather than assuming this snapshot is still current.

## Research safety and evidence rules

- Keep `(sample, instance_id, patch_sha256)` as exact run identity. Some tasks repeat across samples.
- Distinguish *workflow success*, *observed augmented-runner PASS/FAIL*, and *independent test semantic correctness*. They are not interchangeable.
- UNVERIFIED is not FAIL. No old verdict, patch, or dataset revision may be silently relabeled or replaced. **Step 6 semantic review statuses are separate from raw runner outcomes** and never imply that a discarded failure is an agent PASS.
- Do not tune trajectory messiness indicators to observed outcomes; freeze definitions before feature analysis.
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
