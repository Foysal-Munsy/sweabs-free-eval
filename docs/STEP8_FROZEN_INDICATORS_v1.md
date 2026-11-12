# Step 8 — Frozen lightweight trajectory indicators v1

**Frozen before feature extraction/label-association inspection:** 2026-11-12 Asia/Dhaka.  
**Research question unchanged:** Among originally successful Gemini 3 Flash coding-agent runs, are lightweight original-trajectory messiness signals associated with provisional SWE-ABS stronger-test failure?  
**Dataset:** [tarsur385/swe-verified-gemini3-flash-trajectories](https://huggingface.co/datasets/tarsur385/swe-verified-gemini3-flash-trajectories), `train`; pinned prior dataset revision `b5515d1dce40036633293b70477f0633b24593f7`; original selection per [scripts/pilot.py](../scripts/pilot.py). The primary observation ID is `(sample, instance_id, sha256(patch.encode('utf-8')))`, not instance ID alone. Dataset viewer rows may differ from pinned revision; extraction MUST reject any hash mismatch rather than use a wrong row.

## Input schema checked before freeze

A source row has `instance_id`, `sample`, `resolved`, `patch`, `n_steps`, `num_messages`, and `messages`. Messages have `role` and `content`; assistant messages may contain `tool_calls` entries with `function.name` and `function.arguments`, where `arguments` is an object. Observed call types: `terminal`, `file_editor`, `finish`. `tool` messages are tool returns. No outcome labels are inside the feature formulas. Dataset schema evidence: [live dataset row viewer](https://datasets-server.huggingface.co/rows?dataset=tarsur385/swe-verified-gemini3-flash-trajectories&config=default&split=train&offset=0&length=1); this is **schema inspection only**, not evidence that all pinned rows are retrievable.

## Frozen exact computation rules

Iterate `messages` in stored chronological order. Consider only `assistant.tool_calls` where `function.name` is a string. `terminal` arguments must be a dict/object containing a string `command`; all other names remain calls but not terminal commands. Normalize terminal command with `" ".join(command.split())` (whitespace only; do not lowercase). Strip no path or argument. All counts are nonnegative integers.

1. **`tool_calls_total`**: count of all assistant tool-call entries whose `function.name` is string.
2. **`terminal_calls`**: count of calls whose name is exactly `terminal`.
3. **`editor_calls`**: count of calls whose name is exactly `file_editor`.
4. **`verification_commands`**: count of terminal commands matching the following whole-word regex (case insensitive): `(^|[^A-Za-z0-9_])(pytest|unittest|runtests\\.py|tox|nosetests)(?=$|[^A-Za-z0-9_])`, OR `python[0-9.]* -m (pytest|unittest)`, OR commands with whitespace + `test` preceded by a `python` invocation? **No**: only the first two conditions are included; running arbitrary `python script.py` does **not** qualify. This favors precision over broad detection.
5. **`duplicate_terminal_commands`**: count of terminal calls whose normalized command exactly appeared in any previous terminal call in that same run; repeated commands at any distance count once each additional occurrence.
6. **`immediate_duplicate_terminal_commands`**: count of terminal calls whose normalized command is identical to the *immediately previous terminal call's* normalized command (ignore nonterminal calls between terminal calls).
7. **`terminal_errors_observed`**: count of terminal-tool return messages with an explicit `'exit_code': nonzero integer`, `"exit_code": nonzero integer`, `'is_error': True`, or `"is_error": true` in the returned `content`. If there are multiple flags in the same tool return, count **one**. Match only `role=="tool"` content directly following a terminal call; match by `tool_call_id` to the preceding terminal call's `id` if present, otherwise mark this feature as missing (do not guess). Terminal return parser must not use human-readable text such as `Traceback` alone.
8. **`editor_after_last_verification`**: count of file_editor calls *strictly after* the last verification-matching terminal call, or **missing** if no verification command exists. End-of-trajectory counts do not imply absence of external tests.
9. **`any_verification`**: 1 if `verification_commands>0`, else 0.

**Derived normalized measures** (denominator is `max(1, terminal_calls)`): `duplicate_terminal_rate=duplicate_terminal_commands/max(1,terminal_calls)`; `terminal_error_rate=terminal_errors_observed/max(1,terminal_calls)`. Do not collapse missing to zero for `editor_after_last_verification` or error-rate calculations. Store assistant message count and dataset `n_steps` only as scope/baseline descriptors (not messiness primary predictors).

**Primary single-indicator statistical screens** (frozen now, no feature association inspected yet): `duplicate_terminal_rate`, `terminal_error_rate`, `any_verification`, `editor_after_last_verification`. For each use individual raw feature as a score for class 1 (FAIL), with direction **prespecified** as *higher duplicate rate*, *higher observed terminal error rate*, *lower verification presence*, *higher post-verification editor count* implying more messiness. Record both oriented AUROC and raw AUROC when feasible, including orientation; **do not flip after seeing results**. Ties count 0.5. Additional terminal and editor counts are descriptive, not post-hoc selected predictors. No model fitting, thresholds, p-hacking, optimal cutoffs or outcome-tuned indicators.

## Missing data and verification boundaries

- Require `resolved is True`, valid `sample`, `instance_id`, and **exact patch SHA-256 match** to the Step 7 master manifest. Duplicates/missing rows MUST be flagged; never fuzzy-match tasks or silently substitute trajectories. Compare all 198 identities before any reported analysis claim.
- A row with missing/non-list `messages`, malformed `tool_calls` or malformed `terminal.command` has **invalid feature extraction**; report exclusion rather than invent zero.
- Associate terminal return to terminal call using exact tool call ID from assistant's call and tool reply. Missing/duplicate IDs or missing replies imply `terminal_errors_observed` and `terminal_error_rate` are **missing for the run** (conservative), not zero.
- If no terminal call, `terminal_error_rate` is missing; duplicate-rate is set to zero by denominator convention and flagged as zero-exposure.
- If no verification call, `editor_after_last_verification` is missing; `any_verification=0`.
- Full text snippets/terminal output are **not** committed to public GitHub. Only aggregate derived features and identity hashes; no personal data or private trace release.
- Dataset revision must be pinned and recorded. Viewer-mediated extraction with no demonstrable revision pin is **unverified** even if hashes match: hash checks establish patch identity, but not necessarily identical full traces. Preserve coverage and source hashes and qualify conclusions.

## Analysis plan frozen with Step 8

Primary target: Step 7 `primary_y`: 153 runner PASS vs 9 review-supported FAIL; excluded 36. Additional targets `noninvalid_sensitivity_y`, `runner_only_sensitivity_y`, `skipped_as_pass_scenario_y` remain strictly **secondary** and must never be presented as observed semantic truth. Report distinct task IDs and FAIL task IDs. For each prespecified indicator, compute empirical AUROC via pairwise comparisons and **task-ID cluster bootstrap** (not run-iid bootstrap), 500 replicates with fixed PRNG seed `20261112` and 2.5/97.5 percentile interval using only replicates retaining both classes. Do not resample individual runs independently; duplicate task instances must move together. If one class or too few task clusters remain, report undefined. No statistical significance claims merely from an apparent AUROC. Include missing-feature denominators, baseline distribution, directional reverse interpretations, and any task-level confounding.

**Staging invariant:** This file and a versioned extractor specification must be committed *before* all-run feature extraction and any label-dependent statistics. Correct future errors by explicitly versioning an amendment; never silently edit indicator definitions after results.
