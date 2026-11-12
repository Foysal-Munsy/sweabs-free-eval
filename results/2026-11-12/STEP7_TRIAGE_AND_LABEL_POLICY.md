# Step 7 — UNVERIFIED triage and provisional analysis-eligibility freeze (v1)

**Date:** 2026-11-12 (Asia/Dhaka)  
**Status:** DONE **for documentary triage, versioned provisional eligibility and sensitivity policy**. NOT a completed oracle adjudication, a confirmed exact-patch rerun, or a final semantic correctness-label freeze.  
**Research unit:** `(sample, instance_id, patch_sha256)`; identical task IDs across samples are separate agent runs but statistically dependent.

## Inputs and evidence-check boundary

Inputs are the [immutable 198-row current runner v2](sweabs_full_198_cumulative_v2.csv), [historical 83-row raw-evidence reconciliation](sweabs_historical_83_reaudit_evidence.csv), [recent 115-row raw audit](sweabs_samples2_3_full_audit_evidence_115.csv), and [31-row Step 6 review](STEP6_FAIL_REVIEW_31.csv). This session cross-checked all four files from GitHub against their join keys and labels. There are **198 unique exact run identities**, **73 distinct instance IDs**, **198/198 matching per-run audit rows**, and **31/31 FAIL rows with a matching Step 6 review**. The v2 counts remain **153 PASS / 31 FAIL / 14 UNVERIFIED**.

