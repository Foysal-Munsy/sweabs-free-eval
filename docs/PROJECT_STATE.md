# Research Project State — SWE-ABS Free Evaluation

> **Canonical human/AI handoff document.** Read this before continuing work.  
> **Last state verification:** 2026-11-12 (Asia/Dhaka)  
> **Current phase:** Stronger-test execution finished; provisional outcome audit finished; **evidence preservation has been completed with a private raw-ZIP backup; historical 83-row audit consistency is the next unfinished milestone**.  
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
| 1 | 63 | 63 | 48 | 11 | 4 |
| 2 | 68 | 68 | 53 | 11 | 4 |
| 3 | 67 | 67 | 52 | 10 | 5 |
| **Total** | **198** | **198** | **153** | **32** | **13** |

**What is established:** all 198 evaluation attempts completed. The cumulative provisional audit CSV has 198 rows with unique `(sample, offset)` and 73 distinct task IDs. Full raw-log checking was performed for **115 recent records**: Sample 2 offsets 20–67 and Sample 3 offsets 0–66. The earlier **83 records** (Sample 1 and Sample 2 offsets 0–19) were retained from previous audits rather than re-reviewed in the 115-record audit.

**What is NOT established:** a final claim about patch semantic correctness, the strength/soundness of all augmented assertions, the predictive value of messiness indicators, or any final publication-ready results.

**Outstanding validity concerns:**
- **32 provisional FAIL:** independent review of augmented-test semantics and environment assumptions is not done. The earlier audit reported these failures across **16 distinct task IDs**; recheck this figure against the archived CSV before using it in a paper.
- **13 UNVERIFIED:** skipped/incomplete strengthened-test coverage and patch-identity issues; keep excluded or separately analyzed until reviewed.
- **3 exact-patch overlap cases:** Sample 2 offset 63 (`sympy__sympy-23413`), Sample 3 offset 7 (`django__django-11206`), Sample 3 offset 62 (`sympy__sympy-23413`). Augmented-test setup reset a test file also modified by the agent. Do not treat their observed raw runner outcomes as exact-patch PASS/FAIL.
- Skipped database/backend tests include some Django cases. A PASS for the executed subset is **not** full-coverage verification if required augmented tests were skipped.

**Evidence:** [audited workflow history](https://github.com/Foysal-Munsy/sweabs-free-eval/actions), [current public README](../README.md), and the offline audit files in the inventory below. The **198-row CSV, 115-row provenance CSV, audit report, historical 83-row input, and audit script are now archived on GitHub** with verified original bytes. The raw 5.1-MB evidence ZIP is privately backed up to the owner's ChatGPT Library and is **not** publicly accessible. See the [artifact manifest](../results/2026-11-12/MANIFEST.md).

## 3. Full milestone checklist (order matters)

Legend: **DONE** = completed to stated scope, **PROVISIONAL** = complete as a provisional evidence milestone, **NEXT** = first unfinished step, **TODO** = not completed. Do not convert the checklist into a percentage of the entire research project.

| # | Milestone | Status | Completion gate / artifact |
| --- | --- | --- | --- |
| 1 | Research question and data selection | DONE | Originally passing Gemini 3 Flash trajectories, SWE-ABS tests, fixed evaluation setup |
| 2 | Run strengthened evaluations | DONE | 63 + 68 + 67 = 198 evaluation attempts |
| 3 | Audit runner outputs | PROVISIONAL | 198-row provisional CSV; latest 115 raw logs checked, 83 earlier rows preserved |
| 4 | Preserve evidence and provenance | **DONE — PRIVATE RAW ZIP** | [Versioned GitHub audit files and checksums](../results/2026-11-12/MANIFEST.md); original raw ZIP re-downloaded from private Library and SHA-256/ZIP-integrity verified; not public |
| 5 | **Reconcile earlier audit records** | **NEXT** | Recheck the 83 historical rows against available logs, patch identity, coverage, and current label policy; keep original version and any corrections traceable |
| 6 | Validate strengthened-test FAIL cases | TODO | Review all 32 provisional FAIL records, group by task, record soundness / invalidity / unresolved decisions |
| 7 | Triage UNVERIFIED and freeze labels | TODO | Investigate 13 UNVERIFIED, controlled reruns only where justified, documented exclusions and versioned label manifest |
| 8 | Freeze trajectory messiness indicator specification | TODO | Precise indicators, parsing rules, missingness, exclusions fixed without outcome-driven tuning |
| 9 | Extract trajectory features and exact-match | TODO | Reproducible extraction pipeline; match sample + instance + patch hash; coverage/dedup audit |
| 10 | Quantitative analysis | TODO | Appropriate baselines, association metrics (e.g. AUROC), uncertainty and task-aware treatment of repeated instances |
| 11 | Sensitivity and robustness | TODO | Label/coverage assumptions, task grouping, class imbalance, alternate defensible thresholds |
| 12 | Qualitative case studies and interpretation | TODO | Trace-backed illustrative successes, failures, exceptions, opposing explanations |
| 13 | Draft research paper | TODO | Introduction, related work, methods, experiments, results, discussion, limitations, conclusion |
| 14 | Reproducibility and submission readiness | TODO | Code/data provenance, final figures/tables, checked citations, mentor feedback, venue-specific requirements |

**Current checkpoint:** Steps 1–2 DONE; Step 3 PROVISIONAL; Step 4 DONE with an owner-private raw archive; Step 5 is NEXT. Steps 6–14 remain pending. Public release of the raw ZIP is still withheld pending review.

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

## 4A. Next exact action — Step 5 (historical audit consistency)

1. Read the archived [first83 CSV](../results/2026-11-12/sweabs_samples1_2_first83_cumulative.csv) alongside the [198-row CSV](../results/2026-11-12/sweabs_full_198_cumulative_audited.csv). Verify that rows for Sample 1 offsets 0–62 and Sample 2 offsets 0–19 remain identical by field and identity; record the comparison digest/summary.
2. Retrieve available Sample 1 and early Sample 2 GitHub Actions raw evidence (use the explicit run links and existing patch/source evidence; availability may be limited by the workflow's 14-day retention).
3. Re-evaluate those 83 **previously preserved** classifications using the 115-run audit policy: patch/test identity, base commits, repository diff integrity, actual outer augmented runner results, and any skips. Prioritize `RETROSPECTIVE_REVIEW_REQUIRED`, FAIL, and UNVERIFIED.
4. If any outcome changes, save an **append-only corrections table**, keep the original 198-row archival checkpoint immutable, and create a **new version** of the reviewed label manifest; document old vs new and why.
5. Record unresolved missing raw evidence as **unverified**, update this state, WORK_LOG, README, and a new manifest. **Only then mark Step 5 DONE.** No trajectory-feature extraction or final correctness claims yet.

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
