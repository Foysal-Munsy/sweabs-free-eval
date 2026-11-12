# SWE-ABS evaluation — full Sample 2 + Sample 3 raw-log audit

**Audit date:** 2026-11-12. **Scope:** 115 newly downloaded per-patch artifacts (Sample 2 offsets 20–67 and Sample 3 offsets 0–66), combined with 83 previously audited/preserved rows (Sample 1 offsets 0–62, Sample 2 offsets 0–19).

## Cumulative outcomes — provisional augmented-test labels, not semantic correctness

| Sample | Attempted | PASS | FAIL | UNVERIFIED |
|---|---:|---:|---:|---:|
| 1 | 63 | 48 | 11 | 4 |
| 2 | 68 | 53 | 11 | 4 |
| 3 | 67 | 52 | 10 | 5 |
| **Total** | **198** | **153** | **32** | **13** |

Sample 1 and Sample 2 offsets 0–19 were preserved byte-for-byte at the CSV field level from the earlier 83-row cumulative file; this audit did **not** re-check those 83 runs. First 63 Sample 1 rows include prior review notes and are not upgraded to final semantic-correctness judgments.

## Auditing rules applied to all 115 newly obtained artifacts

1. Verified ZIP readability, exact `(sample, offset, instance_id, run_id)` identity, original standard-pass flag, frozen trajectory dataset and augmented-test dataset revisions, pinned SWE-ABS commit, and base commit in metadata plus raw container log.
2. Independently recomputed SHA-256 for the exact prediction patch and augmented test patch; compared against `result.json`, `metadata.json`, and the on-disk `patch.diff`; checked original model patch application in the official per-instance report and pre-test Git diff.
3. Verified the complete test patch appears in `eval.sh`, its target files are reported as applied cleanly in the raw `test_output.txt`, and pre/post repository diff snapshots remain equal (or flagged any overlapping test-file cleanup).
4. Parsed the **outer actual augmented test runner**, not the original SWE-bench `resolved` field: Django `Ran N` plus `OK/FAILED`, pytest final summary (including nested pytester subprocesses and warning-heavy output), Sphinx/tox exit 0 plus pytest summary, and SymPy `tests finished` including exceptions.
5. Assigned PASS only when augmented tests ran successfully without outer skips and the model patch stayed intact; FAIL for observed augmented test failures / code-level test exceptions with valid patch identity; UNVERIFIED for skipped augmented coverage or exact-patch identity mismatch. No infrastructure error was converted into FAIL; any functional FAIL still requires independent augmented-test-validity review.

## Collector corrections (115 newly checked rows only)

- **38 collector UNVERIFIED → audited PASS:** raw Django/pytest/tox/SymPy runner output confirms successful augmented tests, including tests added to existing test files which the collector could not enumerate.
- **7 collector UNVERIFIED → audited FAIL:** raw runner shows actual augmented test failures or functional exceptions (not infrastructure errors).
- **1 collector FAIL → audited UNVERIFIED:** Sample 3 offset 7; the test runner failed, but overlapping augmented-test setup replaced part of the agent patch, so the exact model patch was not under test.
- Two additional collector UNVERIFIED cases (Sample 2 offset 63, Sample 3 offset 62) also have overlapping test-file cleanup and remain UNVERIFIED.

## Unverified runs requiring follow-up (newly checked)

