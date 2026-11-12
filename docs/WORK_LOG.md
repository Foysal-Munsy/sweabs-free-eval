# Work Log — SWE-ABS Free Evaluation

> **Append-only, source-backed research work history.** For the current milestone and next action, see [PROJECT_STATE.md](PROJECT_STATE.md). For public project framing, see [../README.md](../README.md).  
> **Last updated:** 2026-11-12. All files in this public repository are publicly readable.

This log should record **what actually changed**, not hoped-for progress. The newest entry comes first. When a past conclusion needs correction, add a new dated correction entry with sources; do not erase the original record. Every entry should give (a) scope, (b) verified result, (c) files/commit/log evidence, (d) unresolved issues, (e) next handoff.

## 2026-11-12 — Step 11: pinned semantic/coverage evidence crosswalk, 14 original ZIPs and nine added-method attribution

**Milestone/scope:** Step 11 semantic evidence expanded substantially; **not fully CLOSED**, since human/maintainer semantic oracle and targeted backend/exact-patch reruns remain unverified. Original v2 **153 runner PASS / 31 provisional FAIL / 14 UNVERIFIED** and frozen Step 7 **153/9/36** and Step 8 indicators unchanged. No claim of journal-ready semantic failure detection.

**Executed and independently supported evidence:**
1. Reopened [AGENTS.md](../AGENTS.md), [PROJECT_STATE.md](PROJECT_STATE.md), this log, [Step 6 per-run review](../results/2026-11-12/STEP6_FAIL_REVIEW_31.csv), [Step 7 14-case ledger](../results/2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv), and linked pinned-dataset artifacts before proceeding. Identified 16 unresolved and 2 environment-sensitive FAILs, 4 invalid enhanced tests, and 14 UNVERIFIED from prior outcome audit as first unfinished semantic gate.
2. Created [pinned model/test patch structural audit](../scripts/step11_semantic_structural_audit.py) and [45-case archived JSON](../results/2026-11-12/STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json), verified successful [CI #43262365929](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43262365929). Matched **45/45 exact run identities** (31 FAIL + 14 UNVERIFIED; 20 distinct tasks) against agent revision `b5515d1dce40036633293b70477f0633b24593f7`, augmented test revision `79fc07a8f4ce5e3720e069948073f5f910b7577b`, and all 31 Step 6 enhanced test SHA references. Found direct same-file collision for **all 4/4** model/test overlap records, no such collision for nine skipped-coverage records, and **65 `build/` generated paths among 74 changed diff files** in the Requests large-patch case. Did not perform semantic rerun.
3. Added [read-only original ZIP re-audit](../scripts/step11_raw_artifact_reaudit14.py), verified successful [CI #43263048387](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43263048387). Downloaded all 14 short-retention per-patch `sweabs-result-*` ZIPs freshly via `gh run download` using CI `actions:read` permissions, checked **14/14** `metadata.json` sample, task, model patch SHA; found **14/14** original `test_output.txt`, and independently cross-compared **14/14** test-patch SHA against the pinned structural crosswalk. Archived [14-run metadata/test-log digest audit](../results/2026-11-12/STEP11_RAW_ARTIFACT_REAUDIT14_v1.json); raw ZIPs, prediction patches and full test logs stayed private/in temporary CI directories. Runtime skip details corroborate prior 4/28/1 skips in the three repeated Django task families: PostgreSQL-specific (`django-12039`), mixed DB-specific/baseline suite (`django-14434`), unsupported `supports_json_field_contains` (`django-15503`). No runner label inferred.
4. Added [method-to-log attribution script](../scripts/step11_skip_attribution.py) and [nine-run method evidence](../results/2026-11-12/STEP11_SKIP_ATTRIBUTION_9_v1.json), verified successful [CI #43264326911](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43264326911). Extracted only **newly added** `def test_*` names from pinned SWE-ABS unified diff and matched to original Django verbose test result lines: `django-12039` **13 added / 9 PASS / 4 skipped** in each sample; `django-14434` **1 added / 1 PASS / 0 skipped**, despite **28 total suite skips** in each sample; `django-15503` **10 added / 8 PASS / 1 skipped / 1 not found in log** in each sample. These counts do NOT prove all modified *existing* tests, inheritance or setup coverage. No automatic PASS promotion or post-hoc label changes.
5. Authored [Step 11 semantic validity/coverage report](../results/2026-11-12/STEP11_SEMANTIC_VALIDITY_GATE_v1.md) with explicit evidence hierarchy, opposing interpretations, actual changed-path collisions, artifact-log SHA linkages and remaining controlled rerun/oracle prerequisites.

**Interpretation vs evidence:** A total suite skip count does not equal count of skipped newly augmented methods; especially `django-14434`, where the one identified added method passed in all three samples. This could mean the Step 7 conservative exclusion over-excludes *if* no existing methods were modified, but that condition is **unverified**. Conversely `django-12039` has genuinely skipped new PostgreSQL cases, and `django-15503` has a skipped new containment test plus one added method absent from the chosen verbose log. Do not treat mere log absence as proof of test semantics or backend failure.

**Next exact work:** Step 11 **independent semantic validity/coverage**: inspect full in-place `django-14434` test patch and `django-15503` not-seen new Oracle method; run controlled backend-qualified test setups and preserve submitted original agent patch for four overlaps; prove Requests full tested-tree patch identity; independently review 16 unresolved/2 environment-sensitive FAIL issue/test contracts. Any new label assignment needs separately versioned record and sensitivity analysis without modifying v2/Step 7 v1. If oracle/reruns infeasible, constrain research paper to preliminary process vs runner observations and transparent limitations. **Step 12 remains TODO.**

## 2026-11-12 — Step 11: independent pinned Python reproduction and task-aware robustness

**Scope:** Completed Step 11 **technical reproduction/robustness and independent software raw-event spot-checks**. **Step 11 NOT fully closed**: independent human/maintainer semantic test-validity and coverage adjudication remain open. Never alter original v2 runner labels, Step 7 v1 outcome screens or frozen Step 8 indicators to obtain desired AUROCs.

**Evidence-verified actions (repository links):**
- Re-read [AGENTS](../AGENTS.md), [PROJECT_STATE](PROJECT_STATE.md), prior [WORK_LOG](WORK_LOG.md), Step 7 source labels, Steps 8–10 implementations and [corrected analysis v2](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json); confirmed Step 11 first unfinished.
- Detected and fixed an **implementation-only** Python Django `runtests.py` regex escaping mismatch ([commit ec225c0](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/ec225c035818d826eed0ad49e6a3487381b10c2d)); no Step 8 formula change or archived feature reclassification.
- Downloaded 296 rows from public pinned-revision Hugging Face dataset-server to a *temporary* remote workspace. Executed separate Python 3.11 source scripts against those rows, with dataset-loader adapter for snapshot input: **Step 9 `--check` PASS** on 198/198 exact sample/instance/patch SHA, 73 tasks, 198 parseable terminal status sets, 191 detected verification runs; **Step 10 corrected v2 `--check` PASS**; [Step 11 robustness Python script](../scripts/step11_robustness.py) generated [robustness JSON](../results/2026-11-12/STEP11_EXPLORATORY_ROBUSTNESS_v1.json) and its `--check` PASSED. Do not call this first snapshot test a full independent HF Python loader.
- Added [read-only CI workflow](../.github/workflows/step11-reproduction.yml) with **pinned** `datasets==4.8.5` and `huggingface_hub==1.33.0`; initial [CI run #43259079100](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43259079100) PASS; pinned [run #43259488165](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43259488165) PASS. Finally [run #43260088649](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649) **SUCCESS** from clean GitHub checkout, Python 3.11.18. Reviewed actual job steps and logs: five [synthetic parser unit tests](../tests/test_step9_indicators.py) PASS, pinned HF Step 9 full `datasets.load_dataset` + `--check` PASS, Step 10 AUROC `--check` PASS, Step 11 task-aware robustness `--check` PASS, new original-trace recount PASS, read-only `git diff --exit-code` PASS.
- The independently written [trace recount script](../scripts/step11_trace_spotcheck.py) selected the first two PASS, first FAIL, and first UNVERIFIED in each sample by original Step 7 offset: [12-case JSON from passing CI job logs](../results/2026-11-12/STEP11_TRACE_SPOTCHECK_12_v1.json), **12 × 14 = 168 feature comparisons, zero mismatches**. The checks do not independently label test semantic correctness, and no raw trajectory output was committed.
- Produced the [full Step 11 research report](../results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md), including post-hoc, task-aware sensitivity: duplicate rate primary run-level AUROC **0.489**, task-macro **0.522**, within-project **0.390** (only three projects with comparable cross-task class pairs), leave-one-positive-task influence **0.382–0.620**. Broad raw-runner-only target: **0.708 / 0.741 / 0.738**, leave-one-positive-task **0.683–0.759**. Primary positive task IDs only five; full quantitative interpretation remains provisional. These Step 11 diagnostics are **post-hoc exploratory**, not confirmatory or out-of-sample predictive tests.

**Limitations/opposing explanations:** Duplicates may reflect reasonable retry, project/test setup or task difficulty; missing augmented assertions and invalid enhanced tests produce uncertain outcomes. Five primary positive task IDs and task/project confounders make generalization weak. The broader label analysis may include invalid/problematic tests; conversely conservative exclusion may mask true failures. No human semantic oracle was produced. Source runner v2 counts **153/31/14** and Step 7 primary **153/9/36** unchanged.

**Exact NEXT:** Step 11 **independent semantic validity/coverage gate**, especially the 16 unresolved and 2 environment-sensitive Step 6 FAIL reviews, four invalid enhanced tests if broad-label inference is discussed, and 14 Step 7 UNVERIFIED. Decide from new defensible evidence or constrain paper claims; retain append-only versioning for reruns. Only then Step 12 qualitative case studies. Update all handoff docs on next verified change.

## 2026-11-12 — Steps 8–10: frozen trajectory features and task-aware exploratory AUROCs

**Scope/status:** Step 8 **DONE (precommitted indicator specification)**; Step 9 **DONE for 198/198 exact-match derived feature extraction (independent Python reproduction remains unverified)**; Step 10 **DONE at exploratory, task-aware in-sample AUROC scope (no validated predictor)**. The first unfinished milestone is now **Step 11 independent reproduction/robustness**. Unchanged research question, exact patch identities, raw v2 runner labels and Step 7 v1 eligibility definitions.

**What happened and immutable evidence order:**
1. Reopened [AGENTS](../AGENTS.md), [PROJECT_STATE](PROJECT_STATE.md), and [prior WORK_LOG](WORK_LOG.md); cross-checked [Step 7 primary/sensitivity labels](../results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv) and [pilot selection script](../scripts/pilot.py).
2. Inspected the actual Hugging Face `train` dataset row schema independently of outcome association. Fields include `sample`, `instance_id`, `resolved`, `patch`, `n_steps`, and `messages` with assistant terminal/file_editor tool calls and tool return IDs. Confirmed current dataset revision equals frozen `b5515d1dce40036633293b70477f0633b24593f7`. Before full feature extraction, committed [Step 8 frozen feature/analysis spec](STEP8_FROZEN_INDICATORS_v1.md) at [commit 3d94b5c](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/3d94b5c227fbb58c94952bea0623ad398785102c), then [Step 9 Python extractor](../scripts/step9_extract_trajectory_features.py) at [commit 290550d](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/290550d478bf56d3b8052e8bd1470896dbd5fa30).
3. Extracted the frozen features from 296 dataset viewer rows using browser-resident JavaScript implementing the same indicator rules; **198 resolved/198 exact (sample, instance, SHA-256 patch) matches, no mismatches**, across 73 task IDs. Archived [198-row feature CSV](../results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv) at [commit cc756bf](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/cc756bfeb27f763cf57c2b30f7a2ef135d00df2d) and [Step 9 coverage JSON](../results/2026-11-12/STEP9_COVERAGE_v1.json) at [commit 64b8124](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/64b81241099f0ae692049e6aa16ecef62becbc75). **198/198** terminal error statuses were parsable; **191/198** runs had a recognized verification command; seven post-verification edit features missing by definition. Public results store derived counts only, not raw trajectory text.
4. Added [Python Step 10 script](../scripts/step10_analyze_frozen_features.py) and computed all **four frozen individual features × four prespecified Step 7 target screens**, 500 task-ID-cluster bootstrap replicates (seed 20261112), via a browser-independent JavaScript calculation on the committed feature and label CSVs. The [full Step 10 report](../results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md) and [corrected v2 metrics](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) are checked into GitHub.
5. **Detected and corrected an inference bug instead of hiding it:** the first archived [v1 JSON](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v1.json) sampled clusters using low-order PRNG modulo; at 64 clusters the sample pattern repeated and confidence intervals were degenerate. v1 point estimates remained unchanged, but **all v1 bootstrap intervals must be treated invalid**. Fixed the [Python script](../scripts/step10_analyze_frozen_features.py) and generated [v2 corrected bootstrap JSON](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) using high-bit scaled sampling. Recorded the bug in the report and [evidence manifest](../results/2026-11-12/MANIFEST.md); did not silently overwrite v1.

**Main numerical outcomes (in-sample AUROC, not validated predictive accuracy):**

| Fixed target | Eligibility (PASS/FAIL/excluded) | Duplicate-terminal AUROC | 95% task-cluster bootstrap CI |
| --- | --- | ---: | --- |
| Conservative primary | 153/9/36; 61 tasks and only 5 FAIL task IDs | **0.489** | 0.270–0.706 |
| Noninvalid FAIL sensitivity | 153/27/18 | **0.721** | 0.565–0.857 |
| Raw runner-only sensitivity | 153/31/14 | **0.708** | 0.562–0.834 |
| Hypothetical skip-as-PASS | 162/9/27 | **0.478** | 0.255–0.686 |

Other primary AUROCs: explicit terminal error rate **0.599** (0.420–0.790), negated recognized verification presence **0.480** (0.459–0.497), editor calls after last recognized verification **0.435** (0.166–0.757; six primary feature-missing runs). There is no class-independent tuned threshold, model fit, p-value or held-out validation. The difference between 0.489 (primary) and 0.708 (raw runner-only) means labels materially affect the interpretation; do **not** claim the signals establish unreliable success.

**Opposing explanations and limitations:** The original coding-task difficulty and project may drive both trajectory length/repeated commands and stronger-test outcomes. Conversely, overly strict conservative filtering leaves only five distinct positive task IDs, weakening power. The primary review-supported FAILs are still provisional; the 14 UNVERIFIED, 16 unresolved and 2 environment-sensitive FAIL test-validity issues have not been independently resolved. A repeated command may be rational verification, and regex-recognized test commands are incomplete proxies. [Step 10 report](../results/2026-11-12/STEP10_QUANTITATIVE_REPORT_v1.md) records further evidence and competing interpretations.

**Unverified reproduction boundary:** Browser-side extraction and analysis were executed; the checked-in pinned **Python `--check` scripts were NOT independently run end-to-end**, and no CI job, trace-by-trace independent spot-check, or oracle adjudication is claimed. [Manifest](../results/2026-11-12/MANIFEST.md) identifies the GitHub blob digests, file sizes and exact links. The isolated local container could not resolve external network hosts. A remote browser session permitted dataset fetching but did not provide a verified separate Python checkout.

**Next exact action:** **Step 11** — independently run the Python pipeline from clean checkout, compare full feature/metric files and fix any discrepant implementation by versioned amendment; inspect a sample of raw traces, assess task/project/length confounding and label-policy sensitivity with task-disjoint designs, prioritize external semantic validity and controlled reruns, then proceed to qualitative cases and paper only with proportionate claims.

**Documentation synchronized:** PROJECT_STATE yes; WORK_LOG yes; README yes; AGENTS yes; results index yes; dated results MANIFEST yes. No original evidence or runner outcomes changed.

## 2026-11-12 — Step 7: 14-case UNVERIFIED triage and provisional analysis-label freeze

**Milestone/scope:** Step 7 **DONE for documentary triage and versioned provisional eligibility/sensitivity screening**. **No human oracle, no fresh per-patch ZIP examination, no Docker rerun, no new trajectory indicator, and no alteration of any prior runner outcome.** Step 8 is NEXT.

**Source-based verification this session:**
- Read [AGENTS.md](../AGENTS.md), [PROJECT_STATE](PROJECT_STATE.md) and this log before proceeding. Queried [recent commits](https://github.com/Foysal-Munsy/sweabs-free-eval/commits/main/) and [Actions history](https://github.com/Foysal-Munsy/sweabs-free-eval/actions) for changes. The documented v2 remained the latest evaluation-label data before this Step 7 screening.
- Independently re-joined the [198-run v2 CSV](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv) to 83 historical + 115 recent [audit-evidence CSVs](../results/2026-11-12/MANIFEST.md) on sample/offset and checked instance, patch SHA and outcome. **198/198 evidence matches, 198 unique (sample, instance, patch) identities, 73 tasks, no mismatches**. Joined all 31 FAIL against the [Step 6 review ledger](../results/2026-11-12/STEP6_FAIL_REVIEW_31.csv): **31/31 matched**, with 9 supported, 4 invalid-test, 2 environment-sensitive, 16 unresolved.
- Looked up GitHub Actions artifact metadata for the **11 workflow runs** containing the 14 UNVERIFIED records; all 14 expected `sweabs-result-*-*` per-patch artifact names were present and not expired. **Did not download or re-examine each raw ZIP in this session; prior detailed audit tables remain the substantive raw-evidence basis.**
- Triaged **14 UNVERIFIED across 6 tasks**: **9 skipped/backend coverage; 4 original-model/augmented-test-file overlaps; 1 large generated-patch integrity gap**. None was promoted to observed PASS/FAIL.

**Artifacts created, linked and GitHub-fetched:**
- [198-row STEP7_ANALYSIS_LABELS_v1.csv](../results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv) — initial commit [7c772e8](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/7c772e8ddfdf4d69d8e3996c8dba9691d2d11c57), 51,518 bytes; [14-row STEP7_UNVERIFIED_TRIAGE_14.csv](../results/2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv) — [68a3cfd](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/68a3cfd377fd51df4d66d796d043a5e50e5bab38), 7,965 bytes.
- [Source-constrained deterministic rebuild/check script](../scripts/build_step7_analysis_labels.py) — [26d7fb4](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/26d7fb4c2f2f0b07808e1decbd5aa38946863f84); [Step 7 documentary report with competing interpretations and exact decisions](../results/2026-11-12/STEP7_TRIAGE_AND_LABEL_POLICY.md) — [04d0aa3](https://github.com/Foysal-Munsy/sweabs-free-eval/commit/04d0aa319d156a7fe71fb4e6bcad48aa82168be3).
- [Evidence manifest](../results/2026-11-12/MANIFEST.md) includes **GitHub-read-back byte lengths and recomputed SHA-256** for these four new artifacts. The isolated local terminal could not resolve GitHub to clone, so the Python `--check` was **not** independently run against a cloned checkout; that end-to-end reproducibility check remains **unverified**. The generating logic was validated at the join/count/output level in this session.

**Provisional analysis-policy freeze (before feature extraction):**

| Scenario | 0 (runner PASS) | 1 (provisional FAIL) | Excluded |
| --- | ---: | ---: | ---: |
| Conservative primary: PASS vs Step 6 review-supported `valid_failure` | 153 | 9 | 36 |
| Sensitivity A: include unresolved/environment-sensitive FAIL | 153 | 27 | 18 |
| Sensitivity B: all observed runner FAIL (includes 4 invalid-test reviews) | 153 | 31 | 14 |
| Sensitivity C: hypothetical 9 skipped UNVERIFIED as PASS | 162 | 9 | 27 |

**Limits/opposing interpretation:** The primary target has **162 rows / 61 distinct task IDs and only 9 positive FAIL observations across 5 tasks**; the data must not be treated as 162 independent task IDs or a gold-standard oracle. A runner-defined study could reasonably prefer all 31 FAILs; this alternative is preserved as Sensitivity B, with known test-validity weaknesses stated. The skipped-as-PASS scenario is *only an assumption* and does not reclassify v2. No predictive association is reported.

**Unresolved evidence:** Four overlap runs require non-destructive exact-patch rerun design, nine backend-skipped runs require targeted coverage checks, `psf__requests-1142` needs full-patch integrity verification; independent validity review is still missing for Step 6 provisional judgments. Artifact retention is 14 days, with separate private raw backups documented in [manifest](../results/2026-11-12/MANIFEST.md). No task reruns were scheduled or performed.

**Next exact action:** **Step 8 — freeze a theory-driven trajectory indicator specification** (event schema, parsing rules, run-level formulas and denominators, missingness, exact sample/instance/patch matching, leakage controls, task dependence), then test parser coverage without outcome-driven tuning. Track targeted reruns and human oracle checks as separate outstanding validity tasks; do not convert provisional Step 7 screens into final semantic truth.

**Documentation synchronized:** PROJECT_STATE = yes; WORK_LOG = yes; README = yes; AGENTS = yes; results index = yes; archive manifest = yes. All public files; original v1/v2/raw materials unchanged.

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
