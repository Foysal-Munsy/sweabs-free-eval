# Step 10 — Frozen univariate trajectory analysis (2026-11-12)

**Stage:** quantitative, exploratory/preliminary association analysis complete **for the prespecified Step 7 provisional label screens**; no independent semantic oracle, no causal inference or publication-ready reliability claim. Step 11 robustness/validation remains NEXT.

## Study provenance and freeze

The [Step 8 indicator specification](../../docs/STEP8_FROZEN_INDICATORS_v1.md) and [Step 9 extractor](../../scripts/step9_extract_trajectory_features.py) were committed **before** all-run feature extraction or label association analysis. The [198-row exact-match feature table](STEP9_TRAJECTORY_FEATURES_v1.csv) and [coverage record](STEP9_COVERAGE_v1.json) were committed before Step 10 analysis. Original v2 outcome CSV and the Step 7 eligibility manifest were not altered.

The source Hugging Face trajectory dataset currently identifies revision `b5515d1dce40036633293b70477f0633b24593f7`; the dataset-server viewer returned **296 rows**, of which **198** were originally `resolved=True`. For these 198, **198/198** matched the exact `(sample,instance_id,sha256(patch))` identity in the Step 7 manifest, with zero matched-task hash mismatches and 73 distinct tasks. There were 198/198 parseable terminal-result sets and 191/198 runs with at least one regex-recognized verification command. Seven runs lack such commands, so `editor_after_last_verification` is missing for them. Every analysis excludes per-feature missing rows without substituting zero. The feature definitions are *proxies*, not semantic judgments of actual verification quality or blind retries.

## Prespecified primary outcome and AUROC

**Primary screen:** 153 provisional runner PASS, **9** Step 6 documentary-review-supported FAIL, **36** excluded; **162 agent runs** across **61 distinct tasks**, but only **5 distinct FAIL tasks**. Observations from repeated task IDs are correlated.

All scores are oriented such that a *larger score means more presumed messiness*; `any_verification` is negated. AUROC of 0.5 represents no pairwise discrimination, 1.0 ideal discrimination in the specified direction. The **95% intervals** are 500 resamples of **task-ID clusters**, fixed 20261112 PRNG seed, retaining all runs of any drawn task. These are *bootstrap intervals* under a small and nonrepresentative sample, not proof of scientific significance.

| Frozen individual indicator | AUROC (primary) | 95% task-cluster bootstrap interval | Nonmissing primary runs |
| --- | ---: | --- | ---: |
| Exact duplicate terminal-command rate | **0.489** | 0.270–0.706 | 162 |
| Explicit terminal error rate | **0.599** | 0.420–0.790 | 162 |
| No verification command (negated any-verification) | **0.480** | 0.459–0.497 | 162 |
| Editor calls after last recognized verification | **0.435** | 0.166–0.757 | 156 |

**Fact:** The duplicate-command indicator does not discriminate under the conservative 9-FAIL target (AUROC approximately 0.49), and the only mildly above-chance point estimate is explicit terminal error rate (0.60) with an interval spanning 0.5. **Interpretation:** The primary evidence is *insufficient* to support a reliable messiness-based predictor. Absence of a regex-matching test command is not the same as absence of all verification. **Opposing view:** Because the primary target includes just five FAIL task IDs, lack of observed discrimination could reflect insufficient effective positive-task sample rather than absence of a real relationship.

## Label-policy sensitivity (same frozen features)

| Label target (0 PASS / 1 FAIL / excluded) | Duplicate terminal rate AUROC | Terminal error rate AUROC | No-verification AUROC | Post-verification edits AUROC |
| --- | ---: | ---: | ---: | ---: |
| Primary: 153 / 9 / 36 | **0.489** | 0.599 | 0.480 | 0.435 |
| Noninvalid FAIL: 153 / 27 / 18 | **0.721** | 0.498 | 0.499 | 0.405 |
| All runner FAIL: 153 / 31 / 14 | **0.708** | 0.477 | 0.497 | 0.398 |
| Hypothetical skipped-as-PASS: 162 / 9 / 27 | **0.478** | 0.588 | 0.481 | 0.448 |

