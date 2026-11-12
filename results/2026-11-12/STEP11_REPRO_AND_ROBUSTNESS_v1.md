# Step 11 — Independent reproduction and exploratory robustness (2026-11-12)

**Milestone status: IN PROGRESS.** Independent Python snapshot-based reproduction and task-aware robustness checks have passed. The read-only [GitHub Actions full pinned-dataset Python run](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43259079100) was launched; its status must be checked before declaring the full end-to-end `datasets` gate. Unresolved Step 6/7 enhanced-test semantic and coverage questions are still open. Nothing in this report asserts journal readiness.

## Research data and methodology boundaries

The [198-run Step 7 provisional label manifest](STEP7_ANALYSIS_LABELS_v1.csv), [original v2 runner CSV](sweabs_full_198_cumulative_v2.csv) and [Step 8 frozen indicator specification](../../docs/STEP8_FROZEN_INDICATORS_v1.md) are **unchanged**. Only an implementation-level bug in the Step 9 Python script was corrected: its Django test-command regex encoded a literal backslash before a wildcard instead of matching the period in `runtests.py`. This is a **versioned reproducibility repair** [source file](../../scripts/step9_extract_trajectory_features.py), not a change in the frozen indicator definition. The already archived Step 9 features had been generated using the correctly escaped JavaScript regex; independent Python comparison confirms the final CSV is unchanged.

All Step 11 task-macro, within-project, leave-one-positive-task-out and length diagnostics below were added **after** the Step 10 results were seen. They are explicitly **post-hoc exploratory stress tests, not confirmatory hypotheses or calibrated/generalizable classifier performance**. The original four prespecified Step 10 screens remain primary/secondary as documented.

## Reproduction evidence — observed execution

Using a separate remote Python 3.11.2 runtime, the public repository scripts and immutable CSV/JSON inputs were downloaded from GitHub. The public [Hugging Face dataset](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories) model metadata returned the pinned SHA `b5515d1dce40036633293b70477f0633b24593f7`. A snapshot of all **296** rows was fetched from the dataset-server viewer, copied to **temporary local storage only** (roughly 236 MB of raw NDJSON; NOT publicly committed), and passed to the unmodified Python Step 9 `produce()` implementation through an adapter overriding only its dataset-loader function. That comparison returned **PASS**, matching all 198 exact identities, all 198 feature rows, all fields, 73 distinct task IDs, 198/198 parseable explicit terminal statuses and 191 recognized test-command rows. The archived Step 9 feature CSV and coverage JSON were **not rewritten**.

The separately executed Python `scripts/step10_analyze_frozen_features.py --check` returned **PASS** on the versioned corrected v2 AUROC JSON. The Python `scripts/step11_robustness.py --check` returned **PASS** against the newly stored [Step 11 robustness JSON](STEP11_EXPLORATORY_ROBUSTNESS_v1.json). Five synthetic [unit tests](../../tests/test_step9_indicators.py) covering Django regex, normalized command duplicates, explicit nonzero terminal status, post-verification edit ordering, missing tool replies and malformed inputs passed in this separate runtime. These checks do not prove all synthetic regex matches are a perfect behavioral operationalization.

**Important limit:** The remote Python snapshot check is a reproducibility test of the **full archived rows and frozen code**, but it is **not** an independent `datasets.load_dataset` installation/fetch code path. The read-only GitHub Actions [Step 11 workflow](../../.github/workflows/step11-reproduction.yml) performs that stricter test using `datasets>=3,<5`, pinned source revision and `--check`. Treat that gate as **unverified until its job conclusion and logs are checked**; a workflow file alone is not a passed experiment.

## Exploratory task-aware robustness — duplicate terminal command rate

Source [machine-readable Python Step 11 results](STEP11_EXPLORATORY_ROBUSTNESS_v1.json), produced by [standard-library script](../../scripts/step11_robustness.py). Task-macro AUROC averages run-level feature scores by task only for tasks that have unanimous labels; **discordant tasks are excluded**. Within-project AUROC counts only positive/negative run pairs from different tasks but sharing a project prefix, so it is not a cross-validated estimate. Leave-one-positive-task-out removes **all runs for one positive task** and recomputes run-level AUROC; it is an influence check, not model training or test-set validation.

| Step 7 label screen | Run-level AUROC | Task-macro AUROC | Within-project AUROC | Range after omitting each positive task |
| --- | ---: | ---: | ---: | ---: |
| Primary (153 PASS/9 FAIL; **5 FAIL task IDs**) | **0.489** | **0.522** | **0.390** | **0.382–0.620** |
| Noninvalid (153/27; 13 FAIL task IDs) | **0.721** | **0.798** | **0.739** | **0.693–0.782** |
| All runner FAIL (153/31; 15 FAIL task IDs) | **0.708** | **0.741** | **0.738** | **0.683–0.759** |
| Hypothetical skipped-as-PASS (162/9; 5 FAIL task IDs) | **0.478** | **0.508** | **0.370** | **0.372–0.605** |

Primary task-macro calculation has **60 unanimous-label tasks**: just **4 positive task IDs**, because one discordant task was removed. Only **3 projects** have comparable same-project positive/negative cross-task pairs in all shown scenarios; within-project robustness is therefore a particularly narrow sample. The primary duplicate-command vs `n_steps` Spearman correlation is **−0.112** and `n_steps` itself has primary outcome AUROC **0.660**; these do **not** establish that length confounds the association, but they demonstrate baseline task-effort differences worth investigating. No post-hoc threshold, fit or p-value is claimed.

**Fact:** None of the primary duplicate-command robustness checks shows stable evidence of meaningful discrimination, while the broader label policies give higher and somewhat more stable in-sample AUROCs. **Interpretation:** The dataset's uncertain stronger-test label validity is a major factor; under the conservative primary screen the effective positive sample is very small. **Opposing explanations:** The restrictive documentary screen may discard true failure examples and reduce power, whereas including unresolved or invalid tests may create spurious correlations. Project-specific task difficulty, environment retries or rational repeated tests can also explain duplicate-command counts. A held-out task-disjoint predictive result is **unverified**, so an apparent AUROC under the broadest outcome must not be called a deployable detector.

## What remains before Step 11 can be closed

1. Verify the [Actions workflow run](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43259079100) has actually completed successfully, and inspect test logs/versions; if it fails, diagnose without silently changing frozen indicator definitions or Step 7 outcomes.
2. Record independent event-by-event sample spot checks or a structured audit of tool invocation/output integrity. The independent full Python calculation compared the archived outputs, but a separate human/manual event-level ground-truth review is **not yet done**.
3. Review unresolved Step 6 FAIL test validity (especially 16 unresolved, 2 environment-sensitive) and the Step 7 14 UNVERIFIED cases against original issue, original tests, augmented assertions and appropriate backends. New reruns, if done, must produce **new separately versioned evidence**; original counts and labels remain preserved.
4. Decide whether Step 11's remaining oracle/coverage questions can only be acknowledged as limitations, or require adjudication before journal-quality claims. No research conclusion may be promoted by moving labels after inspecting effects without versioning an explicit post-hoc amendment.

**Next:** after the remaining reproduction/semantic gates, Step 12 qualitative case studies, then Step 13 manuscript writing and Step 14 submission audit. Currently **Step 11 is in progress**, not journal submission-ready.
