# Step 5 — Historical 83-run raw-evidence reconciliation

**Date:** 2026-11-12  
**Study:** SWE-ABS Free Evaluation, Gemini 3 Flash originally passing patches  
**Status:** Completed at the *provisional strengthened-test label* level. Independent semantic validity of augmented FAIL tests remains pending (Step 6).

## Scope and method

The original `sweabs_samples1_2_first83_cumulative.csv` (Sample 1 offsets 0–62; Sample 2 offsets 0–19) was compared field-for-field with the first 83 rows of the immutable archived `sweabs_full_198_cumulative_audited.csv`. **All 83 original rows matched exactly** across 12 fields.

For each of these 83 records, the corresponding per-patch GitHub Actions artifact ZIP was downloaded, opened and checked. The corrected rerun for **Sample 1 offset 5** (`pilot_42858519379_1_1_5`) was used as the authoritative test attempt, and the earlier failed attempt (`pilot_42853996382_1_1_5`) was retained in the *private* evidence backup (not counted twice). This is 83 run records represented by 84 downloaded patch ZIP artifacts.

Raw audit included: ZIP integrity; original resolved flag; sample, instance, patch SHA-256 and stored prediction identity; SWE-ABS harness revision; agent/test dataset revision consistency; base commit, pre-patch base marker and harness patch-application report; exact test patch SHA and its application in the evaluation script and stdout; preserved repository source diff before and after test; outer Django, SymPy, pytest and Sphinx/tox test summaries; augmented test skips and failures. The 83 records spanned 49 Django, 11 SymPy, 20 pytest and 3 tox/pytest outer-runner summaries. **Raw runner success is not semantic correctness of a submitted patch**.

The re-audit used a conservative policy consistent with the more recent 115-run audit: *UNVERIFIED* when exact model patch integrity or full targeted coverage was not established; *FAIL* when a genuine augmented test assertion/exception was observed with confirmed patch integrity, pending independent test soundness review; *PASS* only where executed augmented tests passed with required coverage and integrity checks. The scripts did **not** rerun any SWE-ABS evaluation.

## Outcome of reconciliation

| Historical 83 records | PASS | FAIL | UNVERIFIED | Total |
| --- | ---: | ---: | ---: | ---: |
| Before Step 5 | 63 | 15 | 5 | 83 |
| After Step 5 | 63 | 14 | 6 | 83 |

**82 of 83 historical labels were retained. One correction was required.**

### Correction — Sample 1 offset 58

- Instance: `sympy__sympy-23413`
- Patch SHA-256: `894c7d6aaa65dd46b524cda9507c23c93f42cb2049ee7a47f18492248e28b33b`
- Evidence: [GitHub Actions run 43169378297](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43169378297), artifact `sweabs-result-1-58`.
- Original provisional label: **FAIL**. The raw SymPy test runner recorded **7 passed, 1 exception** (`IndexError: list index out of range` in an added strengthened test).
- New label: **UNVERIFIED**. The model patch also edited `sympy/polys/matrices/tests/test_normalforms.py`, a path modified/reset during augmented test setup/cleanup. The repository's pre-test and post-test model diffs are *not identical*; this test file disappeared from the final patch diff. Under the conservative exact-patch-preservation rule, the complete submitted patch was **not verified** through the evaluation procedure. The exception remains an observed raw fact; it cannot be counted as a validated exact-patch FAIL.
- Affected fields in the versioned cumulative CSV: `outcome`, `source`, `note` and `failed` (correcting the historical `0` to the observed `1`). Original archived CSV left untouched.

### Retained unresolved case — Sample 1 offset 36

`psf__requests-1142` executed **15 passing augmented pytest tests**, but the agent's **884 KB** patch includes extensive generated `build/lib/` paths. The collector's whole-patch diff check was `NOT_CHECKED`, and the raw log establishes only two source file modifications. Therefore **UNVERIFIED stays UNVERIFIED**; upgrading it to PASS based solely on a green runner would overstate patch-integrity evidence. See [run 43161212626](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43161212626).

