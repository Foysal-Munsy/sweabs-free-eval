#!/usr/bin/env python3
"""Step 12 deterministic illustrative case roster + independent pinned raw trace recount.

No raw messages or terminal commands are printed/written; only derived counts.
The eight-slot selection protocol was committed first at
docs/STEP12_CASE_SELECTION_PROTOCOL_v1.md.
Usage:
  python scripts/step12_cases.py --check
  python scripts/step12_cases.py --check --recount-source
"""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results/2026-11-12"
OUTPUT = ROOT / "results/2026-11-13/STEP12_CASE_ROSTER_v1.json"
LABELS = DATA / "STEP7_ANALYSIS_LABELS_v1.csv"
FEATURES = DATA / "STEP9_TRAJECTORY_FEATURES_v1.csv"
TRIAGE = DATA / "STEP7_UNVERIFIED_TRIAGE_14.csv"
REVIEW = DATA / "STEP6_FAIL_REVIEW_31.csv"
V2 = DATA / "sweabs_full_198_cumulative_v2.csv"
DATASET = "tarsur385/swe-verified-gemini3-flash-trajectories"
REVISION = "b5515d1dce40036633293b70477f0633b24593f7"
AUDIT_FIELDS = ("assistant_message_count", "tool_calls_total", "terminal_calls",
                "editor_calls", "verification_commands", "duplicate_terminal_commands",
                "immediate_duplicate_terminal_commands", "terminal_errors_observed",
                "editor_after_last_verification", "any_verification",
                "duplicate_terminal_rate", "terminal_error_rate",
                "zero_terminal_exposure", "error_coverage_complete")

def rows(path):
    with path.open(encoding="utf8", newline="") as f:
        return list(csv.DictReader(f))

def identity(row):
    return (int(row["sample"]), row["instance_id"], row["patch_sha256"])

def sort_id(row):
    return (row["instance_id"], int(row["sample"]), int(row["offset"]), row["patch_sha256"])

def indexed(items, name):
    m = {}
    for row in items:
        k = identity(row)
        if k in m:
            raise ValueError(f"duplicate {name} identity: {k}")
        m[k] = row
    return m

def build_roster():
    ll, ff, tt, rr, vv = [rows(p) for p in (LABELS, FEATURES, TRIAGE, REVIEW, V2)]
    if (len(ll), len(ff), len(tt), len(rr), len(vv)) != (198, 198, 14, 31, 198):
        raise ValueError("Unexpected frozen source row counts")
    fmap, tmap, rmap, vmap = [indexed(z,n) for z,n in
          ((ff,"feature"),(tt,"triage"),(rr,"review"),(vv,"v2"))]
    if set(identity(z) for z in ll) != set(fmap) or set(vmap) != set(fmap):
        raise ValueError("Frozen three-way identity mismatch")
    for x in ll:
        if x["raw_outcome_v2"] != vmap[identity(x)]["outcome"]:
            raise ValueError("Raw v2 label mismatches Step 7")
    ordered = []
    for x in ll:
        k=identity(x)
        if x["step6_review_status"] != rmap.get(k,{}).get("semantic_review_status",""):
            raise ValueError("Step 6 review identity/status mismatch")
        if x["step7_triage_category"] != tmap.get(k,{}).get("triage_category",""):
            raise ValueError("Step 7 triage identity/category mismatch")
        ordered.append((x,fmap[k]))
    slots=[]
    used_tasks=set()
    def choose(slot, candidates):
        for l,f in candidates:
            if l["instance_id"] in used_tasks:
                continue
            used_tasks.add(l["instance_id"])
            slots.append((slot,l,f))
            return
        raise ValueError("No identity for declared slot "+slot)
    def score_sort(items, reverse):
        return sorted(items,key=lambda pair:
            ((-1 if reverse else 1)*float(pair[1]["duplicate_terminal_rate"]),
             sort_id(pair[0])))
    choose("PRIMARY_FAIL_HIGH",score_sort([(a,b) for a,b in ordered if a["primary_y"]=="1"],True))
    choose("PRIMARY_FAIL_LOW",score_sort([(a,b) for a,b in ordered if a["primary_y"]=="1"],False))
    choose("PRIMARY_PASS_HIGH",score_sort([(a,b) for a,b in ordered if a["primary_y"]=="0"],True))
    choose("PRIMARY_PASS_LOW",score_sort([(a,b) for a,b in ordered if a["primary_y"]=="0"],False))
    fixed = (
        ("INVALID_TEST_CHALLENGE",lambda x: x["raw_outcome_v2"]=="FAIL" and x["step6_review_status"]=="invalid_test"),
        ("ENVIRONMENT_CHALLENGE",lambda x: x["raw_outcome_v2"]=="FAIL" and x["step6_review_status"]=="environment_sensitive"),
        ("SKIPPED_COVERAGE_CHALLENGE",lambda x: x["raw_outcome_v2"]=="UNVERIFIED" and x["step7_triage_category"]=="partial_coverage_skips"),
        ("PATCH_OVERLAP_CHALLENGE",lambda x: x["raw_outcome_v2"]=="UNVERIFIED" and x["step7_triage_category"]=="patch_file_overlap"))
    for slot,pred in fixed:
        choose(slot,sorted([(a,b) for a,b in ordered if pred(a)],key=lambda pair:sort_id(pair[0])))
    cases=[]
    for slot,l,f in slots:
        cases.append({
            "slot":slot, "sample":int(l["sample"]), "offset":int(l["offset"]),
            "instance_id":l["instance_id"], "patch_sha256":l["patch_sha256"],
            "raw_outcome_v2":l["raw_outcome_v2"], "primary_y":l["primary_y"] or None,
            "step6_review_status":l["step6_review_status"] or None,
            "step7_triage_category":l["step7_triage_category"] or None,
            "source_run_url":l["source_run_url"],
            "source_pr_url":rmap.get(identity(l),{}).get("pr_url") or None,
            "terminal_calls":int(f["terminal_calls"]),
            "duplicate_terminal_commands":int(f["duplicate_terminal_commands"]),
            "duplicate_terminal_rate":float(f["duplicate_terminal_rate"]),
            "terminal_errors_observed":int(f["terminal_errors_observed"]) if f["terminal_errors_observed"] else None,
            "verification_commands":int(f["verification_commands"]),
            "editor_after_last_verification":int(f["editor_after_last_verification"]) if f["editor_after_last_verification"] else None
        })
    return {
        "selection_protocol":"docs/STEP12_CASE_SELECTION_PROTOCOL_v1.md",
        "source_labels":"results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv",
        "source_features":"results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv",
        "source_v2":"results/2026-11-12/sweabs_full_198_cumulative_v2.csv",
        "trace_dataset":DATASET, "trace_revision":REVISION,
        "roster_is_descriptive_not_representative":True,
        "independent_human_semantic_oracle":False,
        "cases":cases
    }

