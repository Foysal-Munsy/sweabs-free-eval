# Supervisor questions — frozen-data diagnostic extension (23 November 2026)

**Scope:** post-hoc, supplementary calculations using *unchanged* 198-row Step 9 feature CSV, Step 7 frozen label CSV and Step 6 documentary ledger. No strengthened-test executions, new human labels, or changes to original Step 10 results were performed. Calculations were independently implemented here in JavaScript and checked against the archived v2 bootstrap CI; the newly generated artifacts should be independently reviewed before inclusion as scientific results in a manuscript.

## Q1 — Editing after verification
The original frozen [Step 8 specification](../../docs/STEP8_FROZEN_INDICATORS_v1.md) and [Step 9 Python extractor](../../scripts/step9_extract_trajectory_features.py) define `editor_after_last_verification` as the **count of `file_editor` calls strictly after the final regex-recognized verification `terminal` call**. If no recognized test call exists, assign missing; *not zero*. Seven of 198 runs have no recognized verification; six of 162 eligible primary runs are missing this feature, leaving 156 in the relevant primary AUROC.

## Q2 — Binary verification feature / interval diagnostics
The oriented score is `-any_verification` (higher = less recognized checking). In the primary 162-run cohort **all 9 provisional FAIL runs have recognized verification**. Of 153 runner PASS runs, 147 have verification and six do not. Therefore the binary scores yield **1377 positive/negative pairs: 0 favorable rankings, 1323 ties (96.078%), 54 unfavorable rankings**, and exact oriented AUROC **0.480392**. The near-constant/tied score constrains the numerical bootstrap distribution but is *not evidence of high true precision*.

Reproduction of original Python v2 task-cluster LCG (500 resamples, seed 20261112, task-ID groups sampled with replacement, same high-bit index scaling): 496 valid two-class samples, 4 invalid. **95% percentile CI 0.459215–0.496795 matches the frozen JSON**. A separate 10,000-draw xorshift32 task-cluster resampling, seed 7919, yielded 9940 valid, 60 invalid and a similar 95% percentile CI **0.458861–0.496835**. This is an independent implementation and random-stream check, not a guarantee of ideal small-cluster CI coverage. The original earlier **v1 modulo-index bootstrap was buggy** and must not be cited. See [recorded bootstrap values](SUPERVISOR_BOOTSTRAP_500_v1.csv) and [bins/summary](SUPERVISOR_DIAGNOSTICS_v1.json).

- Bin <0.44: original 500 = 0, alternate 10,000 = 2
- Bin 0.44–0.45: original 500 = 5, alternate 10,000 = 45
- Bin 0.45–0.46: original 500 = 10, alternate 10,000 = 261
- Bin 0.46–0.47: original 500 = 46, alternate 10,000 = 1174
- Bin 0.47–0.48: original 500 = 152, alternate 10,000 = 2859
- Bin 0.48–0.49: original 500 = 185, alternate 10,000 = 3720
- Bin 0.49–<0.50: original 500 = 89, alternate 10,000 = 1714
- Bin =0.50: original 500 = 9, alternate 10,000 = 165

## Q3 — Adjudication consistency and borderline-case sensitivity
An actual *across-time intra-rater* consistency/repeat-review estimate cannot be computed: the historical ledger contains one documentary review, not two time-stamped blinded reviews of each case. Among 15 original runner-FAIL task IDs, **14 have identical documentary categories across their recorded run samples**; `django__django-14999` is mixed (one issue-aligned case, two unresolved), because the failing assertions differ. This is **within-task descriptive agreement across distinct cases**, not inter-rater or temporal reliability.

There are **16 original unresolved FAIL runs belonging to eight task IDs**. As a *hypothetical*, do not edit their archival `primary_y`: add two or three such runs as extra eligible positives while keeping the 153 original primary PASS runs and nine original supported provisional positives. Exhaustive possibilities, unchanged oriented duplicate-command score, and recalculated raw in-sample run-level AUROC:

| Hypothetical toggles | Scenarios | Minimum AUROC | Middle scenario AUROC | Maximum AUROC |
|---|---:|---:|---:|---:|
| 2 unresolved **runs** | 120 | 0.478 | 0.556 | 0.582 |
| 3 unresolved **runs** | 560 | 0.497 | 0.577 | 0.617 |
| Entire 2 unresolved **task groups** | 28 | 0.514 | 0.590 | 0.650 |
| Entire 3 unresolved **task groups** | 56 | 0.544 | 0.622 | 0.682 |

The 2–3 **run-level** toggles yield 680 unique combinations. Task-level toggles include every unresolved run within two or three whole task families (84 combinations, adding variable run counts). These are post-hoc **sensitivity bounds**, not evidence that those assertions were valid, and no uncertainty intervals were computed for these hypothetical re-labelings. Full exact-case selections and AUROCs: [scenario CSV](SUPERVISOR_BORDERLINE_TOGGLES_v1.csv). Changes also alter the positive task composition, not only putative label validity.

