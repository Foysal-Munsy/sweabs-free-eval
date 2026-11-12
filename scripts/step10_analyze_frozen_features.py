#!/usr/bin/env python3
"""Step 10: prespecified univariate AUROCs with task-cluster bootstrap.
No model training, threshold search, iid-run confidence intervals, or label changes.
Uses only Python standard library. v2 fixes low-bit LCG modulo sampling from v1. Run at repo root:
 python scripts/step10_analyze_frozen_features.py
 python scripts/step10_analyze_frozen_features.py --check
"""
from __future__ import annotations
import argparse,csv,json,math
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
FEATURES=D/"STEP9_TRAJECTORY_FEATURES_v1.csv"
LABELS=D/"STEP7_ANALYSIS_LABELS_v1.csv"
OUT=D/"STEP10_AUROC_TASK_CLUSTER_v2.json"
SEED=20261112
B=500
PREDICTORS=[
 ("duplicate_terminal_rate",1),
 ("terminal_error_rate",1),
 ("any_verification",-1),
 ("editor_after_last_verification",1),
]
TARGETS=["primary_y","noninvalid_sensitivity_y","runner_only_sensitivity_y","skipped_as_pass_scenario_y"]

def read(path):
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def identity(x):
    return (x["sample"],x["instance_id"],x["patch_sha256"])

def roc_auc(rows):
    positives=[x for x,y,t in rows if y==1]
    negatives=[x for x,y,t in rows if y==0]
    if not positives or not negatives:return None
    wins=sum(1 if p>n else 0.5 if p==n else 0 for p in positives for n in negatives)
    return wins/(len(positives)*len(negatives))

def quantile(v,p):
    v=sorted(v)
    x=(len(v)-1)*p
    a=int(math.floor(x));b=int(math.ceil(x))
    return v[a]+(x-a)*(v[b]-v[a])

def bootstrap(rows,seed=SEED,b=B):
    groups=defaultdict(list)
    for x in rows:groups[x[2]].append(x)
    keys=sorted(groups)
    state=seed
    values=[]
    for _ in range(b):
        draw=[]
        for _ in keys:
            state=(1664525*state+1013904223)&0xffffffff
            chosen=keys[(state*len(keys))//(1<<32)]  # high-bit scaling avoids short cycles when len(keys) is power-of-two
            draw.extend(groups[chosen])
        result=roc_auc(draw)
        if result is not None:values.append(result)
    if not values:return {"ci95":None,"valid_bootstraps":0}
    return {"ci95":[round(quantile(values,.025),6),round(quantile(values,.975),6)],"valid_bootstraps":len(values)}

def analyze():
    labs=read(LABELS);features=read(FEATURES)
    if len(labs)!=198 or len(features)!=198:raise ValueError("Expected 198 labels/features")
    fmap={identity(r):r for r in features}
    if len(fmap)!=198:raise ValueError("Duplicate exact feature identities")
    if set(fmap)!={identity(r) for r in labs}:raise ValueError("Exact feature-label match failure")
    if any(r.get("trace_source_revision")!="b5515d1dce40036633293b70477f0633b24593f7" for r in features):
        raise ValueError("Unexpected trajectory revision")
    output={"source_features":str(FEATURES.relative_to(ROOT)),"source_labels":str(LABELS.relative_to(ROOT)),
        "spec":"docs/STEP8_FROZEN_INDICATORS_v1.md","seed":SEED,"bootstrap_replicates":B,
        "resampling_unit":"instance_id (all sample/patch runs kept in same task cluster)",
        "score_orientation":"Higher score means presumed messier; any_verification is negated.",
        "targets":{}}
    for target in TARGETS:
        selected=[r for r in labs if r[target] in ("0","1")]
        tasks=sorted({r["instance_id"] for r in selected})
        ptasks=sorted({r["instance_id"] for r in selected if r[target]=="1"})
        taskgroups=defaultdict(set)
        for r in selected:taskgroups[r["instance_id"]].add(r[target])
        info={"eligible_runs":len(selected),"fail_runs":sum(r[target]=="1" for r in selected),
            "pass_runs":sum(r[target]=="0" for r in selected),"excluded_runs":198-len(selected),
            "unique_tasks":len(tasks),"fail_tasks":len(ptasks),
            "discordant_tasks":sum(len(y)>1 for y in taskgroups.values()),
            "features":{}}
        for key,direction in PREDICTORS:
            rows=[]
            for r in selected:
                f=fmap[identity(r)]
                text=f.get(key,"")
                if text=="" or text is None:continue
                score=direction*float(text)
                rows.append((score,int(r[target]),r["instance_id"]))
            valid_fail=sum(y for _,y,_ in rows)
            valid_pass=len(rows)-valid_fail
            auc=roc_auc(rows)
            bt=bootstrap(rows) if auc is not None else {"ci95":None,"valid_bootstraps":0}
            info["features"][key]={"n":len(rows),"missing":len(selected)-len(rows),
                "pass":valid_pass,"fail":valid_fail,
                "oriented_auroc":round(auc,6) if auc is not None else None,
                "ci95_task_cluster":bt["ci95"],
                "valid_bootstraps":bt["valid_bootstraps"],
                "direction":"negative" if direction==-1 else "positive"}
        output["targets"][target]=info
    return output

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    out=analyze()
    content=json.dumps(out,indent=2,sort_keys=True)+"\n"
    if args.check:
        if OUT.read_text(encoding="utf-8")!=content:raise ValueError("Analysis mismatch")
    else:OUT.write_text(content,encoding="utf-8")
    print(json.dumps(out["targets"]["primary_y"],indent=2))
if __name__=="__main__":main()
