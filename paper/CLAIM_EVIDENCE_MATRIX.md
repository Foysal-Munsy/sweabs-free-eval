# Manuscript draft v0.1 claim/evidence matrix — 13 November 2026

| Claim | Source | Status |
|---|---|---|
| 198 originally successful runs / 73 task IDs / 296 source dataset rows | [Step 9 coverage](../results/2026-11-12/STEP9_COVERAGE_v1.json); [Step 11 independent reproduction](../results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md) | Exact source identity checked; not randomly representative |
| 153 PASS / 31 provisional FAIL / 14 UNVERIFIED | [Original v2 audit](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv) | Runner-only statuses, not gold semantics |
| 9/4/2/16 Step 6 documentary FAIL validity categories | [31-row review](../results/2026-11-12/STEP6_FAIL_REVIEW_31.csv) | AI-assisted documentary; no independent expert oracle |
| 4 frozen individual indicators and exact formula/code | [Step 8](../docs/STEP8_FROZEN_INDICATORS_v1.md); [Step 9 implementation](../scripts/step9_extract_trajectory_features.py) | Frozen before full-run feature–outcome analysis, not a prospective full preregistration |
| Primary 153/9/36, 61 tasks, 5 positive tasks | [Step 7 label manifest](../results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv) | Positive tasks not 9 independent positive observations |
| Primary AUROCs/CIs and four-target sensitivity table | [Corrected Step 10 v2](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) | 500 task-cluster draws; 496 eligible primary bootstrap draws |
| 8 case studies and independent 112-check raw recount | [Step 12 cases](../results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md); [recount ledger](../results/2026-11-13/STEP12_SOURCE_RECOUNT_8_v1.json); [successful CI](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43440488895) | Illustrations, not prospective accuracy or independent semantic review |
| New PostgreSQL and patch-preserving probes cannot rewrite historical outcomes | [Step 11 bounded closure](../results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md) | Controlled runtime is not original Docker replay |
| SWE-bench / SWE-ABS / AgentLens / TraceProbe / LLM-SE guidelines bibliography | Verified primary proceedings and preprint/publisher URLs in \`references.bib\` | Initial source audit; fuller novelty survey pending |
| Synthetic 80-run AUROC .663 and odds ratio 2.18 | September historical draft | Not current empirical results |
| Human semantic ground truth; external prediction; Q1 readiness | None | **UNVERIFIED / NOT ESTABLISHED** |