def source_recount(roster):
    # Separate source/raw recount from the Step 9 feature extractor, matching
    # the independent Step 11 recount implementation (14 exact fields).
    sys.path.insert(0,str(ROOT/"scripts"))
    from step11_trace_spotcheck import recount
    from datasets import load_dataset
    wanted={(c["sample"],c["instance_id"],c["patch_sha256"]):c for c in roster["cases"]}
    features=indexed(rows(FEATURES),"feature")
    seen=set()
    for source in load_dataset(DATASET,split="train",revision=REVISION):
        if source.get("resolved") is not True:
            continue
        raw_patch=source.get("patch")
        if not isinstance(raw_patch,str):
            raise ValueError("Missing exact patch source")
        key=(int(source["sample"]),source["instance_id"],
             hashlib.sha256(raw_patch.encode("utf8")).hexdigest())
        if key not in wanted:
            continue
        if key in seen:
            raise ValueError("Duplicate source trace for "+str(key))
        seen.add(key)
        observed=recount(source["messages"])
        expected=features[key]
        diffs={f:(str(observed[f]),expected[f]) for f in AUDIT_FIELDS
               if str(observed[f]) != expected[f]}
        if diffs:
            raise ValueError("Independent raw recount failed for "+str(key)+" "+json.dumps(diffs))
    if seen != set(wanted):
        raise ValueError("Missing selected source traces: "+str(set(wanted)-seen))
    return {"pinned_source_recounted":len(seen),
            "feature_comparisons":len(seen)*len(AUDIT_FIELDS),
            "mismatches":0,"source_revision":REVISION,
            "raw_trace_text_released":False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    ap.add_argument("--recount-source",action="store_true")
    args=ap.parse_args()
    roster=build_roster()
    if args.check:
        archived=json.loads(OUTPUT.read_text(encoding="utf8"))
        if archived != roster:
            raise ValueError("Frozen Step 12 case roster mismatch")
    else:
        OUTPUT.parent.mkdir(parents=True,exist_ok=True)
        OUTPUT.write_text(json.dumps(roster,indent=2,sort_keys=True)+"\n",encoding="utf8")
    audit=source_recount(roster) if args.recount_source else {"frozen_roster_cases":len(roster["cases"]),"distinct_tasks":len({c["instance_id"] for c in roster["cases"]})}
    print(json.dumps(audit,sort_keys=True))

if __name__=="__main__":
    main()
