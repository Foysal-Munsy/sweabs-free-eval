# Step 13 — Mentor-review candidate v0.2 (13 November 2026)

**Most recent verified technical build:** [Expanded read-only GitHub Actions #43454789699](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43454789699) — **success**; six-page PDF preview, BibTeX and full Overleaf-source ZIP artifacts. This does **not** certify scientific, human visual, or Q1 journal readiness. The current Overleaf ZIP contains the four modular section files and three mentor-review documents.

**Read first:** [Mentor scientific decision brief](MENTOR_REVIEW_BRIEF.md), [historical review response](REVIEW_RESPONSE_MATRIX_v1.md), [2026 literature source audit](LITERATURE_SOURCE_AUDIT_2026-11-13.md), and [claim/evidence matrix](CLAIM_EVIDENCE_MATRIX.md).

## Mentor-review refinement v0.2 — 13 November 2026

The manuscript now includes four separately editable source sections in [sections/](sections/): outcome validity and sample counts, task-aware robustness plus a deterministic TikZ interval figure, interpretive/expert-adjudication boundaries, and replication/AI disclosure. An updated [mentor review brief](MENTOR_REVIEW_BRIEF.md), [historical review-response matrix](REVIEW_RESPONSE_MATRIX_v1.md), and [verified literature audit](LITERATURE_SOURCE_AUDIT_2026-11-13.md) are included in the Overleaf ZIP. The [read-only manuscript workflow](../.github/workflows/paper-latex-build.yml) imports all section source files when building ZIP artifacts.

**Mentor-ready scope is limited to review of the scientific framing and evidence**. It is NOT the same as a final, journal-submission-ready manuscript; author/coauthor approval, comprehensive novelty survey, human semantic labels and external validation are outstanding.

# Overleaf-compatible research manuscript (Step 13 mentor-review draft v0.2)

**Earlier v0.1 verified CI:** [Final corrected-source run #43450060997](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43450060997) compiled a four-page PDF with BibTeX and uploaded both the Overleaf-importable source ZIP and PDF preview (short-lived GitHub Actions artifacts). Open that run and select the corresponding artifact in its Artifacts area. Source revision/checks remain in the research repository; this was draft v0.1; v0.2 current source is described above.

**Status:** Expanded six-page source-grounded scientific manuscript for mentor/coauthor review, **not** journal-submission-ready.

**Use in Overleaf:** Import the entire \`paper/\` folder as a new project, with main document \`main.tex\`; compiler **pdfLaTeX**; bibliography **BibTeX**. It uses the standard \`IEEEtran\` journal class as a working layout, **not** a verified target-journal-specific template. The GitHub Actions LaTeX workflow produces a PDF artifact without changing any frozen experiment file.

Current v0.2 concerns the 198 real, originally passing Gemini 3 Flash runs, four prespecified individual indicators, a conservative task-cluster analysis, frozen sensitivity screens, and eight fixed case illustrations. It **does not reuse** synthetic six-feature composite AUROC 0.663 or synthetic logistic odds ratio 2.18 from the September draft. No trained model, held-out prediction, semantic truth oracle, or journal acceptance is claimed.

Before Step 13 can be declared DONE, the team must check every scientific statement, every bibliography record, select/confirm author names/order/affiliations and AI disclosure, review novelty and literature coverage more comprehensively, inspect the compiled PDF for layout and references, and obtain coauthor/mentor scientific feedback. Step 14 later audits the target venue and reproducibility gates; if semantic-defect prediction is desired, new human-reviewed labels/replication are necessary.

Canonical evidence: \`docs/PROJECT_STATE.md\`, \`results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json\`, \`results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md\`, \`results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md\`.

**Build locally:** \`cd paper && latexmk -pdf -halt-on-error -interaction=nonstopmode main.tex\`. \`main.pdf\` is intentionally a generated preview, not an archival source-of-truth result.
