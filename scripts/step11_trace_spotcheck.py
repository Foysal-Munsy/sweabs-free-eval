#!/usr/bin/env python3
"""Step 11 independently recounted small raw-trajectory spot-check sample.

Deterministic selection: in each sample the first two PASS, first FAIL, and
first UNVERIFIED rows by original Step 7 offset. This checks *parser alignment*
but does NOT establish strengthened-test semantic correctness or unseen traces.
Unlike Step 9 it does not import its extraction function.
Usage: python scripts/step11_trace_spotcheck.py [--check]
"""
import argparse,csv,hashlib,json,re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
LABELS=D/"STEP7_ANALYSIS_LABELS_v1.csv"
FEATURES=D/"STEP9_TRAJECTORY_FEATURES_v1.csv"
OUTPUT=D/"STEP11_TRACE_SPOTCHECK_12_v1.json"
DATASET="tarsur385/swe-verified-gemini3-flash-trajectories"
REVISION="b5515d1dce40036633293b70477f0633b24593f7"
FIELDS=("assistant_message_count","tool_calls_total","terminal_calls","editor_calls",
        "verification_commands","duplicate_terminal_commands",
        "immediate_duplicate_terminal_commands","terminal_errors_observed",
        "editor_after_last_verification","any_verification",
        "duplicate_terminal_rate","terminal_error_rate",
        "zero_terminal_exposure","error_coverage_complete")

def rows(path):
    with path.open(encoding="utf8",newline="") as f:return list(csv.DictReader(f))

def identity(x):
    return (int(x["sample"]),x["instance_id"],x["patch_sha256"])

def selected_labels():
    all_rows=rows(LABELS)
    if len(all_rows)!=198:raise ValueError("Expected complete Step 7 manifest")
    picked=[]
    for sample in (1,2,3):
        rr=sorted((x for x in all_rows if int(x["sample"])==sample),key=lambda x:int(x["offset"]))
        for outcome,n in (("PASS",2),("FAIL",1),("UNVERIFIED",1)):
            subset=[x for x in rr if x["raw_outcome_v2"]==outcome][:n]
            if len(subset)!=n:raise ValueError("Missing selected outcome")
            picked+=subset
    if len(picked)!=12 or len({identity(x) for x in picked})!=12:raise ValueError("Invalid audit identities")
    return picked

def source_rows():
    from datasets import load_dataset
    return load_dataset(DATASET,split="train",revision=REVISION)

def recount(messages):
    # Independent iteration and aggregation implementation (no Step 9 imports).
    if not isinstance(messages,list):raise ValueError("Invalid trace")
    commands=[]
    calls=[]
    answers={}
    for at,m in enumerate(messages):
        if m["role"]=="assistant":
            for tc in (m.get("tool_calls") or []):
                name=tc["function"]["name"]
                cid=tc.get("id")
                command=None
                if name=="terminal":
                    command=" ".join(tc["function"]["arguments"]["command"].split())
                    commands.append((at,cid,command))
                calls.append((at,name,cid))
        if m["role"]=="tool":
            answers.setdefault(m.get("tool_call_id"),[]).append(str(m.get("content","")))
    normal=[s for _,_,s in commands]
    # Same frozen decision boundary, separately implemented with word-boundary matching.
    verification=[at for at,ident,cmd in commands if re.search(
        r"\\b(?:pytest|unittest|runtests\\.py|tox|nosetests)\\b|python[0-9.]* -m (?:pytest|unittest)",cmd,re.I)]
    seen=Counter(normal)
    exact_duplicate=sum(v-1 for v in seen.values() if v>1)
    immediate=sum(normal[i]==normal[i-1] for i in range(1,len(normal)))
    terminal_ids=Counter(cid for _,cid,_ in commands)
    observed_errors=0
    all_results=True
    for _,cid,_ in commands:
        reply=answers.get(cid,[])
        if not isinstance(cid,str) or not cid or terminal_ids[cid]!=1 or len(reply)!=1:
            all_results=False
            continue
        result=reply[0]
        statuses=[int(n) for n in re.findall(r"""['"]exit_code['"]\s*:\s*(-?\d+)""",result)]
        err=bool(re.search(r"""'is_error'\s*:\s*True|"is_error"\s*:\s*true""",result))
        if not statuses and not err:all_results=False
        observed_errors+=int(err or any(n!=0 for n in statuses))
    nt=len(commands)
    nedit=sum(name=="file_editor" for _,name,_ in calls)
    return {
        "assistant_message_count":sum(m["role"]=="assistant" for m in messages),
        "tool_calls_total":len(calls),"terminal_calls":nt,
        "editor_calls":nedit,
        "verification_commands":len(verification),
        "duplicate_terminal_commands":exact_duplicate,
        "immediate_duplicate_terminal_commands":immediate,
        "terminal_errors_observed":observed_errors if all_results else "",
        "editor_after_last_verification":sum(at>verification[-1] and name=="file_editor" for at,name,_ in calls) if verification else "",
        "any_verification":int(bool(verification)),
        "duplicate_terminal_rate":format(exact_duplicate/max(1,nt),".12g"),
        "terminal_error_rate":format(observed_errors/nt,".12g") if nt and all_results else "",
        "zero_terminal_exposure":int(not nt),
        "error_coverage_complete":int(bool(nt and all_results))
    }

def produce():
    selected=selected_labels()
    wanted={identity(x):x for x in selected}
    evidence={identity(x):x for x in rows(FEATURES)}
    audited=[]
    for row in source_rows():
        if row.get("resolved") is not True:continue
        patch=row["patch"]
        ident=(int(row["sample"]),row["instance_id"],hashlib.sha256(patch.encode("utf8")).hexdigest())
        if ident not in wanted:continue
        actual=recount(row["messages"])
        expected=evidence[ident]
        mismatches={k:{"expected":expected[k],"observed":str(actual[k])}
                    for k in FIELDS if expected[k]!=str(actual[k])}
        x=wanted[ident]
        audited.append({"sample":int(x["sample"]),"offset":int(x["offset"]),
            "instance_id":x["instance_id"],"patch_sha256":x["patch_sha256"],
            "raw_outcome_v2":x["raw_outcome_v2"],
            "checked_indicators":len(FIELDS),"mismatched_indicators":mismatches})
    audited.sort(key=lambda x:(x["sample"],x["offset"]))
    if len(audited)!=12 or len({(x["sample"],x["instance_id"]) for x in audited})!=12:
        raise ValueError(f"Missing/duplicate raw spot-check evidence: {len(audited)}")
    if any(x["mismatched_indicators"] for x in audited):
        raise ValueError("Independent recount differs from archived feature table: "+json.dumps(audited))
    return {"source_dataset":DATASET,"source_revision":REVISION,
        "selection":"for each sample (1,2,3): first two PASS, first FAIL and first UNVERIFIED, sorted by Step 7 offset",
        "n_trajectories":len(audited),"n_indicator_comparisons":len(audited)*len(FIELDS),
        "n_mismatches":0,
        "scope_limit":"Independent software recount of selected raw trajectory messages; not human review or oracle confirmation of strengthened-test outcomes",
        "rows":audited}

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    result=produce()
    if args.check:
        if json.loads(OUTPUT.read_text(encoding="utf8"))!=result:raise ValueError("Spotcheck result differs from stored report")
    else:OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({k:result[k] for k in ("n_trajectories","n_indicator_comparisons","n_mismatches","source_revision")},indent=2))
if __name__=="__main__":main()
