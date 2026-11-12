# Research Project State — SWE-ABS Free Evaluation

> **Canonical human/AI handoff document.** Read this before continuing work.  
> **Last state verification:** 2026-11-12 (Asia/Dhaka)  
> **Current phase:** All 198 strengthened-test attempts and 83+115 raw audits completed; Step 6 documentary FAIL review completed; **Step 7 14-case UNVERIFIED triage and versioned provisional eligibility/sensitivity-label freeze completed (no new runner verdicts, no oracle validation). Step 8 trajectory-indicator specification is NEXT.**  
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
| 8 | **Freeze trajectory messiness indicator specification** | **NEXT** | Precisely predefine indicators, trajectory parser and data availability checks, missingness, aggregation, leakage controls and grouping without viewing association with current labels |
| 9 | Extract trajectory features and exact-match | TODO | Reproducible extraction pipeline; match sample + instance + patch hash; coverage/dedup audit |
| 10 | Quantitative analysis | TODO | Appropriate baselines, association metrics (e.g. AUROC), uncertainty and task-aware treatment of repeated instances |
| 11 | Sensitivity and robustness | TODO | Label/coverage assumptions, task grouping, class imbalance, alternate defensible thresholds |
| 12 | Qualitative case studies and interpretation | TODO | Trace-backed illustrative successes, failures, exceptions, opposing explanations |
| 13 | Draft research paper | TODO | Introduction, related work, methods, experiments, results, discussion, limitations, conclusion |
| 14 | Reproducibility and submission readiness | TODO | Code/data provenance, final figures/tables, checked citations, mentor feedback, venue-specific requirements |

**Current checkpoint:** Steps 1–2 DONE; Step 3 runner labels PROVISIONAL; Steps 4–5 DONE; Step 6 documentary review DONE for its limited scope; **Step 7 documentary triage and provisional analysis-policy freeze DONE**. Original v2 runner counts remain **153 PASS / 31 FAIL / 14 UNVERIFIED**. Primary v1 analysis screen is **153 runner PASS / 9 review-supported FAIL / 36 excluded** (162 rows, 61 unique tasks; only 5 distinct FAIL task IDs). Alternative sensitivity labels are 153/27/18 (noninvalid), 153/31/14 (runner-only), and 162/9/27 (hypothetical skipped-as-PASS). **Step 8 is NEXT**, Steps 9–14 TODO. Semantic oracles, targeted reruns, trajectory features and predictive findings remain unverified/not performed.

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

### Next exact action — Step 8: indicator specification freeze

1. Read the Step 7 [policy and manifest](../results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md) and the original [trajectory selection logic](../scripts/pilot.py) alongside the pinned agent dataset revision; preserve `(sample,instance_id,patch_sha256)` identities.
2. Define the trajectory schema and **lightweight messiness indicators** using theory/process criteria *before* reading indicator–label associations. Specify exact formulas/regex/event rules, time-order rules, parsing edge cases, missingness, denominators and run-level aggregation; forbid outcome-driven threshold tuning.
3. Write a frozen versioned feature specification and tests. Confirm availability and reproducibility of the trajectory records and commit a data-lineage plan. **Do not run feature-based predictive analysis before the freeze.**
4. Separately track open Step 7 validation: non-destructive patch-overlap reruns (4), whole patch integrity (`requests-1142`), database/backend coverage reruns (9), and Step 6 human/oracle adjudication. These are *not* resolved by an unchanged runner label.

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
