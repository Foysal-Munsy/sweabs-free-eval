# SWE-ABS Free Evaluation

Reproducible GitHub Actions evaluation of **coding-agent patches that originally passed SWE-bench Verified** against **SWE-ABS strengthened tests**.

> **Research question:** Among originally successful coding-agent trajectories, do lightweight trajectory-level messiness indicators predict failure under strengthened tests?

This repository now covers **strengthened-test evaluation, exact-match trajectory feature extraction, and exploratory task-aware AUROC analysis**. A validated classifier, independently adjudicated semantic labels, external/generalization testing, and paper writing have **not** been completed. The outcomes below remain *provisional augmented-test labels*, not final correctness judgments.

### Project continuity and research handoff

This README is the **public summary**. For a precise human/AI continuation point, use [**PROJECT_STATE.md**](docs/PROJECT_STATE.md) (milestones, current snapshot, unresolved issues, next exact action) and [**WORK_LOG.md**](docs/WORK_LOG.md) (dated, evidence-backed work history). Coding/research agents should start with [**AGENTS.md**](AGENTS.md).

> The repository and the linked handoff documents are public. Operational details belong in the handoff docs, but secrets and sensitive/private data do not. These records must be updated together when the verified research state changes.

## Research status — 2026-11-12

**Milestone: all 198 stronger-test attempts and audits complete; Step 8 indicators frozen before extraction, Step 9 features exactly matched, and Step 10 exploratory AUROCs computed.** Step 6 reviewed the 31 FAILs and Step 7 retained 14 UNVERIFIED with explicit provisional analysis screens. None is an independent human/maintainer semantic oracle. **Step 11 technical reproduction and task-aware robustness now PASS; independent semantic validity/coverage review remains the current unfinished gate.**

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

## Step 7 — UNVERIFIED triage and analysis eligibility (documentary/provisional)

The [Step 7 report](results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md) and [14-case ledger](results/2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv) classify the **14 existing UNVERIFIED runs** as **9 skipped-test/partial-backend-coverage, 4 agent-patch/strengthened-test-file overlap, and 1 unverified entire large patch**. All 14 expected GitHub Actions artifacts were listed as present and unexpired when checked on 2026-11-12. **No runner v2 label was revised, no task was rerun, and individual ZIPs were not freshly re-audited in Step 7.**

A [versioned 198-row analysis-label manifest](results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv) retains every exact run identity, raw outcome, review status, triage, exclusion rule, GitHub evidence link and four prespecified target scenarios; the [rebuild/check script](scripts/build_step7_analysis_labels.py) asserts the expected joins and row counts. The screening policies were documented before any trajectory indicators were extracted.

| Analysis target (0=audited PASS, 1=provisional FAIL) | 0 | 1 | Excluded |
| --- | ---: | ---: | ---: |
| **Conservative primary** (PASS vs review-supported FAIL) | **153** | **9** | **36** |
| Noninvalid-test sensitivity (includes unresolved/environment-sensitive FAIL) | 153 | 27 | 18 |
| All-raw-runner sensitivity (includes disputed failing assertions) | 153 | 31 | 14 |
| Hypothetical skipped-as-PASS sensitivity (not a genuine runner PASS) | 162 | 9 | 27 |

The **primary screen has 162 runs representing 61 distinct tasks, but just 9 FAIL runs across 5 tasks**. Its review-supported FAILs remain provisional, and the excluded cases are **not** relabeled PASS. Any later analysis must group by task, report uncertainty and compare sensitivity definitions. This work does not establish a trajectory-messiness predictor.

## Steps 8–10 — frozen trajectory indicators and provisional quantitative analysis

**Step 8:** [Versioned indicator/analysis specification](docs/STEP8_FROZEN_INDICATORS_v1.md) was committed before all-run feature extraction. Four prespecified messiness proxies: exact duplicate terminal command rate, explicitly observed terminal errors, absence of a recognized verification command, and file-editor calls after the last recognized verification. These are *proxies*, not proof of blind retries or substantive verification.

