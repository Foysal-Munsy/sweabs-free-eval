#!/usr/bin/env python3
"""Step 11 controlled merged model+augmented test run for 4 overlap records.

New, separate direct checkout, not the original SWE-ABS Docker image. No
label changes; preserves frozen dataset revisions and exact sample+patch SHA.
Usage: python scripts/step11_overlap_execution.py prepare --task <...> --sample <1-3>
       python scripts/step11_overlap_execution.py execute --task <...> --sample <1-3>
"""
from __future__ import annotations
import argparse,csv,hashlib,json,os,re,subprocess,sys,time
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
AGENT="tarsur385/swe-verified-gemini3-flash-trajectories"
AGENT_REV="b5515d1dce40036633293b70477f0633b24593f7"
ABS="OpenAgentLab/SWE-Bench_Verified_ABS"
ABS_REV="79fc07a8f4ce5e3720e069948073f5f910b7577b"
TARGETS={
 "django__django-11206":{
     "samples":(3,),"repo":"https://github.com/django/django.git",
     "test_modules":["utils_tests.test_numberformat","utils_tests.test_numberformat_small_decimals"],
     "test_type":"django"},
 "sympy__sympy-23413":{
     "samples":(1,2,3),"repo":"https://github.com/sympy/sympy.git",
     "test_modules":["sympy/polys/matrices/tests/test_normalforms.py","sympy/polys/matrices/tests/test_normalforms_hnf_extra.py"],
     "test_type":"pytest"}}
