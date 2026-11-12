#!/usr/bin/env python3
"""Step 11: read-only exact-file Requests whole-model-patch reconstruction.

Uses frozen source revisions and verifies full submitted patch on pinned base,
every changed file at the index/worktree, and unchanged model files after
a non-overlapping augmented test patch. This is a NEW reconstruction, NOT
proof the historical Docker runner tested this exact complete tree.

Run: python scripts/step11_reconstruct_requests_patch.py [--check]
Requires git, datasets==4.8.5; network to GitHub and Hugging Face.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,subprocess,tempfile
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
OUT=D/"STEP11_REQUESTS_FULL_PATCH_RECONSTRUCTION_v1.json"
TASK="psf__requests-1142"
SAMPLE=1
AGENT="tarsur385/swe-verified-gemini3-flash-trajectories"
AGENT_REV="b5515d1dce40036633293b70477f0633b24593f7"
ABS="OpenAgentLab/SWE-Bench_Verified_ABS"
ABS_REV="79fc07a8f4ce5e3720e069948073f5f910b7577b"
REMOTE="https://github.com/psf/requests.git"

def sha(x:bytes)->str:return hashlib.sha256(x).hexdigest()
def git(where,*args):
    p=subprocess.run(["git","-C",str(where),*args],capture_output=True,text=True,timeout=180)
    if p.returncode:raise RuntimeError("git "+args[0]+" returned "+str(p.returncode)+": "+p.stderr[:550])
    return p.stdout
def get_row(dataset,revision,split,filterfn):
    from datasets import load_dataset
    rows=[dict(r) for r in load_dataset(dataset,split=split,revision=revision) if filterfn(r)]
    if len(rows)!=1:raise ValueError("Expected one pinned "+dataset+" row, got "+str(len(rows)))
    return rows[0]
def diff_paths(text):
    out=[]
    for line in text.splitlines():
        if line.startswith("diff --git "):
            m=re.fullmatch(r"diff --git a/(.*?) b/(.*?)",line)
            if not m or m.group(1)!=m.group(2):
                raise ValueError("Unsupported rename/path syntax in source patch")
            out.append(m.group(2))
    if len(set(out))!=len(out):raise ValueError("Duplicate file diff headers")
    return out
def line_changes(text):
    result=Counter()
    path=None
    for line in text.splitlines():
        if line.startswith("diff --git "):
            m=re.fullmatch(r"diff --git a/(.*?) b/(.*?)",line)
            if not m or m.group(1)!=m.group(2):raise ValueError("Changed path failed")
            path=m.group(2)
        elif path is not None and line.startswith(("+","-")) and not line.startswith(("+++","---")):
            result[(path,line[0],line[1:])]+=1
    return result
def record():
    with (D/"STEP7_UNVERIFIED_TRIAGE_14.csv").open(newline="",encoding="utf8") as f:
        triage=[r for r in csv.DictReader(f) if r["instance_id"]==TASK and int(r["sample"])==SAMPLE]
    if len(triage)!=1:raise ValueError("Missing exact Requests source record")
    entry=triage[0]
    agent=get_row(AGENT,AGENT_REV,"train",lambda r:r.get("instance_id")==TASK and int(r.get("sample",-1))==SAMPLE and r.get("resolved") is True)
    absrow=get_row(ABS,ABS_REV,"test",lambda r:r.get("instance_id")==TASK)
    model=agent["patch"];test=absrow["test_patch"]
    if sha(model.encode())!=entry["patch_sha256"]:raise ValueError("Wrong submitted patch SHA")
    cross=json.loads((D/"STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json").read_text(encoding="utf8"))
    original=[c for c in cross["rows"] if c["case_type"]=="UNVERIFIED" and c["instance_id"]==TASK]
    if len(original)!=1 or original[0]["augmented_test_patch_sha256"]!=sha(test.encode()):
        raise ValueError("Pinned test patch SHA mismatch")
    modelpaths=diff_paths(model)
    testpaths=diff_paths(test)
    overlap=sorted(set(modelpaths)&set(testpaths))
    if overlap:raise ValueError("Unexpected Requests model/test overlap")
    with tempfile.TemporaryDirectory(prefix="step11-requests-") as root:
        d=Path(root)/"requests"
        d.mkdir()
        git(d,"init","--quiet")
        git(d,"remote","add","origin",REMOTE)
        git(d,"fetch","--quiet","--depth","1","origin",absrow["base_commit"])
        git(d,"checkout","--quiet","--detach","FETCH_HEAD")
        if git(d,"rev-parse","HEAD").strip()!=absrow["base_commit"]:
            raise ValueError("Wrong baseline")
        patchfile=Path(root)/"exact-model.diff"
        patchfile.write_bytes(model.encode())
        # --index means the complete model patch must apply without changing
        # unrelated tracked files; all additions are written to the index.
        git(d,"apply","--check","--index","--binary",str(patchfile))
        git(d,"apply","--index","--binary",str(patchfile))
        changed=git(d,"diff","--cached","--name-only","HEAD").splitlines()
        if set(changed)!=set(modelpaths):
            raise ValueError(f"Submitted patch paths changed: {len(changed)}/{len(modelpaths)}")
        actual=git(d,"diff","--cached","--binary","HEAD")
        want=line_changes(model)
        got=line_changes(actual)
        if want!=got:
            raise ValueError(f"Model added/removed line mismatch {sum(want.values())}/{sum(got.values())}")
        if git(d,"diff","--name-only").strip():
            raise ValueError("Git working tree differs from exact model staged index")
        pre={}
        for p in modelpaths:
            x=d/p
            if x.is_file():pre[p]=sha(x.read_bytes())
            elif x.exists():raise ValueError("Non-file model changed path "+p)
            else:pre[p]=None # pure delete
        tested=Path(root)/"pinned-abs-tests.diff"
        tested.write_bytes(test.encode())
        git(d,"apply","--check","--binary",str(tested))
        git(d,"apply","--binary",str(tested))
        altered=[p for p in modelpaths if (sha((d/p).read_bytes()) if (d/p).is_file() else None)!=pre[p]]
        if altered:raise ValueError("Augmented test patch damaged model files "+repr(altered[:10]))
        stats={
            "base_commit":absrow["base_commit"],
            "model_patch_sha256":entry["patch_sha256"],
            "test_patch_sha256":sha(test.encode()),
            "model_patch_changed_file_paths":len(modelpaths),
            "generated_build_file_paths":sum(p.startswith("build/") for p in modelpaths),
            "tested_model_changed_path_count":len(pre),
            "model_diff_line_add_remove_entries":sum(want.values()),
            "line_multiset_verified":True,
            "model_file_hashes_preserved_after_augmented_patch":len(pre),
            "direct_model_test_file_collisions":len(overlap),
            "model_patch_git_apply_index_passed":True,
            "model_test_git_apply_passed":True,
            "verified_tested_tree_in_this_reconstruction_only":True,
            "model_file_sha256_after_model_patch":pre,
        }
    return {"task":TASK,"sample":SAMPLE,"source_runner_outcome":"UNVERIFIED",
        "source_agent_revision":AGENT_REV,"source_test_revision":ABS_REV,
        "git_remote":REMOTE,"status":"new independent exact-full-patch reconstruction passed; original harness tree not inspected",
        "new_reconstruction":stats,
        "historical_docker_tested_tree_verified":False,
        "original_outcome_changed":False,
        "limitations":"This check reproduces model+test patch effects on a new pristine original base, not the historical SWE-ABS Docker test image. It does not prove all original augmented assertions behaved correctly, or independently establish semantic correctness."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    a=p.parse_args()
    x=record()
    if a.check:
        if json.loads(OUT.read_text(encoding="utf8"))!=x:raise ValueError("Requests reconstruction output drift")
    else:OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({k:v for k,v in x.items() if k not in ("new_reconstruction",)},indent=2))
    print(json.dumps({k:v for k,v in x["new_reconstruction"].items() if k!="model_file_sha256_after_model_patch"},indent=2))
if __name__=="__main__":main()
