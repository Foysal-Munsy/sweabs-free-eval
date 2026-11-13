# Step 12 — Eight prespecified qualitative illustrations and counterexamples (v1)

**Date:** 2026-11-13 (Asia/Dhaka). **Research scope:** original SWE-ABS **runner-association**, not human-validated semantic defect prediction. **Selection rule frozen before case inspection:** [Step 12 protocol](../../docs/STEP12_CASE_SELECTION_PROTOCOL_v1.md), commit [`dd2be953`](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/dd2be9537095c81d47ae6eb4a71cb2caa7ff9b94). **Machine-readable identity roster:** [eight exact patches](STEP12_CASE_ROSTER_v1.json). **Independent eight-trace evidence:** [112-check audit](STEP12_SOURCE_RECOUNT_8_v1.json). **Reproduction script:** [Step 12 case audit](../../scripts/step12_cases.py), [read-only source-recount workflow](../../.github/workflows/step12-qualitative-audit.yml), [CI run #43440488895](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43440488895).

## Research boundary and how cases were selected

This is not a sample of independent successes/failures: all eight are intentionally selected as **extremes or validity/coverage counterexamples** from 198 originally successful Gemini 3 Flash runs. The **exact** run key is `(sample, instance_id, patch_sha256)`; eight distinct task IDs were required. Only the already frozen Step 8 `duplicate_terminal_rate = duplicate_terminal_commands / max(1,terminal_calls)` was used to rank the four primary cases. The remaining four were selected by fixed Step 6/7 documentary categories and ascending exact identity, without choosing favorable stories. No post-hoc indicator, cutoff, evaluation label, or analysis target is introduced. The ranked cases can illustrate non-monotonic examples but cannot estimate accuracy or generalization.

Original [runner v2](../2026-11-12/sweabs_full_198_cumulative_v2.csv): **153 PASS / 31 provisional FAIL / 14 UNVERIFIED**. Conservative [Step 7 primary](../2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv): **153 PASS / 9 documentary-supported FAIL / 36 excluded** (162 runs / 61 tasks / **five** distinct positive tasks). [Step 10 corrected task-bootstrap](../2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json): duplicate-terminal rate primary AUROC **0.489** (95% task-cluster interval **0.270–0.706**), vs **0.708** runner-only sensitivity. [Step 11 limited-claim closure](../2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md) rules out treating either as a validated semantic-defect detector.

**Event provenance:** Raw trajectories are fetched only at the frozen [agent dataset revision `b5515d1dce40036633293b70477f0633b24593f7`](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories/tree/b5515d1dce40036633293b70477f0633b24593f7) with patch SHA matching. Source counts derive from [Step 9](../2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv); independent recount is separately tested by the linked Step 12 CI. The [Step 11 historical raw spot-check](../2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json) also covered precisely the selected Django-12039 sample 1 and Django-11206 sample 3 (14 comparison fields each, no discrepancies). **No private trajectory messages, exact command strings, intentions, or unverified step-by-step behavior are reproduced here.** The remaining chronology and why a command was repeated are **unverified**; derived event counts are not a qualitative claim of intentional retries.

## Exact-case findings — observation, alternative, outstanding evidence

### 1. PRIMARY_FAIL_HIGH — SymPy #15599, sample 1 offset 53

**Frozen identity:** `sympy__sympy-15599`; patch SHA-256 `ea1dbe72023645b09c6213b43535323a2c19c19f1bcad12fbfec457e8da2597d`. [Original runner](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43169378297) · [upstream merged PR](https://github.com/sympy/sympy/pull/15599).

- **Observed:** `12 / 42 = 0.285714` duplicate terminal commands; six immediate duplicates, six terminal returns with error flags, two recognized verification commands, four editor calls after last recognized verification. Original runner **FAIL**. Review source reports **17 passed, 2 failed and 3 exceptions** in strengthened Mod tests; documentary Step 6 label `valid_failure` (not gold). [Exact review ledger](../2026-11-12/STEP6_FAIL_REVIEW_31.csv) · [Step 6 issue review](../2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md).
- **Interpretation:** This is a higher-duplication positive illustration. Several failed `Mod` reduction identities are issue-aligned, including `Mod(3*k, 2)` for integer `k`.
- **Opposing view:** Some other augmented symbolic Mod rearrangement assertions may overconstrain general algebra; count of repeated commands does not establish the cause of the exception or agent correctness.
- **Unverified:** Maintainer adjudication of every failing assertion, exact causal link between repeated commands and the downstream failures, and external replication.

### 2. PRIMARY_FAIL_LOW — Django #14311, sample 2 offset 28

**Frozen identity:** `django__django-14311`; patch SHA-256 `f667c7687a13b7f6c378c09c26d8f260b3c9c0988e0d03edac97735d5ec5515b`. [Original runner](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181184322) · [upstream merged PR](https://github.com/django/django/pull/14311).

- **Observed:** Only `1 / 46 = 0.021739` duplicate terminal commands, but **16 terminal error returns** and **13 verification commands** under frozen parsing. Original runner **FAIL**, 5 of 7 augmented tests passed and 2 failed; documentary `valid_failure`. [Step 9 features](../2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv) · [Step 6](../2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md).
- **Interpretation:** A low duplicate-command score coexists with a review-supported FAIL: clear counterexample to treating that *single* indicator as a necessary signature of runner failure.
- **Opposing view:** The large terminal-error count might carry process information that duplicate rate misses; one `__main__` augmented case uses a potentially unrealistic mock spec, although the `python -m singlemodule` restart case is more directly issue-aligned.
- **Unverified:** Independent execution of real `python -m` autoreload behavior and why the trajectory produced those errors.

### 3. PRIMARY_PASS_HIGH — Django #13820, sample 1 offset 25

**Frozen identity:** `django__django-13820`; patch SHA-256 `210dd33a31251bffa604484405e2186908f3aa355a66b27ea45c9ac3a6da94c6`. [Original runner](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/42864097323).

- **Observed:** `10 / 25 = 0.400000` duplicate commands, **all ten immediately repeated**, eight terminal error returns, four verification commands, one post-verification editor call; original **PASS**, **4/4 targeted strengthened tests passed** with no skip reported in [runner v2](../2026-11-12/sweabs_full_198_cumulative_v2.csv).
- **Interpretation:** A visibly high process duplication score can coexist with observed runner PASS. This is a false-alarm illustration under a simplistic high-duplication heuristic, **not** proof that the agent patch is semantically faultless.
- **Opposing view:** Repetitions could be reasonable repeated checks during development or environment issues; four executed tests cannot validate all relevant behaviors.
- **Unverified:** Which commands repeated, agent intentions, comprehensive issue semantics and independent human review of PASS quality.

### 4. PRIMARY_PASS_LOW — Django #11333, sample 3 offset 8

**Frozen identity:** `django__django-11333`; patch SHA-256 `b94e7c5db0640b70b164821dda8d1490cb6f2046d250444b545d27b1149524c5`. [Original runner](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182603318).

- **Observed:** `0 / 19 = 0` duplicate commands and zero immediate duplicates; two explicit terminal error returns, two verification commands and two post-verification editor calls. Original **PASS**, **8/8 targeted tests passed, zero skipped**. [Frozen features](../2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv) · [runner v2](../2026-11-12/sweabs_full_198_cumulative_v2.csv).
- **Interpretation:** Low duplication is compatible with runner PASS, but **zero duplication does not mean an error-free trajectory**.
- **Opposing view:** Both terminal errors and post-verification edits may be expected when debugging; without chronology/content they cannot be adjudicated as unreliable behavior.
- **Unverified:** Full issue-level semantic completeness and whether any recognized verification actually exercised the final edited state.

### 5. INVALID_TEST_CHALLENGE — Django #11848, sample 1 offset 8

**Frozen identity:** `django__django-11848`; patch SHA-256 `c9669210346bd110928fda85d34aebdef01129f7a383d772fb5590e2a1e3f1c3`. [Original runner](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/42853996382) · [upstream PR](https://github.com/django/django/pull/11848) · [RFC 7231 §7.1.1.1](https://www.rfc-editor.org/rfc/rfc7231.html#section-7.1.1.1).

- **Observed:** `5 / 17 = 0.294118` duplicates; 3/4 original augmented tests passed, one failed. Original **runner FAIL**, but **excluded from primary** because the Step 6 documentary review classified its year-wrap expectation `invalid_test`. The test expects RFC850 `00` at July 2099 to mean **2000**; the standard's more-than-50-years-in-the-future rule supports **2100** instead for January 2100. [Step 6 review](../2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md).
- **Interpretation:** Runner-only analysis could count a high-duplication, **test-questionable** run as a positive example and inflate apparent behavioral association.
- **Opposing view:** An augmented author may have intended a fixed historical mapping convention; that convention must be independently justified against the cited standard. Invalidity of **one** augmented assertion is not proof of fully correct agent code.
- **Unverified:** Independent maintainer judgment of Django-specific compatibility requirements and any alternate valid augmented contract.

### 6. ENVIRONMENT_CHALLENGE — Django #15916, sample 2 offset 38

**Frozen identity:** `django__django-15916`; patch SHA-256 `5614f9fd2100c36f6b588bc62c6dd3ef88978472aca1554d7467387406abab05`. [Original runner](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699) · [upstream PR](https://github.com/django/django/pull/15916) · [Python staticmethod documentation](https://docs.python.org/3/library/functions.html#staticmethod).

- **Observed:** `7 / 17 = 0.411765` duplicate commands; five terminal error returns, three verification commands and five post-verification editor calls. Runner **FAIL** with **150/152 tests passed, two exceptions**. Step 6 classifies these two errors `environment_sensitive` and **excludes** them from primary: Python 3.9 does not make raw `staticmethod` objects callable, unlike Python 3.10+, and test callback precedence remains disputed. [Step 6 review](../2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md).
- **Interpretation:** A high-messiness-looking FAIL can reflect a Python-version-dependent test contract; the benchmark target definition, not just behavior, matters.
- **Opposing view:** Enforcing Meta callback precedence even with a noncallable class attribute might still be valid; the failure should not be silently discarded without a clear historical Python contract.
- **Unverified:** Runtime-comparable maintainer-approved test semantics, independent adjudication and whether process duplication relates to the failure.

### 7. SKIPPED_COVERAGE_CHALLENGE — Django #12039, sample 1 offset 10

**Frozen identity:** `django__django-12039`; patch SHA-256 `13c384a48bed11df0ebfeae126594ab1edd5ec67cca9905e4363150875ee2f60`. [Original runner](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/42859974651) · [new PostgreSQL execution](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43273619675).

- **Observed:** `2 / 24 = 0.083333` duplicates; six terminal errors, four verification commands and no post-verification editor calls. The original strengthened runner reported **9 passed, 4 skipped**, so **UNVERIFIED** under the frozen exact-run policy. **New** source-pinned PostgreSQL run later executed **13/13 added index tests successfully with zero skips** for this exact patch; the controlled result did **not** relabel the original. [Step 11 evidence freeze](../2026-11-12/STEP11_CONTROLLED_EVIDENCE_FREEZE_v1.json).
- **Interpretation:** A partial original runner result should not automatically become PASS; later supported-backend checks strengthen coverage evidence, not historical Docker equivalence.
- **Opposing view:** For analyses whose target is *any observed exercised assertion failing*, the earlier 9/9 executed subset could be counted as PASS. That is a **different outcome policy**, not a correction under the original conservative target.
- **Unverified:** Exact equivalence of original Docker-tested tree to the new PostgreSQL environment and semantic sufficiency of all augmented assertions.

### 8. PATCH_OVERLAP_CHALLENGE — Django #11206, sample 3 offset 7

**Frozen identity:** `django__django-11206`; patch SHA-256 `2b74b39168d3927e80ecce18cc14f3a5b869c56bfc2ffb5643af427693cc65a7`. [Original runner](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182603318) · [preserved merge CI](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43272706376) · [new serial Django CI](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43275841934).

- **Observed:** `5 / 25 = 0.200000` duplicates; four error returns and five verification commands. The original runner observed **7 passes and 5 failures**, but its test-file reset erased an agent-modified file, so **original v2 outcome remains UNVERIFIED**. A new non-destructive 3-way merge preserved the exact patch and executed **12 tests with 5 signed-zero assertion failures**. [Original audit v2](../2026-11-12/sweabs_full_198_cumulative_v2.csv) · [controlled freeze](../2026-11-12/STEP11_CONTROLLED_EVIDENCE_FREEZE_v1.json).
- **Interpretation:** Reproduced runtime failure on a correctly preserved patch distinguishes test failure from earlier overwrite, but does **not** independently prove that the issue requires removal of the minus sign on rounded negative zero.
- **Opposing view:** The upstream fix coerces tiny numbers to positive zero, making the new expectation implementation-consistent; yet the original issue concerned avoiding scientific notation, so signed-zero normalization might be an extra constraint. [Step 6 review](../2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md).
- **Unverified:** Human adjudication of signed-zero requirements and historical official-run exact patch preservation; no retrospective primary relabel.

## Cross-case interpretation and nonclaims

1. The prespecified extremes provide **both directions of contradiction** for duplicate-command rate: a **0.400 PASS** versus a **0.021739 FAIL**, alongside a **0.285714 FAIL** and **0.000000 PASS**. These are *illustrative observed combinations*, not confidence intervals, correlations, human assessments of agent reliability, or evidence of a causal mechanism.
2. Different indicators disagree **within the same exact run**: the low-duplication Django-14311 FAIL has 16 observed terminal-error returns; the zero-duplication Django-11333 PASS has two. No selection rule was adjusted to improve another feature's story; frozen Step 8 univariate analyses already account for all four indicators.
3. Two original runner FAILs in the challenge slots were excluded from primary because of **invalid augmented test** and **environment-sensitive** semantics; two other results remain **UNVERIFIED** despite stronger follow-up controlled evidence. The original experimental statuses are deliberately not collapsed.
4. Django and SymPy examples are not independent evidence of general behavior across projects or tasks. Only **five distinct positive task IDs** survive the conservative primary target, so narrative examples cannot resolve weak statistical power or adjudication uncertainty.
5. **Opposing interpretation of the overall study:** An evaluator specifically interested in exact *runner* outcomes may prefer the 31-FAIL sensitivity and AUROC 0.708. An evaluator interested in *actual task correctness* should demand sound augmented assertions and separate human/adjudicated ground truth. Both interpretations have defensible, distinct targets; they must not be combined into one performance claim.

**Defensible Step 12 finding:** These fixed examples document measurement and label-validity pitfalls behind the exploratory negative/inconclusive conservative association. They do **not** demonstrate a reliable detector, an improvement to existing coding agents, final semantic defects, or external generalization. Independent semantic gold judgments remain **unverified**. The next research milestone is Step 13 manuscript drafting within these explicit claim bounds.

## Audit and reproducibility checklist

- [x] Selection protocol committed *before* observing selected rows: [`dd2be953`](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/dd2be9537095c81d47ae6eb4a71cb2caa7ff9b94).
- [x] Eight fixed slots, eight distinct issue IDs, 198-row identity join; no changes to Step 7 labels or Step 8 feature definitions. [Roster JSON](STEP12_CASE_ROSTER_v1.json).
- [x] Reported both cases supporting and contradicting simple duplicate-process intuition and included specific counterarguments and unverified questions for **all eight**.
- [x] The two previously independent Step 11 raw-trajectory spot checks included selected samples Django-12039 s1 and Django-11206 s3. [Archive](../2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json).
- [x] Eight exact pinned-source trajectories independently recounted: **112 feature comparisons, zero mismatches**. [Successful CI #43440488895](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43440488895) · [archived audit](STEP12_SOURCE_RECOUNT_8_v1.json).
- [x] Research session documentation synchronized with PROJECT_STATE, WORK_LOG, README, AGENTS, and results index; GitHub read-back checks recorded in the work log.

**Data-safety rule:** Full logs and original raw trajectory text remain privately held/source-side. This repository stores identities, aggregate features and reasoned case evidence, not raw conversations or private artifact ZIPs.
