# Reproducibility and Artifact Provenance

This is a source- and script-oriented reproduction guide for the archived exploratory analysis. Exact original Docker test runs and their complete historical raw ZIPs are **not** all independently accessible from the public repository. Rebuilding the derived trajectory features/statistics is narrower than re-validating every SWE-ABS semantic failure.

## Pinned inputs

| Artifact | Recorded input or source |
| --- | --- |
| Original agent trajectories | [Gemini 3 Flash dataset revision `b5515d1dce40036633293b70477f0633b24593f7`](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories/tree/b5515d1dce40036633293b70477f0633b24593f7) |
| Strengthened tests | [SWE-Bench Verified ABS dataset](https://huggingface.co/datasets/OpenAgentLab/SWE-Bench_Verified_ABS), pinned `79fc07a8f4ce5e3720e069948073f5f910b7577b` |
| Original runner outcomes | [198-run v2 CSV](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv) |
| Original analysis labels | [Step 7 CSV](../results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv) |
| Exact trajectory features | [Step 9 CSV](../results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv) |
| Corrected AUROC and task bootstrap | [Step 10 v2 JSON](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) |
| Eight qualitative cases | [Step 12 roster](../results/2026-11-13/STEP12_CASE_ROSTER_v1.json) |

All joins require `(sample, instance_id, SHA-256(patch))`, not task ID alone. See the [source coverage ledger](../results/2026-11-12/STEP9_COVERAGE_v1.json) and [methodology](METHODOLOGY.md).

## Derived-analysis checks

The source-verified GitHub Actions job uses Python **3.11**, `datasets==4.8.5` and `huggingface_hub==1.33.0`. A clean checkout with public dataset access can run:

```bash
python -m pip install 'datasets==4.8.5' 'huggingface_hub==1.33.0'
python -m unittest discover -s tests -p test_step9_indicators.py -v
python scripts/step9_extract_trajectory_features.py --check
python scripts/step10_analyze_frozen_features.py --check
python scripts/step11_robustness.py --check
python scripts/step12_cases.py --check
python scripts/step12_cases.py --check --recount-source
```

The source-backed checks download public trajectories and may require substantial bandwidth and memory. They do **not** rerun all SWE-ABS augmented Docker tests. See the [Step 11 reproduction workflow](../.github/workflows/step11-reproduction.yml) ([successful audited run #43260088649](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43260088649)) and [Step 12 case audit workflow](../.github/workflows/step12-qualitative-audit.yml) ([successful run #43440488895](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43440488895)).

## Manuscript

`paper/` provides a working IEEEtran journal-style LaTeX manuscript. The paper-build workflow compiles it with BibTeX and publishes a PDF preview plus an import-ready source ZIP as short-retention GitHub Actions artifacts:

[Read-only manuscript build workflow](../.github/workflows/paper-latex-build.yml) · [Example successful six-page build](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43454789699).

## Independent checks and limitations

A separate frozen-loader check reproduced the 198 exact matched feature rows; a corrected Step 10 `--check` reproduced AUROCs and task-cluster bootstrap outputs, and Step 12 independently recounted eight exact source trajectories against 112 feature fields with zero mismatches. Sources: [Step 11 technical reproduction](../results/2026-11-12/STEP11_REPRO_AND_ROBUSTNESS_v1.md), [Step 12 independent recount](../results/2026-11-13/STEP12_SOURCE_RECOUNT_8_v1.json).

**Not verified:** independent human/maintainer semantic labels, full historical original Docker-tested-tree equivalence for separately executed controls, new-model transfer, calibrated prediction or public availability of every original result ZIP. The original 14 UNVERIFIED outcomes stay UNVERIFIED.
