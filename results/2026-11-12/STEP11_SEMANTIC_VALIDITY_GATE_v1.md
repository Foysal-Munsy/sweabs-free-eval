# Step 11 — Source-pinned semantic-validity and coverage gate (v1)

**Date:** 2026-11-12 (Asia/Dhaka). **Current disposition:** SOURCE STRUCTURE VERIFIED, **semantic oracle and targeted reruns NOT complete**. Original outcome, Step 7 frozen label screens and Step 8 process indicators **unchanged**.

## Independent sources and audit method

This follow-up started from [Step 6's per-run FAIL evidence ledger](STEP6_FAIL_REVIEW_31.csv), [Step 7's 14-case UNVERIFIED triage](STEP7_UNVERIFIED_TRIAGE_14.csv), and [AGENTS/PROJECT_STATE](../../docs/PROJECT_STATE.md). The added [read-only structural audit script](../../scripts/step11_semantic_structural_audit.py) independently loads the public original agent trajectory dataset pinned at `b5515d1dce40036633293b70477f0633b24593f7`, and the SWE-ABS augmented test dataset pinned at `79fc07a8f4ce5e3720e069948073f5f910b7577b`. Original model patches are matched on **sample + task + SHA-256**, not task alone. For each selected run it hashes the original issue/problem statement, hashes the strengthened test patch, checks changed-file paths and models-vs-test collisions, and validates Step 6's recorded test SHA against the pinned source. No original issue or agent patch text is copied into the public output.

