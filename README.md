# SWE-ABS Free Evaluation

A GitHub Actions pipeline for evaluating **originally successful coding-agent patches** against **SWE-ABS strengthened tests**. This repository covers the stronger-test evaluation stage of an ongoing research project.

## Research Question

> Among coding-agent runs that pass the original benchmark, can lightweight trajectory-level messiness indicators predict failure under stronger tests?

The stronger-test outcomes collected here will later be matched with trajectory features. **That analysis has not been performed yet.**

## Progress — November 12, 2026

| Dataset subset | Originally passing runs | Evaluation attempts | Status |
| --- | ---: | ---: | --- |
| Sample 1 | 63 | 63 | Completed; audit review ongoing |
| Sample 2 | 68 | 0 | Pending |
| Sample 3 | 67 | 0 | Pending |
| **Total** | **198** | **63** | **135 attempts remaining** |

**Sample 1 provisional augmented-test outcomes:**

| PASS | FAIL | UNVERIFIED | Total |
| ---: | ---: | ---: | ---: |
| 48 | 11 | 4 | 63 |

All 63 sample-1 indices (`0–62`) have an evaluation record, with distinct instance IDs and submitted-patch hashes, according to the cumulative audit CSV.

**These are provisional, raw-log-audited augmented-test labels**, not final semantic-correctness judgments or official SWE-bench `resolved` scores. Some FAIL cases still require independent test-validity review.

Four cases remain **UNVERIFIED** because test coverage or patch verification was incomplete: `django__django-12039`, `django__django-14434`, `django__django-15503`, and `psf__requests-1142`.

The cumulative Sample 1 CSV has been prepared separately and is **not yet included in this repository**.

## Data and Evaluation Setup

- **Agent trajectories and submitted patches:** [Gemini 3 Flash SWE-bench Verified trajectories](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories), selecting originally resolved runs by sample.
- **Strengthened-test data:** [SWE-Bench Verified ABS](https://huggingface.co/datasets/OpenAgentLab/SWE-Bench_Verified_ABS).
- **Evaluation harness:** [OpenAgentEval/SWE-ABS](https://github.com/OpenAgentEval/SWE-ABS), pinned in the pilot workflow to commit `26b4c736ca3d566d8395d7999304d0264abe7992`.
- **Execution:** GitHub Actions with Docker-capable runners; the workflow evaluates up to 10 selected patches per dispatch, with at most two evaluation jobs in parallel.

The pipeline selects the requested sample/offset/count, freezes dataset revisions, checks patch identity, prepares the correct task base commit, applies the submitted patch and augmented test patch, runs the task's test command, and uploads per-patch evidence and a batch summary.

## Implementation and Fixes

During the initial smoke test, the SWE-ABS harness's patch fallbacks could undo an already-applied patch. The patch-handling backport now restores a clean state between retries, avoids unintended patch reversal, and records the effective changes before testing.

Further pilot work added base-commit checks, submitted-patch hash verification, and conservative outcome auditing across multiple test runners.

Some runner formats (including Django, SymPy, Sphinx/tox, and nested pytest output) are not reliably classified by the automatic collector. Accordingly, Sample 1 outcomes were reviewed against archived test logs; a workflow-level `UNVERIFIED` label does **not** automatically mean the tests failed.

### Initial Smoke Test

Instance: `astropy__astropy-12907`.

The intended change to `astropy/modeling/separable.py` was present during evaluation, and the strengthened test run reported **11 passed**.

See the [smoke-test workflow](.github/workflows/sweabs-smoke.yml).

## Workflows and Evidence

- [Smoke test](.github/workflows/sweabs-smoke.yml) — single-instance harness validation.
- [Batch pilot](.github/workflows/sweabs-pilot.yml) — manually triggered evaluation with `sample`, `offset`, and `count` (`1–10`).
- [GitHub Actions runs](https://github.com/Foysal-Munsy/sweabs-free-eval/actions) — execution history.

The batch workflow uploads a frozen selection plan, a result artifact per patch (prediction, metadata, raw logs, collected result), and a merged CSV/JSON summary.

**Artifacts have a 14-day retention period**, so important evidence should be archived separately.

## Remaining Work

1. Evaluate Sample 2 (**68 runs**) and Sample 3 (**67 runs**) to reach **198/198 evaluation attempts**.
2. Consolidate and audit all outcomes; resolve incomplete test coverage and check FAIL-case test validity.
3. Extract frozen trajectory messiness indicators and match them with the exact sample/task/patch outcomes.
4. Conduct statistical analysis and report results, uncertainty, and limitations in the research paper.

**Current milestone:** Sample 1 evaluation attempts complete (**63/63**); stronger-test data collection is ongoing. No claim about the predictive value of trajectory messiness is made yet.