## Q4 — Multivariate model feasibility
**No fitted multivariate predictor, logistic model, or task-random-intercept model is part of the frozen study**; see [Step 10 script](../../scripts/step10_analyze_frozen_features.py). Primary data contain just 9 positive runs among only five positive tasks, and only *one* eligible task has both PASS and FAIL runs. Four covariates plus random-effects variance/variance components could be unstable; numerical convergence or a fitted coefficient alone would not yield validated predictive performance. If exploring further, predefine a separately versioned exploratory penalized model (e.g. ridge/Firth, explicitly address missing late edits) and use task-disjoint validation with a bigger independent positive-task pool; do not claim stable random-effects coefficients from these data.

## Q5 — Positive-task heterogeneity
Counts below are **positive/negative runs in the *primary* analysis**, not all source samples. Rates and edit counts are range over positive runs only.

| Positive task | Primary FAIL/PASS | Duplicate rate in FAIL | Error rate in FAIL | Post-verification edits in FAIL |
|---|---:|---:|---:|---:|
| `django__django-11999` | 1/2 | 0.143–0.143 | 0.107–0.107 | 0–0 |
| `django__django-14311` | 3/0 | 0.022–0.160 | 0.174–0.348 | 0–1 |
| `django__django-14999` | 1/0 | 0.159–0.159 | 0.273–0.273 | 0–0 |
| `matplotlib__matplotlib-25775` | 1/0 | 0.184–0.184 | 0.286–0.286 | 0–0 |
| `sympy__sympy-15599` | 3/0 | 0.167–0.286 | 0.143–0.238 | 3–9 |

There are five positive tasks, nine positive runs, and only `django__django-11999` has two additional primary PASS samples. **All nine positive runs have at least one regex-recognized verification**. See [per-run task table](SUPERVISOR_POSITIVE_TASK_RUNS_v1.csv) and [machine-readable summary](SUPERVISOR_DIAGNOSTICS_v1.json). These are raw observations, not evidence of general task effects.

## Q6 — Adding initially unsuccessful runs
The [pinned source dataset](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories) reports 296 total trajectories and 198 originally resolved successes, leaving **98 originally unsuccessful source runs**. Their exact original-trajectory features could potentially be extracted from the pinned source. However the frozen SWE-ABS follow-up runner evaluated **only the 198 original successes**. Therefore **numeric changes to the strengthened-test AUROCs cannot be calculated from the existing runner/label table**. An extension needs a new explicit question/estimand: original standard-test success versus failure, or newly generated strengthened-test outcomes on every eligible run, followed by task-matched contrasts. It must preserve the 198-success conditional cohort result unchanged, identify matching original-task pairs, and address confounding and selection. Do not count originally unsuccessful patches as newly observed SWE-ABS failures without running or explicitly redefining the target.

## Q7 — Versioned evidence profiles and independent validation plan
[Evidence profiles (31 rows)](SUPERVISOR_EVIDENCE_PROFILES_v1.csv) are **derived from the original Step 6 documentary ledger**, not new judgments. They include each run's exact identity and patch SHA, raw runner status, augmented-test patch SHA/files, upstream PR, failing assertion and output pointer, issue/PR/standard-based rationale, opposing interpretation, execution-integrity boundary and next validation action. The profile has **blank** fields for a *new* human reviewer, date, judgment, and blinded second reviewer; do not pretend those reviews are complete.

Recommended v2 human validation: freeze a written per-assertion rubric; provide each qualified reviewer the original issue, PR, patch, test diff, pinned environment and raw logs **without the trajectory score or old documentary label**; use at least two reviewers; independently classify issue-required defect / unsupported test / environment-confounded / unresolved; measure agreement, adjudicate disagreements without forced labels, archive signed decisions and changed-eligibility policy separately; only then rerun all affected AUROCs as a versioned analysis. Future research or newly required experiments remain conditional on supervisor/venue assessment.

## Scientific limitations
- Original runner PASS, FAIL and UNVERIFIED records are operational, not human semantic gold.
- All sensitivity comparisons here are **post-hoc descriptive**; none establishes effect of *invalid labels alone* because the eligible population changes.
- Positive-task diversity is tiny; an apparently narrow binary-feature CI is not proof of high confidence in the scientific hypothesis.
- Missing human panel decisions, exact old historical Docker-tested-tree equivalence and external model/agent generalization are **unverified**.
- Nothing in this folder retroactively changes original Step 6 review method, Step 7 primary labels, Step 8 indicators or Step 10 corrected point estimates.

## External methodological context (verified sources, 2026)
- Original benchmark SWE-ABS paper: https://proceedings.mlr.press/v306/yu26b.html
- Wang, Pradel and Liu (ICSE 2026), *Are “Solved Issues” in SWE-bench Really Solved Correctly?*: https://conf.researchr.org/details/icse-2026/icse-2026-research-track/59/Are-Solved-Issues-in-SWE-bench-Really-Solved-Correctly-An-Empirical-Study
- Baltes et al., published online 2026, empirical LLM-SE human-validation guidelines: https://link.springer.com/article/10.1007/s10664-026-10922-3
- Sparse logistic estimation/separation methodological reference: https://academic.oup.com/aje/article/187/4/864/4084405
