#!/usr/bin/env python3
"""Step 11: pinned base-source method ownership of added in-place SWE-ABS assertions.

Source-aware and read-only. Maps each changed test patch hunk of django-14434
back to the exact original test_ method in Django's pinned base source.
Then downloads the three original Actions result ZIPs and compares whether
that method was reported OK / SKIPPED / FAILED / ERROR / NOT_OBSERVED.

Does NOT prove a specific branch or every newly-added assertion executed;
no semantic oracle, no new runner outcome, no change of Step 7 analysis policy.

Usage from checkout with 'datasets==4.8.5', gh CLI and GH_TOKEN:
  python scripts/step11_inplace_method_audit.py
  python scripts/step11_inplace_method_audit.py --check
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, subprocess, tempfile, urllib.request
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
OUT=D/"STEP11_INPLACE_METHOD_AUDIT_DJANGO14434_v1.json"
TASK="django__django-14434"
ABS_DATASET="OpenAgentLab/SWE-Bench_Verified_ABS"
ABS_REV="79fc07a8f4ce5e3720e069948073f5f910b7577b"
REPO="Foysal-Munsy/sweabs-free-eval"
HUNK=re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
BASE_METHOD=re.compile(r"^    (?:async )?def (test_[A-Za-z0-9_]+)\s*\(")
NEW_METHOD=re.compile(r"^\+    (?:async )?def (test_[A-Za-z0-9_]+)\s*\(")
VERBOSE=re.compile(r"^\s*(test_[A-Za-z0-9_]+)\s*\(([^)]+)\)\s*\.\.\.\s*(ok|skipped|FAIL|ERROR)\b",re.I)
def sha(s:bytes):return hashlib.sha256(s).hexdigest()

def source_test_case():
    from datasets import load_dataset
    matches=[dict(x) for x in load_dataset(ABS_DATASET,split="test",revision=ABS_REV) if x["instance_id"]==TASK]
    if len(matches)!=1:raise ValueError("Expected exactly one pinned SWE-ABS source record")
    return matches[0]

def hunks_from_patch(patch):
    segments=[];current=None
    for line in patch.splitlines():
        m=HUNK.match(line)
        if m:
            current={"old_start":int(m.group(1)),"old_length":int(m.group(2) or 1),
                     "new_start":int(m.group(3)),"new_length":int(m.group(4) or 1),
                     "added_lines":[],"removed_lines":[]}
            segments.append(current)
        elif current is not None:
            if line.startswith("diff --git") or line.startswith("--- ") or line.startswith("+++ "):
                current=None
            elif line.startswith("+"):current["added_lines"].append(line)
            elif line.startswith("-"):current["removed_lines"].append(line)
    return segments

def method_owner(before_lines,old_start):
    # Upstream base lines are 1-indexed; mapping uses exact old hunk line anchor.
    candidates=[(i,m.group(1)) for i,line in enumerate(before_lines[:old_start],1)
                if (m:=BASE_METHOD.match(line))]
    if not candidates:raise ValueError(f"No original test method preceding old source line {old_start}")
    return candidates[-1][1]

def read_triage():
    with (D/"STEP7_UNVERIFIED_TRIAGE_14.csv").open(encoding="utf8",newline="") as f:
        rows=[x for x in csv.DictReader(f) if x["instance_id"]==TASK]
    if len(rows)!=3 or set(x["sample"] for x in rows)!={"1","2","3"}:
        raise ValueError("Expected exactly three Django-14434 original samples")
    return sorted(rows,key=lambda x:int(x["sample"]))

def original_logs(rows,temp):
    evidence=[]
    for row in rows:
        sample=int(row["sample"]);offset=int(row["offset"])
        runid=int(row["run_id"].split("_")[1])
        d=Path(temp)/f"s{sample}-o{offset}"
        d.mkdir()
        name=f"sweabs-result-{sample}-{offset}"
        x=subprocess.run(["gh","run","download",str(runid),"-R",REPO,"-n",name,"-D",str(d)],
                 capture_output=True,text=True,timeout=120)
        if x.returncode:raise RuntimeError(f"Artifact fetch {name}: {x.stderr[:260]}")
        logs=list(d.rglob("test_output.txt"))
        if len(logs)!=1:raise ValueError(f"Expected one raw test-output file {name}; got {len(logs)}")
        raw=logs[0].read_bytes()
        findings=defaultdict(list)
        for line in raw.decode("utf8",errors="replace").splitlines():
            m=VERBOSE.match(line)
            if m:
                findings[(m.group(1),m.group(2))].append(m.group(3).lower())
        evidence.append((row,raw,findings))
    return evidence

def produce():
    source=source_test_case()
    if source.get("base_commit") is None:raise ValueError("No base commit")
    patch=source["test_patch"]
    digest=sha(patch.encode("utf8"))
    selected=read_triage()
    cross=json.loads((D/"STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json").read_text(encoding="utf8"))
    crossmap={(x["sample"],x["offset"]):x for x in cross["rows"]}
    for row in selected:
        if crossmap[(int(row["sample"]),int(row["offset"]))]["augmented_test_patch_sha256"]!=digest:
            raise ValueError("Test diff SHA mismatch with archived structural crosswalk")
    file_path="tests/schema/tests.py"
    url=f"https://raw.githubusercontent.com/django/django/{source['base_commit']}/{file_path}"
    with urllib.request.urlopen(url,timeout=30) as response:
        original=response.read()
    lines=original.decode("utf8").splitlines()
    if len(lines)<2000:raise ValueError("Fetched pinned base test source suspiciously short")
    hunks=hunks_from_patch(patch)
    if not hunks:raise ValueError("No diff hunks")
    added,existing=[],[]
    for h in hunks:
        if h["removed_lines"]:
            raise ValueError("Unexpected removals in pinned Django-14434 test patch")
        newnames=[m.group(1) for line in h["added_lines"] if (m:=NEW_METHOD.match(line))]
        if newnames:
            added.extend(newnames)
            continue
        if not h["added_lines"]:continue
        existing.append({"old_source_anchor_line":h["old_start"],
                         "method_name":method_owner(lines,h["old_start"]),
                         "added_test_patch_lines":len(h["added_lines"]),
                         "added_assertion_lines":sum(bool(re.search(r"\bself\.assert[A-Za-z_]*\s*\(",line)) for line in h["added_lines"])})
    if len(added)!=1 or len(existing)<5:raise ValueError("Unexpected source-diff method structure")
    unique_existing=sorted(set(h["method_name"] for h in existing))
    if len(unique_existing)<5:raise ValueError("Too few methods modified; source anchor map issue")
    with tempfile.TemporaryDirectory(prefix="step11-django14434-") as tmp:
        logs=original_logs(selected,tmp)
    cases=[]
    for row,raw,found in logs:
        methods=[]
        for name in unique_existing+added:
            matches=[status for (method,cls),statuses in found.items()
                     if method==name and cls.endswith(".SchemaTests") for status in statuses]
            methods.append({"name":name,"type":"added_method" if name in added else "modified_existing_method",
                            "status_values":sorted(set(matches)),
                            "observed_status_count":len(matches)})
        cases.append({"sample":int(row["sample"]),"offset":int(row["offset"]),
            "patch_sha256":row["patch_sha256"],"original_artifact_id":row["run_id"],
            "original_test_log_sha256":sha(raw),
            "prior_suite_passed":int(row["runner_passed"]),
            "prior_suite_skipped":int(row["runner_skipped"]),
            "methods":methods,
            "modified_existing_skipped":sum("skipped" in m["status_values"] for m in methods if m["type"]=="modified_existing_method"),
            "modified_existing_not_observed":sum(not m["status_values"] for m in methods if m["type"]=="modified_existing_method"),
            "modified_existing_seen_ok":sum("ok" in m["status_values"] for m in methods if m["type"]=="modified_existing_method")})
    cases.sort(key=lambda x:x["sample"])
    return {"status":"read-only code-to-test-log method presence audit; never a complete semantic/case-path oracle",
            "task":TASK,"abs_test_revision":ABS_REV,"abs_test_patch_sha256":digest,
            "upstream_base_commit":source["base_commit"],
            "base_source_file":file_path,"base_source_sha256":sha(original),
            "test_patch_removed_lines":sum(len(h["removed_lines"]) for h in hunks),
            "test_patch_hunks":len(hunks),
            "new_methods":added,"existing_test_methods_modified":unique_existing,
            "added_code_hunks_to_existing_methods":existing,
            "samples":cases,
            "limitations":"Original individual test methods may branch or skip internally; method status OK means method completed but not proof every added assertion branch executed. Only source hunks and exact named test methods in archived verbose logs are mapped. Rerun/semantic oracle not performed.",
            "original_runner_labels_modified":False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    out=produce()
    if args.check:
        if json.loads(OUT.read_text(encoding="utf8"))!=out:raise ValueError("In-place source/test output mismatch")
    else:
        OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"test_patch_hunks":out["test_patch_hunks"],
         "existing_test_methods_modified":out["existing_test_methods_modified"],
         "added_methods":out["new_methods"],
         "sample_summaries":[{"sample":x["sample"],"seen_ok":x["modified_existing_seen_ok"],
                  "skipped":x["modified_existing_skipped"],
                  "not_observed":x["modified_existing_not_observed"]} for x in out["samples"]]},indent=2))
if __name__=="__main__":main()
