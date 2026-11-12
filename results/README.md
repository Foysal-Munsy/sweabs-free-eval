# Research results and audit artifacts

**Current stage:** Strengthened-test collection complete; provisional labels archived; historical audit consistency and semantic FAIL review pending. These files are **not final ground-truth correctness labels**.

## Archived checkpoint — 2026-11-12

Open [2026-11-12/MANIFEST.md](2026-11-12/MANIFEST.md) for checksums, sizes, source provenance, audit limitations, and the privacy boundary around the raw ZIP.

Primary files: [198-row provisional cumulative CSV](2026-11-12/sweabs_full_198_cumulative_audited.csv), [115-row detailed audit evidence CSV](2026-11-12/sweabs_samples2_3_full_audit_evidence_115.csv), [audit report](2026-11-12/sweabs_full_198_audit_report.md), [historical 83-row input](2026-11-12/sweabs_samples1_2_first83_cumulative.csv), and [historical audit script](2026-11-12/sweabs_full_audit.py).

**Observed provisional labels:** 198 evaluated attempts, 153 PASS, 32 FAIL, 13 UNVERIFIED; 73 unique task IDs. Do not treat the 32 FAIL as independently confirmed semantic failures or 13 UNVERIFIED as negative results.

The private 5.1-MB raw evidence ZIP is stored in the owner's ChatGPT Library, not in this GitHub repository. See the manifest. The repository publicly exposes the CSVs, audit report and audit script only.

For current research work and next steps, read [PROJECT_STATE.md](../docs/PROJECT_STATE.md) and [WORK_LOG.md](../docs/WORK_LOG.md).