**Step 9:** [198-run exact-match features](results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv) and [coverage](results/2026-11-12/STEP9_COVERAGE_v1.json) were computed from the pinned [trajectory dataset](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories). The queried dataset revision matched pinned `b5515d1dce40036633293b70477f0633b24593f7`; all 198 originally successful runs matched their sample, instance and **patch SHA-256** among 296 dataset rows. There are 73 distinct tasks; 191 runs contain at least one recognized verification command. No raw private trajectory text was published. [Extractor](scripts/step9_extract_trajectory_features.py) and pinned independent Python `--check` [GitHub Actions run #43260088649](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649) are now independently verified, including 198/198 exact-match patches.

**Step 10:** Frozen individual features were evaluated against four Step 7 outcome screens using in-sample AUROCs and 500 **task-ID-cluster** bootstrap resamples. The conservative primary has **153 runner PASS, 9 review-supported provisional FAIL, 36 excluded**: 162 runs, 61 distinct tasks, only five distinct FAIL task IDs.

| Prespecified feature (higher = more presumed messiness) | Primary AUROC | 95% task-cluster interval |
| --- | ---: | --- |
| Duplicate terminal commands / terminal calls | **0.489** | 0.270–0.706 |
| Explicit terminal error rate | **0.599** | 0.420–0.790 |
| Missing recognized verification | **0.480** | 0.459–0.497 |
| Editor calls after last recognized verification | **0.435** | 0.166–0.757 |

The **same duplicate-command feature** has AUROC **0.721** against noninvalid-test sensitivity labels and **0.708** against all provisional raw runner FAILs. This outcome-policy sensitivity is the most important finding: the **primary dataset does not establish a reliable predictor**, while broader ambiguous labels show a potential association that requires further validity checks. The 95% intervals quantify resampling variability conditional on this sample; they do not establish statistical significance or external generalization.

[Full Step 10 report and competing interpretations](results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md) · [Corrected task-cluster AUROC results v2](results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) · [Analysis script](scripts/step10_analyze_frozen_features.py).

**Reproducibility correction:** The originally archived [Step 10 JSON v1](results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v1.json) contains **invalid degenerate bootstrap confidence intervals** caused by a low-bit PRNG sampling defect; it is preserved for provenance, **not** for use in claims. Corrected v2 retains the original indicators, labels and point estimates. The archived Step 9–11 Python code now passes independent [GitHub Actions verification](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649); no semantic test-validity oracle has been established.

## Step 11 — independently reproduced, semantic validity still open

The read-only [GitHub Actions Step 11 workflow](.github/workflows/step11-reproduction.yml) **passed** on [run #43260088649](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649), from a clean checkout with Python 3.11.18, pinned `datasets==4.8.5` and `huggingface_hub==1.33.0`. It successfully reproduced all 198 exact-match features (296 source trajectories), the corrected Step 10 analysis, task-aware Step 11 robustness, five synthetic unit tests and **12 raw-trajectory event recounts (168 feature checks, zero mismatches)**. The Step 9 Django regex escaping was repaired as a versioned implementation fix without changing frozen Step 8 semantics or any archived feature row.

**Exploratory robustness:** The primary duplicate-command AUROC **0.489** becomes **0.522** when collapsing unanimous-label runs by task and **0.390** for within-project cross-task comparisons; removing any single primary positive task yields **0.382–0.620**, reflecting the **five positive task IDs**. Broader all-runner-FAIL sensitivity has run-level **0.708**, task-level **0.741**, within-project **0.738**, and positive-task omission range **0.683–0.759**. These checks were added after seeing Step 10 results, so they are **post-hoc stress tests, not confirmatory or held-out predictive evidence**. [Full Step 11 report](results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md) · [task-aware data](results/2026-11-12/STEP11_EXPLORATORY_ROBUSTNESS_v1.json) · [12-trace audit](results/2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json).

**Unfinished Step 11 semantic validity gate:** 16 unresolved and 2 environment-sensitive FAIL reviews, invalid enhanced tests and 14 UNVERIFIED runner outcomes still need independent adjudication/controlled evidence or explicit limitation decisions. Their old v2/Step 7 labels were NOT modified. **No final semantic validity, reliable classifier, external generalization, or journal submission readiness is claimed.**

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
- [x] **Step 7: Triage all 14 UNVERIFIED and freeze provisional analysis eligibility/sensitivity rules**, preserving raw labels; publish the [Step 7 report](results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md), [14-case ledger](results/2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv), and [198-row label manifest v1](results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv). No oracle adjudication or fresh benchmark run.
- [x] **Step 8:** Commit [frozen indicator specification](docs/STEP8_FROZEN_INDICATORS_v1.md) before extracting trajectory features.
- [x] **Step 9:** Extract and exact-match all 198 run features with pinned patch hashes; [coverage table](results/2026-11-12/STEP9_COVERAGE_v1.json); independent Python reproduction pending.
- [x] **Step 10:** Compute four prespecified individual-indicator AUROCs under four label screens, task-cluster intervals and [limitations](results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md) — **exploratory, not a validated predictor**.
- [x] **Step 11 technical gates:** Independently reproduced pinned Python feature extraction, Step 10 AUROCs, task-aware exploratory robustness, and 12 selected raw-message spot checks (168 checks, 0 discrepancies) in [successful CI](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649).
- [ ] **Step 11 semantic gate (NEXT):** Resolve/document unresolved strengthened-test validity and backend coverage issues before claiming substantive reliability prediction.
- [ ] Perform task-aware predictive analysis (including repeated-instance dependence), uncertainty checks, and robustness/sensitivity analyses; only then write up the paper.

**Only preliminary in-sample descriptive AUROCs are reported; no validated predictive performance, reliable semantic ground truth, or causal relationship is claimed.** The research question remains open.

## Progress / README maintenance

Update this README **in the same work session as each substantive change** to the evaluation data, label policy, or experiment phase. In particular, keep the status table, limitations, links to reproducible artifacts, and next-step checklist synchronized with the checked-in evidence. Do not mark provisional findings as final, and do not imply that work continues automatically when no audit session is active.
