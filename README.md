# SWE-ABS Free Evaluation

Reproducible GitHub Actions evaluation of **coding-agent patches that originally passed SWE-bench Verified** against **SWE-ABS strengthened tests**.

> **Research question:** Among originally successful coding-agent trajectories, do lightweight trajectory-level messiness indicators predict failure under strengthened tests?

This repository covers the **stronger-test evaluation and evidence collection stage**. Trajectory indicator extraction, predictive analysis, and paper writing have **not** been completed. The outcomes below are *provisional augmented-test labels*, not final semantic-correctness judgments.

### Project continuity and research handoff

This README is the **public summary**. For a precise human/AI continuation point, use [**PROJECT_STATE.md**](docs/PROJECT_STATE.md) (milestones, current snapshot, unresolved issues, next exact action) and [**WORK_LOG.md**](docs/WORK_LOG.md) (dated, evidence-backed work history). Coding/research agents should start with [**AGENTS.md**](AGENTS.md).

> The repository and the linked handoff documents are public. Operational details belong in the handoff docs, but secrets and sensitive/private data do not. These records must be updated together when the verified research state changes.

## Research status — 2026-11-12

**Milestone: all 198 evaluation attempts have run; the cumulative evidence audit is complete at the provisional-label level.**

| Subset | Originally passing agent runs | Evaluation attempts | PASS | FAIL | UNVERIFIED |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sample 1 | 63 | 63 | 48 | 11 | 4 |
| Sample 2 | 68 | 68 | 53 | 11 | 4 |
| Sample 3 | 67 | 67 | 52 | 10 | 5 |
| **Total** | **198** | **198** | **153** | **32** | **13** |

- **PASS:** The audited strengthened-test runner passed the executed augmented tests, with required patch identity and coverage checks met.
- **FAIL:** The strengthened-test runner exhibited test failure or functional test exception with the intended patch present; **all 32 labels remain subject to independent augmented-test-validity review**.
- **UNVERIFIED:** Coverage was incomplete, the exact patch under test could not be established, or another validity check was unresolved. **Never count these as FAIL, or silently drop them from reporting.**
- **GitHub Actions job success is not patch PASS.** Workflow jobs upload evidence even when the model patch fails augmented tests.

The 115 new Sample 2 (offsets 20–67) and Sample 3 (offsets 0–66) records were audited using per-patch ZIPs and raw logs on 2026-11-12. The 83 earlier records (all Sample 1 and Sample 2 offsets 0–19) were **preserved**, not independently re-audited in that last pass. Results should therefore remain explicitly provisional.

**Unit of observation:** an agent run defined by `(sample, instance_id, patch_sha256)`. The 198 records contain **73 distinct instance IDs**; tasks repeat across samples. A later model/association analysis must account for repeated tasks and must not treat 198 records as independent task identities.

### Known audit limitations

- **13 UNVERIFIED total:** 4 in Sample 1, 4 in Sample 2, 5 in Sample 3. Causes include skipped database-dependent tests, incomplete coverage/patch-diff checks, and patch/test-file overlap.
- **Three recently audited patch-overlap cases:** Sample 2 offset 63 (`sympy__sympy-23413`), Sample 3 offset 7 (`django__django-11206`), and Sample 3 offset 62 (`sympy__sympy-23413`). Test setup checked out files also modified by the agent, so the complete agent patch was not proven active at test time. The observed test results **must not** be interpreted as validated PASS/FAIL outcomes.
- **Skipped-test cases** include database-dependent Django tests; a zero-failure report with skipped strengthened tests is not an unqualified PASS under this audit protocol.
- **FAIL labels remain provisional** until the augmented assertions themselves have been checked for correctness and relevance; observed failures alone do not establish semantic incorrectness.

### Audit corrections

The automatic collector cannot reliably parse every Django, SymPy, Sphinx/tox, nested pytest, or warning-heavy output. Among the **115 newly audited** runs, manual raw-runner review corrected **38 collector UNVERIFIED → PASS**, **7 collector UNVERIFIED → FAIL**, and **1 collector FAIL → UNVERIFIED** due to a patch-identity problem. These are auditing corrections, **not** newly executed benchmark tasks.

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

**Evidence retention warning:** GitHub Actions artifacts are retained for **14 days** by this workflow. Full audited outputs currently exist as separately prepared research files but **have not yet been checked into this repository**:

- `sweabs_full_198_cumulative_audited.csv` — 198 provisional labels.
- `sweabs_samples2_3_full_audit_evidence_115.csv` — source-level audit evidence for 115 newly reviewed attempts.
- `sweabs_full_198_audit_report.md` — detailed findings and unresolved cases.
- `sweabs_full_audit_evidence_bundle.zip` — offline snapshot of Sample 2/3 per-patch evidence, audit report, and script.

Archiving these deliverables in version-controlled storage or a release is an immediate reproducibility priority; until then, this README is a **status record**, not a substitute for the underlying files.

## Next research steps

- [x] Collect 198 originally passing agent runs across three samples.
- [x] Complete 198 strengthened-test evaluation attempts.
- [x] Produce a cumulative **provisional** audit CSV and detailed raw-evidence report.
- [ ] **Archive and version the cumulative CSV, audit provenance, report, and evidence bundle** before artifacts expire. Verify their checksums and reconcile any earlier audit caveats.
- [ ] **Validate the 32 provisional FAIL cases** against the intended behavior and strength/relevance of each added test; distinguish genuine counterexamples from invalid or environment-sensitive assertions.
- [ ] **Triage 13 UNVERIFIED cases**: prioritize exact-patch preservation for the three overlap cases and skipped-test/backend limitations; rerun only with controlled, documented fixes, keeping original results.
- [ ] Freeze a reviewed label manifest with explicit exclusions/uncertainty, then match each exact run/patch with **predefined, frozen trajectory messiness indicators**.
- [ ] Perform task-aware predictive analysis (including repeated-instance dependence), uncertainty checks, and robustness/sensitivity analyses; only then write up the paper.

**No predictive result is claimed yet.** The research question is still open.

## Progress / README maintenance

Update this README **in the same work session as each substantive change** to the evaluation data, label policy, or experiment phase. In particular, keep the status table, limitations, links to reproducible artifacts, and next-step checklist synchronized with the checked-in evidence. Do not mark provisional findings as final, and do not imply that work continues automatically when no audit session is active.
