#!/usr/bin/env python3
"""Step 11 read-only independent raw Actions artifact re-audit of the 14 UNVERIFIED runs.

Downloads owner-accessible, short-retention artifacts using GitHub CLI and
GITHUB_TOKEN/actions:read within GitHub Actions. Never publishes raw ZIPs,
predictions, huge test logs or agent patches. Emits metadata-only evidence.
No reruns or new PASS/FAIL adjudication; explicitly distinct from outcome-label
research.
Usage: python scripts/step11_raw_artifact_reaudit14.py [--check]
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"results/2026-11-12"
TRIAGE=DATA/"STEP7_UNVERIFIED_TRIAGE_14.csv"
OUT=DATA/"STEP11_RAW_ARTIFACT_REAUDIT14_v1.json"
REPO="Foysal-Munsy/sweabs-free-eval"
def sha_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def load_json(p:Path):
    return json.loads(p.read_text(encoding="utf8"))
def find_one(d:Path,name:str):
    matches=sorted(d.rglob(name))
    if len(matches)==1:return matches[0]
    if not matches:return None
    return sorted(matches,key=lambda p:len(p.parts))[0]
def summaries(text:str):
    # This is deliberately descriptive, NOT a final runner verdict parser.
    last=text.splitlines()
    matches=[line.strip() for line in last if re.search(
        r"(?:={3,}.*\b(?:passed|failed|error|skipped)\b.*\bin\s+\d|^Ran \d+ tests? in|^FAILED \(|^OK$)",line,re.I)]
    return [x[:250] for x in matches[-6:]]
def reported_skips(text:str):
    lines=[]
    for line in text.splitlines():
        stripped=line.strip()
        if re.search(r"(?:^SKIPPED\s*\[|\bskipped\s+['\"]|^\s*(?:test_\w+.*\.\.\.\s*skipped))",stripped,re.I):
            lines.append(stripped[:250])
    return lines[:35]
def analyze_one(entry,temp:Path):
    sample=int(entry["sample"]);offset=int(entry["offset"]);run_id=int(entry["run_id"].split("_")[1])
    name=f"sweabs-result-{sample}-{offset}"
    directory=temp/f"{sample}-{offset}"
    directory.mkdir(parents=True,exist_ok=True)
    completed=subprocess.run(["gh","run","download",str(run_id),"-R",REPO,
      "-n",name,"-D",str(directory)],capture_output=True,text=True,timeout=100)
    if completed.returncode:
        raise RuntimeError(f"Download failed {sample}:{offset} ({name}), exit {completed.returncode}: {completed.stderr[:250]}")
    metadata_file=find_one(directory,"metadata.json")
    result_file=find_one(directory,"result.json")
    if metadata_file is None:raise ValueError(f"Missing metadata for {name}")
    md=load_json(metadata_file)
    result=load_json(result_file) if result_file else {}
    if md.get("patch_sha256")!=entry["patch_sha256"]:
        raise ValueError(f"model patch SHA mismatch {name}: {md.get('patch_sha256')}")
    if md.get("instance_id")!=entry["instance_id"] or int(md.get("sample",-1))!=sample:
        raise ValueError("metadata run identity mismatch "+name)
    # File path may vary among pilot generations. Preserve logged test bytes,
    # not derived semantic inferences.
    candidates=sorted(p for p in directory.rglob("*") if p.is_file() and
        re.search(r"test_output\.(?:txt|log)$",p.name))
    paths=[str(p.relative_to(directory)) for p in candidates]
    logs=[]
    for p in candidates:
        raw=p.read_bytes()
        if len(raw)>30*1024*1024:raise ValueError("Oversized raw test output")
        t=raw.decode("utf8",errors="replace")
        logs.append({"path":str(p.relative_to(directory)),"bytes":len(raw),
             "sha256":sha_bytes(raw),"observed_summary_lines":summaries(t),
             "skip_related_lines":reported_skips(t)})
    direct=[p for p in directory.rglob("*") if p.is_file()]
    return {
      "sample":sample,"offset":offset,"instance_id":entry["instance_id"],
      "patch_sha256":entry["patch_sha256"],"run_id":run_id,
      "artifact_name":name,"artifact_present":True,
      "triage_category":entry["triage_category"],
      "prior_passed":entry["runner_passed"],"prior_failed":entry["runner_failed"],
      "prior_skipped":entry["runner_skipped"],
      "metadata_patch_sha256":md.get("patch_sha256"),
      "metadata_test_patch_sha256":md.get("test_patch_sha256"),
      "result_available":bool(result_file),
      "result_status":str(result.get("outcome",result.get("result","")))[:200],
      "file_basenames":sorted({p.name for p in direct}),
      "raw_test_outputs":logs,
      "evidence_boundary":"artifact zip downloaded fresh; source identity checked; no new verdict"
    }
def produce():
    with TRIAGE.open(newline="",encoding="utf8") as f:rows=list(csv.DictReader(f))
    if len(rows)!=14:raise ValueError("14 unique cases required")
    with tempfile.TemporaryDirectory(prefix="step11-raw-audit-") as tmp:
        result=[analyze_one(x,Path(tmp)) for x in rows]
    if len({(x["sample"],x["offset"]) for x in result})!=14:
        raise ValueError("Duplicate/missing artifacts")
    return {
      "status":"fresh original Actions ZIP download and identity/status-log metadata inspection only",
      "cases":len(result),
      "all_artifact_downloads_succeeded":True,
      "identity_checked":len(result),
      "test_output_files_total":sum(len(x["raw_test_outputs"]) for x in result),
      "category_counts":{c:sum(x["triage_category"]==c for x in result)
          for c in sorted({x["triage_category"] for x in result})},
      "raw_outputs_published":False,
      "versioned_runner_labels_modified":False,
      "limits":"Test-log checksums and skip snippets are descriptive only; skipped cases remain unresolved without backend-matched reruns, overlap cases require non-destructive exact-patch tests, generated build patch requires full tested-tree integrity.",
      "rows":result
    }
def main():
    a=argparse.ArgumentParser();a.add_argument("--check",action="store_true");args=a.parse_args()
    result=produce()
    if args.check:
        if json.loads(OUT.read_text(encoding="utf8"))!=result:raise ValueError("Raw ZIP audit result changed")
    else:OUT.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:v for k,v in result.items() if k in
        ("cases","identity_checked","test_output_files_total","category_counts")},indent=2))
if __name__=="__main__":main()
