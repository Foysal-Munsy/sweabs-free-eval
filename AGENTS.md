# Instructions for Research and Coding Agents

This repository supports a reproducible academic study of **originally successful Gemini 3 Flash coding-agent patches** re-evaluated against SWE-ABS strengthened tests.

## Read before acting (in this order)

1. [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) — **canonical snapshot, milestone checklist, next action, audit limitations and evidence digests**.
2. [docs/WORK_LOG.md](docs/WORK_LOG.md) — actual prior work and session chronology (newest first).
3. [README.md](README.md) — public research overview; do not confuse it with the operational handoff.
4. [Archived evidence and SHA-256 manifest](results/2026-11-12/MANIFEST.md) — verified public files and private raw-evidence boundary.
5. [Pilot workflow](.github/workflows/sweabs-pilot.yml), [selection/collection script](scripts/pilot.py), and relevant exact source artifacts when the task involves evaluations.

**Last documented checkpoint:** 2026-11-12. All **198** strengthened-test evaluation attempts completed, with provisional **153 PASS, 32 FAIL, 13 UNVERIFIED** labels. The recent audit checked 115 raw per-patch artifacts and preserved the earlier 83 rows. **Evidence preservation is now completed with byte-verified GitHub CSV/report/script files and a private raw-ZIP backup. The next unfinished milestone is historical 83-row audit reconciliation (Step 5)**, not feature extraction. Cross-check current repository/evidence rather than assuming this snapshot is still current.

## Research safety and evidence rules

- Keep `(sample, instance_id, patch_sha256)` as exact run identity. Some tasks repeat across samples.
- Distinguish *workflow success*, *observed augmented-runner PASS/FAIL*, and *independent test semantic correctness*. They are not interchangeable.
- UNVERIFIED is not FAIL. No old verdict, patch, or dataset revision may be silently relabeled or replaced.
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
