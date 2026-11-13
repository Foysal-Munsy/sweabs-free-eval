# Study Methodology

This page summarizes the archived experimental design. The original frozen feature definition and analysis data have not been redefined for repository presentation.

## Question and population

The research asks whether simple original-trajectory process indicators distinguish among coding-agent runs that already passed the standard SWE-bench Verified evaluation and were subsequently executed against stronger SWE-ABS tests.

Source: [pinned Gemini 3 Flash trajectories](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories/tree/b5515d1dce40036633293b70477f0633b24593f7), train split. The recorded upstream dataset contains 296 rows; **198 originally resolved runs** (63/68/67 across three source samples) were evaluated, spanning **73 distinct task IDs**. The unit of provenance is **(sample, instance_id, SHA-256 of exact UTF-8 submitted patch)**. The feature extractor rejects patch identity mismatches. See [source-match coverage](../results/2026-11-12/STEP9_COVERAGE_v1.json).

## Strengthened tests and runner outcomes

The evaluated augmented-test source is [OpenAgentLab/SWE-Bench_Verified_ABS](https://huggingface.co/datasets/OpenAgentLab/SWE-Bench_Verified_ABS) at project-pinned revision `79fc07a8f4ce5e3720e069948073f5f910b7577b`. GitHub Actions supplied Docker-capable execution, with per-patch runner results independently audited; a green GitHub workflow alone is not evidence a patch passed.

The immutable cumulative run-v2 record reports **153 PASS, 31 provisional FAIL and 14 UNVERIFIED**. Documentary inspection of 31 FAILs found **9 issue-aligned, 4 invalid-test, 2 environment-sensitive and 16 unresolved**. The reviewer categories are not independently expert-adjudicated semantic correctness labels. Original UNVERIFIED cases remain unchanged despite separately versioned supported-backend and patch-preserving probes. Sources: [original runner table](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv), [31-case documentary review](../results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md), [scope-limited validity decision](../results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md).

## Four frozen indicators

From chronological original assistant tool calls and explicitly matched tool replies:

1. **Duplicate terminal-command rate:** count of terminal calls whose whitespace-normalized command has appeared earlier, divided by max(1, terminal calls).
2. **Explicit terminal-error rate:** count of uniquely matched terminal replies with an explicit nonzero exit/error flag, divided by max(1, terminal calls).
3. **No recognized verification:** negative of the binary flag for at least one regex-recognized `pytest`, `unittest`, `runtests.py`, `tox`, `nosetests` or supported module test command.
4. **Editor-after-verification:** number of file-editor calls strictly after the final recognized verification command, **missing** where no recognized verification exists.

Indicators were frozen before all-run feature extraction and feature–label association inspection, but the entire project was **not** prospectively preregistered before any stronger-test outcomes had been observed. These features are observable proxies, not judgments about intent or test adequacy. The complete operational definitions and missingness policy are in the [original specification](STEP8_FROZEN_INDICATORS_v1.md); implementation in [Step 9 extractor](../scripts/step9_extract_trajectory_features.py).

## Outcome eligibility and association analysis

| Label-policy target | PASS (0) | Provisional FAIL (1) | Excluded |
| --- | ---: | ---: | ---: |
| Conservative primary | 153 | 9 | 36 |
| Noninvalid runner FAIL sensitivity | 153 | 27 | 18 |
| All runner FAIL sensitivity | 153 | 31 | 14 |
| Hypothetical skipped-as-PASS scenario | 162 | 9 | 27 |

The conservative primary has **162 eligible runs, 61 tasks, five positive task IDs**. For each indicator and policy the study reports oriented univariate AUROC in the frozen direction; no learned composite classifier, threshold fitting or post-hoc score reorientation is claimed. **500 task-ID-cluster bootstrap draws** (seed `20261112`) retain all repeated samples of each selected task; the primary draws yield 496 valid two-class resamples. The [corrected v2 analysis](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) replaces an archived implementation bug in v1. Post-hoc task-macro, within-project, length and leave-one-positive-task-out checks are explicitly exploratory. See [quantitative report](../results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md) and [exploratory robustness](../results/2026-11-12/STEP11_EXPLORATORY_ROBUSTNESS_v1.json).

## Qualitative cases and inference limits

Eight source-matched, deterministically selected illustrative cases use a [selection protocol](STEP12_CASE_SELECTION_PROTOCOL_v1.md) committed before individual case inspection; all are rechecked against exact patch hashes. The [eight-case report](../results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md) and [112-field independent raw-source recount](../results/2026-11-13/STEP12_SOURCE_RECOUNT_8_v1.json) are descriptive, not external predictive validation.

Observed associations may depend on outcome validity, task difficulty, repository, selected PASS-only cohort, model and environment. The study has no independent human semantic gold oracle, task-disjoint predictor evaluation, or cross-agent replication. Interpreting the estimates as verified semantic defect prediction would overstate the evidence.
