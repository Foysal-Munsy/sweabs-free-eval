# Research Manuscript

Overleaf-compatible LaTeX source for the empirical study of process indicators and SWE-ABS strengthened-test runner outcomes among originally successful coding-agent runs.

## Files

| File | Contents |
| --- | --- |
| [`main.tex`](main.tex) | Main IEEEtran working manuscript (abstract, methods, results, analysis and limitations) |
| [`references.bib`](references.bib) | Bibliography with source-checked entries |
| [`sections/`](sections/) | Modular validity, task-aware robustness/figure, interpretation and reproducibility sections |
| [`CLAIM_EVIDENCE_MATRIX.md`](CLAIM_EVIDENCE_MATRIX.md) | Research claim-to-artifact provenance |

The manuscript's quantitative results are grounded in the archived [corrected Step 10 analysis](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json) and [eight-case qualitative audit](../results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md). Older synthetic AUROC/odds-ratio findings are not presented as real-data evidence.

## Build

Import this directory as an Overleaf project, select `main.tex` as the main file, and compile with **pdfLaTeX** and **BibTeX**. With a suitable local LaTeX distribution:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

A [read-only GitHub Actions workflow](../.github/workflows/paper-latex-build.yml) checks LaTeX compilation and produces PDF preview and source ZIP artifacts.

**Study status:** exploratory, label-sensitive runner-association study; no independently established semantic defect predictor, no external generalization validation, and no journal-submission claim. Author names, contribution declarations and venue-specific format remain to be finalized before submission.
