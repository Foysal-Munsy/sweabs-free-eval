#!/usr/bin/env python3
"""Step 11 exploratory robustness (post-hoc, NOT prespecified confirmatory tests).

Task-macro AUROC collapses concordantly labelled runs to one task-level mean and
excludes tasks whose runs disagree on the selected target. Within-project AUROC
compares runs from distinct task IDs sharing repository prefix. Leave-one-positive
TASK-out excludes all runs from each positive task in turn; this is influence
diagnostics, not cross-validated classifier performance. No model fitting.
Usage: python scripts/step11_robustness.py [--check]
"""
from __future__ import annotations
import argparse,csv,json,math,statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"results/2026-11-12"
LABELS=DIR/"STEP7_ANALYSIS_LABELS_v1.csv"
FEATURES=DIR/"STEP9_TRAJECTORY_FEATURES_v1.csv"
OUT=DIR/"STEP11_EXPLORATORY_ROBUSTNESS_v1.json"
TARGETS=["primary_y","noninvalid_sensitivity_y","runner_only_sensitivity_y","skipped_as_pass_scenario_y"]
INDICATORS=[("duplicate_terminal_rate",1),("terminal_error_rate",1),("any_verification",-1),("editor_after_last_verification",1)]

def load(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def key(row):return row["sample"],row["instance_id"],row["patch_sha256"]

def auc(rows):
    positive=[x[0] for x in rows if x[1]==1]
    negative=[x[0] for x in rows if x[1]==0]
    if not positive or not negative:return None
    return sum((p>n)+0.5*(p==n) for p in positive for n in negative)/(len(positive)*len(negative))

def rnd(v):
    return round(v,6) if v is not None else None

def task_macro(rows):
    groups=defaultdict(list)
    for score,y,task,project in rows:groups[task].append((score,y))
    classified=[]
    discordant=[]
    for task,vals in sorted(groups.items()):
        outcomes={y for _,y in vals}
        if len(outcomes)>1:
            discordant.append(task)
            continue
        classified.append((statistics.mean(score for score,_ in vals),vals[0][1]))
    return {"task_macro_auc":rnd(auc(classified)),"included_tasks":len(classified),
            "positive_tasks":sum(y for _,y in classified),"discordant_tasks_excluded":len(discordant)}

def within_project(rows):
    positives=[r for r in rows if r[1]==1]
    negatives=[r for r in rows if r[1]==0]
    same=[(p,n) for p in positives for n in negatives if p[3]==n[3] and p[2]!=n[2]]
    if not same:return {"auroc":None,"comparable_pairs":0,"projects_with_both_classes":0}
    value=sum((p[0]>n[0])+0.5*(p[0]==n[0]) for p,n in same)/len(same)
    return {"auroc":rnd(value),"comparable_pairs":len(same),
        "projects_with_both_classes":len({p[3] for p,n in same})}

def loo_positive_tasks(rows):
    failures=sorted({r[2] for r in rows if r[1]==1})
    result=[]
    for task in failures:
        retained=[r for r in rows if r[2]!=task]
        value=auc(retained)
        if value is not None:result.append(value)
    return {"positive_task_omissions":len(failures),
        "valid_auroc_values":len(result),
        "min_auroc":rnd(min(result)) if result else None,
        "max_auroc":rnd(max(result)) if result else None}

def ranks(values):
    order=sorted(enumerate(values),key=lambda kv:kv[1])
    out=[0.0]*len(values)
    i=0
    while i<len(order):
        j=i+1
        while j<len(order) and order[j][1]==order[i][1]:j+=1
        rank=(i+1+j)/2
        for k in range(i,j):out[order[k][0]]=rank
        i=j
    return out

def spearman(xs,ys):
    if len(xs)!=len(ys) or len(xs)<3:return None
    rx,ry=ranks(xs),ranks(ys)
    ax,ay=statistics.mean(rx),statistics.mean(ry)
    xdev=[v-ax for v in rx];ydev=[v-ay for v in ry]
    denom=math.sqrt(sum(v*v for v in xdev)*sum(v*v for v in ydev))
    return sum(x*y for x,y in zip(xdev,ydev))/denom if denom else None

def produce():
    labels,features=load(LABELS),load(FEATURES)
    fmap={key(x):x for x in features}
    if len(labels)!=198 or len(features)!=198 or len(fmap)!=198 or set(fmap)!={key(x) for x in labels}:
        raise ValueError("198 unique, exact label-to-feature joins required")
    out={"status":"post-hoc exploratory robustness only; no preregistration, model fitting or externally held-out prediction",
         "source_features":str(FEATURES.relative_to(ROOT)),
         "source_labels":str(LABELS.relative_to(ROOT)),
         "task_macro_policy":"one per task, mean score across samples, drop discordant-label tasks; complete-case feature rows",
         "within_project_policy":"pairwise within project prefix before '__', exclude comparisons of same task ID",
         "leave_one_positive_task_out_policy":"remove all runs of one positive task, recompute raw run-level AUROC; not predictive cross-validation",
         "targets":{}}
    for name in TARGETS:
        selected=[x for x in labels if x[name] in ("0","1")]
        featuremap={}
        for predictor,orientation in INDICATORS:
            rows=[]
            for x in selected:
                text=fmap[key(x)][predictor]
                if text=="" or text is None:continue
                task=x["instance_id"]
                rows.append((orientation*float(text),int(x[name]),task,task.split("__",1)[0]))
            macro=task_macro(rows)
            local=within_project(rows)
            loo=loo_positive_tasks(rows)
            featuremap[predictor]={"n_runs":len(rows),"raw_run_auroc":rnd(auc(rows)),
                "task_macro":macro,"within_project":local,"leave_one_positive_task_out":loo}
        # outcome-independent confounding proxy and simple non-confirmatory baseline
        base_rows=[(float(fmap[key(x)]["n_steps_dataset"]),int(x[name]),x["instance_id"],
             x["instance_id"].split("__",1)[0]) for x in selected]
        dup_x=[float(fmap[key(x)]["duplicate_terminal_rate"]) for x in selected]
        len_y=[float(fmap[key(x)]["n_steps_dataset"]) for x in selected]
        out["targets"][name]={"n":len(selected),"fail_runs":sum(x[name]=="1" for x in selected),
            "n_unique_tasks":len({x["instance_id"] for x in selected}),
            "n_fail_tasks":len({x["instance_id"] for x in selected if x[name]=="1"}),
            "n_projects":len({x["instance_id"].split("__",1)[0] for x in selected}),
            "indicator_results":featuremap,
            "exploratory_length_baseline":{"n_steps_auroc":rnd(auc(base_rows)),
                "duplicate_rate_vs_steps_spearman":rnd(spearman(dup_x,len_y))}}
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    output=produce()
    if args.check:
        if json.loads(OUT.read_text(encoding="utf8"))!=output:raise ValueError("Robustness JSON mismatch")
    else:
        OUT.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({k:{"n":v["n"],"fail_tasks":v["n_fail_tasks"],
                     "duplicate":v["indicator_results"]["duplicate_terminal_rate"],
                     "length":v["exploratory_length_baseline"]} for k,v in output["targets"].items()},indent=2))
if __name__=="__main__":main()
