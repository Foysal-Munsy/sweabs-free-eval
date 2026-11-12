#!/usr/bin/env python3
"""New controlled Step 11 Django backend / collection probe, versioned separately.

Preparation loads exact frozen Gemini 3 Flash patch and pinned SWE-ABS test
patch and reconstructs both in pristine base checkout. Execution is targeted,
NOT a full SWE-ABS Docker evaluation; original runner outcomes stay frozen.

CLI:
  python scripts/step11_django_backend_probe.py prepare --task ... --sample 1
  python scripts/step11_django_backend_probe.py execute --task ... --sample 1
Path scratch/step11-django-<...>/ is transient, NEVER committed.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,os,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
AGENT="tarsur385/swe-verified-gemini3-flash-trajectories"
REV="b5515d1dce40036633293b70477f0633b24593f7"
ABS="OpenAgentLab/SWE-Bench_Verified_ABS"
TEST_REV="79fc07a8f4ce5e3720e069948073f5f910b7577b"
ALLOWED={
 "django__django-14434":{
     "method":"schema.tests.SchemaTests.test_func_unique_constraint_covering",
     "feature_flags":["supports_expression_indexes","supports_covering_indexes"]},
 "django__django-15503":{
     "method":"model_fields.test_jsonfield_numeric_keys.JSONFieldNumericKeyLookupsTests.test_oracle_json_path_final_key_is_quoted_for_numeric_strings",
     "feature_flags":["supports_json_field_contains"]}
}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(args,cwd=None,timeout=180,env=None):
    p=subprocess.run(args,cwd=cwd,encoding="utf8",errors="replace",
         stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout,env=env)
    return p
def must(args,cwd=None,timeout=180):
    p=run(args,cwd,timeout)
    if p.returncode!=0:raise RuntimeError("Command failed "+args[0]+": "+p.stdout[-1200:])
    return p.stdout
def model_paths(text):
    paths=[]
    for l in text.splitlines():
        if l.startswith("diff --git "):
            m=re.fullmatch(r"diff --git a/(.*?) b/(.*?)",l)
            if not m or m.group(1)!=m.group(2):raise ValueError("Nonstandard patch path")
            paths.append(m.group(2))
    if len(paths)!=len(set(paths)):raise ValueError("Duplicate diff paths")
    return sorted(paths)
def entry(task,sample):
    with (D/"STEP7_UNVERIFIED_TRIAGE_14.csv").open(encoding="utf8",newline="") as f:
        matched=[x for x in csv.DictReader(f) if x["instance_id"]==task and int(x["sample"])==sample]
    if len(matched)!=1:raise ValueError("Missing exact ledger record")
    return matched[0]
def source_rows(dataset,rev,split,pred):
    from datasets import load_dataset
    rows=[dict(x) for x in load_dataset(dataset,revision=rev,split=split) if pred(x)]
    if len(rows)!=1:raise ValueError("Expected one source, found "+str(len(rows)))
    return rows[0]
def location(task,sample):
    return ROOT/"scratch"/("step11-django-"+task.split("-")[-1]+"-sample"+str(sample))
def load(task,sample):
    if task not in ALLOWED or sample not in (1,2,3):raise ValueError("Not approved")
    return entry(task,sample)
def prepare(task,sample):
    row=load(task,sample)
    model=source_rows(AGENT,REV,"train",lambda x:x["instance_id"]==task and int(x["sample"])==sample and x.get("resolved") is True)
    tests=source_rows(ABS,TEST_REV,"test",lambda x:x["instance_id"]==task)
    if sha(model["patch"].encode())!=row["patch_sha256"]:raise ValueError("Model patch hash mismatch")
    dest=location(task,sample)
    if dest.exists():raise ValueError("Scratch dir already exists")
    dest.mkdir(parents=True)
    root=dest/"django";root.mkdir()
    must(["git","init","--quiet"],cwd=root)
    must(["git","remote","add","origin","https://github.com/django/django.git"],cwd=root)
    must(["git","fetch","--quiet","--depth","1","origin",tests["base_commit"]],cwd=root,timeout=300)
    must(["git","checkout","--quiet","--detach","FETCH_HEAD"],cwd=root)
    if must(["git","rev-parse","HEAD"],cwd=root).strip()!=tests["base_commit"]:
        raise ValueError("Pinned base commit mismatch")
    modfile=dest/"model.patch";modfile.write_bytes(model["patch"].encode())
    testfile=dest/"augmented-tests.patch";testfile.write_bytes(tests["test_patch"].encode())
    must(["git","apply","--check","--index","--binary",str(modfile)],cwd=root)
    must(["git","apply","--index","--binary",str(modfile)],cwd=root)
    changed=must(["git","diff","--cached","--name-only","HEAD"],cwd=root).splitlines()
    if sorted(changed)!=model_paths(model["patch"]):
        raise ValueError("Model diff paths mismatch")
    pre={x:sha((root/x).read_bytes()) if (root/x).exists() else None for x in changed}
    must(["git","apply","--check","--binary",str(testfile)],cwd=root)
    must(["git","apply","--binary",str(testfile)],cwd=root)
    post={x:sha((root/x).read_bytes()) if (root/x).exists() else None for x in changed}
    if pre!=post:raise ValueError("Enhanced test patch changed submitted model code")
    if sha(tests["test_patch"].encode())!=next(x["augmented_test_patch_sha256"]
          for x in json.loads((D/"STEP11_SEMANTIC_STRUCTURAL_CROSSWALK_v1.json").read_text())["rows"]
          if x["instance_id"]==task and x["sample"]==sample and x["case_type"]=="UNVERIFIED"):
        raise ValueError("Frozen enhanced test SHA not matched")
    cfg=root/"tests"/"test_step11_pg.py"
    cfg.write_text("""from test_sqlite import *\nDATABASES = {\n'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'postgres', 'USER': 'postgres', 'PASSWORD': 'postgres', 'HOST': '127.0.0.1', 'PORT': '5432'},\n'other': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'postgres', 'USER': 'postgres', 'PASSWORD': 'postgres', 'HOST': '127.0.0.1', 'PORT': '5432'},\n}\n""")
    output={"task":task,"sample":sample,"patch_sha256":row["patch_sha256"],
      "test_patch_sha256":sha(tests["test_patch"].encode()),
      "base_commit":tests["base_commit"],"model_files":len(pre),
      "model_files_hash_preserved_after_test_patch":len(post),
      "source_revision":REV,"test_revision":TEST_REV,
      "expected_method":ALLOWED[task]["method"],
      "status":"prepared_exact_original_model_and_test_patch_in_fresh_base",
      "runner_labels_modified":False}
    (dest/"manifest.json").write_text(json.dumps(output,sort_keys=True,indent=2)+"\n")
    print(json.dumps(output,sort_keys=True))
def execute(task,sample):
    row=load(task,sample)
    dest=location(task,sample)
    m=json.loads((dest/"manifest.json").read_text())
    root=dest/"django"
    osenv=os.environ.copy()
    osenv.update({"PYTHONPATH":str(root/"tests")+os.pathsep+str(root),
          "DJANGO_SETTINGS_MODULE":"test_step11_pg",
          "PYTHONDONTWRITEBYTECODE":"1"})
    feature=run([sys.executable,"-c",
       "import django; django.setup(); from django.db import connection; print('FEATURES',"+
       "{k: bool(getattr(connection.features,k,False)) for k in "+
       repr(ALLOWED[task]["feature_flags"])+ "})"],cwd=root,env=osenv,timeout=60)
    matches=re.findall(r"FEATURES (\{[^\n]+\})",feature.stdout)
    supported=bool(matches) and all(re.search(r"'"+f+r"': True",matches[-1]) for f in ALLOWED[task]["feature_flags"])
    target=ALLOWED[task]["method"]
    cmd=[sys.executable,"tests/runtests.py",target,"--settings=test_step11_pg","--verbosity=2","--noinput"]
    begin=time.monotonic()
    try:
        test=run(cmd,cwd=root,env=osenv,timeout=540)
        exit_code=test.returncode
        output=test.stdout
        timed_out=False
    except subprocess.TimeoutExpired as e:
        exit_code=124
        output=str(e.stdout or "")[-2000:]
        timed_out=True
    duration=round(time.monotonic()-begin,2)
    # Only bounded public assertion/status metadata, no credential or full source/log.
    lines=output.splitlines()
    detail=[x.strip()[:300] for x in lines if
       re.search(r"(^test_.*\.\.\. (?:ok|skipped|FAIL|ERROR)|^Ran \d+ tests?|^FAILED \(|^OK$|^System check|^Creating test database|^Destroying test database|^ERROR:|^FAIL:)",x)]
    status="INCOMPLETE_SETUP_OR_ENVIRONMENT"
    if (supported and exit_code==0 and any(re.search(r"^Ran 1 test",x) for x in lines) and
            any(re.search(r"\.\.\. ok\s*$",x) for x in lines)):
        status="TARGETED_TEST_PASSED_ON_POSTGRES"
    elif (supported and exit_code!=0 and
            any(re.search(r"^Ran 1 test",x) for x in lines)):
        status="TARGETED_TEST_FAILED_ON_POSTGRES"
    elif any("skipped" in x.lower() for x in detail):
        status="TARGET_SKIPPED_OR_INCOMPLETE"
    elif exit_code==0:
        status="AMBIGUOUS_ZERO_EXIT"
    preexisting=json.loads((dest/"manifest.json").read_text())
    full={
       **preexisting,
       "new_runtime":"direct upstream Django unittest PostgreSQL service, NOT SWE-ABS Docker harness",
       "python_version":sys.version.split()[0],
       "backend_features_sufficient":supported,
       "backend_probe_exit_code":feature.returncode,
       "backend_probe_features_observed":matches[-1] if matches else None,
       "method_label":target,
       "target_execution_exit_code":exit_code,
       "target_execution_status":status,
       "timed_out":timed_out,
       "wall_seconds":duration,
       "bounded_test_status_lines":detail[-28:],
       "bounded_output_tail_for_setup_diagnostics":output[-900:] if status=="INCOMPLETE_SETUP_OR_ENVIRONMENT" else "",
       "historical_sweabs_outcome_remains":"UNVERIFIED",
       "no_original_labels_changed":True,
       "limitation":"New targeted PostgreSQL result is conditional on this environment and exact reconstruction; it is not a full suite, nor necessarily the original SWE-ABS Docker runtime. Test correctness needs source-aligned semantic review."
    }
    if full["patch_sha256"]!=row["patch_sha256"]:raise ValueError("Ledger drift")
    destination=ROOT/"scratch"/("STEP11_PG_"+task.split("-")[-1]+"_s"+str(sample)+".json")
    destination.write_text(json.dumps(full,indent=2,sort_keys=True)+"\n")
    print("STEP11_CONTROLLED_JSON_BEGIN")
    print(json.dumps(full,sort_keys=True))
    print("STEP11_CONTROLLED_JSON_END")
    # Do not treat actual failing agent test as a GitHub workflow infrastructure failure.
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("command",choices=["prepare","execute"])
    ap.add_argument("--task",choices=sorted(ALLOWED),required=True)
    ap.add_argument("--sample",type=int,choices=[1,2,3],required=True)
    args=ap.parse_args()
    if args.command=="prepare":prepare(args.task,args.sample)
    else:execute(args.task,args.sample)
if __name__=="__main__":main()
