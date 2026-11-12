# Step 11 — In-place enhanced-assertion coverage and unobserved Oracle method

**Date:** 2026-11-12. **Status:** evidence-backed *method-level collection audit*, **not** a semantic correctness oracle or enhanced-backend test rerun. No v2 runner verdict, Step 7 analysis label, or Step 8 feature changed.

## Why this additional check was required

The prior [nine-run raw-log attribution](STEP11_SKIP_ATTRIBUTION_9_v1.json) counted methods **newly declared** in the augmented test patch, not assertions inserted into existing tests. In particular, `django__django-14434` reported only **one new method (observed OK)** but the full suite reported **28 skips**. It was invalid to infer complete enhanced-assertion coverage from this narrow count.

## Django-14434 — base-source mapped *existing* methods

The [read-only pinned-source analyzer](../../scripts/step11_inplace_method_audit.py), in [successful GitHub Actions #43267304895](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43267304895), retrieved `tests/schema/tests.py` at exact upstream Django base commit `5e04e84d67da8163f365e9f5fcd169e2630e2873`, with source SHA-256 `70a046a812c17e7c8dbf0ec8d34cd6a4c5e3cd8bbcd0615c85460469769bfa5a`. It mapped the 10 augmented-diff hunks to the original source method owners and matched those names with three original per-run `test_output.txt` files from immutable artifact ZIP evidence (samples 1:28, 2:30, 3:30). [Exact per-hunk and per-sample metadata](STEP11_INPLACE_METHOD_AUDIT_DJANGO14434_v1.json).

**Source finding:** The pinned SWE-ABS patch contains **10 insertion hunks**, **zero removals**: **one newly declared test method** `test_unique_constraint_field` plus **nine existing test methods** with in-place augmented code. The nine are: `test_composite_func_index`, `test_func_index`, `test_func_index_collate_f_ordered`, `test_func_index_lookups`, `test_func_unique_constraint`, `test_func_unique_constraint_covering`, `test_func_unique_constraint_lookups`, `test_func_unique_constraint_partial`, and `test_unique_constraint_field_and_expression`.

| Original agent sample | Newly added method | Modified pre-existing methods observed `ok` | Modified method `skipped` | Modified methods unobserved | Original suite-level skips |
| --- | --- | ---: | --- | ---: | ---: |
| 1:28 | `test_unique_constraint_field` — OK | 8 | `test_func_unique_constraint_covering` | 0 | 28 |
| 2:30 | `test_unique_constraint_field` — OK | 8 | `test_func_unique_constraint_covering` | 0 | 28 |
| 3:30 | `test_unique_constraint_field` — OK | 8 | `test_func_unique_constraint_covering` | 0 | 28 |

The independently re-downloaded [original raw-log evidence](STEP11_RAW_ARTIFACT_REAUDIT14_v1.json) specifies the skip reason, identically for the three runs: **`Database doesn't support feature(s): supports_expression_indexes, supports_covering_indexes`**. Thus at least one *enhanced assertion-bearing existing method* was not executed as part of the archived default-backend run. This directly corroborates the **UNVERIFIED / incomplete strengthened-coverage** classification for all three runs, beyond simply counting total suite skips.

**Boundary:** `ok` means the whole named unittest method reported success; it does **not prove every conditional branch, or each inserted assertion, was necessarily reached**. Conversely `skipped` establishes the entire method was skipped and its inserted assertions **were not tested in that archived run**. Backend-matched rerun remains necessary for the skipped method.

## Django-15503 — source confirms declaration, execution/collection missing

The [pinned-source method auditor](../../scripts/step11_missing_oracle_method_audit.py) independently matched the SWE-ABS test patch's added method `test_oracle_json_path_final_key_is_quoted_for_numeric_strings`, defined inside **`JSONFieldNumericKeyLookupsTests`** in `tests/model_fields/test_jsonfield_numeric_keys.py`. The source has **10 newly declared methods**. The [source and three-run SHA-identified log evidence](STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json) confirms this exact method was **not present in the archived verbose result lines** for 1:34, 2:37, 3:36. These archived cases each report **9 passing tests and 1 skipped test**, but source-vs-verbose method comparison previously found **8 added methods OK, one added method skipped, one added method unobserved**. [Prior original log digest evidence](STEP11_RAW_ARTIFACT_REAUDIT14_v1.json); [added-method-to-log attribution](STEP11_SKIP_ATTRIBUTION_9_v1.json).

**Critical limitation:** Source-level presence plus log-level absence **does not show the method failed, was skipped, or was even collected**. The absent method's behavior may depend on runner test selection, class setup/inheritance, backend specificity, or test-patch application; none of these causes was resolved by this source/metadata inspection. This audit reuses *already independently verified* original raw-log digests rather than redownloading raw ZIPs.

## Transient artifact egress and controlled reproduction

One new [read-only CI run #43268071356](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268071356) failed while repeating a previously successful nine-run artifact download: upstream artifact storage returned **HTTP 503 `Egress is over the account limit`**. This is **infrastructure failure, not a coding-agent test outcome**. The earlier [in-place source audit #43267304895](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43267304895) succeeded and is independently versioned. A subsequent [Oracle source-audit run #43268521977](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268521977) succeeded with archived metadata, and the [workflow](../../.github/workflows/step11-reproduction.yml) now makes repeat short-retention raw-ZIP downloads **manual opt-in**, not a default push action. Raw ZIP evidence can expire; the checked-in artifact hashes, case IDs and run links preserve partial provenance but **are not a substitute for future runtime reruns**.

## Impact on frozen research analysis

**NO CHANGE** to original runner 153 PASS / 31 provisional FAIL / 14 UNVERIFIED or primary 153 PASS / 9 reviewed FAIL / 36 excluded. This is not a post-hoc eligibility amendment. The `django-14434` finding gives a *stronger factual reason* to retain UNVERIFIED (a specific modified assertion-bearing method really skipped). The `django-15503` source/log gap confirms a distinct untested/collection-unknown method alongside one explicitly skipped JSON containment test.

**Exact next independent experiment:** Use a version-pinned backend with `supports_expression_indexes` and `supports_covering_indexes` to execute `test_func_unique_constraint_covering` against **the exact original submitted model patch** under a new run ID. For `django-15503`, first run a **collection-only** command with pinned Django source/tests and recorded backend selection to establish whether the Oracle-named method is discovered; if not, determine whether the cause is test path, inheritance, setup, or patch materialization. Then execute the missing assertions under supported backend capabilities where possible. These checks must retain all exact model patch SHA and before/after tested-tree evidence, be separately versioned, and avoid overwriting old labels. Step 11 remains **IN PROGRESS**; Steps 12–14 remain TODO.