### Remaining historical UNVERIFIED records

| Sample | Offset | Instance | Reason |
| --- | ---: | --- | --- |
| 1 | 10 | `django__django-12039` | 4 database/backend-dependent tests skipped |
| 1 | 28 | `django__django-14434` | 28 skipped; modified existing test file; complete target coverage unresolved |
| 1 | 34 | `django__django-15503` | 1 database-specific test skipped |
| 1 | 36 | `psf__requests-1142` | Full large agent patch diff not verified |
| 1 | 58 | `sympy__sympy-23413` | Model patch partially overwritten/removed on overlapping test path |
| 2 | 11 | `django__django-12039` | 4 database/backend-dependent tests skipped |

## Whole-study versioned result

The prior `sweabs_full_198_cumulative_audited.csv` is an **immutable v1 archival checkpoint**. The new [`sweabs_full_198_cumulative_v2.csv`](sweabs_full_198_cumulative_v2.csv) is the **current provisional label dataset**, with one historically corrected record and all other 197 rows unchanged.

| Sample | PASS | FAIL | UNVERIFIED | Total |
| --- | ---: | ---: | ---: | ---: |
| 1 | 48 | 10 | 5 | 63 |
| 2 | 53 | 11 | 4 | 68 |
| 3 | 52 | 10 | 5 | 67 |
| **Total v2** | **153** | **31** | **14** | **198** |

The 198 run records correspond to **73 unique instance IDs** (repeated tasks across samples). Do not treat them as 198 independent tasks for statistical inference.

## Artifacts and reproducibility

- [`sweabs_historical_83_reaudit_evidence.csv`](sweabs_historical_83_reaudit_evidence.csv) — per-run identity/patch/test checks, runner summaries, original and candidate labels, evidence URLs.
- [`sweabs_historical_83_corrections.csv`](sweabs_historical_83_corrections.csv) — append-only change record for the one corrected row.
- [`sweabs_full_198_cumulative_v2.csv`](sweabs_full_198_cumulative_v2.csv) — immutable v1 plus documented correction; original v1 preserved.
- [Re-audit script](../../scripts/reaudit_historical_83.py) — offline standard-library Python reproduction using previously archived per-patch ZIPs. It does not require Docker or rerun the benchmark; it *does* require access to the private raw archive.

Example invocation from the repository root, after placing the 83 selected ZIPs in a single directory:

```bash
python scripts/reaudit_historical_83.py \
  --evidence-dir /path/to/unzipped-raw-patch-zips \
  --checkpoint results/2026-11-12/sweabs_samples1_2_first83_cumulative.csv \
  --baseline results/2026-11-12/sweabs_full_198_cumulative_audited.csv \
  --output-dir /tmp/sweabs-step5
```

### Private raw evidence preservation

A ZIP containing 83 selected per-patch artifacts, the earlier failed Sample 1 offset-5 attempt, and an artifact hash manifest was backed up to the owner's **private ChatGPT Library** at `/Research/SWE-ABS/2026-11-12/sweabs_historical_83_raw_evidence_private.zip`. It was materialized back, passed ZIP integrity verification, and matched SHA-256 `cc7c5f4280c3dd7e4ccfb34f55ea151f472435e33d1e7465fb73cf9c75c586e4` (2,790,331 bytes; 86 ZIP entries). **Not a public GitHub file.** Some raw logs or test fixtures may contain sensitive strings; no public release was attempted.

## Outstanding limitations and next step

**Step 5 is complete as an evidence reconciliation, not as semantic test validity confirmation.** Thirty-one provisional FAIL labels across all samples still need independent augmented-test soundness review. Fourteen UNVERIFIED runs cannot be treated as FAIL, or as confirmed PASS, without controlled examination or documented exclusion. Repeated instance IDs require task-aware statistical analysis.

**Next: Step 6 — Review provisional FAIL augmented tests for validity.** Group by unique task ID, inspect the asserted behavior and environment dependencies, retain structured review outcomes, and update PROJECT_STATE/WORK_LOG/README without rewriting raw v1/v2 evidence.
