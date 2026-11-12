# Research results and audit artifacts

**Current stage (2026-11-12):** 198 strengthened-test attempts completed, raw-log audits completed for both the earlier 83 and later 115 records. **Current provisional v2 labels: 153 PASS, 31 FAIL, 14 UNVERIFIED**. Strengthened-test assertion soundness still requires independent review; these labels are not final semantic-correctness ground truth.

## Current version: Step 5, 83-run reconciliation

- [Current 198-row cumulative provisional CSV (v2)](2026-11-12/sweabs_full_198_cumulative_v2.csv)
- [Step 5 detailed 83-row historical re-audit evidence](2026-11-12/sweabs_historical_83_reaudit_evidence.csv)
- [Step 5 one-row correction ledger](2026-11-12/sweabs_historical_83_corrections.csv)
- [Step 5 report — correction justification and limitations](2026-11-12/STEP5_RECONCILIATION_REPORT.md)
- [Re-audit reproduction script](../scripts/reaudit_historical_83.py)

**Version control:** [v1 (198 runs)](2026-11-12/sweabs_full_198_cumulative_audited.csv) recorded 153 PASS, 32 FAIL, 13 UNVERIFIED. v2 corrects **Sample 1 offset 58: FAIL → UNVERIFIED** due to overlapping agent-modified/augmented test files. **Original v1 is preserved unchanged**. No other v1 rows were changed.

## Other archived evidence

- [Detailed 115-run raw-audit evidence](2026-11-12/sweabs_samples2_3_full_audit_evidence_115.csv) and [original audit report](2026-11-12/sweabs_full_198_audit_report.md).
- [Historical first83 input](2026-11-12/sweabs_samples1_2_first83_cumulative.csv) and [original audit script](2026-11-12/sweabs_full_audit.py).
- [Full file manifest, sizes, SHA-256 checksums and raw-archive access limitations](2026-11-12/MANIFEST.md).

**Private raw data:** Two checksum-verified ZIP archives are backed up in the owner's ChatGPT Library (historical 83 and Sample 2/3 combined). They contain raw logs/test fixtures and **are not publicly hosted here**. The public GitHub files are audit tables, scripts, and reports only.

**Next milestone:** Step 6 — independently review 31 provisional FAIL outcomes for augmented-test validity; then triage 14 UNVERIFIED and freeze an analysis-ready version. Statistical/trajectory feature work has **not** started.

For current research state: [PROJECT_STATE.md](../docs/PROJECT_STATE.md) · [WORK_LOG.md](../docs/WORK_LOG.md).
