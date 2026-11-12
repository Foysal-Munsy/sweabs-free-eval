# SWE-ABS Free Evaluation

Reproducible GitHub Actions evaluation of **coding-agent patches that originally passed SWE-bench Verified** against **SWE-ABS strengthened tests**.

> **Research question:** Among originally successful coding-agent trajectories, do lightweight trajectory-level messiness indicators predict failure under strengthened tests?

This repository covers the **stronger-test evaluation and evidence collection stage**. Trajectory indicator extraction, predictive analysis, and paper writing have **not** been completed. The outcomes below are *provisional augmented-test labels*, not final semantic-correctness judgments.

### Project continuity and research handoff

This README is the **public summary**. For a precise human/AI continuation point, use [**PROJECT_STATE.md**](docs/PROJECT_STATE.md) (milestones, current snapshot, unresolved issues, next exact action) and [**WORK_LOG.md**](docs/WORK_LOG.md) (dated, evidence-backed work history). Coding/research agents should start with [**AGENTS.md**](AGENTS.md).

> The repository and the linked handoff documents are public. Operational details belong in the handoff docs, but secrets and sensitive/private data do not. These records must be updated together when the verified research state changes.

## Research status — 2026-11-12

**Milestone: all 198 evaluation attempts complete; all per-patch raw logs reconciled to a current provisional v2 dataset.** An AI-assisted documentary review of all 31 raw FAILs is complete; **human/maintainer semantic adjudication and final label freezing are not complete**.

| Subset | Originally passing agent runs | Evaluation attempts | PASS | FAIL | UNVERIFIED |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sample 1 | 63 | 63 | 48 | 10 | 5 |
| Sample 2 | 68 | 68 | 53 | 11 | 4 |
| Sample 3 | 67 | 67 | 52 | 10 | 5 |
| **Total** | **198** | **198** | **153** | **31** | **14** |

- **PASS:** The audited strengthened-test runner passed the executed augmented tests, with required patch identity and coverage checks met.
- **FAIL:** The strengthened-test runner exhibited test failure or functional test exception with the intended patch present; **all 31 raw FAILs have a documented AI-assisted validity disposition; independent human/maintainer oracle validation remains pending**.
- **UNVERIFIED:** Coverage was incomplete, the exact patch under test could not be established, or another validity check was unresolved. **Never count these as FAIL, or silently drop them from reporting.**
- **GitHub Actions job success is not patch PASS.** Workflow jobs upload evidence even when the model patch fails augmented tests.

The 115 recent Sample 2 (offsets 20–67) and Sample 3 (offsets 0–66) records were audited from raw artifacts, followed by a separate [83-run historical raw re-audit](results/2026-11-12/STEP5_RECONCILIATION_REPORT.md). The archived v1 (153 PASS / 32 FAIL / 13 UNVERIFIED) remains intact; **v2 corrects Sample 1 offset 58 from FAIL to UNVERIFIED** due to incomplete exact-patch preservation. All outcomes remain provisional.

**Unit of observation:** an agent run defined by `(sample, instance_id, patch_sha256)`. The 198 records contain **73 distinct instance IDs**; tasks repeat across samples. A later model/association analysis must account for repeated tasks and must not treat 198 records as independent task identities.

### Known audit limitations

- **14 UNVERIFIED total:** 5 in Sample 1, 4 in Sample 2, 5 in Sample 3. Causes include skipped database-dependent tests, incomplete coverage/patch-diff checks, and patch/test-file overlap.
- **Four patch-overlap cases:** Sample 1 offset 58 (`sympy__sympy-23413`), Sample 2 offset 63 (`sympy__sympy-23413`), Sample 3 offset 7 (`django__django-11206`), and Sample 3 offset 62 (`sympy__sympy-23413`). Test setup checked out files also modified by the agent, so the complete agent patch was not proven active at test time. The observed test results **must not** be interpreted as validated PASS/FAIL outcomes.
- **Skipped-test cases** include database-dependent Django tests; a zero-failure report with skipped strengthened tests is not an unqualified PASS under this audit protocol.
- **FAIL labels remain provisional** until the augmented assertions themselves have been checked for correctness and relevance; observed failures alone do not establish semantic incorrectness.

### Audit corrections

The automatic collector cannot reliably parse every Django, SymPy, Sphinx/tox, nested pytest, or warning-heavy output. Among the **115 newly audited** runs, manual raw-runner review corrected **38 collector UNVERIFIED → PASS**, **7 collector UNVERIFIED → FAIL**, and **1 collector FAIL → UNVERIFIED** due to a patch-identity problem. These are auditing corrections, **not** newly executed benchmark tasks.

