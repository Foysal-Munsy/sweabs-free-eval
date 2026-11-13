# Research Project State — SWE-ABS Free Evaluation

> **Canonical human/AI handoff document.** Read this before continuing work.  
> **Last state verification:** 2026-11-13 (Asia/Dhaka)  
> **Current phase:** **Steps 1–12 DONE at their explicitly limited exploratory runner-association scopes; Step 12 eight preselected qualitative case studies and independent 8/8 raw-trajectory recount (112 comparisons, 0 mismatches) verified in CI. Step 13 Overleaf-compatible full-section manuscript draft v0.1 COMMITTED; scientific review and reproducible PDF build gates underway, so Step 13 IN PROGRESS. Step 14 reproducibility/submission audit TODO.** The original 198-run v2 **153 PASS / 31 FAIL / 14 UNVERIFIED** and frozen Step 7 primary **153/9/36** remain unchanged. **Independent human/maintainer semantic ground truth and original Docker-tested-tree equivalence remain UNVERIFIED**; Step 11 closure **is not** proof of a reliable semantic-defect detector or journal submission readiness. [Authoritative closure decision](../results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md) · [read-only reconciliation CI #43276679251](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43276679251).  
> **Project repository:** https://github.com/Foysal-Munsy/sweabs-free-eval  
> **This is a public repository:** this document is not private. Never add passwords, access tokens, personal information, or unreleased sensitive material.

## 0. Quick resume (read in order)

1. Read this entire file, especially **Current snapshot**, **Next exact action**, and **Do not change**.
2. Read [WORK_LOG.md](WORK_LOG.md) for the latest completed session and [../README.md](../README.md) for the public project overview.
3. Inspect the current GitHub files and [Actions history](https://github.com/Foysal-Munsy/sweabs-free-eval/actions) **before** treating this snapshot as live; the repository may have changed since the date above.
4. For any label update, check the underlying per-patch evidence. Do **not** infer patch PASS from the GitHub workflow's green status.
5. Do the **first unchecked milestone** below, then update this file, append a source-backed entry to WORK_LOG, and reconcile the public README in the **same work session**.

If resuming in a new chat, give the assistant the repository URL and ask it to read `AGENTS.md`, `docs/PROJECT_STATE.md`, and `docs/WORK_LOG.md` first. Chat access to repository files must still be established in that session; documents are not self-executing.

## 1. Research identity and frozen scope

**Research question:** Among coding-agent runs that pass the original evaluation, do simple, lightweight trajectory-level messiness indicators predict failure under SWE-ABS strengthened tests?

**Study design:** Select originally resolved Gemini 3 Flash SWE-bench Verified agent runs, preserve the exact agent patch identity, evaluate those patches on corresponding SWE-ABS strengthened tests, then **later** compute frozen trajectory-process indicators and test their association with strengthened-test outcomes.

**Primary observation identity:** `(sample, instance_id, patch_sha256)`, not instance ID alone. A task can appear in more than one sample. The current 198-row cumulative CSV reports **73 distinct instance IDs**; use task-aware inference, not a naive assumption of 198 independent tasks.

**Sources and implementation:**
- Agent dataset: [tarsur385/swe-verified-gemini3-flash-trajectories](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories)
- Stronger-test dataset: [OpenAgentLab/SWE-Bench_Verified_ABS](https://huggingface.co/datasets/OpenAgentLab/SWE-Bench_Verified_ABS)
- Pinned harness: [SWE-ABS](https://github.com/OpenAgentEval/SWE-ABS), commit `26b4c736ca3d566d8395d7999304d0264abe7992`
- Exact selection/collection logic: [scripts/pilot.py](../scripts/pilot.py)
- Patch fallback correction: [scripts/patch_harness.py](../scripts/patch_harness.py)
- Current evaluation workflow: [.github/workflows/sweabs-pilot.yml](../.github/workflows/sweabs-pilot.yml)
- Relevant frozen dataset revisions for newly audited records (from the [README](../README.md)): agent `b5515d1dce40036633293b70477f0633b24593f7`; SWE-ABS test data `79fc07a8f4ce5e3720e069948073f5f910b7577b`. Verify revision fields in each artifact instead of assuming historical runs share them.

### Do not change without recording a methodological amendment

- Do not change the research question based on results.
- Do not change indicator definitions after seeing their association with FAIL labels.
- Do not modify original run rows, patch hashes, test revisions, or old raw evidence silently.
- Do not collapse UNVERIFIED into FAIL; distinguish runner outcomes from semantic validity.
- Do not equate workflow/job success with strengthened-test PASS.
- Do not start trajectory feature extraction or write results claims before the outcome-label validation gate is documented.
- Do not edit `.github/sweabs-sample2-batch.json` or `.github/sweabs-sample3-batch.json` casually: they are wired to push-triggered evaluation.
- Do not make unverified claims: link the file, run, commit, log, or paper for each research fact; write **unverified** where evidence is missing.

## 2. Current snapshot (provisional, 2026-11-12)

| Sample | Originally passing runs | Evaluated | Provisional PASS | Provisional FAIL | UNVERIFIED |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 63 | 63 | 48 | 10 | 5 |
| 2 | 68 | 68 | 53 | 11 | 4 |
| 3 | 67 | 67 | 52 | 10 | 5 |
| **Total** | **198** | **198** | **153** | **31** | **14** |

**What is established:** all 198 evaluation attempts completed. The cumulative provisional audit CSV has 198 rows with unique `(sample, offset)` and 73 distinct task IDs. Full raw-log checking was performed for **115 recent records** (Sample 2 offsets 20–67 and Sample 3 offsets 0–66), followed by a separate **83-run historical re-audit** (Sample 1 offsets 0–62 and Sample 2 offsets 0–19). Historical 83-row v1 values were preserved unmodified in the immutable checkpoint. Step 5 produced [the current 198-row v2](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv), with exactly one documented historical correction, and [an append-only corrections ledger](../results/2026-11-12/sweabs_historical_83_corrections.csv).

**What is NOT established:** final patch semantic correctness, an adjudicated outcome for the 16 unresolved or 2 environment-sensitive Step 6 reviews, comprehensive strength/soundness of every augmented assertion, the predictive value of messiness indicators, or final publication-ready results. Step 6 compared original issue and verified upstream PR descriptions to enhanced assertions and raw logs but did **not** rerun task-specific oracles or receive independent maintainer/human judgments.

**Outstanding validity concerns:**
- **31 provisional FAIL across 15 distinct instance IDs:** [Step 6 AI-assisted documentary validity review](../results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md) completed with **9 review-supported valid_failure, 4 invalid_test, 2 environment_sensitive, 16 unresolved** dispositions. These are review statuses, not revised v2 outcomes, not independent human oracle proof, and not grounds to silently relabel raw FAIL.
- **14 UNVERIFIED across 6 distinct instance IDs:** [Step 7 triage](../results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md) documented **9 partial-coverage skips, 4 patch/test-file overlaps, 1 whole-patch-integrity gap**; all remain UNVERIFIED in runner v2, excluded from primary labels, and require distinct follow-up evidence.
- **4 exact-patch overlap cases:** Sample 1 offset 58 (`sympy__sympy-23413`, newly corrected FAIL → UNVERIFIED), Sample 2 offset 63 (`sympy__sympy-23413`), Sample 3 offset 7 (`django__django-11206`), Sample 3 offset 62 (`sympy__sympy-23413`). Augmented-test setup/cleanup reset a test file also modified by the agent; complete patch preservation was not established. Do not treat their observed raw runner outcomes as exact-patch PASS/FAIL.
- Skipped database/backend tests include some Django cases. A PASS for the executed subset is **not** full-coverage verification if required augmented tests were skipped.

**Evidence:** [audited workflow history](https://github.com/Foysal-Munsy/sweabs-free-eval/actions), [current public README](../README.md), and the offline audit files in the inventory below. The **198-row CSV, 115-row provenance CSV, audit report, historical 83-row input, and audit script are now archived on GitHub** with verified original bytes. Two private raw evidence ZIPs are backed up in the owner's ChatGPT Library: the prior 5.1-MB Sample 2/3 bundle, and the new 2.8-MB historical 83-run ZIP (plus the initial failed Sample 1 offset-5 attempt). Neither is publicly accessible from GitHub. See the [artifact manifest](../results/2026-11-12/MANIFEST.md).

## 3. Full milestone checklist (order matters)

Legend: **DONE** = completed to stated scope, **PROVISIONAL** = complete as a provisional evidence milestone, **NEXT** = first unfinished step, **TODO** = not completed. Do not convert the checklist into a percentage of the entire research project.

| # | Milestone | Status | Completion gate / artifact |
| --- | --- | --- | --- |
| 1 | Research question and data selection | DONE | Originally passing Gemini 3 Flash trajectories, SWE-ABS tests, fixed evaluation setup |
| 2 | Run strengthened evaluations | DONE | 63 + 68 + 67 = 198 evaluation attempts |
| 3 | Audit runner outputs | PROVISIONAL | 198-run v2 provisional CSV; all 115 recent and all 83 historical raw artifacts checked; independent augmented-test semantics pending |
| 4 | Preserve evidence and provenance | **DONE — PRIVATE RAW ZIP** | [Versioned GitHub audit files and checksums](../results/2026-11-12/MANIFEST.md); original raw ZIP re-downloaded from private Library and SHA-256/ZIP-integrity verified; not public |
| 5 | Reconcile earlier audit records | **DONE** | All 83 per-patch ZIPs checked; [report](../results/2026-11-12/STEP5_RECONCILIATION_REPORT.md), [83-row evidence](../results/2026-11-12/sweabs_historical_83_reaudit_evidence.csv), [one correction](../results/2026-11-12/sweabs_historical_83_corrections.csv), [current v2 CSV](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv) |
| 6 | Review strengthened-test FAIL assertions | **DONE — DOCUMENTARY, PROVISIONAL** | [31-row review ledger](../results/2026-11-12/STEP6_FAIL_REVIEW_31.csv), [15-task summary](../results/2026-11-12/STEP6_TASK_SUMMARY_15.csv), [reasoned report with opposing views](../results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md); 9 supported / 4 invalid-test / 2 environment-sensitive / 16 unresolved, no outcome relabel |
| 7 | **Triage UNVERIFIED and freeze analysis labels** | **DONE — DOCUMENTARY / PROVISIONAL** | [14-case triage](../results/2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv), [versioned 198-row provisional label manifest](../results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv), [methodological report](../results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md), [rebuild/check script](../scripts/build_step7_analysis_labels.py). No runner v2 relabel or new test run; final semantic validation pending. |
| 8 | Freeze trajectory messiness indicator specification | **DONE — FROZEN v1** | [Precommitted exact feature/analysis specification](STEP8_FROZEN_INDICATORS_v1.md), [extractor](../scripts/step9_extract_trajectory_features.py); committed before any full extraction/association. |
| 9 | Extract trajectory features and exact-match | **DONE — CI REPRODUCED** | [198-run feature table](../results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv), [coverage](../results/2026-11-12/STEP9_COVERAGE_v1.json); 198/198 exact SHA IDs across 296 rows (73 tasks); independent pinned HF/Python [CI run #43260088649](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649) PASS. |
| 10 | Quantitative analysis | **DONE — EXPLORATORY/PROVISIONAL** | [Quantitative report](../results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md), [corrected task-bootstrap JSON v2](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json), [Python analysis script](../scripts/step10_analyze_frozen_features.py). Prespecified four univariate AUROCs × four label policies with 500 task-cluster resamples; preliminary v1 bootstrap defects documented. |
| 11 | **Independent reproduction, robustness and validity** | **DONE — BOUNDED RUNNER-ASSOCIATION SCOPE ONLY** | [Formal Step 11 closure & limitations](../results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md), [exact-run controlled evidence freeze](../results/2026-11-12/STEP11_CONTROLLED_EVIDENCE_FREEZE_v1.json), [successful evidence reconciliation CI #43276679251](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43276679251). 9 PostgreSQL run checks, 4 non-destructive overlapping-patch tests, 1 full 74-file Requests reconstruction; no source labels changed. **Gold semantic oracle, independent adjudication of 16 unresolved/2 environment-sensitive FAIL and external predictor validation NOT completed; publication claim must explicitly be bounded.** |
| 12 | **Qualitative case studies and interpretation** | **DONE — FIXED ILLUSTRATIVE SCOPE** | [Precommitted selection protocol](STEP12_CASE_SELECTION_PROTOCOL_v1.md) before case inspection; [eight exact-run roster](../results/2026-11-13/STEP12_CASE_ROSTER_v1.json), [case/counterexample report](../results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md), [8-source/112-field audit](../results/2026-11-13/STEP12_SOURCE_RECOUNT_8_v1.json) and successful [CI #43440488895](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43440488895). Selection is illustrative, not a new validated predictor. |
| 13 | **Draft research paper** | **IN PROGRESS** | [Full-section IEEEtran manuscript draft](../paper/main.tex), [verified initial bibliography](../paper/references.bib), [claim-to-evidence ledger](../paper/CLAIM_EVIDENCE_MATRIX.md), [draft scientific scope](STEP13_MANUSCRIPT_SCOPE_v1.md), [read-only PDF build workflow](../.github/workflows/paper-latex-build.yml). Pending PDF verification, final source audit, author/mentor scientific review and AI disclosure sign-off. |
| 14 | Reproducibility and submission readiness | TODO | Code/data provenance, final figures/tables, checked citations, mentor feedback, venue-specific requirements |

**Current checkpoint:** **Steps 1–12 completed at their explicitly stated scopes**, including Step 11 source-pinned controlled follow-up and formal claim-bounding decision; Step 3 runner outcomes remain provisional. Original runner **198 = 153 PASS / 31 provisional FAIL / 14 UNVERIFIED**, frozen Step 7 conservative primary **153/9/36** (162 runs; only 5 positive task IDs); AUROC duplicate terminal rate **0.489** primary (95% task-cluster interval 0.270–0.706) vs **0.708** runner-only sensitivity, strongly label-policy-dependent. **Step 12 DONE within illustrative, raw-recount-verified scope; Step 13 NEXT; Step 14 TODO**. Human/maintainer semantic oracles and external validation remain unverified and must not be implied by the bounded Step 11 closure. [Closure report](../results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md).

## 4. Completed archival checkpoint — Step 4 (evidence preservation)

**Status: DONE for owner-accessible preservation, not a public raw-data release.** On 2026-11-12 the following files were committed to [the GitHub artifact directory](../results/2026-11-12/), read back, and checked for byte identity against the original outputs. The three principal files' SHA-256 digests were independently recomputed on the GitHub-fetched content.

| File | Original bytes | SHA-256 | Location |
| --- | ---: | --- | --- |
| `sweabs_full_198_cumulative_audited.csv` | 93852 | `7a848f2dfbbad224ea110a9d090ba4f2194ed157df7fd49d1946ae88743c6da8` | [GitHub](../results/2026-11-12/sweabs_full_198_cumulative_audited.csv) |
| `sweabs_samples2_3_full_audit_evidence_115.csv` | 132150 | `3e4218862ac500872b2645ad766835579e146e58b004e394031e8c9c707cb18f` | [GitHub](../results/2026-11-12/sweabs_samples2_3_full_audit_evidence_115.csv) |
| `sweabs_full_198_audit_report.md` | 11814 | `76559162321d9cab1e5fee4f9ad7bdba999a4379a0e38f651819f1571201ea07` | [GitHub](../results/2026-11-12/sweabs_full_198_audit_report.md) |
| `sweabs_samples1_2_first83_cumulative.csv` | 23453 | `919c137b315fbe8ba6e9cdbe9491222304a36f17e920ae05aa15f405ab08aea4` | [GitHub](../results/2026-11-12/sweabs_samples1_2_first83_cumulative.csv) |
| `sweabs_full_audit.py` | 15509 | `8f9061760eda1c8f4f6188a66bce4b6d6da24e75c7977be05a95ad0f719f74f9` | [GitHub](../results/2026-11-12/sweabs_full_audit.py) |

**Private raw ZIP:** `sweabs_full_audit_evidence_bundle.zip`, 5136675 bytes, SHA-256 `b7f5fd76f747a23a83fb5b2d5e2c355d6123c2e2c9ddfe6fea974b3ac3c73d99`. Archived in the owner's **personal ChatGPT Library**: `/Research/SWE-ABS/2026-11-12/sweabs_full_audit_evidence_bundle.zip`. It was materialized back to the analysis runtime, its SHA-256 matched, and ZIP integrity testing passed for its 140 entries. **This is not a public GitHub download and is not automatically available to an arbitrary chat/account.** It contains Sample 2 and 3 per-patch ZIPs; Sample 1 raw evidence remains outside this bundle.

**Privacy boundary:** Nested raw artifacts contain email-like and password-like strings in test data/logs. Automated scanning found no obvious GitHub PAT/AWS-key/private-key patterns, but this is not a comprehensive security audit. The raw ZIP was intentionally kept private. Public release remains a later, separately reviewed reproducibility decision.

**Source of truth for exact hashes and storage status:** [2026-11-12/MANIFEST.md](../results/2026-11-12/MANIFEST.md). No evaluation was rerun and no outcome labels were changed by archival. The archived offline audit script has session-specific paths; it is historical provenance, not a newly tested production tool.

## 4A. Completed Step 5 — historical 83-run reconciliation

**Completed on 2026-11-12.** Recovered all 83 historical selected GitHub Actions per-patch artifacts and the prior failed Sample 1 offset-5 artifact. Verified 83 original CSV records field-for-field against archived v1 (all identical), inspected each raw ZIP and model/test-patch identity, pinned revisions, base commits, pre/post repository diffs, outer runner counts, skips and infrastructure issues. Review details: [Step 5 report](../results/2026-11-12/STEP5_RECONCILIATION_REPORT.md) and [83-run evidence](../results/2026-11-12/sweabs_historical_83_reaudit_evidence.csv).

**82 existing labels unchanged; one correction:** Sample 1 offset 58, `sympy__sympy-23413`, **FAIL → UNVERIFIED**. Raw tests reported 7 passed and 1 exception; however, the exact agent-modified test file did not survive augmented-test file reset, so the complete intended patch was not verified. The original v1 CSV remains immutable, and [the corrections ledger](../results/2026-11-12/sweabs_historical_83_corrections.csv) explains the reclassification. Sample 1 offset 36, `psf__requests-1142`, remains UNVERIFIED despite 15 executed tests passing because the 884 KB patch's full source/build diff was not verified.

**Revised 198-run v2 totals:** 153 PASS, 31 FAIL, 14 UNVERIFIED. New sample-specific counts in the current snapshot above. The analysis unit still repeats 73 unique task IDs across 198 agent runs.

**Raw evidence privately preserved:** `sweabs_historical_83_raw_evidence_private.zip`, 2,790,331 bytes, SHA-256 `cc7c5f4280c3dd7e4ccfb34f55ea151f472435e33d1e7465fb73cf9c75c586e4`. Owner's private ChatGPT Library path: `/Research/SWE-ABS/2026-11-12/sweabs_historical_83_raw_evidence_private.zip`. Re-materialized, SHA-256 verified, ZIP integrity clean (86 members). **Not public or automatically available to new users/chats**. See [the updated manifest](../results/2026-11-12/MANIFEST.md).

### Completed Step 6 — stronger-test FAIL validity documentary review (2026-11-12)

**Status:** The 31 provisional FAIL runner records from 15 distinct task IDs were individually reviewed against their archived original issue statement, corresponding upstream merged PR (verified on GitHub), exact SWE-ABS augmented test patch, and the actual failing log. Per-run model patch SHA-256, test patch SHA-256 and base commit metadata were checked. Two HTTP/URI standards and Python `staticmethod` runtime documentation were used where pertinent. **No task oracle was re-executed and no human/maintainer review was obtained.**

**Results — supplementary semantic dispositions, not new runner labels:**

| Disposition | FAIL runs | What it means |
| --- | ---: | --- |
| `valid_failure` | 9 | A failing assertion is aligned with a defensible issue requirement; still needs independent oracle/human confirmation |
| `invalid_test` | 4 | Specific assertion contradicts authoritative requirement or tests a nonrequired auxiliary API |
| `environment_sensitive` | 2 | Python 3.9 descriptor behavior can explain errors; equivalence across runtimes unverified |
| `unresolved` | 16 | Requirement or contract is ambiguous, extended beyond issue scope, or test behavior needs further evidence |
| **Total** | **31** | All cases documented; original v2 raw FAIL labels unchanged |

**High-impact review concerns:** Django RFC850 century-wrapping for 2099→2100 contradicts the cited >50-year rule (three runs); SymPy #13877's failure tests `random_complex_number(tolerance=...)` although the task concerns determinant pivot behavior (one run); Django ModelForm 3.9 staticmethod descriptor differs from Python 3.10+ semantics (two runs). See [full 15-task report](../results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md) for caveats, specific assertion names, explicit competing interpretations, and cited sources.

**Artifacts:** [31-row review ledger](../results/2026-11-12/STEP6_FAIL_REVIEW_31.csv) · [15-task summary](../results/2026-11-12/STEP6_TASK_SUMMARY_15.csv) · [review report](../results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md) · [review extraction script](../scripts/review_step6_fail_cases.py). All committed and fetched back from GitHub; SHA-256 manifest in [results](../results/2026-11-12/MANIFEST.md). Versioned v2 outcomes remain 153 PASS / 31 raw FAIL / 14 UNVERIFIED.

## 4C. Completed Step 7 — versioned provisional analysis-label gate

**Status:** DONE for documented eligibility/sensitivity rules and 14-case triage, *not* for final test semantic correctness. See [the full Step 7 report and counterarguments](../results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md), [all 14 UNVERIFIED details](../results/2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv), [198-row analysis manifest v1](../results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv), and [deterministic generation/check script](../scripts/build_step7_analysis_labels.py).

The previously archived original v1 and audited v2 are unchanged. All 198 v2 identities match the 83+115 raw-evidence tables; all 31 v2 FAIL rows match Step 6 review rows. The 14 UNVERIFIED cases fall into **9 skips / 4 patch overlaps / 1 full large-patch integrity gap**. All 14 expected Actions per-patch artifact names were present and none marked expired when checked on 2026-11-12. This session re-reviewed archived audit tables and artifact metadata, **not** each new raw ZIP, did no Docker reruns, and sought no new independent human/maintainer oracle.

The machine-readable v1 manifest freezes the following analysis **screens** before extraction of any trajectory indicators. Here 0=audited runner PASS, 1=provisional stronger-test FAIL, blank=excluded.

| Analysis definition | 0 (PASS) | 1 (FAIL) | Excluded | Research status |
| --- | ---: | ---: | ---: | --- |
| Conservative primary (`primary_y`) | 153 | 9 | 36 | 9 review-supported Step 6 failures, **not** semantic oracles; 162 rows/61 tasks, only 5 FAIL tasks |
| Sensitivity: noninvalid FAIL (`noninvalid_sensitivity_y`) | 153 | 27 | 18 | Includes unresolved + environment-sensitive as FAIL provisionally |
| Sensitivity: all runner FAIL (`runner_only_sensitivity_y`) | 153 | 31 | 14 | Retains disputed invalid-test outcomes only as runner-measured scenario |
| Sensitivity: skipped-as-PASS hypothesis (`skipped_as_pass_scenario_y`) | 162 | 9 | 27 | Hypothetical assumption for nine incomplete-coverage cases; **not actual PASS** |

**Caution:** Selection on review-supported semantic test validity reduces positive failure cases and may bias analysis; report all prespecified sensitivity targets and group repeated tasks, not independent 198-run statistics. The remaining unverified semantic/coverage/identity issues require additional evidence before a gold-standard reliability claim. Controlled reruns must preserve old outcomes and be logged as new versioned evidence. Private archived raw ZIPs remain private.

## 4D. Completed Steps 8–10 — frozen indicators, exact-match features, provisional AUROC

**Step 8 (DONE):** [Frozen v1 feature specification and prespecified analysis plan](STEP8_FROZEN_INDICATORS_v1.md) was committed before feature extraction and label association; [exact-match extractor](../scripts/step9_extract_trajectory_features.py) was also committed first. Indicators: duplicate-terminal rate, explicit terminal error rate, verification presence, editor calls after last verification. No post-result changes to indicator rules.

**Step 9 (DONE, independently reproducible Python execution remains unverified):** The current Hugging Face dataset revision matched pinned `b5515d1dce40036633293b70477f0633b24593f7`. Across 296 trajectory rows, 198 were originally resolved and **all 198 exactly matched `(sample,instance_id,sha256(patch))`** against the Step 7 ledger, with 73 tasks. [Feature CSV](../results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv) contains derived data only; [coverage](../results/2026-11-12/STEP9_COVERAGE_v1.json) documents 198/198 error parse coverage and 191/198 with a recognized test command. Seven `editor_after_last_verification` values are missing by design. No raw trace text or secrets were committed.

**Step 10 (DONE for exploratory, task-group-aware in-sample AUROCs):** [Corrected 500-replicate task-cluster bootstrap v2 JSON](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) · [full quantified interpretation and alternatives](../results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md) · [analysis script](../scripts/step10_analyze_frozen_features.py).

| Frozen duplicate-terminal rate versus target | AUROC | 95% task-cluster interval | Task IDs / FAIL task IDs |
| --- | ---: | ---: | --- |
| Conservative primary (153 PASS, 9 review-supported FAIL) | **0.489** | **0.270–0.706** | 61 / 5 |
| Noninvalid FAIL sensitivity (153/27) | **0.721** | **0.565–0.857** | 67 / 13 |
| All raw-runner FAIL sensitivity (153/31) | **0.708** | **0.562–0.834** | 69 / 15 |
| Hypothetical skipped-as-PASS (162/9) | **0.478** | **0.255–0.686** | 64 / 5 |

Other prespecified primary AUROCs: terminal error rate **0.599**, absence of recognized verification **0.480**, post-last-verification editor count **0.435**. Bootstrap resampled task IDs, not iid runs. **Critical interpretation:** broader provisional FAIL labels suggest a potential repeated-command signal, but the conservative primary does not; positive-label semantic uncertainty, only five positive task IDs and task difficulty confounding prevent an affirmative reliability claim.

**Bug caught and retained transparently:** [Step 10 v1 JSON](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v1.json) had invalid degenerate 64-cluster bootstrap intervals caused by low-bit PRNG modulo. v1 is preserved as **INVALID for confidence intervals**; corrected v2 uses high-bit scaling for task draws, same frozen predictors, outcomes, seed and 500 resamples. No original outcome was rewritten.

## 4E. Step 11 technical results — independently reproduced (2026-11-12)

**Read-only source integrity:** [GitHub Actions workflow](../.github/workflows/step11-reproduction.yml) from a clean GitHub checkout ran Python **3.11.18**, `datasets==4.8.5`, `huggingface_hub==1.33.0`, with [verified successful run #43260088649](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649). Steps for five synthetic tests, exact Step 9 pinned-HF 198-run `--check`, corrected Step 10 AUROC `--check`, Step 11 robustness `--check`, the 12-trajectory event recount, and no-diff source protection ALL PASSED. An independent earlier remote Python snapshot check also passed; CI gives the stronger full-loader verification.

**Event spot-check:** [Independent recount script](../scripts/step11_trace_spotcheck.py) checked first 2 PASS, first FAIL, first UNVERIFIED in each sample: **12 trajectories × 14 frozen derived fields = 168 comparisons, zero mismatches**. [Versioned 12-case JSON](../results/2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json), transcribed from passing CI job logs; raw messages never committed.

**Post-hoc exploratory sensitivity:** [Robustness JSON](../results/2026-11-12/STEP11_EXPLORATORY_ROBUSTNESS_v1.json) and [transparent report](../results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md) show the duplicate-command rate has primary run-level AUROC **0.489**, task-macro **0.522**, within-project **0.390** (only **3 projects with comparable class pairs**), and leave-one-positive-task-out run AUROC **0.382–0.620** (only 5 positive task IDs). Broader runner-only sensitivity: run-level **0.708**, task-macro **0.741**, within-project **0.738**, leave-one-positive-task-out **0.683–0.759**. These diagnostics were computed **after Step 10** and are **not confirmatory or held-out predictive performance**. The primary result does not establish a reliable predictor, while broadened semantic-uncertain labels lead to different conclusions.

**Reproducibility correction:** the Step 9 Python Django `runtests.py` pattern had an incorrect escape, fixed in [commit ec225c0](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/ec225c035818d826eed0ad49e6a3487381b10c2d) **without altering frozen Step 8 semantics**. Full CI reproduces existing archived features byte-/row-equivalently via `--check`.

### Next exact action — Step 11 semantic validity and coverage gate

1. **TECHNICAL CHECKS PASS** — do not redo the 198-run extraction or interpretation unless a new discrepancy appears; preserve independent [successful CI run](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649).
2. **STILL OPEN:** human/maintainer or independent oracle adjudication of **16 unresolved and 2 environment-sensitive Step 6 FAILs**, appropriate discussion of 4 invalid enhanced tests, and **14 Step 7 UNVERIFIED** (skipped coverage, patch/test overlap, patch-integrity gap). Only controlled **versioned** reruns may alter subsequent, *separate* analysis snapshots; original v2/Step 7 v1 must remain unchanged.
3. **Research decision:** either obtain materially stronger semantic evidence or explicitly keep conclusions provisional/negative and limit generalization. Keep the 5-positive-task primary bound visible. Do not promote broader label associations to journal-ready predictive performance.
4. After validity closure or formal limitation decision, update this state, append WORK_LOG, keep README/AGENTS/results manifest in sync, then do Step 12 case studies.

## 4F. Step 11 source/test structural validity crosswalk (2026-11-12)

The [Python pinned-dataset audit](../scripts/step11_semantic_structural_audit.py) loaded original Gemini 3 Flash patches at `b5515d1dce40036633293b70477f0633b24593f7` and SWE-ABS augmented test patches at `79fc07a8f4ce5e3720e069948073f5f910b7577b`. It independently checked **45 unique exact (sample, task, patch SHA) identities**, [31 FAIL documentary test hashes](../results/2026-11-12/STEP6_FAIL_REVIEW_31.csv), six UNVERIFIED task-family test diffs and issue source hashes. [Actions #43262365929 SUCCESS](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43262365929), with [complete 45-run source metadata ledger](../results/2026-11-12/STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json) and [explicit limitations and adversarial interpretations](../results/2026-11-12/STEP11_SEMANTIC_VALIDITY_GATE_v1.md). No semantic oracle or augmented-test runner was executed in this audit.

- **4/4 collision triage cases independently have same changed file in agent and enhanced-test patch:** SymPy `sympy/polys/matrices/tests/test_normalforms.py` (three agent samples) and Django `tests/utils_tests/test_numberformat.py` (Sample 3). This is corroborating static evidence for potential model/test patch overwrite, **not** proof of final runtime test result.
- **9/9 skipped-coverage cases have no direct changed-file overlap;** corresponding pinned test-patch diffs contain skip-related conditions, but runtime skipped test identity and pass-on-supported-backend are not established by static code alone.
- **1 Requests integrity case** has 74 changed diff files including **65 `build/` or `build/lib/` files**; complete tested-tree correspondence remains unverified.
- **31/31 FAIL review source/test SHA identities match**, but their previous documentary semantic decisions remain 9 supported, 4 invalid-test, 2 environment-sensitive, 16 unresolved. Original v2 **153/31/14**, Step 7 primary **153/9/36**, and Step 8 frozen metrics unchanged.
- The [14-run private Actions ZIP re-audit script](../scripts/step11_raw_artifact_reaudit14.py) **passed** in [CI #43263048387](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43263048387): 14/14 original artifact ZIPs freshly retrieved; 14/14 exact model identities/SHA verified; 14/14 pinned augmented test SHA matched [crosswalk source](../results/2026-11-12/STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json); 14/14 test output SHA digests preserved in [raw ZIP audit](../results/2026-11-12/STEP11_RAW_ARTIFACT_REAUDIT14_v1.json). Each of the nine skip-bearing logs matches the originally recorded skip count; no raw ZIP/full log was publicly committed.

The [added-method raw skip attribution](../scripts/step11_skip_attribution.py) **passed** in [CI #43264326911](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43264326911), [nine-run JSON](../results/2026-11-12/STEP11_SKIP_ATTRIBUTION_9_v1.json). For each of three sample runs per task: Django-12039 added 13 named tests (9 seen PASS, 4 skipped PostgreSQL); Django-14434 added 1 named test (1 seen PASS, 0 skipped) **despite 28 suite-level skips**; Django-15503 added 10 named tests (8 seen PASS, 1 skipped, 1 absent from verbose log). **Caveat:** analysis of *newly defined methods* does not by itself cover assertions added to existing methods, inherited test collection or backend-dependent behavior; do NOT relabel Django-14434 PASS automatically. Raw runner v2 and frozen Step 7 remain unchanged.

**Exact next gate:** The source, archived raw ZIP and newly added test-method coverage audits **passed**, so do not repeat them without a discrepancy. Now inspect in-place modified test methods for Django-14434 and the not-seen added Oracle method for Django-15503, design **non-destructive exact-agent-patch reruns** for four overlaps, prove complete Requests tested-tree integrity, and undertake **backend-matched validation** for unexecuted PostgreSQL/JSON-related cases. Independently judge the 16 unresolved and 2 environment-sensitive FAIL semantic assertions. These require new separately versioned evidence. If such work is infeasible, mark semantic correctness unverified and narrow publication claims; do not silently reassign outcomes. Step 12 remains TODO.

## 4G. Step 11 in-place enhanced tests and source/collection gap (2026-11-12)

[Detailed evidence and opposing interpretations](../results/2026-11-12/STEP11_INPLACE_AND_ORACLE_COLLECTION_REVIEW_v1.md) · [Django-14434 exact original-base method map](../results/2026-11-12/STEP11_INPLACE_METHOD_AUDIT_DJANGO14434_v1.json) · [Django-15503 pinned Oracle method/log gap](../results/2026-11-12/STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json).

**Django-14434:** The pinned augmented patch contains **one newly defined test + in-place added code in nine pre-existing test methods** (10 insertion hunks, no deleted source lines), mapped to Django base `5e04e84d67da8163f365e9f5fcd169e2630e2873` and all three original sample test outputs. Each sample's one new method PASSED; **8/9 modified existing methods PASSED; `test_func_unique_constraint_covering` was SKIPPED**. The original log explicitly states the runner backend lacks **`supports_expression_indexes` and `supports_covering_indexes`**. Verified source-aware CI [#43267304895 SUCCESS](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43267304895). **Therefore the three Django-14434 UNVERIFIEDs have a concrete unexecuted enhanced assertion-bearing method**; 28 total suite skips alone would not have established this. A method reported OK is not proof every internal conditional executed.

**Django-15503:** An Oracle-named newly declared method, `test_oracle_json_path_final_key_is_quoted_for_numeric_strings`, is present in pinned `JSONFieldNumericKeyLookupsTests` but absent from three original verbose logs; source check and archived per-log SHA [Oracle audit JSON](../results/2026-11-12/STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json), [CI #43268521977 success](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268521977), [CI #43268574096 success](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268574096). This is **collection/coverage uncertainty, not evidence of FAIL or an executed SKIP**; the separate numeric-key containment test was explicitly skipped due unsupported `supports_json_field_contains`.

**Infrastructure:** A [CI attempt #43268071356](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268071356) failed during *redundant* original artifact download with HTTP 503 egress-limit error. Historical successful ZIP audits are unaffected; the updated [read-only Step11 workflow](../.github/workflows/step11-reproduction.yml) **defaults to archived SHA-checked original ZIP metadata** and only repeats raw ZIP downloads on manual `workflow_dispatch` opt-in. [CI #43268574096](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43268574096) passed after this change.

**Exact next unfinished evidence:** Controlled tests on a compatible backend for Django-14434 `supports_expression_indexes` and `supports_covering_indexes`, and collection-only + backend test of Django-15503's Oracle method, all under exact original submitted model patches; independently review unresolved/environment-sensitive FAIL semantics, four model/test patch overlaps and Requests full tested-tree integrity. Existing v2 153/31/14 and Step7 primary 153/9/36 stay unchanged. **Step 11 OPEN, Steps 12–14 TODO.**

## 4H. Final Step 11 limited-scope closure decision (2026-11-12)

**Authoritative status: DONE within the existing 14-milestone process for a reproducible, exploratory *runner-association* pilot with formal uncertainty limitations. NOT DONE for definitive semantic gold labels or journal-quality prediction validation.** This limited closure is allowed by the previous handoff plan's option to **formally constrain claims when independent oracles are infeasible**, rather than silently force 14 UNVERIFIED cases into binary labels. The earlier "Step 11 NEXT/OPEN" instructions in §§4D–4G document earlier checkpoints and are **superseded by this section**.

**Audited new evidence:** [Versioned 14-run controlled freeze](../results/2026-11-12/STEP11_CONTROLLED_EVIDENCE_FREEZE_v1.json) and independent [successful CI #43276679251](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43276679251), plus [scientific scope/limitations decision](../results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md).

- **3 `django__django-12039` exact patches:** 13/13 added augmented index tests ran and passed under PostgreSQL with no skip, each of the three samples; [successful test CI #43273619675](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43273619675). The original feature-flag probe recorded `AMBIGUOUS_ZERO_EXIT` because it unnecessarily required a different flag, but raw unittest logs prove 13 `ok`, `Ran 13`, `OK` without skip; the new reconciler validates this evidence. No frozen relabel.
- **3 `django__django-14434` exact patches:** formerly unexecuted enhanced `test_func_unique_constraint_covering` **passed for all 3** on a PostgreSQL backend supporting both expression and covering indexes, with exact model and augmented patch preservation ([CI #43272808138](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43272808138)). Full schema module separately ran 168 tests per sample with some *other* backend-specific skips ([CI #43274797864](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43274797864)); **not** 168/168 unskipped.
- **3 `django__django-15503` exact patches:** 10/10 patched JSON numeric-key tests passed with no skips per sample, plus separately the formerly unobserved Oracle-named method passed when explicitly targeted; independent Python unittest loader found its test ID among 10 ([module CI #43274797864](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43274797864); [direct Oracle CI #43273244869](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43273244869); [loader CI #43276011253](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43276011253)).
- **4 overlapping model/test-patch exact runs:** independently reconstructed original agent patch first, then inserted SWE-ABS tests non-destructively via `git apply --3way` (all 4 success). New merged tests yield SymPy samples 1/2/3 **7 passed +1 IndexError / 8 passed / 7 passed +1 IndexError**, and Django sample3 **12 tests/5 negative-zero assertion failures** after disabling old runner's traceback-pickling parallel error ([merge CI #43272706376](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43272706376); [merged execution CI #43274187213](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43274187213); [corrected Django serial CI #43275841934](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43275841934)). Reproducing an assertion failure does **not** establish the issue genuinely requires its contested semantics.
- **`psf__requests-1142` exact run:** reconstructed full **74 modified files, including 65 `build/`**, with **16,234 added/removed line entries** and model file hashes preserved **74/74 after augmented test patch** ([CI #43271576166](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43271576166)); original Docker tested tree remains unverified.
- All original **14 UNVERIFIED** labels and 31 provisional FAIL runner outcomes are unchanged; 31 FAIL documentary classifications **9 review-supported / 4 invalid-test / 2 environment-sensitive / 16 unresolved**, **not independently human-adjudicated**. The 5 distinct conservative positive task IDs and label sensitivity prevent a validated reliability-prediction claim.

**Explicit limits/decision:** These are new **different-runtime** controlled test observations and provenance checks; not identical historical SWE-ABS Docker replays, not independent human semantic truth, and not a calibrated, externally validated predictor. Original Step 7 `primary_y` and three prespecified sensitivity targets remain unchanged. The allowable study thesis is **negative/inconclusive primary discrimination with substantial label-policy sensitivity**. If a journal or mentor requires gold semantic labels, **reopen the Step 11 human-oracle gate** instead of strengthening the manuscript claim.

### Historical next-action plan — Step 12 qualitative case studies (executed 2026-11-13)

1. Predefine reproducible **case-selection rules without choosing examples for favorable AUROC or narrative**; use exact `(sample, task, patch SHA)` identifiers and issue-level grouping.
2. Illustrate well-audited PASS/FAIL, disputed/inconclusive, backend-limited and contradictory runs, verify original trajectory-event references and augmented-test evidence, and include counterexamples/alternative explanations.
3. Build a versioned qualitative ledger and interpretive report. Keep Step 11 closure scope and the original Step 7/8 frozen methods visible; update this PROJECT_STATE, WORK_LOG, README and manifest after each completed stage.
4. Step 13 manuscript; Step 14 venue-specific submission readiness later, with **no journal-ready claim** now.

## 4I. Step 12 reproducible qualitative case studies — completed 2026-11-13

**Authoritative status: DONE for eight prespecified illustrative, source-backed case studies, with no human-oracle claim.** The [case-selection protocol](STEP12_CASE_SELECTION_PROTOCOL_v1.md) was committed **first** in [commit dd2be953](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/dd2be9537095c81d47ae6eb4a71cb2caa7ff9b94), before inspecting selected individual rows. The [versioned roster](../results/2026-11-13/STEP12_CASE_ROSTER_v1.json) contains **eight distinct task IDs** with full exact patch hashes. The [qualitative report](../results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md) includes high/low duplicate-rate primary PASS/FAIL pairs and four prespecified validity/coverage/patch-integrity challenges, each with original runner evidence, opposing explanation, and explicit unverified fields.

**Independent reproducibility:** [Step 12 source checker](../scripts/step12_cases.py) reconstructs the same eight slots from frozen Step 7 and Step 9 data and uses a separate raw-message recount implementation. New [CI #43440488895 completed SUCCESS](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43440488895); logs report **8 distinct exact sources / 112 frozen indicator comparisons / 0 mismatches**, no raw trace text published. [Archived CI result provenance](../results/2026-11-13/STEP12_SOURCE_RECOUNT_8_v1.json). The original 198-run v2 **153 PASS / 31 FAIL / 14 UNVERIFIED**, conservative Step 7 **153/9/36**, Step 8 indicator definitions and Step 10 AUROCs remain unchanged.

**Illustrative observations, not inference:** selected **duplicate rate 0.400 PASS** versus **0.021739 FAIL**, plus **0.285714 FAIL** and **0.000000 PASS**; invalid-test, Python-runtime-sensitive, skipped-backend and model/test overlap examples show why raw runner results are not human semantic ground truth. These examples were chosen using outcomes and ranks and cannot estimate prospective accuracy. No individual terminal command, intention, raw-message chronology, or causality is inferred. The original Step 6 `9/4/2/16` review disposition and unresolved human semantics remain unverified.

### First unfinished milestone — Step 13 manuscript (exact next action)

1. Read the Step 11 closure decision, corrected Step 10 task-cluster results, prespecified sensitivity screens, and the full Step 12 report and roster. **Freeze the manuscript claim at a negative/inconclusive in-sample runner-association pilot with high label-policy sensitivity**, not a semantic defect predictor.
2. Create a versioned paper outline and **draft the actual Introduction, Related Work, Method, Experimental Setup, Quantitative Results, Qualitative Results, Discussion, Limitations and Conclusion**, with checked citations/figures/tables. Clearly distinguish evidence, interpretation, alternative explanations, and unverified external/human semantic validity.
3. Inspect linked upstream papers and citations for bibliographic accuracy instead of inventing literature; do not reuse raw private logs or misrepresent 198 runs as 198 independent tasks. Keep source/data provenance in the draft.
4. Update PROJECT_STATE and append WORK_LOG with verified artifacts; synchronize public README in the same session. After Step 13 completion, Step 14 final reproducibility, mentor feedback and venue-specific submission readiness remains unfinished.

## 4J. Step 13 Overleaf-compatible manuscript draft begun — 2026-11-13

**Authoritative status: IN PROGRESS, not DONE.** [Source-grounded full-section working manuscript](../paper/main.tex), [initial checked primary-source BibTeX](../paper/references.bib), [import/build instructions](../paper/README.md), and [claim-to-evidence ledger](../paper/CLAIM_EVIDENCE_MATRIX.md) created in [commit 43b21ad7](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/43b21ad7f119c91b67b42b53a38b3c7fdd2a75de). It uses an IEEEtran journal layout compatible with Overleaf, **without** assuming that a target journal has been selected or that final authorship is confirmed. The [read-only PDF build workflow](../.github/workflows/paper-latex-build.yml) compiles this source and uploads a preview; historical original labels/data remain untouched.

**Scientific novelty/claim choice:** The September synthetic six-indicator composite, AUROC 0.663 and odds ratio 2.18 are not represented as real results. The November paper describes four individually frozen original-trajectory indicators, exact 198-run/73-task identities, 153/31/14 runner outcomes, conservative Step 7 153/9/36 (five positive task IDs), corrected task-cluster AUROC, three sensitivity labels, and the eight fixed qualitative source-audited examples. The allowable conclusion remains **negative/inconclusive conservative in-sample runner association with substantial outcome-definition sensitivity**, not semantic defect prediction or causal effects.

**Initial literature checked against primary publisher/arXiv pages (not yet a complete novelty survey):** Jimenez et al. SWE-bench ICLR 2024; Yu et al. SWE-ABS ICML/PMLR 2026; Sahoo et al. AgentLens arXiv 2605.12925 (2026); Shu et al. TraceProbe arXiv 2607.06184 (2026); Baltes et al. empirical LLM-SE guidelines published online November 2026. Final coauthor citation verification is still required. See [citation ledger](../paper/CLAIM_EVIDENCE_MATRIX.md).

**Remaining Step 13 checks:** confirm successful clean PDF compilation and inspect output, independently review each manuscript claim, strengthen related-work/novelty coverage, confirm author name/order/affiliations, approve substantive AI-assistance disclosure, and obtain mentor/coauthor scientific feedback. Do not equate machine-compiled LaTeX or AI-polished prose with Q1 submission readiness. Independent human/maintainer semantic oracle, external predictive replication and target-venue-specific scientific bar remain unresolved. **First unfinished milestone remains Step 13**, then Step 14.

## 5. Where to find workflow evidence

- [Sample 2 offset 0–9: run #11](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43176426126); [offset 10–19: run #12](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43179075950)
- Sample 2 remainder: [20–29](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181184322) · [30–39](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699) · [40–49](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181336920) · [50–59](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181340403) · [60–67](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181346009)
- Sample 3: [0–9](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182603318) · [10–19](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182697559) · [20–29](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182701126) · [30–39](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182706543) · [40–49](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182715959) · [50–59](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182719908) · [60–66](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182738449)
- Failed Sample 3 push-trigger run [#18](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182320416) was a **prepare failure with zero patch evaluations**; Sample 3 offsets 0–9 were successfully rerun in #19. Do not double count #18.

## 6. Resumption and documentation maintenance protocol

For **every substantive work session**:

1. Read these files and inspect the latest relevant Git commit, workflow run, or versioned data artifact.
2. State the exact first unchecked milestone and evidence needed. If inputs are absent or a checkpoint is unverifiable, state **unverified** and do not invent completion.
3. Work only on the next agreed milestone; keep any methodological change explicit and justified.
4. Record **what changed, what was verified, artifact paths/links, unresolved blockers, and the next action** in an append-only [WORK_LOG.md](WORK_LOG.md) entry.
5. Update the status table/checklist and `Last state verification` here. Update [README.md](../README.md) when public-facing status or method changes.
6. Verify the GitHub writes succeeded by fetching the new content, and cite the exact commit. Never claim a file is archived until it can be retrieved from durable storage.
7. End with a short next-chat handoff. A future chat must **explicitly open these files**; GitHub connection does not imply automatic continuous monitoring or background work.

### Copy-paste starter prompt for a new chat

> Connect to my GitHub repository `Foysal-Munsy/sweabs-free-eval`. First read `AGENTS.md`, `docs/PROJECT_STATE.md`, and `docs/WORK_LOG.md`, and cross-check the actual repository/evidence. Continue from the **first unfinished milestone**, do not change the research method without documenting it, and update PROJECT_STATE + WORK_LOG + public README in the same session. Report only evidence-backed progress and the exact next step.

---

**Rule of record:** `PROJECT_STATE.md` answers **where we are and what comes next**. `WORK_LOG.md` answers **what actually happened, when, and why**. `README.md` communicates **what the project is and the public high-level status**.
