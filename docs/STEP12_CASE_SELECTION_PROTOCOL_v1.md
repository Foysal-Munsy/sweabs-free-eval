# Step 12 — Frozen qualitative case-selection protocol v1

**Declared:** 2026-11-13 (Asia/Dhaka), **before selecting or inspecting the selected per-run rows** for Step 12. This is a descriptive, illustrative extension of the already frozen Step 7/Step 8 analysis, **not** a new predictor, a new label policy, or blinded prospective validation.

## Fixed inputs and identity

- Source outcomes: [198-row runner v2](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv).
- Source eligibility and validity notes: [Step 7 label manifest](../results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv) and [Step 6 documentary review](../results/2026-11-12/STEP6_FAIL_REVIEW_31.csv).
- Source features: [Step 9 exact-match feature table](../results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv); feature definitions remain [Step 8 v1](STEP8_FROZEN_INDICATORS_v1.md).
- Source non-primary review category: [Step 7 UNVERIFIED triage](../results/2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv); contextual controlled tests remain [Step 11 immutable evidence](../results/2026-11-12/STEP11_CONTROLLED_EVIDENCE_FREEZE_v1.json).
- Match rows **only** on `(sample, instance_id, patch_sha256)`. Require one and only one corresponding row in each relevant manifest. Reject missing or duplicated identities, never substitute a different sample/patch on the same task.
- All case selections use **only** the previously defined `duplicate_terminal_rate` score, original frozen category and immutable identities. Other features are reported, not used to select cases.

## Deterministic illustrative roster: eight slots

Build the following roster **in order**, without manual substitutions based on perceived narrative usefulness.

1. **PRIMARY_FAIL_HIGH:** among `primary_y == 1`, select highest numeric `duplicate_terminal_rate`.
2. **PRIMARY_FAIL_LOW:** among `primary_y == 1`, select lowest numeric score, excluding task IDs already selected.
3. **PRIMARY_PASS_HIGH:** among `primary_y == 0`, select highest numeric score, excluding task IDs already selected.
4. **PRIMARY_PASS_LOW:** among `primary_y == 0`, select lowest numeric score, excluding task IDs already selected.
5. **INVALID_TEST_CHALLENGE:** among original `raw_outcome_v2 == FAIL` with `step6_review_status == invalid_test`, choose the earliest identity lexicographically, excluding already selected task IDs.
6. **ENVIRONMENT_CHALLENGE:** among original `raw_outcome_v2 == FAIL` with `step6_review_status == environment_sensitive`, choose the earliest identity lexicographically, excluding already selected task IDs.
7. **SKIPPED_COVERAGE_CHALLENGE:** among original `raw_outcome_v2 == UNVERIFIED` with `step7_triage_category == partial_coverage_skips`, choose the earliest identity lexicographically, excluding already selected task IDs.
8. **PATCH_OVERLAP_CHALLENGE:** among original `raw_outcome_v2 == UNVERIFIED` with `step7_triage_category == patch_file_overlap`, choose the earliest identity lexicographically, excluding already selected task IDs.

For the four score-ranked slots, sort on signed numeric score in the stated direction; break all ties by `(instance_id, numeric sample, numeric offset, patch_sha256)` ascending. For slots 5–8, sort by that same identity tuple ascending. For all slots, exclude the **entire task ID**, not only the same patch, to avoid mistaking multiple samples for independent cases. If any slot is empty, record `unavailable` with the reason rather than silently changing the rule.

## Evidence and interpretation discipline

- Preserve the original runner v2 outcome and Step 7 primary label/exclusion exactly; the four non-primary slots are **not** new primary positives or negatives.
- For every chosen row report sample, offset, instance ID, full model patch SHA, source CI run URL, duplicate-command numerator/denominator, score, verification and terminal-error aggregate, Step 6/7 annotation, and the exact source/result links available.
- Independent raw-message evidence is **only** established if the frozen Step 11 12-trajectory spot-check explicitly covers that same identity, or a new independently source-pinned audit is performed. The archived Step 9 feature table itself supports aggregate event counts, but **not** invented narrative sequences, quoted dialogue, exact terminal commands, or assumed intent. Do not publish raw trace text. Mark non-spot-checked qualitative event chronology **unverified**.
- Step 6 documentary judgments are not human gold labels. For every selected case write a *supported observation*, a *plausible opposing interpretation*, and an *unresolved question*. Separate test execution from assertion validity.
- The four extremes are deliberately illustrative, **not representative population estimates**. Selection uses observed labels and scores, so no inference, tuning, significance testing, or predictive accuracy claim may be based on these cases.
- Controlled Step 11 rechecks are a separate runtime and must not overwrite original outcome labels or be described as the historical SWE-ABS Docker outcome.
- Keep other historical Step 7 cases unselected but not erased. Cite the full manifests and Step 11 sensitivity analysis to counter cherry-picking.
- When the roster/report is committed, update PROJECT_STATE + WORK_LOG + public README in the same research session and verify read-back. If any evidence gate cannot be met, mark Step 12 partial, not DONE.

## Completion gate

A versioned exact-run roster plus a report documenting **all eight fixed slots**, evidence/bounds/opposing interpretations, actual reproducible count checks, full source links, and without any changed frozen Step 7 or Step 8 data. **Writing a narrative without trace provenance is not sufficient to claim human-oracle-confirmed case analysis.**
