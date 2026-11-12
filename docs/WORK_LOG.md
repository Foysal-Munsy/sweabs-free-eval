# Work Log — SWE-ABS Free Evaluation

> **Append-only, source-backed research work history.** For the current milestone and next action, see [PROJECT_STATE.md](PROJECT_STATE.md). For public project framing, see [../README.md](../README.md).  
> **Last updated:** 2026-11-12. All files in this public repository are publicly readable.

This log should record **what actually changed**, not hoped-for progress. The newest entry comes first. When a past conclusion needs correction, add a new dated correction entry with sources; do not erase the original record. Every entry should give (a) scope, (b) verified result, (c) files/commit/log evidence, (d) unresolved issues, (e) next handoff.

## 2026-11-12 — Step 6: documented validity review of 31 provisional FAIL cases

**Milestone/scope:** Step 6 DONE for **AI-assisted documentary review**, not independently executed semantic ground truth; Step 7 is NEXT. **No modifications to the 198-row v2 runner outcomes.**

**Evidence-backed work completed:**
- Identified the **31 v2 FAIL runs across 15 distinct instance IDs**, retrieved the corresponding per-run GitHub artifact ZIPs, and rechecked instance/sample identity, model patch SHA-256, enhanced test patch SHA-256, and base commit. A given task's strengthened test patch was identical across its sampled FAIL runs.
- Inspected each failing enhanced assertion and raw failure/log output; read the original issue statement in the SWE-ABS record and independently checked corresponding merged [Django](https://github.com/django/django/pulls), [Matplotlib](https://github.com/matplotlib/matplotlib/pulls), and [SymPy](https://github.com/sympy/sympy/pulls) pull requests (exact 15 PR URLs appear in the review ledger).
- Used [RFC 7231 §7.1.1.1](https://www.rfc-editor.org/rfc/rfc7231.html#section-7.1.1.1), [RFC 3986 §3.2.1](https://www.rfc-editor.org/rfc/rfc3986.html#section-3.2.1), and [Python staticmethod documentation](https://docs.python.org/3/library/functions.html#staticmethod) to check contested assertions.
- Created the [31-run semantic review ledger](../results/2026-11-12/STEP6_FAIL_REVIEW_31.csv), [15-task summary](../results/2026-11-12/STEP6_TASK_SUMMARY_15.csv), [full issue-level report](../results/2026-11-12/STEP6_FAIL_VALIDITY_REVIEW.md), and [review extraction script](../scripts/review_step6_fail_cases.py). Committed all to GitHub and verified content via read-back; SHA-256 digests listed in [manifest](../results/2026-11-12/MANIFEST.md).
- Dispositions among the same 31 raw FAILs: **9 `valid_failure` (issue-aligned/review-supported but not oracle-confirmed), 4 `invalid_test`, 2 `environment_sensitive`, 16 `unresolved`**. This is a secondary review field; original raw runner FAIL labels are preserved.

**High-impact issues and opposing interpretations:**
1. **Django #11848 (3 runs):** Enhanced RFC850 century-wrap expects 2000 for a \'00\' date when current time is July 2099; raw parser returns 2100. RFC7231 requires mapping to past year only when the candidate is over 50 years in the future; 2100 is under one year away, so the augmented assertion is invalid. [Original PR](https://github.com/django/django/pull/11848) · [RFC rule](https://www.rfc-editor.org/rfc/rfc7231.html#section-7.1.1.1).
2. **SymPy #13877 (1 run):** Enhanced failure is a `random_complex_number(tolerance=...)` TypeError, while the original bug/PR concerns zero pivots in symbolic matrix determinants. The reference patch included an auxiliary tolerance API; whether to require that is an additional implementation-equivalence choice, not shown to be necessary for determinant correctness. [PR](https://github.com/sympy/sympy/pull/13877).
3. **Django #15916 (2 runs):** `formfield_callback=staticmethod(...)` tests fail at class construction on Python 3.9. Direct callability of staticmethod descriptors was introduced in Python 3.10. This is runtime-sensitive, and class-level vs Meta callback precedence remains ambiguous. [PR](https://github.com/django/django/pull/15916) · [Python docs](https://docs.python.org/3/library/functions.html#staticmethod).

**Limitations and decisions:** No independent human/maintainer adjudication, no new Docker test runs, no reapplication of reference patch as a semantic oracle, no final exclusion decisions, and no feature/statistical analysis. `valid_failure` is **review-supported**, not publication-ready ground truth. `invalid_test` does **not** mean the agent patch passes or is correct. Contrasting plausible interpretations are explicitly stored per run.

**Next exact action:** **Step 7 — review all 14 UNVERIFIED**, prepare traceable reruns/exclusions when necessary, and create a frozen analysis label manifest separating raw runner outcomes from semantic review and sensitivity assumptions. Update all milestone documentation in the same session.

**Documentation synchronized:** PROJECT_STATE = yes; WORK_LOG = yes; README = yes; AGENTS = yes; results index/manifest = yes.

## 2026-11-12 — Step 5: completed historical 83-run raw-evidence reconciliation

**Milestone:** Step 5 DONE; Step 6 (independent FAIL-test validity review) NEXT. Step 3 labels remain *provisional*.

**Verified actions:**
- Read [first83 archival input](../results/2026-11-12/sweabs_samples1_2_first83_cumulative.csv) and [198-row v1](../results/2026-11-12/sweabs_full_198_cumulative_audited.csv); **all 83 historical rows matched exactly across all 12 columns**.
- Retrieved and inspected **83 per-patch ZIPs** for Sample 1 offsets 0–62 and Sample 2 offsets 0–19. Also downloaded the **earlier unsuccessful Sample 1 offset-5 artifact**, but used the corrected [run #42858519379](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/42858519379) as primary evidence; the original failed [run #42853996382](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/42853996382) was retained, not counted twice.
- Recomputed submitted-patch and augmented-test SHA-256, compared base commits, frozen dataset revisions, model patch application and pre/post repository diffs, examined augmented test runner stdout (Django/SymPy/pytest/Sphinx-tox), detected explicit skipped tests and model-patch/test-file overlap. The [83-row audit evidence CSV](../results/2026-11-12/sweabs_historical_83_reaudit_evidence.csv) retains the per-run checks and sources.
- **82 labels unchanged; 1 correction:** Sample 1 offset 58, `sympy__sympy-23413`: **FAIL → UNVERIFIED** because an agent-modified test file was removed/reset during augmented test setup/cleanup. Raw tests still reported **7 passed, 1 exception**. Details in the [correction ledger](../results/2026-11-12/sweabs_historical_83_corrections.csv) and [Step 5 report](../results/2026-11-12/STEP5_RECONCILIATION_REPORT.md).
- Kept Sample 1 offset 36 `psf__requests-1142` UNVERIFIED despite 15 passing tests: the ~884-KB patch includes `build/lib` generated files and full repository diff preservation was not verified.
- Created [versioned current 198-row CSV v2](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv), retaining the original v1 unchanged. **New totals: 153 PASS, 31 FAIL, 14 UNVERIFIED**, with 73 distinct instance IDs. There are **31 FAIL runs across 15 unique task IDs**.
- Archived the [reproduction script](../scripts/reaudit_historical_83.py); it completed locally and generated the audited v2, detailed evidence and correction table, without Docker or fresh benchmark runs. All files were committed and read back through GitHub.
- Privately preserved `sweabs_historical_83_raw_evidence_private.zip` in the owner's ChatGPT Library `/Research/SWE-ABS/2026-11-12`. Verified after materialization: **2,790,331 bytes**, SHA-256 `cc7c5f4280c3dd7e4ccfb34f55ea151f472435e33d1e7465fb73cf9c75c586e4`, ZIP integrity clean (86 members). **Not public on GitHub.**

**Decisions and limitations:** This is a **stronger-test runner evidence reconciliation**, *not* independent confirmation that any strengthened test's asserted behavior is semantically valid. The 31 remaining FAIL and 14 UNVERIFIED must remain provisional. Old v1 is not overwritten; changed label is explicit and reproducible in v2. Raw logs can contain test fixture secrets or user traces, so the backup stays private.

**Source of truth:** [Step 5 reconciliation report](../results/2026-11-12/STEP5_RECONCILIATION_REPORT.md), [evidence manifest](../results/2026-11-12/MANIFEST.md), [current v2 dataset](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv), and linked GitHub Actions run IDs.

**Next exact action:** Step 6 — independently evaluate 31 provisional FAIL cases across 15 tasks against the strengthened test assertions and original task requirements, recording per-case dispositions and evidence links; defer feature extraction until analysis labels are frozen.

**Documentation synchronized:** PROJECT_STATE = yes; WORK_LOG = yes; README = yes; AGENTS = yes; results manifest = yes.

## 2026-11-12 — Step 4: archived audited results with a private raw-evidence backup

**Milestone / scope:** Step 4 evidence preservation, completed for the repository owner's durable access; **public raw-ZIP release deferred**. Step 5 historical audit consistency remains pending.

**Actions and verified evidence:**
- Rechecked the local originals before archival: **198 cumulative rows** (Sample 1: 63, Sample 2: 68, Sample 3: 67; 153 PASS, 32 FAIL, 13 UNVERIFIED), **115 detailed evidence rows** (48 Sample 2 and 67 Sample 3), and unchanged source SHA-256 checksums.
- Committed the [198-row CSV](../results/2026-11-12/sweabs_full_198_cumulative_audited.csv), [115-row evidence CSV](../results/2026-11-12/sweabs_samples2_3_full_audit_evidence_115.csv), [audit report](../results/2026-11-12/sweabs_full_198_audit_report.md), [historical 83-row CSV](../results/2026-11-12/sweabs_samples1_2_first83_cumulative.csv), and the [original offline audit script](../results/2026-11-12/sweabs_full_audit.py) under an immutable dated archival directory.
- Detected that an initial content-reader pass normalized CSV CRLF and trimmed a terminal newline; corrected and committed **byte-identical** originals. Re-fetched GitHub content and verified the first three source SHA-256 digests matched local originals. Historical input/script content and original byte sizes also matched after GitHub read-back.
- Created a [hash and storage manifest](../results/2026-11-12/MANIFEST.md) and [results index](../results/README.md).
- Uploaded the **5,136,675-byte raw evidence bundle** privately to the owner's ChatGPT Library at `/Research/SWE-ABS/2026-11-12/sweabs_full_audit_evidence_bundle.zip`. Retrieved it back from Library, verified SHA-256 `b7f5fd76f747a23a83fb5b2d5e2c355d6123c2e2c9ddfe6fea974b3ac3c73d99`, passed ZIP integrity test (`testzip() is None`), and confirmed 140 entries. The raw bundle is **not on public GitHub** and excludes original Sample 1 raw per-patch ZIPs.
- Limited regex-based scanning found email-like and password-like test strings inside nested raw artifacts; it found no clear GitHub PAT/AWS-key/private-key markers. This **does not** certify safety for public release, so no public raw-ZIP upload was made.

**Verified files and checksums:** see [the authoritative manifest](../results/2026-11-12/MANIFEST.md), which records each byte count and digest. GitHub write/read-back confirmation is recorded by the repository's file history and SHA values in that manifest.

**What did not happen:** No label changes, feature extraction, statistical analysis, semantic FAIL review, or benchmark reruns. No claim that a public reader can download the raw private archive.

**Decision and limitation:** Step 4 may be marked **DONE for owner-accessible durable preservation**. Public release of raw artifacts requires stronger screening and is deferred as a reproducibility/publication concern. This is separate from analysis label validity.

**Next exact action:** **Step 5 — reconcile the 83 historical rows** using available per-patch logs, patch/base/test integrity, and current conservative audit policy; retain an append-only corrections table if anything changes.

**Documentation synchronized:** PROJECT_STATE = yes; WORK_LOG = yes; README = yes; AGENTS = yes.

## 2026-11-12 — Established project handoff documentation

**Milestone:** Documentation organization; research Step 4 (durable evidence archiving) **not completed**.

**Completed:**
- Added a canonical [project-state file](PROJECT_STATE.md), this chronological log, and a root-level `AGENTS.md` entrypoint for future AI-assisted continuation.
- Separated public README summary from operational research state and immutable-attribution log.
- Linked the handoff files from README. Future research sessions should synchronize these files with verified state.

**Source:** This file's creation commit, other documentation commits in the [repository history](https://github.com/Foysal-Munsy/sweabs-free-eval/commits/main/), and the content of [PROJECT_STATE.md](PROJECT_STATE.md).

**Not completed:** Research evidence was **not** archived to GitHub as part of this documentation reorganization. No changed test labels, fresh evaluations, trajectory extraction, statistics, or paper results are claimed.

**Next:** Step 4 — checksum-verify and archive the four previously generated audit outputs, inspect raw ZIP for public-release suitability, then verify durable access and update state.

## 2026-11-12 — Provisional audit of all 198 evaluation attempts

**Milestones:** Step 2 DONE; Step 3 PROVISIONAL.

**Verified snapshot:**
- Sample 1: **63** evaluated; **48 PASS / 11 FAIL / 4 UNVERIFIED**.
- Sample 2: **68** evaluated; **53 PASS / 11 FAIL / 4 UNVERIFIED**.
- Sample 3: **67** evaluated; **52 PASS / 10 FAIL / 5 UNVERIFIED**.
- Total **198** evaluated attempts, **153 PASS / 32 FAIL / 13 UNVERIFIED**. The cumulative CSV has **73 distinct instance IDs**, so repeated-task dependence must be handled.
- **115 new records** (Sample 2 offsets 20–67, Sample 3 offsets 0–66) were checked using full raw per-patch logs, hashes, patch-diff checks, base commits, and test-patch placement.
- **83 earlier rows** (Sample 1 and Sample 2 offsets 0–19) were **preserved** and **not independently re-audited** in the new 115-run pass.
- Among the new audits, the collector's UNVERIFIED was corrected to **PASS in 38 cases** and **FAIL in 7 cases**; one collector FAIL became **UNVERIFIED** for patch-identity overlap.

**Sources:** [GitHub Actions history](https://github.com/Foysal-Munsy/sweabs-free-eval/actions), [README status](../README.md), audit-derived evidence filenames and their SHA-256 digests in [PROJECT_STATE.md](PROJECT_STATE.md). The supporting detailed audit CSV, audit report, and evidence ZIP existed as previous-session files, **not yet as committed repository files**.

**Unresolved:** 32 provisional FAIL test-validity reviews; 13 UNVERIFIED cases; 3 known test-file overlap cases; historical 83-row reconciliation; evidence archival.

**Next at that checkpoint:** durable evidence preservation, then historical consistency and validity review.

## 2026-11-12 — Launched Sample 2 and Sample 3 remaining batches

**Milestone:** Step 2 DONE.

**Verified result:** Sample 2 offsets 20–67 ran in [#13](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181184322), [#14](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181332699), [#15](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181336920), [#16](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181340403), and [#17](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43181346009). Sample 3 offsets 0–66 ran in [#19](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182603318) through [#25](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182738449), seven distinct batches.

**Correction:** The first Sample 3 trigger [#18](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43182320416) failed in `prepare` before any patch was evaluated. The trigger detection was fixed and the first valid Sample 3 batch ran as #19. This is not an extra dataset run.

**Implementation source:** [batch workflow](../.github/workflows/sweabs-pilot.yml); [workflow run history](https://github.com/Foysal-Munsy/sweabs-free-eval/actions). Restricted manifest push triggers were added for this campaign; manual workflow dispatch remains available.

**Caveat:** The success of an Actions workflow says nothing by itself about the model patch's augmented-test verdict. Raw logs must determine labels.

## 2026-11-10 to 2026-11-12 — Earlier pilot and audit checkpoint

**Milestones:** initial harness smoke validation, then Sample 1 63/63 and Sample 2 offsets 0–19.

**Earlier reported result:** A harness patch-fallback bug could reverse a submitted patch; the correction is in [scripts/patch_harness.py](../scripts/patch_harness.py) and evaluated through the [smoke-test workflow](../.github/workflows/sweabs-smoke.yml). Sample 1 had 63 previous records (48/11/4), and Sample 2 offsets 0–19 added 20 (15 PASS / 4 FAIL / 1 UNVERIFIED), yielding the 83-row preserved checkpoint (63 PASS / 15 FAIL / 5 UNVERIFIED).

**Sources:** previous [README revision and Git history](https://github.com/Foysal-Munsy/sweabs-free-eval/commits/main/README.md), [Sample 2 run #11](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43176426126), and [run #12](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43179075950).

**Caveat:** Earlier audit details must be reconciled against raw evidence as a separate unfinished milestone; preserving old rows does **not** mean the new audit independently established their semantics.

---

## Entry template for every future work session

Copy this section to the **top** of the log after actual work has been performed:

### YYYY-MM-DD — Short factual title

- **Milestone / scope:** Step number and explicit boundary.
- **Status before → after:** DONE / PROVISIONAL / BLOCKED / TODO; do not invent progress.
- **Action performed:** Exact code/data/docs changes, evaluation inputs, or analysis tasks.
- **Verified evidence:** Links to GitHub commits, Actions run IDs, versioned data artifacts, relevant log lines, row counts, and SHA-256 checksums.
- **Results:** Facts only; separate interpretation or conjecture, state **unverified** when unsupported.
- **Decisions / alternative explanations:** Why a label, filter, test, or method was retained or changed.
- **Blockers and limitations:** Remaining unresolved issues and impact.
- **Next exact action:** First unchecked step, required inputs, and a testable completion gate.
- **Documentation synchronized:** PROJECT_STATE (yes/no); README (yes/no + why).

**Maintenance policy:** Update this log and PROJECT_STATE during the same substantive session. Update README for outward-facing status/method changes. Do not silently alter old evidence or commit logs containing secrets.