def sha(data):return hashlib.sha256(data).hexdigest()
def work(task,sample):return ROOT/"scratch"/("step11-merge-"+task.split("-")[-1]+"-s"+str(sample))
def sub(cmd,cwd=None,timeout=180,env=None):
    return subprocess.run(cmd,cwd=cwd,env=env,text=True,errors="replace",
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
def must(cmd,cwd=None,timeout=180):
    p=sub(cmd,cwd,timeout)
    if p.returncode!=0:raise RuntimeError("Command "+cmd[0]+" failed "+p.stdout[-480:])
    return p.stdout
def paths(text):
    a=[]
    for line in text.splitlines():
        if line.startswith("diff --git "):
            m=re.fullmatch(r"diff --git a/(.*?) b/(.*?)",line)
            if not m or m.group(1)!=m.group(2):raise ValueError("Unrecognized diff")
            a.append(m.group(2))
    if len(a)!=len(set(a)):raise ValueError("Duplicate diff path")
    return a
def find_rows(task,sample):
    from datasets import load_dataset
    sources=[dict(x) for x in load_dataset(AGENT,split="train",revision=AGENT_REV)
          if x.get("resolved") is True and x["instance_id"]==task and int(x["sample"])==sample]
    tests=[dict(x) for x in load_dataset(ABS,split="test",revision=ABS_REV) if x["instance_id"]==task]
    if len(sources)!=1 or len(tests)!=1:raise ValueError("Wrong pinned dataset identity")
    with (D/"STEP7_UNVERIFIED_TRIAGE_14.csv").open(newline="",encoding="utf8") as f:
        triage=[x for x in csv.DictReader(f) if x["instance_id"]==task and int(x["sample"])==sample]
    if len(triage)!=1:raise ValueError("Triage identity missing")
    return sources[0],tests[0],triage[0]
def added_lines(diff,overlap):
    counts=Counter()
    name=None
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            name=paths(line)[0]
        elif name in overlap and line.startswith("+") and not line.startswith("+++"):
            counts[(name,line[1:])]+=1
    return counts
def preserved(root,counter):
    actual={p:Counter((root/p).read_text(encoding="utf8",errors="replace").splitlines())
            for p in {p for p,line in counter}}
    return sum(actual[p][text]>=n for (p,text),n in counter.items())
def prepare(task,sample):
    if task not in TARGETS or sample not in TARGETS[task]["samples"]:
        raise ValueError("Not an approved original overlap task")
    agent,test,triage=find_rows(task,sample)
    model,testpatch=agent["patch"],test["test_patch"]
    if sha(model.encode())!=triage["patch_sha256"]:raise ValueError("Source model hash mismatch")
    cross=json.loads((D/"STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json").read_text())
    records=[x for x in cross["rows"] if x["case_type"]=="UNVERIFIED" and x["instance_id"]==task and x["sample"]==sample]
    if len(records)!=1 or sha(testpatch.encode())!=records[0]["augmented_test_patch_sha256"]:
        raise ValueError("Wrong enhanced test source SHA")
    dest=work(task,sample)
    if dest.exists():raise ValueError("Workdir already exists")
    root=dest/"repo";root.mkdir(parents=True)
    must(["git","init","--quiet"],root)
    must(["git","remote","add","origin",TARGETS[task]["repo"]],root)
    must(["git","fetch","--quiet","--depth","1","origin",test["base_commit"]],root,300)
    must(["git","checkout","--quiet","--detach","FETCH_HEAD"],root)
    if must(["git","rev-parse","HEAD"],root).strip()!=test["base_commit"]:
        raise ValueError("Wrong base commit")
    model_file=dest/"model.patch";model_file.write_bytes(model.encode())
    aug_file=dest/"tests.patch";aug_file.write_bytes(testpatch.encode())
    must(["git","apply","--check","--index","--binary",str(model_file)],root)
    must(["git","apply","--index","--binary",str(model_file)],root)
    expected=set(paths(model))
    if set(must(["git","diff","--cached","--name-only","HEAD"],root).splitlines())!=expected:
        raise ValueError("Exact model patch changed files missing")
    overlap=sorted(expected&set(paths(testpatch)))
    if not overlap:raise ValueError("Expected one or more same-file collisions")
    want=added_lines(model,overlap)
    if preserved(root,want)!=len(want):raise ValueError("Model original inserted lines not found")
    merged=sub(["git","apply","--check","--binary",str(aug_file)],root)
    mode="direct" if merged.returncode==0 else "three_way"
    if merged.returncode==0:must(["git","apply","--binary",str(aug_file)],root)
    else:must(["git","apply","--3way","--binary",str(aug_file)],root)
    if must(["git","ls-files","-u"],root).strip():raise ValueError("Unmerged paths after 3way")
    preserved_count=preserved(root,want)
    if preserved_count!=len(want):
        raise ValueError("Original model added lines lost during augmented merge")
    info={"task":task,"sample":sample,"base_commit":test["base_commit"],
        "source_revision":AGENT_REV,"test_revision":ABS_REV,
        "patch_sha256":triage["patch_sha256"],
        "test_patch_sha256":sha(testpatch.encode()),
        "model_changed_file_count":len(expected),
        "overlap_paths":overlap,
        "model_added_line_types_in_collision_paths":len(want),
        "model_added_line_types_preserved_after_merge":preserved_count,
        "augmented_patch_merge_mode":mode,
        "test_type":TARGETS[task]["test_type"],"test_modules":TARGETS[task]["test_modules"],
        "original_runner_outcome":"UNVERIFIED",
        "new_patch_test_integration_verified":True,
        "original_outcomes_modified":False,
        "limitation":"Only original inserted source line presence is proved, not full semantic equivalence of every model change. Original SWE-ABS Docker runtime not reconstructed."}
    (dest/"manifest.json").write_text(json.dumps(info,sort_keys=True,indent=2)+"\n")
    print(json.dumps(info,sort_keys=True))
def execute(task,sample):
    dest=work(task,sample)
    data=json.loads((dest/"manifest.json").read_text())
    root=dest/"repo"
    env=os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"]="1"
    env["PYTHONPATH"]=str(root)+os.pathsep+str(root/"tests")
    if data["test_type"]=="django":
        cmd=[sys.executable,"tests/runtests.py",*data["test_modules"],
            "--settings=test_sqlite","--noinput","--verbosity=2"]
    else:
        cmd=[sys.executable,"-m","pytest","-q",*data["test_modules"]]
    start=time.monotonic()
    try:
        x=sub(cmd,cwd=root,timeout=720,env=env)
        exit_code=x.returncode
        stdout=x.stdout
        timeout=False
    except subprocess.TimeoutExpired as exc:
        exit_code=124
        stdout=str(exc.stdout or "")[-2000:]
        timeout=True
    seconds=round(time.monotonic()-start,2)
    summary=[s.strip()[:260] for s in stdout.splitlines()
       if re.search(r"(?i)(?:=+ .*? (?:passed|failed|error|skipped)|^Ran \d+ tests?|^OK$|^FAILED \(|^ERROR:|^FAIL:|^test_.*?\.\.\. (?:ok|skipped|FAIL|ERROR))",s)]
    observed=bool(summary)
    status=("NEW_MERGED_TARGET_SUITE_PASSED" if exit_code==0 and observed
            else "NEW_MERGED_TARGET_SUITE_FAILED_OR_ERRORS" if exit_code!=0 and observed
            else "INCOMPLETE_OR_INCONCLUSIVE_EXECUTION")
    data.update({
       "new_test_runtime":"direct upstream Python test runner, NOT SWE-ABS Docker",
       "runtime_python":sys.version.split()[0],
       "tested_modules":data["test_modules"],
       "execution_exit_code":exit_code,
       "execution_timeout":timeout,
       "wall_seconds":seconds,
       "bounded_result_lines":summary[-32:],
       "bounded_error_tail":stdout[-1100:] if status=="INCOMPLETE_OR_INCONCLUSIVE_EXECUTION" else "",
       "new_merged_execution_status":status,
       "original_v2_relabelled":False,
       "not_historical_sweabs_verdict":True,
       "limitation":"New merged original model/test source on a fresh pinned base, but distinct dependency/runtime versions from original Docker image. Passing/failing tests require issue-scoped semantic review; runner v2 is immutable."})
    print("STEP11_MERGED_EXECUTION_BEGIN")
    print(json.dumps(data,sort_keys=True))
    print("STEP11_MERGED_EXECUTION_END")
def main():
    a=argparse.ArgumentParser()
    a.add_argument("phase",choices=["prepare","execute"])
    a.add_argument("--task",choices=sorted(TARGETS),required=True)
    a.add_argument("--sample",type=int,choices=(1,2,3),required=True)
    opt=a.parse_args()
    if opt.phase=="prepare":prepare(opt.task,opt.sample)
    else:execute(opt.task,opt.sample)
if __name__=="__main__":main()
