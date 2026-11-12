#!/usr/bin/env python3
"""Frozen Step 8 v1 trajectory feature extractor, exact-match run identity.

Step 11 implementation-only fix: Django runtests.py verification pattern uses an
escaped dot rather than an escaped backslash plus wildcard. Formula unchanged.
Usage: pip install datasets huggingface_hub; python scripts/step9_extract_trajectory_features.py
       python scripts/step9_extract_trajectory_features.py --check
Outputs derived metadata only. No trajectory text is written to results.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv"
OUTPUT=ROOT/"results/2026-11-12/STEP9_TRAJECTORY_FEATURES_v1.csv"
SUMMARY=ROOT/"results/2026-11-12/STEP9_COVERAGE_v1.json"
DATASET="tarsur385/swe-verified-gemini3-flash-trajectories"
REVISION="b5515d1dce40036633293b70477f0633b24593f7"
VERIFY=re.compile(r"(^|[^A-Za-z0-9_])(pytest|unittest|runtests\.py|tox|nosetests)(?=$|[^A-Za-z0-9_])|python[0-9.]* -m (pytest|unittest)",re.I)
NONZERO=re.compile(r"""['"]exit_code['"]\s*:\s*(-?\d+)""")
ERROR=re.compile(r"""(?:'is_error'\s*:\s*True|"is_error"\s*:\s*true)""")
FIELDS=["sample","offset","instance_id","patch_sha256","n_steps_dataset","assistant_message_count",
        "tool_calls_total","terminal_calls","editor_calls","verification_commands",
        "duplicate_terminal_commands","immediate_duplicate_terminal_commands","terminal_errors_observed",
        "editor_after_last_verification","any_verification","duplicate_terminal_rate",
        "terminal_error_rate","zero_terminal_exposure","error_coverage_complete","trace_source_revision"]

def extract(row:dict[str,Any])->dict[str,Any]:
    messages=row.get("messages")
    if not isinstance(messages,list): raise ValueError("messages not list")
    calls,terminal_ids,tool_outputs=[],{},{}
    for ix,m in enumerate(messages):
        if not isinstance(m,dict): raise ValueError("non-dict message")
        role=m.get("role")
        if role=="assistant":
            raw=m.get("tool_calls")
            if raw is None: raw=[]
            if not isinstance(raw,list): raise ValueError("tool_calls not list")
            for tool in raw:
                if not isinstance(tool,dict) or not isinstance(tool.get("function"),dict):
                    raise ValueError("malformed tool call")
                name=tool["function"].get("name")
                if not isinstance(name,str): raise ValueError("missing tool call name")
                args=tool["function"].get("arguments")
                if name=="terminal" and (not isinstance(args,dict) or not isinstance(args.get("command"),str)):
                    raise ValueError("terminal command malformed")
                call={"name":name,"command":args["command"] if name=="terminal" else "", "ix":ix,"id":tool.get("id")}
                calls.append(call)
                if name=="terminal":
                    ident=tool.get("id")
                    if isinstance(ident,str) and ident:
                        terminal_ids[ident]=terminal_ids.get(ident,0)+1
        elif role=="tool":
            ident=m.get("tool_call_id")
            if isinstance(ident,str):
                tool_outputs.setdefault(ident,[]).append(str(m.get("content","")))
    terminals=[x for x in calls if x["name"]=="terminal"]
    commands=[" ".join(x["command"].split()) for x in terminals]
    verification_ix=[x["ix"] for x in terminals if VERIFY.search(" ".join(x["command"].split()))]
    counts=Counter(commands)
    duplicated=sum(n-1 for n in counts.values() if n>1)
    immediate=sum(commands[i]==commands[i-1] for i in range(1,len(commands)))
    error_n,complete=0,True
    for x in terminals:
        ident=x["id"]
        if not isinstance(ident,str) or terminal_ids.get(ident)!=1 or len(tool_outputs.get(ident,[]))!=1:
            complete=False
            continue
        output=tool_outputs[ident][0]
        statuses=[int(v) for v in NONZERO.findall(output)]
        flags=bool(ERROR.search(output))
        if not statuses and not flags:  # no explicit parseable terminal result
            complete=False
        if any(v!=0 for v in statuses) or flags:
            error_n+=1
    error_value=error_n if complete else ""
    nterm=len(terminals)
    return {
        "n_steps_dataset":row.get("n_steps",""),"assistant_message_count":sum(m.get("role")=="assistant" for m in messages),
        "tool_calls_total":len(calls),"terminal_calls":nterm,
        "editor_calls":sum(x["name"]=="file_editor" for x in calls),
        "verification_commands":len(verification_ix),
        "duplicate_terminal_commands":duplicated,
        "immediate_duplicate_terminal_commands":immediate,
        "terminal_errors_observed":error_value,
        "editor_after_last_verification":sum(x["name"]=="file_editor" and x["ix"]>verification_ix[-1] for x in calls) if verification_ix else "",
        "any_verification":int(bool(verification_ix)),
        "duplicate_terminal_rate":format(duplicated/max(1,nterm),".12g"),
        "terminal_error_rate":format(error_n/nterm,".12g") if complete and nterm else "",
        "zero_terminal_exposure":int(nterm==0),
        "error_coverage_complete":int(complete and nterm>0),
        "trace_source_revision":REVISION,
    }