GitHub Actions artifacts were enumerated for the 11 workflow runs containing the 14 UNVERIFIED records: **all 14 expected per-patch artifact names existed and none was marked expired** at the time of checking. See each run link in the [14-row triage ledger](STEP7_UNVERIFIED_TRIAGE_14.csv) and the [Actions history](https://github.com/Foysal-Munsy/sweabs-free-eval/actions). **This is a documentary cross-check against already audited raw-log tables and Actions artifact metadata, not a fresh independent extraction of every raw ZIP or a new test run.** Raw ZIPs remain private per [archival manifest](MANIFEST.md).

## Investigation of all 14 UNVERIFIED records

The [14-row triage ledger](STEP7_UNVERIFIED_TRIAGE_14.csv) preserves exact identities, reported runner counts, audit reason, action priority, underlying Actions URL, and unresolved evidence required. Counts in the table are **observed passed / failed-or-error / skipped tests**, not proven patch outcomes.

| Sample:offset | Instance | Observed P/F/S | Triage reason | Next evidence gate |
| --- | --- | --- | --- | --- |
| 1:10 | django__django-12039 | 9/0/4 | Skipped database/backend tests | Backend-matched rerun |
| 1:28 | django__django-14434 | 140/0/28 | Skipped cases in in-place strengthened tests | Identify enhanced vs existing skips; backend-matched rerun |
| 1:34 | django__django-15503 | 9/0/1 | SQLite lacks JSON containment feature | Backend-matched rerun |
| 1:36 | psf__requests-1142 | 15/0/0 | Large generated `build/lib` patch; entire diff unverified | Prove whole-patch integrity |
| 1:58 | sympy__sympy-23413 | 7/1/0 | Model-modified test file reset by test setup | Non-destructive exact-patch rerun |
| 2:11 | django__django-12039 | 9/0/4 | Skipped database/backend tests | Backend-matched rerun |
| 2:30 | django__django-14434 | 140/0/28 | Skipped cases in in-place strengthened tests | Identify enhanced vs existing skips; backend-matched rerun |
| 2:37 | django__django-15503 | 9/0/1 | SQLite lacks JSON containment feature | Backend-matched rerun |
| 2:63 | sympy__sympy-23413 | 8/0/0 | Model-modified test file reset by test setup | Non-destructive exact-patch rerun |
| 3:7 | django__django-11206 | 7/5/0 | Model-modified test file reset by test setup | Non-destructive exact-patch rerun |
| 3:12 | django__django-12039 | 9/0/4 | Skipped database/backend tests | Backend-matched rerun |
| 3:30 | django__django-14434 | 140/0/28 | Skipped cases in in-place strengthened tests | Identify enhanced vs existing skips; backend-matched rerun |
| 3:36 | django__django-15503 | 9/0/1 | SQLite lacks JSON containment feature | Backend-matched rerun |
| 3:62 | sympy__sympy-23413 | 7/1/0 | Model-modified test file reset by test setup | Non-destructive exact-patch rerun |

**Nine** are coverage-limited (three `django-12039`, three `django-14434`, three `django-15503`); **four** are patch/test-file overlap (three `sympy-23413`, one `django-11206`); **one** is whole-patch-integrity unproven (`requests-1142`). Six distinct task IDs are affected. None is promoted to PASS or FAIL.

For skipped cases, a clean result on the *executed subset* is real runner evidence, but not proof that the skipped augmented assertions pass. For patch overlap, a failing or passing raw runner may still reflect correct source-code behavior, but the **submitted exact patch** was not preserved through testing. For the large patch, a reviewer might plausibly consider generated build files immaterial to runtime behavior; the study's preexisting exact-submission criterion does not permit assuming that without proof. These are alternatives, not revised outcomes.

## Frozen analysis-label rules — v1

The machine-readable [198-row analysis manifest](STEP7_ANALYSIS_LABELS_v1.csv) retains **every original run**, original outcome, Step 6 review and Step 7 triage fields, exact patch hash, source audit table and raw Actions URL. `y=1` means *provisional strengthened-test failure*; `y=0` means *audited runner PASS*. A blank label means **excluded**, never automatically FAIL.

Eligibility is set by **test coverage, patch identity and independently documented assertion concerns**, not by any trajectory messiness feature. These rules were recorded before feature extraction or predictive modeling.

| Prespecified dataset | y=0 | y=1 | Excluded | Meaning |
| --- | ---: | ---: | ---: | --- |
| **Primary (documentary-provisional): `primary_y`** | **153** | **9** | **36** | Audited v2 PASS vs Step 6 review-supported `valid_failure` only. Exclude all 14 UNVERIFIED, 16 unresolved FAIL, 2 environment-sensitive FAIL and 4 invalid-test FAIL. **162 runs; 61 unique tasks; only 5 distinct FAIL tasks.** |
| Sensitivity A: `noninvalid_sensitivity_y` | 153 | 27 | 18 | Adds unresolved and environment-sensitive FAIL; still excludes 4 invalid-test FAIL + all 14 UNVERIFIED. **Not ground truth.** |
| Sensitivity B: `runner_only_sensitivity_y` | 153 | 31 | 14 | Uses all raw v2 FAILs, including 4 test-questioned cases, to show dependence on *runner-only* target definition. **Not a semantic failure claim.** |
| Sensitivity C: `skipped_as_pass_scenario_y` | 162 | 9 | 27 | Assumes the 9 coverage-skipped UNVERIFIED would pass missing tests; **hypothetical optimistic coverage scenario only**, not an observed PASS or corrected v2 label. Other 5 UNVERIFIED remain excluded. |

**Primary-label screening does not make `valid_failure` final oracle truth.** There is no independent human adjudication of these 9 runs and no full proof that every PASS is a semantically correct or sufficiently comprehensive test. The primary sample has only **9 failure runs across 5 task IDs**, so any future metric must disclose small effective failure-task count, repeated-task correlation and uncertainty. The 198 rows are **not** 198 independent tasks. Do not describe the screened 162 rows as a final gold-standard dataset.

**Opposing view:** The research question explicitly says "failure under strengthened tests", so runner-only outcomes (31 FAIL) arguably belong in the main analysis rather than restricting to 9 documentary-supported FAILs. **Response:** Runner-only targets are retained exactly in Sensitivity B; the conservative primary is selected to reduce known invalid-test contamination, and conclusions must be reported across both definitions rather than claiming one is objectively correct. Conversely, optimistic inclusion of 9 skipped passes can inflate reliability; it is therefore only a hypothetical sensitivity branch.

## Reproduction and versioning

Run `python scripts/build_step7_analysis_labels.py --check` at repository root to verify the checked-in Step 7 CSVs against the four existing source CSVs; omit `--check` to deterministically rebuild the two CSVs. The script asserts row identities, join agreement, all 31 reviewed FAILs, 14 triage categories and each sensitivity count. Source: [build script](../../scripts/build_step7_analysis_labels.py). Files are **v1**; never overwrite raw v2, Step 6 ledger, or earlier evidence when new oracle evidence arrives. Create a v2 *analysis manifest* and append the exact changed identities, reasons, rerun IDs, source hashes and analysis-policy implications.

No benchmark rerun, human/maintainer adjudication, or newly claimed semantic correctness has occurred in this Step 7 documentary freeze. Existing Actions artifact retention is 14 days per [workflow](../../.github/workflows/sweabs-pilot.yml); use the private archival evidence per [manifest](MANIFEST.md) after expiry.

## Remaining validation and handoff

1. **Step 8 NEXT:** Freeze trajectory indicator definitions, event-parsing rules, missingness rules and leakage restrictions **without inspecting indicator–outcome association**. Do not begin fitting models yet.
2. As a separately tracked validation stream, first design a **non-destructive exact-patch test protocol** for the four overlap runs; verify the full `requests-1142` patch diff; identify which skipped tests are newly enhanced and whether a backend-specific targeted rerun can execute them. Rerun only under explicitly recorded, comparable harness and dataset revisions. **No blind workflow-dispatch reruns.**
3. Seek human/maintainer or credible issue-specific oracle review for Step 6's 16 unresolved, 2 environment-sensitive and 4 test-questioned FAILs, as well as checks on the 9 review-supported cases before any final semantic-accuracy claim.
4. Keep `AGENTS.md`, `docs/PROJECT_STATE.md`, `docs/WORK_LOG.md`, `README.md`, and [results index](../README.md) synchronized after new evidence. Preserve all original run outcomes.

**Research status:** Feature extraction, statistical modeling, trajectory-based prediction, and paper conclusions have **not** begun. A versioned, transparent provisional analysis-label gate exists; it is not the publication-ready ground truth.
