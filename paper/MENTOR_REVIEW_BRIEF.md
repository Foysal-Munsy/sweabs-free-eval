# Mentor Review Brief — Step 13 v0.2 (13 November 2026)

**Decision requested:** Scientific go/no-go and experimental-extension guidance before a Q1 journal submission. This is a source-grounded, AI-assisted manuscript review candidate, NOT a submission or journal acceptance claim.

## One-paragraph study summary

We matched 198 originally successful Gemini 3 Flash coding-agent runs spanning 73 SWE-bench Verified task IDs to frozen, exact submitted patch SHA-256 records and audited SWE-ABS stronger-test runs. Original outcomes remain **153 PASS / 31 provisional FAIL / 14 UNVERIFIED**. Four frozen trajectory proxies were examined with task-cluster bootstrap and prespecified label-policy sensitivity. The conservative primary analysis has 153 PASS, nine documentary-supported provisional FAIL and 36 excluded, with only **five** distinct positive task IDs. Duplicate-terminal-command rate gives AUROC **0.489** (95% task-bootstrap CI **0.270–0.706**), while the broader runner-only sensitivity gives **0.708** (**0.562–0.834**). Eight prespecified exact-run illustrations show contradictory behavior and invalid/ambiguous enhanced tests. The study does not establish a trained predictor of semantic code defects.

**Primary evidence:** [original runner](../results/2026-11-12/sweabs_full_198_cumulative_v2.csv), [frozen Step 7 labels](../results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv), [corrected Step 10 AUROCs](../results/2026-11-12/STEP10_AUROC_TASK_CLUSTER_v2.json), [Step 11 claim boundary](../results/2026-11-12/STEP11_SCOPE_LIMITED_CLOSURE_DECISION_v1.md), [Step 12 eight cases](../results/2026-11-13/STEP12_QUALITATIVE_CASE_REPORT_v1.md).

## Materials for review

The [Overleaf manuscript](main.tex) and [source-checked bibliography](references.bib) now include a cohort table, documentary label categories, task-aware robustness table and a reproducible label-policy AUROC/CI figure, alongside qualitative examples and a transparent AI-disclosure draft. The [claim-to-evidence matrix](CLAIM_EVIDENCE_MATRIX.md) documents supporting artifacts. The [historical reviewer-response matrix](REVIEW_RESPONSE_MATRIX_v1.md) distinguishes resolved technical problems from unresolved scientific limitations.

## Six questions to decide before extensive writing polish

1. **Contribution:** Is a reproducible negative/inconclusive runner-association study showing substantial label-policy sensitivity sufficiently meaningful and novel for empirical software engineering?
2. **Gold labels:** Should two independent human/domain experts adjudicate the 31 runner FAIL records and selected coverage-limited cases before journal submission?
3. **Statistical sample:** What minimum independent positive-task and project/agent replication would support stronger prediction or generalizability claims? The current conservative target has only five positive tasks.
4. **Confounding:** Would a task-matched comparison, explicit difficulty adjustment or hierarchical analysis be necessary for the intended causal or associative claim?
5. **Venue:** Which journal and which Q1 index/year are intended? Confirm topic fit before selecting the journal-specific Overleaf template.
6. **Authorship and AI policy:** Confirm final authors/order/affiliations, contributions, AI-assistance disclosures and necessary supplementary files.

## Non-negotiable limitations to preserve

- No independently expert-adjudicated semantic gold labels; all 153 PASS are test-relative and 14 original UNVERIFIED labels remain unchanged.
- The primary analysis is effectively small: five positive task IDs, despite nine positive run rows.
- Same agent/model trajectory source; PASS-only selection and repository/task-difficulty confounding unaddressed.
- No trained or calibrated detector, no task-disjoint or cross-model held-out validation.
- Open benchmark exposure / contamination is a plausible external concern, **not measured for this model**.
- Technical PDF compilation and citation lookup do not prove Q1 journal readiness.

**Suggested sequence:** Review scientific framing and source evidence first. If the bounded contribution is acceptable, give content revision requests. If not, decide a new versioned empirical extension before polishing. Only afterwards run Step 14 venue-specific submission audit.

**Status:** Mentor-review candidate **after PDF build and visual confirmation**, not submitted. Human mentor approval and Q1 outcome remain **unverified**.
