#!/usr/bin/env python3
"""Step 11: identify unobserved Django-15503 newly added test method in original logs.

Read-only pinned SWE-ABS source and previously independently verified original ZIP evidence; only derived
metadata is saved publicly. Never infer PASS from absence or retune labels.

Usage: python scripts/step11_missing_oracle_method_audit.py [--check]
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,subprocess,tempfile
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
OUTPUT=D/"STEP11_MISSING_DJANGO15503_ORACLE_METHOD_v1.json"
TASK="django__django-15503"
MISSING="test_oracle_json_path_final_key_is_quoted_for_numeric_strings"
ABS="OpenAgentLab/SWE-Bench_Verified_ABS"
REV="79fc07a8f4ce5e3720e069948073f5f910b7577b"
GHREPO="Foysal-Munsy/sweabs-free-eval"
METHOD=re.compile(r"^\+\s*(?:async\s+)?def (test_[A-Za-z0-9_]+)\(")
CLASS=re.compile(r"^[ +]class\s+([A-Za-z0-9_]+)\s*\(")
VERBOSE=re.compile(r"^\s*(test_[A-Za-z0-9_]+)\s*\(([^)]+)\)\s*\.\.\.\s*(ok|skipped|FAIL|ERROR)\b",re.I)
def load_dataset_row():
    from datasets import load_dataset
    matches=[dict(x) for x in load_dataset(ABS,split="test",revision=REV) if x["instance_id"]==TASK]
    if len(matches)!=1:raise ValueError("Pinned SWE-ABS identity missing or duplicated")
    return matches[0]
def sha(b):return hashlib.sha256(b).hexdigest()
def source_location(diff):
    file_path=""
    last_class=None
    new_methods=[]
    oracle=[]
    plus_lines=diff.splitlines()
    for i,line in enumerate(plus_lines):
        if line.startswith("diff --git "):
            file_path=line.split(" b/",1)[-1]
            last_class=None
        cls=CLASS.match(line)
        if cls:last_class=cls.group(1)
        m=METHOD.match(line)
        if m:
            item={"name":m.group(1),"class_from_patch_context":last_class,
                  "file":file_path,
                  "added_def_indentation":len(line[1:])-len(line[1:].lstrip())}
            new_methods.append(item)
            if m.group(1)==MISSING:
                snippet=plus_lines[max(i-14,0):i]
                decorators=[x.strip()[1:] for x in snippet if x.lstrip().startswith("+@") or x.lstrip().startswith("+    @")]
                oracle.append({**item,"nearby_decorator_names":[x[:160] for x in decorators[-8:]],
                    "preceding_context_class":last_class})
    return new_methods,oracle

def source_logs(entries,temp):
    result=[]
    for row in entries:
        sam=int(row["sample"]);off=int(row["offset"]);run=int(row["run_id"].split("_")[1])
        dst=Path(temp)/f"s{sam}-o{off}"
        dst.mkdir()
        name=f"sweabs-result-{sam}-{off}"
        p=subprocess.run(["gh","run","download",str(run),"-R",GHREPO,"-n",name,"-D",str(dst)],
            capture_output=True,text=True,timeout=120)
        if p.returncode:raise RuntimeError(f"Cannot fetch original {name}: {p.stderr[:160]}")
        logs=list(dst.rglob("test_output.txt"))
        if len(logs)!=1:raise ValueError("Expected exactly one original test_output.txt")
        raw=logs[0].read_bytes()
        cases=[]
        for line in raw.decode("utf8",errors="replace").splitlines():
            m=VERBOSE.match(line)
            if m:cases.append((m.group(1),m.group(2),m.group(3).lower()))
        hit=[{"class_path":cls,"status":status} for method,cls,status in cases if method==MISSING]
        result.append({"sample":sam,"offset":off,"original_runner_artifact":row["run_id"],
             "test_output_sha256":sha(raw),"verbose_methods_observed":len(cases),
             "target_method_observed":bool(hit),"target_method_statuses":hit,
             "observed_test_class_paths":sorted({cls for meth,cls,status in cases}),
             "reported_passed":int(row["runner_passed"]),
             "reported_failed":int(row["runner_failed"]),
             "reported_skipped":int(row["runner_skipped"])})
    return result
def archived_logs(entries):
    # Logs were already independently downloaded and checked in the successful
    # CI #43263048387 (raw ZIP hashes) and #43264326911 (method-to-verbose logs).
    # Re-use immutable published metadata rather than causing repeated
    # short-retention egress; explicitly record this evidence boundary.
    zip_evidence=json.loads((D/"STEP11_RAW_ARTIFACT_REAUDIT14_v1.json").read_text(encoding="utf8"))
    methods=json.loads((D/"STEP11_SKIP_ATTRIBUTION_9_v1.json").read_text(encoding="utf8"))
    zmap={(int(x["sample"]),int(x["offset"])):x for x in zip_evidence["rows"]}
    mmap={(int(x["sample"]),int(x["offset"])):x for x in methods["rows"]}
    result=[]
    for row in entries:
        sam=int(row["sample"]);off=int(row["offset"]);key=(sam,off)
        z=zmap.get(key);m=mmap.get(key)
        if z is None or m is None:raise ValueError("Missing archived original log evidence")
        if z["patch_sha256"]!=row["patch_sha256"] or m["model_patch_sha256"]!=row["patch_sha256"]:
            raise ValueError("Archived patch identity mismatch")
        if len(z["raw_test_outputs"])!=1:
            raise ValueError("Expected one archived test-output digest per case")
        method=[x for x in m["augmented_added_test_function_names"] if x["name"]==MISSING]
        if len(method)!=1:raise ValueError("Oracle method not found in archived method audit")
        observed=method[0]["observed_result_types"]
        if observed or method[0]["observed_verbose_matches"]:
            raise ValueError("Archived method was observed; contradicts evidence")
        tallies=m["observed_verbose_test_status_tallies"]
        result.append({"sample":sam,"offset":off,
             "original_runner_artifact":row["run_id"],
             "test_output_sha256":z["raw_test_outputs"][0]["sha256"],
             "verbose_methods_observed":sum(tallies.values()),
             "target_method_observed":False,"target_method_statuses":[],
             "observed_test_class_paths":[],
             "reported_passed":int(row["runner_passed"]),
             "reported_failed":int(row["runner_failed"]),
             "reported_skipped":int(row["runner_skipped"]),
             "verification_mode":"reused SHA-identified archived original test logs from prior passing CI, not newly downloaded"})
    return result

def produce(fresh_zips=False):
    source=load_dataset_row()
    patch=source["test_patch"]
    digest=sha(patch.encode("utf8"))
    cross=json.loads((D/"STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json").read_text(encoding="utf8"))
    crosscases=[r for r in cross["rows"] if r["case_type"]=="UNVERIFIED" and r["instance_id"]==TASK]
    if len(crosscases)!=3 or any(r["augmented_test_patch_sha256"]!=digest for r in crosscases):
        raise ValueError("Original source/test patch identity disagreement")
    with (D/"STEP7_UNVERIFIED_TRIAGE_14.csv").open(encoding="utf8",newline="") as f:
        rows=sorted((r for r in csv.DictReader(f) if r["instance_id"]==TASK),
                    key=lambda x:int(x["sample"]))
    if len(rows)!=3:raise ValueError("Expected all three original samples")
    methods,oracle=source_location(patch)
    if len(oracle)!=1:raise ValueError("Expected one newly-added Oracle method definition; got "+str(len(oracle)))
    if len(methods)<10:raise ValueError("Missing source added test methods")
    if fresh_zips:
        with tempfile.TemporaryDirectory(prefix="step11-oracle-") as tmp:
            logs=source_logs(rows,tmp)
    else:
        logs=archived_logs(rows)
    if any(l["target_method_observed"] for l in logs):
        raise ValueError("Oracle target is observed; contradicts original Step 11 attribution")
    return {"status":"Pinned test definition and independently archived unittest verbose-collection evidence; no execution of unobserved test",
        "log_evidence_mode":"fresh-original-zip" if fresh_zips else "reused-confirmed-zip-and-method-audits",
        "task":TASK,"test_revision":REV,"test_patch_sha256":digest,
        "new_method_definitions_count":len(methods),
        "target_test_method_name":MISSING,
        "target_source_structure":oracle[0],
        "raw_log_checks":logs,
        "all_three_unobserved":True,
        "not_in_verbose_log_does_not_mean_failed_or_skipped":True,
        "notes":"Source class and method declaration verified, but no claim whether collection omitted test due vendor restrictions, runner selection, class inheritance or another cause without a separate controlled collection experiment.",
        "labels_modified":False}
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--fresh-zips",action="store_true",help="Optional fresh downloads; default uses verified archived raw-log metadata")
    args=parser.parse_args()
    out=produce(fresh_zips=args.fresh_zips)
    if args.check:
        if json.loads(OUTPUT.read_text(encoding="utf8"))!=out:raise ValueError("Oracle method audit mismatch")
    else:OUTPUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"target":out["target_source_structure"],
             "cases":[{"sample":r["sample"],"verbose_methods":r["verbose_methods_observed"],
                       "method_seen":r["target_method_observed"]} for r in out["raw_log_checks"]]},indent=2))
if __name__=="__main__":main()