### Step 6 — enhanced-test validity review (documentary, not new labels)

All **31 provisional FAILs across 15 unique task IDs** were compared against [the raw per-run failure evidence and the original upstream issue/PR text](results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md). Review dispositions: **9 issue-supported** (`valid_failure`, still provisional), **4 problematic tests** (`invalid_test`), **2 environment-sensitive**, **16 unresolved**. The raw [v2 cumulative CSV](results/2026-11-12/sweabs_full_198_cumulative_v2.csv) remains **153 PASS / 31 FAIL / 14 UNVERIFIED**; **no agent was relabeled PASS** based on a test-validity concern.

Significant caveats: the Django RFC850 2099→2100 test expectation conflicts with [RFC 7231's 50-year rule](https://www.rfc-editor.org/rfc/rfc7231.html#section-7.1.1.1), an enhanced SymPy determinant test requires an auxiliary tolerance API not established by [the reported pivot bug](https://github.com/sympy/sympy/pull/13877), and two Django ModelForm tests use [Python-version-sensitive `staticmethod` behavior](https://docs.python.org/3/library/functions.html#staticmethod).

Full sources and counterarguments: [31-row review ledger](results/2026-11-12/STEP6_FAIL_REVIEW_31.csv) · [15-task summary](results/2026-11-12/STEP6_TASK_SUMMARY_15.csv) · [detailed review report](results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md). These are **documentary review judgments**, not publication-ready semantic correctness labels.

## Dataset and reproducibility

| Component | Frozen source |
| --- | --- |
| Agent trajectories and submitted patches | [tarsur385/swe-verified-gemini3-flash-trajectories](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories) |
| Agent dataset revision (newly audited runs) | `b5515d1dce40036633293b70477f0633b24593f7` |
| Strengthened test dataset | [OpenAgentLab/SWE-Bench_Verified_ABS](https://huggingface.co/datasets/OpenAgentLab/SWE-Bench_Verified_ABS) |
| Strengthened test dataset revision (newly audited runs) | `79fc07a8f4ce5e3720e069948073f5f910b7577b` |
| Evaluation harness | [OpenAgentEval/SWE-ABS](https://github.com/OpenAgentEval/SWE-ABS), pinned to `26b4c736ca3d566d8395d7999304d0264abe7992` |
| Runtime | GitHub-hosted Docker-capable runners; one patch per evaluation job, max 2 concurrent jobs per workflow run |

The [pilot selection script](scripts/pilot.py) filters `resolved=True` for each sample, sorts by `instance_id`, rejects duplicate IDs *within that sample*, and creates a plan for up to 10 exact patches per dispatch. It records the sample/index/instance, dataset revisions, patch SHA-256, test patch SHA-256, base commit, and harness revision.

The workflow evaluates the exact submitted patch against the task's strengthened test record. The initial smoke-test issue—one patch fallback accidentally reversing an already-applied patch—was addressed in [`scripts/patch_harness.py`](scripts/patch_harness.py). This fix was verified in the [smoke-test workflow](.github/workflows/sweabs-smoke.yml), including `astropy__astropy-12907` with 11 augmented tests passed.

### Audit protocol

For each newly audited per-patch artifact:

1. Check `sample`, `offset`, `instance_id`, submitted patch hash, original `resolved` flag, frozen dataset revisions, base commit, and run ID.
2. Recompute prediction/test-patch SHA-256; inspect patch application, the actual pre-test repository diff, test-patch placement, and any later cleanup that may have removed part of the model patch.
3. Read the **outer** augmented test runner summary in raw `test_output.txt`, including Django, pytest, nested pytest, Sphinx/tox, and SymPy formats; distinguish executed PASS/FAIL/ERROR from SKIP and infrastructure failure.
4. Assign a conservative provisional label; keep test-validity or missing-coverage problems flagged rather than inventing a definitive outcome.

The **existing 83 earlier rows** were not rechecked in the most recent 115-run raw-log pass.

## Workflows and evidence

- [Batch evaluation workflow](.github/workflows/sweabs-pilot.yml) — manual `workflow_dispatch` inputs: `sample` (1–3), `offset` (zero-based), `count` (1–10).
- [Smoke-test workflow](.github/workflows/sweabs-smoke.yml) — harness smoke validation.
- [GitHub Actions history](https://github.com/Foysal-Munsy/sweabs-free-eval/actions) — source logs, frozen selection manifests, individual patch evidence, and per-batch summary artifacts.

Batch run index (2026-11-12, new audits):

| Subset | Offsets and GitHub Actions runs |
| --- | --- |
| Sample 2 | [20–29](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181184322), [30–39](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699), [40–49](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181336920), [50–59](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181340403), [60–67](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181346009) |
| Sample 3 | [0–9](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182603318), [10–19](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182697559), [20–29](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182701126), [30–39](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182706543), [40–49](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182715959), [50–59](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182719908), [60–66](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182738449) |

For automation convenience, the pilot also supports narrowly scoped push-trigger manifests `.github/sweabs-sample2-batch.json` and `.github/sweabs-sample3-batch.json` from the completed batch campaign. **Do not edit these to rerun tasks unintentionally.** Manual `workflow_dispatch` remains available for deliberate reruns.

**Evidence retention:** The GitHub Actions workflow retains temporary artifacts for **14 days**. The principal audited evidence has therefore been archived with verified original bytes in [**results/2026-11-12/**](results/2026-11-12/MANIFEST.md):

- [**Current 198-run provisional cumulative CSV (v2)**](results/2026-11-12/sweabs_full_198_cumulative_v2.csv) — **153 PASS, 31 FAIL, 14 UNVERIFIED**; [archived v1](results/2026-11-12/sweabs_full_198_cumulative_audited.csv) preserved
- [Historical 83-run raw audit evidence](results/2026-11-12/sweabs_historical_83_reaudit_evidence.csv), [correction ledger](results/2026-11-12/sweabs_historical_83_corrections.csv), and [reconciliation report](results/2026-11-12/STEP5_RECONCILIATION_REPORT.md)
- [115-run raw-audit provenance CSV](results/2026-11-12/sweabs_samples2_3_full_audit_evidence_115.csv)
- [Full audit report](results/2026-11-12/sweabs_full_198_audit_report.md)
- [Earlier 83-row snapshot](results/2026-11-12/sweabs_samples1_2_first83_cumulative.csv) and [historical audit script](results/2026-11-12/sweabs_full_audit.py)

A 5.1-MB raw-evidence ZIP for the original recent audits and a separate **2.8-MB historical 83-run raw archive** (including the earlier failed offset-5 attempt) were independently checksum-verified after retrieval from the owner's **private ChatGPT Library**. **Neither is publicly downloadable from this GitHub repository.** Nested test fixtures/logs include email-like and password-like strings; public release requires additional screening. See the [artifact manifest](results/2026-11-12/MANIFEST.md) for checksums, exact scope, and access limitations.

## Next research steps

- [x] Collect 198 originally passing agent runs across three samples.
- [x] Complete 198 strengthened-test evaluation attempts.
- [x] Produce a cumulative **provisional** audit CSV and detailed raw-evidence report.
- [x] **Archive the provisional cumulative CSV, provenance, report, historical input and audit script**, preserving original bytes; keep the raw ZIP in a checksum-verified private Library archive (not a public release).
- [x] **Reconcile the 83 historical rows** against raw GitHub Actions evidence, retain original v1, and document the one patch-identity correction in a reviewed v2.
- [x] **Document an AI-assisted semantic validity review for all 31 FAILs across 15 tasks**, with evidence-backed dispositions, opposing interpretations, and open questions; no raw label changes.
- [ ] Seek independent/human issue-specific confirmation for unresolved or environment-sensitive FAIL tests before claiming final semantic correctness.
- [ ] **Step 7 (next): Triage 14 UNVERIFIED cases and freeze analysis labels**, with explicit exclusion/sensitivity policies for the Step 6 review; prioritize four patch-overlap cases and skipped/backend-limited tests. Any rerun must preserve original evidence.
- [ ] Freeze a reviewed label manifest with explicit exclusions/uncertainty, then match each exact run/patch with **predefined, frozen trajectory messiness indicators**.
- [ ] Perform task-aware predictive analysis (including repeated-instance dependence), uncertainty checks, and robustness/sensitivity analyses; only then write up the paper.

**No predictive result is claimed yet.** The research question is still open.

## Progress / README maintenance

Update this README **in the same work session as each substantive change** to the evaluation data, label policy, or experiment phase. In particular, keep the status table, limitations, links to reproducible artifacts, and next-step checklist synchronized with the checked-in evidence. Do not mark provisional findings as final, and do not imply that work continues automatically when no audit session is active.