**Execution verified:** [successful read-only GitHub Actions #43262365929](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43262365929) completed this crosswalk with no hash or identity assertion failure: **45 exact selected agent runs across 20 distinct task IDs**, comprising **31 FAIL review runs and 14 UNVERIFIED**. [Per-run 45-row source/test evidence](STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json) is preserved with source revisions and hashes. This is *independent static artifact provenance*, **not** a human maintainer oracle or evidence of runtime behavior on a proper backend.

## Objective findings in the 14 UNVERIFIED runs

| Group | Distinct task | Affected samples | Pinned augmented test files | Source-level finding |
| --- | --- | --- | --- | --- |
| Incomplete coverage | `django__django-12039` | 1, 2, 3 | `tests/indexes/test_whitespace_create_index.py` | 3 reported incomplete runs; original/augmented changed files do not directly overlap; skip-related syntax exists in patch |
| Incomplete coverage | `django__django-14434` | 1, 2, 3 | `tests/schema/tests.py` | 3 reported incomplete runs; no direct overlap; `skipUnlessDBFeature` appears in patch |
| Incomplete coverage | `django__django-15503` | 1, 2, 3 | `tests/model_fields/test_jsonfield_numeric_keys.py` | 3 reported incomplete runs; no direct overlap; `skipUnlessDBFeature` appears in patch |
| **Model/test collision** | `sympy__sympy-23413` | 1, 2, 3 | `sympy/polys/matrices/tests/test_normalforms.py`, `test_normalforms_hnf_extra.py` | **Exact changed-path collision** on `sympy/polys/matrices/tests/test_normalforms.py` in all three agent patches |
| **Model/test collision** | `django__django-11206` | 3 | `tests/utils_tests/test_numberformat.py`, `test_numberformat_small_decimals.py` | **Exact changed-path collision** on `tests/utils_tests/test_numberformat.py` |
| **Patch-integrity gap** | `psf__requests-1142` | 1 | `tests/test_content_length.py` | One agent diff changes **74 diff files**, including **65 paths under `build/` or `build/lib/`**; the augmented patch does not directly overlap its changed paths, but the original whole-tested-tree diff was not proved |

All **4/4** previously triaged collision records have a concrete matching changed path in the pinned original/test patches; **0/9** skip group rows and **0/1** generated patch row have a direct changed-file collision. The source patch includes skip-related tokens for the three coverage tasks, but **this alone does not identify which runtime assertions were skipped** or prove they would pass on another backend. The existing runtime audit reported 9/0/4, 140/0/28 and 9/0/1 PASS/FAIL/SKIP, respectively, for the three coverage task families; the full per-run [Step 7 ledger](STEP7_UNVERIFIED_TRIAGE_14.csv) remains the source of those runner counts. The Requests patch's 65 generated paths establish *complexity and integrity-review burden*, not that those files were lost/altered when tested.

## Step 6 FAIL cases — provenance independently matched, judgment NOT adjudicated

The same pinned-source check verified **31/31 reviewed FAIL models** against exact agent patch SHA and their recorded SWE-ABS augmented test patch SHA. Their previous documentary classifications remain: **9 `valid_failure`**, **4 `invalid_test`**, **2 `environment_sensitive`**, **16 `unresolved`**, across **15 FAIL task IDs**. [Original case-specific issue/PR/test analysis](STEP6_FAIL_VALIDITY_REVIEW.md) supplies the actual failing assertions, downstream behavioral concerns, competing explanations and task PR links. The structural check **does not convert the documentary statuses to human-verified semantic truth**.

The 16 unresolved FAIL runs cluster by task across the following **eight source issues**: `django-11206` (signed-zero formatting policy), `django-12273` (new primary key vs copy-with-`pk=None` semantics), `django-12304` (subclass override vs template-use default), `django-14999` (schema operation/many-to-many rebuild behavior), `django-16661` (admin lookup allowlisting), `sympy-24066` (internal dimensional tuple contract), `django-10097` (userinfo colon policy under competing URL standards), and `django-15252` (mock-call flag vs actual migration table side effect). This is a regrouping of existing documented assertions, **not eight newly confirmed bugs**. The two `django-15916` form-callback cases remain runtime-version/descriptor-sensitive and cannot be conclusively adjudicated by test patch hashes.

## Evidence-based gate decisions and rerun prerequisites

1. **Priority P1: four patch/test collisions.** Before a controlled rerun, preserve the submitted exact original agent patch (including edits to model-owned test files), demonstrate the tested repository tree still contains every submitted model change, and merge augmented assertions **non-destructively** on common files. A successful test run on an overwritten patch is not evidence about the originally submitted patch.
2. **Priority P1: one large generated-patch integrity case.** Verify all changed code, built and duplicated `build/lib` paths using original base commit, patch SHA and resulting tree before treating a test run as exact-patch evidence. 65 generated files alone do not establish a defect; a diff/hash comparison is required.
3. **Priority P2: nine backend/skip coverage cases.** Identify precisely which augmented tests and backend features were skipped in the executed logs, then execute under a version-compatible supported backend or explain the unsupported coverage. Do not assume SQLite-tested subsets cover PostgreSQL-only or other backend-dependent assertions.
4. **Semantic adjudication:** Cross-check each unresolved enhanced assertion against original issue, contemporaneous repository contract/tests, runtime versions and (when possible) maintainer assessment or controlled minimal behavioral reproduction. It is acceptable to retain **unresolved** rather than force binary semantic labels.
5. **Immutable method discipline:** Keep original v2 **153 runner PASS / 31 runner FAIL / 14 UNVERIFIED** and Step 7 primary **153 provisional PASS / 9 documentary review-supported FAIL / 36 excluded**. Only versioned future runs/oracle protocols may support a *distinct* secondary analysis snapshot. Do not retroactively tune Step 8 indicators based on outcome changes.

## Opposing interpretations and publication limitations

**Interpretation A (conservative):** Exclude disputed failures and incomplete/overwritten/large-patch tests, use primary 9 documentary-supported FAILs, and report the near-chance duplicate-command result (AUROC 0.489). **Problem:** just **five distinct positive task IDs**, so effective power and inference are weak.

**Interpretation B (runner-centric):** Evaluate what the strengthened runner actually reported as FAIL, retain 31 failed runs and find duplicate-command AUROC approximately 0.708. **Problem:** includes documented invalid tests, unresolved/unsupported assertions, and a change in research target from semantic defect to particular runner disagreement. See [Step 10 results](STEP10_AUROC_TASK_CLUSTER_v2.json) and [Step 11 task-aware stress tests](STEP11_EXPLORATORY_ROBUSTNESS_v1.json).

**Conclusion:** Reproducible process features and runner outcomes are real evidence, but a **validated coding-agent reliability detector is not established** from this sample. Static source-crosswalks cannot close the independent semantic oracle gate. Present separate scopes transparently, and proceed to Step 12 case studies only after explicitly accepting this inconclusive/provisional framing or obtaining stronger human/controlled-run evidence.

## Remaining action

A separate [private-artifact re-audit script](../../scripts/step11_raw_artifact_reaudit14.py) is intended to download the 14 original short-retention Actions result ZIPs and compare artifact identity and skip-log metadata. Treat its output as **pending until a successful run and archived report exist**. Even if all ZIP files verify, skipped tests, overwritten patches and semantic questions require further independent evidence. Do not publish private raw ZIPs or claim outcomes have changed.
