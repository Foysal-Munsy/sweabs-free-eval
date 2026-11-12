#!/usr/bin/env python3
"""Step 11 pinned-source structural crosswalk: 31 FAIL-review + 14 UNVERIFIED run IDs.

No semantic oracle, tests, patch application, or raw runner relabeling. Inspects
original patch diff, augmented test patch diff and issue-statement provenance.
Run from a clean checkout:
    python scripts/step11_semantic_structural_audit.py
    python scripts/step11_semantic_structural_audit.py --check
Packages: datasets==4.8.5 huggingface_hub==1.33.0
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
REV_AGENT="b5515d1dce40036633293b70477f0633b24593f7"
REV_TEST="79fc07a8f4ce5e3720e069948073f5f910b7577b"
OUT=D/"STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json"
AGENT_ID="tarsur385/swe-verified-gemini3-flash-trajectories"
ABS_ID="OpenAgentLab/SWE-Bench_Verified_ABS"

def read_csv(name):
    with (D/name).open(encoding="utf8",newline="") as f:return list(csv.DictReader(f))
def sha(s):return hashlib.sha256(s.encode("utf8")).hexdigest()
def identity(row):return int(row["sample"]),row["instance_id"],row["patch_sha256"]

def file_paths(diff):
    # conservative full-path parse from literal git diff headers
    paths=[]
    for line in diff.splitlines():
        if not line.startswith("diff --git a/"):continue
        match=re.match(r"diff --git a/(.*?) b/(.*?)$",line)
        if match:paths.append({"old":match.group(1),"new":match.group(2)})
    return paths

def test_source(rows,ids):
    from datasets import load_dataset
    found={}
    for row in load_dataset(ABS_ID,split="test",revision=REV_TEST):
        tid=row["instance_id"]
        if tid in ids:
            if tid in found:raise ValueError("duplicate SWE-ABS test task "+tid)
            found[tid]=dict(row)
    if set(found)!=ids:raise ValueError("ABS test tasks missing: "+str(ids-set(found)))
    return found

def agent_source(identities):
    from datasets import load_dataset
    found={}
    for row in load_dataset(AGENT_ID,split="train",revision=REV_AGENT):
        if row.get("resolved") is not True:continue
        key=(int(row["sample"]),row["instance_id"],sha(row["patch"]))
        if key in identities:
            if key in found:raise ValueError("duplicate exact agent row: "+str(key))
            found[key]=dict(row)
        elif (key[0],key[1]) in {(k[0],k[1]) for k in identities}:
            raise ValueError("source agent patch mismatch on selected sample/task "+str(key[:2]))
    if len(found)!=len(identities):
        raise ValueError("missing exact agent rows "+str(identities-set(found)))
    return found

def produce():
    fails=read_csv("STEP6_FAIL_REVIEW_31.csv")
    unknown=read_csv("STEP7_UNVERIFIED_TRIAGE_14.csv")
    if len(fails)!=31 or len(unknown)!=14:raise ValueError("Wrong audit-ledger size")
    combined=fails+unknown
    keys=[identity(x) for x in combined]
    if len(set(keys))!=45:raise ValueError("Duplicate exact audit identities")
    ids={x["instance_id"] for x in combined}
    agents=agent_source(set(keys))
    tests=test_source(combined,ids)
    cases=[]
    for kind,records in (("FAIL",fails),("UNVERIFIED",unknown)):
        for entry in records:
            key=identity(entry)
            agent=agents[key]
            absrow=tests[entry["instance_id"]]
            test_patch=absrow.get("test_patch")
            issue=absrow.get("problem_statement")
            if not isinstance(test_patch,str) or not test_patch.strip():
                raise ValueError("Empty augmented test patch "+entry["instance_id"])
            if not isinstance(issue,str) or not issue.strip():
                raise ValueError("Empty original issue statement "+entry["instance_id"])
            agent_files=file_paths(agent["patch"])
            changed={x["new"] for x in agent_files}
            test_files=file_paths(test_patch)
            augmented={x["new"] for x in test_files}
            overlap=sorted(changed & augmented)
            test_hash=sha(test_patch)
            review_hash=entry.get("test_patch_sha256","")
            if kind=="FAIL" and review_hash!=test_hash:
                raise ValueError("Review and pinned ABS test SHA mismatch "+str(key))
            case={
                "case_type":kind,
                "sample":key[0],"offset":int(entry["offset"]),
                "instance_id":key[1],"model_patch_sha256":key[2],
                "raw_outcome_v2":kind,
                "original_issue_sha256":sha(issue),
                "original_issue_bytes":len(issue.encode("utf8")),
                "augmented_test_patch_sha256":test_hash,
                "augmented_test_file_paths":sorted(augmented),
                "augmented_test_diff_file_count":len(test_files),
                "submitted_patch_diff_file_count":len(agent_files),
                "submitted_patch_changed_repo_paths":sorted(
                    changed-{x for x in changed if x.startswith(("workspace/bash_events/","workspace/conversations/"))}),
                "submitted_patch_runtime_trace_file_count":sum(x.startswith(("workspace/bash_events/","workspace/conversations/")) for x in changed),
                "direct_changed_file_overlap":overlap,
                "generated_build_lib_files":sorted(x for x in changed if x.startswith(("build/lib/","build/"))),
                "test_patch_skip_marker_counts":{word:len(re.findall(re.escape(word),test_patch))
                    for word in ("skipUnlessDBFeature","skipIfDBFeature","skipUnless","skipIf","skipTest(","@unittest.skip")},
                "source_agent_revision":REV_AGENT,
                "source_abs_revision":REV_TEST,
                "verification_class":"structural_crosswalk_not_semantic_oracle",
            }
            if kind=="FAIL":
                case["prior_review_status"]=entry["semantic_review_status"]
                case["pr_url"]=entry["pr_url"]
            else:
                case["prior_triage_category"]=entry["triage_category"]
                case["prior_runner_passed"]=entry["runner_passed"]
                case["prior_runner_failed"]=entry["runner_failed"]
                case["prior_runner_skipped"]=entry["runner_skipped"]
            cases.append(case)
    cases.sort(key=lambda c:(c["sample"],c["offset"],c["instance_id"]))
    sub=[c for c in cases if c["case_type"]=="UNVERIFIED"]
    categories=Counter(c["prior_triage_category"] for c in sub)
    overlap_by_cat={k:Counter(bool(c["direct_changed_file_overlap"]) for c in sub if c["prior_triage_category"]==k)
        for k in sorted(categories)}
    return {
        "status":"source-pinned structural crosswalk only; no independent semantic adjudication or reruns",
        "source_agent_dataset":AGENT_ID,"source_agent_revision":REV_AGENT,
        "source_sweabs_dataset":ABS_ID,"source_sweabs_revision":REV_TEST,
        "inputs":["results/2026-11-12/STEP6_FAIL_REVIEW_31.csv","results/2026-11-12/STEP7_UNVERIFIED_TRIAGE_14.csv"],
        "selected_exact_runs":len(keys),"unique_tasks":len(ids),
        "reviewed_fail_runs":len(fails),"reviewed_unverified_runs":len(unknown),
        "unverified_categories":dict(sorted(categories.items())),
        "unverified_direct_file_overlap_by_category":{k:{"true":int(v[True]),"false":int(v[False])} for k,v in overlap_by_cat.items()},
        "limitations":"Matching source SHA and changed paths does not prove runtime patch integrity, actually executed/skipped test identities, semantic validity, or ground truth.",
        "rows":cases
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true")
    args=p.parse_args()
    result=produce()
    if args.check:
        if json.loads(OUT.read_text(encoding="utf8"))!=result:raise ValueError("Pinned crosswalk JSON mismatch")
    else:
        OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({k:v for k,v in result.items() if k in ("selected_exact_runs","unique_tasks","reviewed_fail_runs","reviewed_unverified_runs","unverified_categories","unverified_direct_file_overlap_by_category")},indent=2))
if __name__=="__main__":main()
