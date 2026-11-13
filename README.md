# Trajectory Signals Under Strengthened Coding-Agent Evaluation

Reproducible exploratory study of whether lightweight trajectory-process indicators are associated with failure under **SWE-ABS strengthened tests** among coding-agent runs that originally passed standard SWE-bench Verified evaluation.

The study evaluates **runner-observed outcomes**, not independently human-adjudicated semantic defects. No trained or externally validated failure predictor is claimed.

## Research question

> Among coding-agent runs that pass the standard evaluation, do simple original-trajectory indicators help distinguish patches that fail under strengthened tests?

## Study at a glance

| Item | Recorded evidence |
| --- | --- |
| Trajectory source | [Gemini 3 Flash SWE-bench Verified trajectories](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories) (pinned revision in [methods](docs/METHODOLOGY.md)) |
| Selected originally successful runs | **198** across **73** distinct task IDs |
| Original strengthened-test runner outcomes | **153 PASS · 31 provisional FAIL · 14 UNVERIFIED** |
| Primary conservative analysis | **153 PASS · 9 documentary-supported provisional FAIL · 36 excluded** (162 runs, 61 tasks, only **5 positive task IDs**) |
| Trajectory features | Four fixed, transparent process proxies |
| Uncertainty estimation | 500 task-cluster bootstrap resamples; original task IDs remain the clustering unit |

Counts and provenance: [original runner v2](results/2026-11-12/sweabs_full_198_cumulative_v2.csv), [Step 7 label policy](results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md), [Step 9 coverage](results/2026-11-12/STEP9_COVERAGE_v1.json).

## Main findings

| Fixed indicator (higher = presumed messier) | Primary AUROC | 95% task-cluster bootstrap interval |
| --- | ---: | --- |
| Duplicate terminal-command rate | **0.489** | 0.270–0.706 |
| Explicit terminal-error rate | **0.599** | 0.420–0.790 |
| No recognized verification command | **0.480** | 0.459–0.497 |
| Editor calls after final recognized verification | **0.435** | 0.166–0.757 |

Under alternative, less restrictive provisional runner-label policies, duplicate-command AUROC changes to **0.721** (noninvalid sensitivity) or **0.708** (all runner FAILs). The fixed indicator is unchanged; the outcome-policy and eligible run set differ. These comparisons do **not** demonstrate true semantic-defect prediction. Source: [corrected Step 10 results](results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json).

The conservative analysis is inconclusive: the primary interval spans 0.5, and only five task IDs contribute positive evidence. Eight deterministically selected qualitative cases illustrate high-duplication passing runs, low-duplication failures, disputed enhanced assertions, skipped tests, and tested-patch overlap; they are illustrative rather than representative. See [case report](results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md).

## Research materials

| Resource | Contents |
| --- | --- |
| [Paper](paper/) | Editable LaTeX manuscript, bibliography and figure/table source |
| [Methodology](docs/METHODOLOGY.md) | Population, exact patch matching, indicators, label policy and analysis design |
| [Reproducibility](docs/REPRODUCIBILITY.md) | Pinned inputs, checks, computing environment and evidence boundaries |
| [Results](results/) | Archived run outcomes, validity reviews, AUROC JSON and qualitative audit |
| [Code](scripts/) | Evaluation, extraction, statistical analysis and audit scripts |
| [Tests](tests/) | Parser and pipeline unit tests |
| [Workflows](.github/workflows/) | Docker evaluation, source-audit CI and read-only manuscript compilation |

The original frozen [indicator specification](docs/STEP8_FROZEN_INDICATORS_v1.md) and [qualitative selection protocol](docs/STEP12_CASE_SELECTION_PROTOCOL_v1.md) are maintained alongside the scientific evidence.

## Limitations

The 31 original runner FAILs were reviewed against documentary evidence: **9 issue-aligned**, **4 invalid-test**, **2 environment-sensitive**, and **16 unresolved**; these are **not** human gold labels. Fourteen original outcomes remain UNVERIFIED. The conservative analysis has only five distinct positive tasks, repeated runs share tasks, and task difficulty, PASS-only selection, a single agent/model source and incomplete external validation limit generalization. A task-aware confidence interval does not eliminate these threats. The original raw result ZIPs are not all publicly republished, and later controlled test rechecks were not identical historical Docker reruns.

Evidence: [failure-validity review](results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md), [bounded scientific conclusion](results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md), [reproduction audit](results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md).

**Interpretation:** The available real-data evidence supports reproducible, label-sensitive exploratory **runner association**. It does not establish that messy trajectories cause incorrect patches, that no relationship exists in other samples, or that a semantic-defect detector is ready for deployment.
