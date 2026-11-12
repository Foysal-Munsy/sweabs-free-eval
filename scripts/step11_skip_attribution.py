#!/usr/bin/env python3
"""Step 11: descriptive attribution of in-place/added Django tests to raw skips.

Pin source test_patch to SWE-ABS revision, inspect added 'def test_*' names,
and match their individual unittest verbose result lines in fresh original
Actions result ZIPs. Does NOT conclude all augmented assertions executed:
modified existing test methods and setup decorators require separate review.
No original outcome or frozen analysis labels are edited.
"""
import argparse,csv,json,re,subprocess,tempfile,hashlib
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
TRIAGE=D/"STEP7_UNVERIFIED_TRIAGE_14.csv"
SOURCE=D/"STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json"
OUT=D/"STEP11_SKIP_ATTRIBUTION_9_v1.json"
REPO="Foysal-Munsy/sweabs-free-eval"
TEST_ID="OpenAgentLab/SWE-Bench_Verified_ABS"
TEST_REV="79fc07a8f4ce5e3720e069948073f5f910b7577b"
ADDED=re.compile(r"^\+\s*(?:async\s+)?def\s+(test_[A-Za-z0-9_]+)\s*\(")
VERBOSE=re.compile(r"^\s*(test_[A-Za-z0-9_]+)\s*\([^\n)]*\)\s*\.\.\.\s*(ok|skipped|FAIL|ERROR)\b",re.I)

def test_patches(ids):
    from datasets import load_dataset
    found={}
    for x in load_dataset(TEST_ID,split="test",revision=TEST_REV):
        if x["instance_id"] in ids:
            if x["instance_id"] in found:raise ValueError("duplicate test id")
            found[x["instance_id"]]=dict(x)
    if set(found)!=ids:raise ValueError("missing pinned test patches")
    return found

def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");args=p.parse_args()
    with TRIAGE.open(newline="",encoding="utf8") as f:all_rows=list(csv.DictReader(f))
    cases=[x for x in all_rows if x["triage_category"]=="partial_coverage_skips"]
    if len(cases)!=9:raise ValueError("expected nine skip cases")
    source=json.loads(SOURCE.read_text(encoding="utf8"))
    recorded={(x["sample"],x["offset"]):x for x in source["rows"]}
    patches=test_patches({x["instance_id"] for x in cases})
    result=[]
    with tempfile.TemporaryDirectory(prefix="step11-skips-") as t:
        for row in cases:
            sample=int(row["sample"]);offset=int(row["offset"])
            run=int(row["run_id"].split("_")[1])
            name=f"sweabs-result-{sample}-{offset}"
            directory=Path(t)/name
            directory.mkdir(exist_ok=True)
            proc=subprocess.run(["gh","run","download",str(run),"-n",name,"-R",REPO,"-D",str(directory)],
                capture_output=True,text=True,timeout=100)
            if proc.returncode:raise RuntimeError(f"download failed {name}: {proc.stderr[:150]}")
            logs=sorted(p for p in directory.rglob("test_output.txt") if p.is_file())
            if len(logs)!=1:raise ValueError(f"expected one original test output for {name}")
            text=logs[0].read_text(encoding="utf8",errors="replace")
            patch=patches[row["instance_id"]]["test_patch"]
            digest=hashlib.sha256(patch.encode("utf8")).hexdigest()
            if digest!=recorded[(sample,offset)]["augmented_test_patch_sha256"]:
                raise ValueError("SWE-ABS pinned source test SHA mismatch "+name)
            added=sorted(set(m.group(1) for line in patch.splitlines() if (m:=ADDED.match(line))))
            observed={}
            for line in text.splitlines():
                match=VERBOSE.match(line)
                if match:observed.setdefault(match.group(1),[]).append(match.group(2).lower())
            meth=[{"name":nm,"observed_result_types":sorted(set(observed.get(nm,[]))),
                    "observed_verbose_matches":len(observed.get(nm,[]))}
                  for nm in added]
            statuses=Counter(v for vals in observed.values() for v in vals)
            prior=int(row["runner_skipped"])
            result.append({"sample":sample,"offset":offset,"instance_id":row["instance_id"],
                "model_patch_sha256":row["patch_sha256"],"test_patch_sha256":digest,
                "augmented_added_test_function_names":meth,
                "added_function_count":len(added),
                "observed_verbose_test_status_tallies":dict(statuses),
                "prior_reported_skips":prior,
                "added_function_names_observed_skipped":sum("skipped" in x["observed_result_types"] for x in meth),
                "added_function_names_observed_ok":sum("ok" in x["observed_result_types"] for x in meth),
                "added_function_names_not_seen":sum(not x["observed_result_types"] for x in meth),
                "limits":"Only newly added def test_* names are matched. Existing test functions modified by the augmented patch are NOT identified; inherited test cases and setup/backend skips may affect coverage. No label promotion."})
    result.sort(key=lambda x:(x["sample"],x["offset"]))
    output={"source_revision":TEST_REV,"cases":len(result),
        "complete_source_test_SHA_matches":len(result),
        "purpose":"descriptive method-to-log crosswalk, not semantic oracle or coverage completion",
        "labels_modified":False,"rows":result}
    if args.check:
        if json.loads(OUT.read_text(encoding="utf8"))!=output:raise ValueError("Skip attribution differs")
    else:OUT.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({x["instance_id"]+f"/s{x['sample']}":{"added":x["added_function_count"],"added_seen_ok":x["added_function_names_observed_ok"],"added_seen_skip":x["added_function_names_observed_skipped"],"existing_plus_all_skips":x["prior_reported_skips"]} for x in result},indent=2))
if __name__=="__main__":main()
