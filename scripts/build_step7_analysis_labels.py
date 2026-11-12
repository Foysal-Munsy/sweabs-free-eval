#!/usr/bin/env python3
"""Rebuild Step 7 provisional labels from immutable v2 and audit/review CSV inputs.

This freezes *eligibility rules*, not semantic ground truth. No evaluation is rerun.
Usage: python scripts/build_step7_analysis_labels.py [--check]
"""
import argparse
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "2026-11-12"
V2 = OUT / "sweabs_full_198_cumulative_v2.csv"
HIST = OUT / "sweabs_historical_83_reaudit_evidence.csv"
RECENT = OUT / "sweabs_samples2_3_full_audit_evidence_115.csv"
STEP6 = OUT / "STEP6_FAIL_REVIEW_31.csv"
MASTER = OUT / "STEP7_ANALYSIS_LABELS_v1.csv"
TRIAGE = OUT / "STEP7_UNVERIFIED_TRIAGE_14.csv"
REPO = "Foysal-Munsy/sweabs-free-eval"

FOLLOWUPS = {
    "partial_coverage_skips": ("P2", "Identify exact skipped strengthened assertions and rerun with appropriate supported database/backend under versioned comparable conditions; retain existing result."),
    "patch_file_overlap": ("P1", "Design non-destructive patch/test setup preserving all submitted patch files; rerun exact patch and augmented tests as a separately versioned result only after verifying before/after source diff."),
    "whole_patch_integrity_unproven": ("P1", "Verify entire submitted patch including generated build/lib files against tested tree; if impossible, execute controlled exact-patch rerun without changing frozen selection."),
}

MASTER_COLUMNS = ["sample","offset","instance_id","patch_sha256","run_id","raw_outcome_v2","step6_review_status","step7_triage_category","primary_y","noninvalid_sensitivity_y","runner_only_sensitivity_y","skipped_as_pass_scenario_y","primary_exclusion_reason","source_audit_csv","source_run_url"]
TRIAGE_COLUMNS = ["sample","offset","instance_id","patch_sha256","run_id","runner_passed","runner_failed","runner_skipped","triage_category","audit_reason","patch_identity_or_coverage_boundary","priority","required_followup","source_audit_csv","source_run_url","new_rerun_performed"]

