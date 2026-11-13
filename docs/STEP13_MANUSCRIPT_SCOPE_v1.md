## Mentor handoff refinement (v0.2 — 2026-11-13)

- Added [cohort/validity section](../paper/sections/outcome_audit.tex), [task-aware robustness and source-computed AUROC interval figure](../paper/sections/robustness_and_plot.tex), [future blinded human annotation protocol](../paper/sections/interpretation_and_validation.tex), and [data/AI disclosure section](../paper/sections/reproducibility_and_ethics.tex).
- Added [mentor review brief](../paper/MENTOR_REVIEW_BRIEF.md), [old-to-current review response](../paper/REVIEW_RESPONSE_MATRIX_v1.md), and [source-verified literature audit](../paper/LITERATURE_SOURCE_AUDIT_2026-11-13.md). New references are SWE-Cycle, the original 2024 SWE-bench Verified release, and the February 2026 benchmark limitations report.
- These changes are documentation/manuscript extensions, **not** changes to four frozen indicators, label targets, patch identities, or original runner output. Step 13 remains **IN PROGRESS until the mentor/coauthors review claims and approve any needed additional experiments**. Step 14 has not started.

# Step 13 manuscript scope — initial draft v0.1 (2026-11-13)

**Technical audit:** [GitHub build #43450060997](https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/43450060997) SUCCESS; four-page journal-style PDF, parsed BibTeX, Overleaf source ZIP and PDF preview archived as short-lived workflow artifacts; original experimental data unchanged. Human visual/semantic/citation review remains unverified.

**Status:** Step 13 manuscript draft in progress. Overleaf-compatible \`paper/main.tex\` and \`paper/references.bib\` provide an initial full-section academic paper, with a claim-evidence matrix, read-only build workflow and bibliography. Do **not** call Step 13 fully DONE until successful PDF verification, human coauthor/mentor scientific review and complete source/citation audit.

Scientific claim: exploratory, in-sample runner association with negative/inconclusive conservative discrimination and substantial label-policy sensitivity, not a validated true-semantic-failure detector. Current 198-run exact-patch corpus, 153/31/14 original outcomes and Step 7 153/9/36 primary labels remain immutable. There are only five distinct positive tasks under primary policy.

This manuscript **does not** port the earlier September six-indicator composite and synthetic AUROC .663/OR 2.18 into the 2026 real-data results. Four fixed univariate indicators, task-cluster uncertainty and the eight deterministic Step 12 source-audited case slots are reported instead.

Before closure: verify PDF build and inspect visual output; independently check every numerical sentence and table against frozen v2, source-pinned citation metadata, full state and case ledgers; confirm author list/order, research provenance, AI-use disclosure and coauthor/mentor sign-off. Step 14 will cover target venue selection, comprehensive reproducibility and paper-submission requirements. If semantic defect prediction becomes a requirement, new versioned human validation/out-of-sample experiments are necessary.