def source_rows():
    from datasets import load_dataset
    return load_dataset(DATASET,split="train",revision=REVISION)

def produce():
    with INPUT.open(newline="",encoding="utf8") as f: labels=list(csv.DictReader(f))
    needed={(int(x["sample"]),x["instance_id"],x["patch_sha256"]):x for x in labels}
    if len(labels)!=198 or len(needed)!=198:raise ValueError("Identity ledger has duplicates or wrong length")
    mapped={};seen=set();missing_identity=0;seen_total=0
    for row in source_rows():
        seen_total+=1
        if row.get("resolved") is not True:continue
        patch=row.get("patch")
        if not isinstance(patch,str):raise ValueError("resolved run missing patch")
        hashval=hashlib.sha256(patch.encode("utf8")).hexdigest()
        key=(int(row["sample"]),row["instance_id"],hashval)
        if key in needed:
            if key in seen:raise ValueError("duplicate exact matched run")
            seen.add(key)
            mapped[key]=extract(dict(row))
        elif any(k[0]==key[0] and k[1]==key[1] for k in needed):
            missing_identity+=1
    if len(mapped)!=198:
        raise ValueError(f"Exact-match coverage {len(mapped)}/198; mismatched same-task rows {missing_identity}. Reject partial analysis.")
    result=[]
    for label in labels:
        key=(int(label["sample"]),label["instance_id"],label["patch_sha256"])
        result.append({**{k:label[k] for k in ["sample","offset","instance_id","patch_sha256"]},**mapped[key]})
    summary={"dataset":DATASET,"revision":REVISION,"dataset_rows_seen":seen_total,"expected_exact_runs":len(labels),
             "matched_exact_runs":len(mapped),"mismatched_same_task_rows":missing_identity,
             "unique_task_ids":len({x["instance_id"] for x in result}),
             "error_coverage_complete":sum(x["error_coverage_complete"] for x in result),
             "with_verification":sum(x["any_verification"] for x in result),
             "feature_spec":"docs/STEP8_FROZEN_INDICATORS_v1.md",
             "label_manifest":"results/2026-11-12/STEP7_ANALYSIS_LABELS_v1.csv"}
    return result,summary

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    records,summary=produce()
    if args.check:
        with OUTPUT.open(newline="",encoding="utf8") as f: old=list(csv.DictReader(f))
        if old!=[{k:str(x.get(k,"")) for k in FIELDS} for x in records]:
            raise ValueError("Feature CSV mismatch")
        if json.loads(SUMMARY.read_text())!=summary:raise ValueError("Coverage mismatch")
    else:
        OUTPUT.parent.mkdir(parents=True,exist_ok=True)
        with OUTPUT.open("w",newline="",encoding="utf8") as f:
            w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n");w.writeheader();w.writerows(records)
        SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
