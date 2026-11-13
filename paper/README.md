# Overleaf-compatible research manuscript (Step 13 draft v0.1)

**Status:** Complete initial source-grounded manuscript draft, not author-reviewed or journal-submission-ready.

**Use in Overleaf:** Import the entire \`paper/\` folder as a new project, with main document \`main.tex\`; compiler **pdfLaTeX**; bibliography **BibTeX**. It uses the standard \`IEEEtran\` journal class as a working layout, **not** a verified target-journal-specific template. The GitHub Actions LaTeX workflow produces a PDF artifact without changing any frozen experiment file.

The current paper concerns the 198 real, originally passing Gemini 3 Flash runs, four prespecified individual indicators, a conservative task-cluster analysis, frozen sensitivity screens, and eight fixed case illustrations. It **does not reuse** synthetic six-feature composite AUROC 0.663 or synthetic logistic odds ratio 2.18 from the September draft. No trained model, held-out prediction, semantic truth oracle, or journal acceptance is claimed.

Before Step 13 can be declared DONE, the team must check every scientific statement, every bibliography record, select/confirm author names/order/affiliations and AI disclosure, review novelty and literature coverage more comprehensively, inspect the compiled PDF for layout and references, and obtain coauthor/mentor scientific feedback. Step 14 later audits the target venue and reproducibility gates; if semantic-defect prediction is desired, new human-reviewed labels/replication are necessary.

Canonical evidence: \`docs/PROJECT_STATE.md\`, \`results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json\`, \`results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md\`, \`results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md\`.

**Build locally:** \`cd paper && latexmk -pdf -halt-on-error -interaction=nonstopmode main.tex\`. \`main.pdf\` is intentionally a generated preview, not an archival source-of-truth result.