| Sample | Offset | Instance | Observed raw runner | Audit blocker | Workflow |
|---|---:|---|---|---|---|
| 2 | 30 | `django__django-14434` | 140 passed, 0 failed/errors, 28 skipped | Partial test coverage / skipped tests | [#43181332699](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699) |
| 2 | 37 | `django__django-15503` | 9 passed, 0 failed/errors, 1 skipped | Partial test coverage / skipped tests | [#43181332699](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699) |
| 2 | 63 | `sympy__sympy-23413` | 8 passed, 0 failed/errors, 0 skipped | Model patch/test-file overlap; exact patch not preserved | [#43181346009](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181346009) |
| 3 | 7 | `django__django-11206` | 7 passed, 5 failed/errors, 0 skipped | Model patch/test-file overlap; exact patch not preserved | [#43182603318](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182603318) |
| 3 | 12 | `django__django-12039` | 9 passed, 0 failed/errors, 4 skipped | Partial test coverage / skipped tests | [#43182697559](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182697559) |
| 3 | 30 | `django__django-14434` | 140 passed, 0 failed/errors, 28 skipped | Partial test coverage / skipped tests | [#43182706543](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182706543) |
| 3 | 36 | `django__django-15503` | 9 passed, 0 failed/errors, 1 skipped | Partial test coverage / skipped tests | [#43182706543](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182706543) |
| 3 | 62 | `sympy__sympy-23413` | 7 passed, 1 failed/errors, 0 skipped | Model patch/test-file overlap; exact patch not preserved | [#43182738449](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182738449) |

The overlapping-path runs are **not** infrastructure FAILs; they are validity-limited evaluations. In such runs, the test script checked out an agent-modified test file before inserting the augmented tests. The original complete patch is therefore not proven active at test time.

## Newly audited FAIL observations

All items below are **provisional augmented-runner FAIL** and still require semantic/test-validity checks; this is not a claim that the patch is semantically incorrect.

| Sample | Offset | Instance | Test result | Raw source |
|---|---:|---|---|---|
| 2 | 28 | `django__django-14311` | FAILED (failures=2) | [#43181184322](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181184322) |
| 2 | 32 | `django__django-14999` | FAILED (failures=1) | [#43181332699](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699) |
| 2 | 34 | `django__django-15252` | FAILED (failures=1) | [#43181332699](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699) |
| 2 | 38 | `django__django-15916` | FAILED (errors=2) | [#43181332699](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699) |
| 2 | 41 | `matplotlib__matplotlib-25775` | 3 failed, 11 passed, 2 skipped in 2.93s | [#43181336920](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181336920) |
| 2 | 59 | `sympy__sympy-15599` | tests finished: 17 passed, 2 failed, 3 exceptions, in 4.87 seconds ====== | [#43181340403](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181340403) |
| 2 | 65 | `sympy__sympy-24066` | tests finished: 9 passed, 1 failed, in 0.30 seconds ============== | [#43181346009](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181346009) |
| 3 | 4 | `django__django-10097` | FAILED (failures=2) | [#43182603318](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182603318) |
| 3 | 10 | `django__django-11848` | FAILED (failures=1) | [#43182697559](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182697559) |
| 3 | 11 | `django__django-11999` | FAILED (failures=1) | [#43182697559](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182697559) |
| 3 | 18 | `django__django-12273` | FAILED (failures=1) | [#43182697559](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182697559) |
| 3 | 20 | `django__django-12304` | FAILED (failures=1) | [#43182701126](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182701126) |
| 3 | 28 | `django__django-14311` | FAILED (failures=2) | [#43182701126](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182701126) |
| 3 | 32 | `django__django-14999` | FAILED (failures=1) | [#43182706543](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182706543) |
| 3 | 37 | `django__django-15916` | FAILED (errors=2) | [#43182706543](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182706543) |
| 3 | 38 | `django__django-16661` | FAILED (failures=1) | [#43182706543](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182706543) |
| 3 | 57 | `sympy__sympy-15599` | tests finished: 20 passed, 2 failed, in 1.05 seconds ============= | [#43182719908](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182719908) |

**Important failure-context examples:** Sample 2 offset 41 (`matplotlib__matplotlib-25775`) has 3 executed assertion failures and 2 SVG-conversion skips, so it is FAIL with incomplete coverage; Sample 2 offset 59 (`sympy__sympy-15599`) has assertions and functional exceptions; Sample 3 offset 62 (`sympy__sympy-23413`) has a functional `IndexError`, but is UNVERIFIED due model/test-patch overlap. Django model form callback errors are raised inside code under test, not container setup errors. See per-patch ZIP logs and linked workflow run pages.

## GitHub Actions evidence sources

| Sample | Offset range | Count | Workflow run |
|---|---|---:|---|
| 2 | 20–29 | 10 | [GitHub Actions #43181184322](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181184322) |
| 2 | 30–39 | 10 | [GitHub Actions #43181332699](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699) |
| 2 | 40–49 | 10 | [GitHub Actions #43181336920](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181336920) |
| 2 | 50–59 | 10 | [GitHub Actions #43181340403](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181340403) |
| 2 | 60–67 | 8 | [GitHub Actions #43181346009](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181346009) |
| 3 | 0–9 | 10 | [GitHub Actions #43182603318](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182603318) |
| 3 | 10–19 | 10 | [GitHub Actions #43182697559](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182697559) |
| 3 | 20–29 | 10 | [GitHub Actions #43182701126](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182701126) |
| 3 | 30–39 | 10 | [GitHub Actions #43182706543](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182706543) |
| 3 | 40–49 | 10 | [GitHub Actions #43182715959](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182715959) |
| 3 | 50–59 | 10 | [GitHub Actions #43182719908](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182719908) |
| 3 | 60–66 | 7 | [GitHub Actions #43182738449](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182738449) |

Every above workflow run had a successful `prepare` step, the expected number of completed evaluation jobs, and a successful `summarize` step, checked through the connected GitHub Actions jobs API. **Job success is not a patch PASS verdict.**

## What has not been done

- No independent examination of strengthened test semantic soundness; all FAILs remain provisional.
- No reruns on alternate databases/backend environments for skipped cases, and no corrected reruns of overlapping-patch test files.
- No extraction of trajectory messiness features, statistical significance testing, AUROC, or paper writing.

## Deliverables

- `sweabs_full_198_cumulative_audited.csv`: 198 cumulative rows, unchanged original 83 plus 115 audited rows.
- `sweabs_samples2_3_full_audit_evidence_115.csv`: explicit per-run provenance, hashes, checks, runner summaries, changes from collector labels, and GitHub source URLs.
- `sweabs_full_audit_evidence_bundle.zip`: preserves 135 Sample 2/3 per-patch ZIPs (68 Sample 2 + 67 Sample 3), CSVs, this report, and the audit script, because GitHub Actions artifacts are configured for **14-day** retention (see [workflow YAML](https://github.com/Foysal-Munsy/sweabs-free-eval/blob/main/.github/workflows/sweabs-pilot.yml)).