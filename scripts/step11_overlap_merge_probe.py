#!/usr/bin/env python3
"""Step 11: attempt original full agent + augmented test patch non-destructive merge.

Pins exact run by sample/instance/patch-SHA and original SWE-ABS test patch
revision. Reconstructs on fresh base; first applies entire model diff, then
checks whether exact augmented test diff applies without overwriting model
additions. If direct merge fails, tries git apply --3way; report conflicts
honestly rather than treating a failed merge as a model failure.
NO new semantic PASS/FAIL label and NO original Docker result alteration.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,subprocess,tempfile
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
AGENT="tarsur385/swe-verified-gemini3-flash-trajectories"
AGENT_REV="b5515d1dce40036633293b70477f0633b24593f7"
ABS="OpenAgentLab/SWE-Bench_Verified_ABS"
ABS_REV="79fc07a8f4ce5e3720e069948073f5f910b7577b"
ALLOWED={"sympy__sympy-23413":(1,2,3),"django__django-11206":(3,)}
OUTPUT=D/"STEP11_COLLISION_MERGE_PROBES_v1.json"
def sha(b):return hashlib.sha256(b).hexdigest()
def run(cmd,cwd=None,timeout=180):
    return subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=timeout)
def must(cmd,cwd=None,timeout=180):
    x=run(cmd,cwd,timeout)
    if x.returncode:raise ValueError("Command "+cmd[0]+" failed: "+x.stderr[-400:])
    return x.stdout
def changed_paths(diff):
    a=[]
    for x in diff.splitlines():
        if x.startswith("diff --git "):
            m=re.fullmatch(r"diff --git a/(.*?) b/(.*?)",x)
            if not m or m.group(1)!=m.group(2):raise ValueError("Unexpected rename")
            a.append(m.group(2))
    if len(a)!=len(set(a)):raise ValueError("Duplicate diff path")
    return a
def added_line_counts(diff,overlap):
    current=None
    counts=Counter()
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            current=changed_paths(line)[0]
        elif current in overlap and line.startswith("+") and not line.startswith("+++"):
            counts[(current,line[1:])]+=1
    return counts
def actual_line_counts(root,overlap):
    found={}
    for p in overlap:
        if (root/p).is_file():
            found[p]=Counter((root/p).read_text(encoding="utf8",errors="replace").splitlines())
        else:found[p]=Counter()
    return found
def load_data():
    from datasets import load_dataset
    sources=[dict(x) for x in load_dataset(AGENT,revision=AGENT_REV,split="train")
       if x.get("resolved") is True and x.get("instance_id") in ALLOWED
       and int(x.get("sample",-1)) in ALLOWED[x["instance_id"]]]
    tests={x["instance_id"]:dict(x) for x in load_dataset(ABS,revision=ABS_REV,split="test")
           if x["instance_id"] in ALLOWED}
    return sources,tests
def case(agent,test,record,cross):
    task=agent["instance_id"];sam=int(agent["sample"]);model=agent["patch"];aug=test["test_patch"]
    if sha(model.encode())!=record["patch_sha256"]:raise ValueError("wrong pinned model SHA")
    if sha(aug.encode())!=cross["augmented_test_patch_sha256"]:raise ValueError("wrong pinned test SHA")
    modelpaths=changed_paths(model);testpaths=changed_paths(aug);overlap=sorted(set(modelpaths)&set(testpaths))
    if not overlap:raise ValueError("Expected at least one overlapping changed path")
    remotes={"sympy__sympy-23413":"https://github.com/sympy/sympy.git",
             "django__django-11206":"https://github.com/django/django.git"}
    with tempfile.TemporaryDirectory(prefix="step11-merge-") as tmp:
        root=Path(tmp)/"repo";root.mkdir()
        must(["git","init","--quiet"],root)
        must(["git","remote","add","origin",remotes[task]],root)
        must(["git","fetch","--quiet","--depth","1","origin",test["base_commit"]],root,300)
        must(["git","checkout","--quiet","--detach","FETCH_HEAD"],root)
        if must(["git","rev-parse","HEAD"],root).strip()!=test["base_commit"]:
            raise ValueError("Wrong base commit")
        a=Path(tmp)/"original-model.patch";a.write_bytes(model.encode())
        b=Path(tmp)/"augmented.patch";b.write_bytes(aug.encode())
        applied=run(["git","apply","--check","--index","--binary",str(a)],root)
        if applied.returncode:
            return {"task":task,"sample":sam,"source_patch_sha256":record["patch_sha256"],
              "test_sha256":sha(aug.encode()),"base_commit":test["base_commit"],
              "overlap_files":overlap,"original_model_patch_applied":False,
              "status":"MODEL_PATCH_APPLY_FAILED_ON_PRISTINE_BASE",
              "bounded_diagnostic":applied.stderr[-380:],"runner_relabel":False}
        must(["git","apply","--index","--binary",str(a)],root)
        changed=must(["git","diff","--cached","--name-only","HEAD"],root).splitlines()
        if set(changed)!=set(modelpaths):raise ValueError("Model patch changed file manifest mismatch")
        before=actual_line_counts(root,overlap)
        want=added_line_counts(model,set(overlap))
        for (path,text),count in want.items():
            if before[path][text]<count:
                raise ValueError("Model add line missing before augmented patch: "+path)
        direct=run(["git","apply","--check","--binary",str(b)],root)
        method="direct"
        if direct.returncode==0:
            must(["git","apply","--binary",str(b)],root)
            outcome="PATCHES_APPLIED_NONDESTRUCTIVELY"
        else:
            method="git_3way"
            three=run(["git","apply","--3way","--binary",str(b)],root)
            conflicts=must(["git","ls-files","-u"],root).strip().splitlines()
            outcome="THREE_WAY_MERGE_OK" if three.returncode==0 and not conflicts else "TEST_PATCH_CONFLICT_UNRESOLVED"
        after=actual_line_counts(root,overlap)
        preserved=sum(after[path][text]>=n for (path,text),n in want.items())
        eliminated=[path for (path,text),n in want.items() if after[path][text]<n]
        return {"task":task,"sample":sam,"source_patch_sha256":record["patch_sha256"],
            "test_sha256":sha(aug.encode()),"base_commit":test["base_commit"],
            "model_changed_files":len(modelpaths),"test_changed_files":len(testpaths),
            "overlap_files":overlap,"original_model_patch_applied":True,
            "model_files_staged_match_submitted_patch":True,
            "augmented_application_attempt":method,
            "status":outcome,
            "direct_test_patch_check_returncode":direct.returncode,
            "model_added_overlap_line_types":len(want),
            "model_added_overlap_line_types_still_present_after_merge":preserved,
            "added_line_types_missing_after_merge":len(eliminated),
            "missing_model_code_paths":sorted(set(eliminated)),
            "model_code_proven_semantically_preserved":False,
            "enhanced_tests_executed":False,
            "historical_docker_runner_reproduced":False,
            "runner_relabel":False,
            "limitations":"One textual merge or line-presence count does not guarantee semantic equality of the original agent edit. A conflicting merge requires a separately reviewed non-destructive integration and executed strengthened tests."}
def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");args=p.parse_args()
    with (D/"STEP7_UNVERIFIED_TRIAGE_14.csv").open(encoding="utf8",newline="") as f:
        selected={(r["instance_id"],int(r["sample"])):r for r in csv.DictReader(f)
          if r["instance_id"] in ALLOWED and int(r["sample"]) in ALLOWED[r["instance_id"]]}
    evidence=json.loads((D/"STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json").read_text(encoding="utf8"))
    cross={(r["instance_id"],r["sample"]):r for r in evidence["rows"] if r["case_type"]=="UNVERIFIED"}
    agents,tests=load_data()
    if len(selected)!=4 or len(agents)!=4 or len(tests)!=2:raise ValueError("Expected exact four sample runs and two augmented tasks")
    out=[]
    for agent in sorted(agents,key=lambda a:(a["instance_id"],int(a["sample"]))):
        key=(agent["instance_id"],int(agent["sample"]))
        out.append(case(agent,tests[key[0]],selected[key],cross[key]))
    output={"status":"new source-pinned non-destructive merge attempts, not semantic test runs",
        "original_outcomes_modified":False,"source_model_revision":AGENT_REV,
        "source_test_revision":ABS_REV,
        "cases":len(out),
        "cases_with_complete_model_patch_on_base":sum(x["original_model_patch_applied"] for x in out),
        "cases_with_direct_test_patch_application":sum(x["status"]=="PATCHES_APPLIED_NONDESTRUCTIVELY" for x in out),
        "cases_with_3way_merge_application":sum(x["status"]=="THREE_WAY_MERGE_OK" for x in out),
        "cases_with_unresolved_conflict":sum(x["status"]=="TEST_PATCH_CONFLICT_UNRESOLVED" for x in out),
        "rows":out}
    if args.check:
        if json.loads(OUTPUT.read_text(encoding="utf8"))!=output:raise ValueError("Mismatch in repeat probe")
    else:OUTPUT.write_text(json.dumps(output,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:output[k] for k in ("cases","cases_with_complete_model_patch_on_base",
         "cases_with_direct_test_patch_application","cases_with_3way_merge_application",
         "cases_with_unresolved_conflict")},indent=2))
    print("STEP11_COLLISION_RESULT_BEGIN")
    print(json.dumps(output,sort_keys=True))
    print("STEP11_COLLISION_RESULT_END")
if __name__=="__main__":main()