The corrected cluster-bootstrap intervals for duplicate-command rate are, respectively: **0.270–0.706**, **0.565–0.857**, **0.562–0.834**, and **0.255–0.686**; see [machine-readable Step 10 results v2](STEP10_AUROC_TASK_CLUSTER_v2.json) for all four features, valid replicate counts, class counts and other intervals.

**Critical result:** Label selection changes the central conclusion. The same exact duplicate-command feature gives AUROC **0.49** for the conservative documentary-supported 9-FAIL primary set but **0.71–0.72** on broader provisional runner FAIL targets. Neither is a validated finding of semantic unreliability. Calling 0.71 a demonstrated predictive signal while ignoring the original test-validity concerns would overclaim; conversely, calling the research gap disproven using only 5 positive task IDs also overclaims. No indicator was chosen, reoriented, redefined or threshold-tuned in response to these numbers.

## Statistical safeguards, known weaknesses and competing explanations

- **Effective sample:** 198 runs are not 198 independent tasks. Only 5 primary FAIL task IDs; 61 unique primary tasks; one task in the primary set has both PASS and FAIL runs. The task-bootstrap has 496/500 valid primary replicates and 500/500 in broader and skipped-as-PASS sensitivity targets. Intervals do not incorporate upstream dataset sampling bias, independent test semantic uncertainty, or label-policy selection.
- **Confounding:** Original coding-task difficulty, project, patch size or agent steps may influence both process behavior and strengthened-test outcome. Univariate AUROC does **not** adjust for those factors. No task-disjoint predictive model has been trained or externally validated. Post-hoc multivariate feature selection would violate this stage's freeze.
- **Measurement:** The terminal error parser recognizes explicit statuses, not every possible hidden failure. A repeated command may be rational verification or environment setup, not blind retry. The test-command regex excludes custom `python script.py` checks; absence is a proxy, not proof of no testing. `editor_after_last_verification` ignores later external checks and has structural missingness.
- **Labels:** Nine review-supported `valid_failure` entries are not independent oracle-confirmed failures. The broader FAIL sets include unresolved/environment-sensitive and, in the runner-only scenario, identified invalid enhanced tests. Nine optimistic skipped-as-PASS values are hypothetical.
- **Inference:** AUROC alone is an in-sample descriptive discrimination statistic. The cluster-bootstrap intervals are conditional on the particular sampled tasks; **no p-values, causal conclusions, classifier performance, calibrated probabilities or generalization estimates are claimed**.

## Reproducibility and a caught inference defect

Step 10 initially generated [v1 preliminary JSON](STEP10_AUROC_TASK_CLUSTER_v1.json) with an LCG `state % cluster_count` draw. For the **64-cluster skipped-as-PASS scenario**, its low-order bits cycled deterministically, producing **degenerate bootstrap intervals**. This implementation defect was detected during validation, after the first result had been archived. The **v1 bootstrap intervals are INVALID and must never be cited**; point-estimate AUROCs were unaffected. The corrected [v2 JSON](STEP10_AUROC_TASK_CLUSTER_v2.json) changes only the cluster-draw mapping to `floor(state * cluster_count / 2^32)`, keeping seed, 500 resamples, task grouping, frozen indicators and all labels unchanged. The [Step 10 Python analysis script](../../scripts/step10_analyze_frozen_features.py) now implements the corrected calculation.

Read-only quantitative outputs were computed from GitHub-fetched public feature/label CSVs using equivalent JavaScript calculations and committed to GitHub. **Independent end-to-end execution of the checked-in Python `--check` commands is still unverified** and should be recorded as a separate reproducibility gate; do not claim this version has passed an independent Python CI run.

## Next milestone: Step 11

Preserve v1 label manifests and Step 8 indicators. Reproduce the entire pipeline under pinned Python dependencies; audit feature extraction against raw messages for a deterministic subset and check GitHub CSV exact identity. Independently review boosted performance under broader labels, issue-level cross-validation, project/task difficulty and predeclared robustness analyses. Prioritize human/maintainer semantic oracle checks for unresolved FAIL assertions and the 14 UNVERIFIED outcomes before journal-quality claims. Use the conservative primary as default, but display all sensitivity scenarios.