def read(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def index(rows):
    keys = [(r["sample"], r["offset"]) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate sample/offset")
    return dict(zip(keys, rows))

def output(rows, columns, path, check):
    import io
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\r\n")
    writer.writeheader()
    writer.writerows(rows)
    expected = buffer.getvalue().encode("utf-8")
    if check:
        if path.read_bytes() != expected:
            raise ValueError(f"Output mismatch: {path}")
    else:
        path.write_bytes(expected)

def build(check=False):
    v2, historical, recent, step6 = (read(path) for path in (V2, HIST, RECENT, STEP6))
    if (len(v2), len(historical), len(recent), len(step6)) != (198, 83, 115, 31):
        raise ValueError("Unexpected input shape; inspect version change")
    if len({(r["sample"], r["instance_id"], r["patch_sha256"]) for r in v2}) != 198:
        raise ValueError("Duplicate observation identity")
    evid = index(historical + recent)
    reviews = index(step6)
    master, triage = [], []
    for v in v2:
        key = v["sample"], v["offset"]
        e = evid.get(key)
        rv = reviews.get(key)
        if not e or e["instance_id"] != v["instance_id"] or e.get("patch_sha256", e.get("sha")) != v["patch_sha256"] or e.get("candidate", e.get("audited_outcome")) != v["outcome"]:
            raise ValueError(f"Missing or mismatched raw-audit evidence: {key}")
        if (v["outcome"] == "FAIL") != (rv is not None):
            raise ValueError(f"Step 6 coverage mismatch: {key}")
        run_match = re.match(r"^pilot_(\d+)_", v["run_id"])
        if not run_match:
            raise ValueError(f"Unexpected run ID: {v['run_id']}")
        run_url = f"https://github.com/{REPO}/actions/runs/{run_match.group(1)}"
        source = HIST.name if int(v["sample"]) == 1 or (int(v["sample"]) == 2 and int(v["offset"]) < 20) else RECENT.name
        category = ""
        if v["outcome"] == "UNVERIFIED":
            reason = e.get("reason", e.get("outcome_reason", ""))
            category = ("partial_coverage_skips" if "skip" in reason else
                        "patch_file_overlap" if "diff_changed" in reason or "reverted" in reason else
                        "whole_patch_integrity_unproven")
            if category not in FOLLOWUPS:
                raise ValueError(f"Unrecognized category: {key}")
            priority, followup = FOLLOWUPS[category]
            boundary = {
                "partial_coverage_skips": "Patch identity reported preserved; required test coverage incomplete",
                "patch_file_overlap": "Model-patch file overwritten/reset by augmented-test setup",
                "whole_patch_integrity_unproven": "Whole submitted large patch diff not established",
            }[category]
            triage.append(dict(sample=v["sample"], offset=v["offset"], instance_id=v["instance_id"],
                patch_sha256=v["patch_sha256"], run_id=v["run_id"], runner_passed=v["passed"],
                runner_failed=v["failed"], runner_skipped=v["skipped"], triage_category=category,
                audit_reason=reason, patch_identity_or_coverage_boundary=boundary,
                priority=priority, required_followup=followup, source_audit_csv=source,
                source_run_url=run_url, new_rerun_performed="NO"))
        review_status = rv["semantic_review_status"] if rv else ""
        if rv and (rv["patch_sha256"] != v["patch_sha256"] or rv["instance_id"] != v["instance_id"]):
            raise ValueError(f"Step 6 patch identity mismatch: {key}")
        primary = ("0" if v["outcome"] == "PASS" else
                   "1" if v["outcome"] == "FAIL" and review_status == "valid_failure" else "")
        noninvalid = ("0" if v["outcome"] == "PASS" else
                      "1" if v["outcome"] == "FAIL" and review_status != "invalid_test" else "")
        runner = "" if v["outcome"] == "UNVERIFIED" else ("0" if v["outcome"] == "PASS" else "1")
        scenario = "0" if category == "partial_coverage_skips" else primary
        exclusion = ("" if primary else category if v["outcome"] == "UNVERIFIED" else
                     f"step6_{review_status}")
        master.append(dict(sample=v["sample"], offset=v["offset"], instance_id=v["instance_id"],
            patch_sha256=v["patch_sha256"], run_id=v["run_id"], raw_outcome_v2=v["outcome"],
            step6_review_status=review_status, step7_triage_category=category,
            primary_y=primary, noninvalid_sensitivity_y=noninvalid,
            runner_only_sensitivity_y=runner, skipped_as_pass_scenario_y=scenario,
            primary_exclusion_reason=exclusion, source_audit_csv=source,
            source_run_url=run_url))
    if len(master) != 198 or len(triage) != 14:
        raise ValueError("Unexpected generated row counts")
    if Counter(r["triage_category"] for r in triage) != Counter({
        "partial_coverage_skips": 9, "patch_file_overlap": 4, "whole_patch_integrity_unproven": 1
    }):
        raise ValueError("Unexpected triage distribution")
    if Counter(r["semantic_review_status"] for r in step6) != Counter({
        "valid_failure": 9, "invalid_test": 4, "unresolved": 16, "environment_sensitive": 2
    }):
        raise ValueError("Unexpected Step 6 review distribution")
    for column, expected in [
        ("primary_y", (153, 9, 36)),
        ("noninvalid_sensitivity_y", (153, 27, 18)),
        ("runner_only_sensitivity_y", (153, 31, 14)),
        ("skipped_as_pass_scenario_y", (162, 9, 27)),
    ]:
        c = Counter(r[column] for r in master)
        if (c["0"], c["1"], c[""]) != expected:
            raise ValueError(f"Unexpected {column} distribution: {c}")
    output(master, MASTER_COLUMNS, MASTER, check)
    output(triage, TRIAGE_COLUMNS, TRIAGE, check)
    print(f"Step 7 {'validated' if check else 'generated'}: {len(master)} master; {len(triage)} triage; immutable v2 unchanged.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate existing outputs without writing")
    build(check=parser.parse_args().check)
