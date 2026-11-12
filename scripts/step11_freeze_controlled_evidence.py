#!/usr/bin/env python3
"""Step 11 final evidence aggregation: no new tests and NO outcome relabel.

Reconciles all new limited controlled source/test executions against frozen
Step7 run identities and categorizes ambiguity honestly. Source-specific
compatibility flags are not used in place of actual unittest pass/skip output.
Usage: python scripts/step11_freeze_controlled_evidence.py [--check]
"""
from __future__ import annotations
import argparse,csv,json,re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"results/2026-11-12"
OUT=D/"STEP11_CONTROLLED_EVIDENCE_FREEZE_v1.json"
def load(p):return json.loads((D/p).read_text(encoding="utf8"))
def ledgers():
    with (D/"STEP7_UNVERIFIED_TRIAGE_14.csv").open(encoding="utf8",newline="") as f:
        records=list(csv.DictReader(f))
    if len(records)!=14:raise ValueError("Step7 triage must have 14 original rows")
    return {(r["instance_id"],int(r["sample"])):r for r in records}
def lookup(originals,task,sample,record,source_key="patch_sha256"):
    key=(task,sample)
    if key not in originals:raise ValueError("Missing frozen source ID "+str(key))
    if record[source_key]!=originals[key]["patch_sha256"]:
        raise ValueError("Exact original model patch SHA mismatch "+str(key))
def unittest_clean(record,count):
    lines=record["bounded_test_status_lines"]
    seen=[l for l in lines if re.search(r"^test_.*\.\.\. ok$",l)]
    ran=any(re.search(r"^Ran "+str(count)+r" tests? in ",l) for l in lines)
    ok="OK" in lines
    return record["target_execution_exit_code"]==0 and ran and ok and not record.get("observed_unittest_reported_skips",False),len(seen)
def summarize():
    original=ledgers()
    requests=load("STEP11_REQUESTS_FULL_PATCH_RECONSTRUCTION_v1.json")
    lookup(original,"psf__requests-1142",1,requests["new_reconstruction"],source_key="model_patch_sha256")
    rc=requests["new_reconstruction"]
    if rc["model_patch_changed_file_paths"]!=74 or rc["generated_build_file_paths"]!=65 or not rc["line_multiset_verified"] or rc["model_file_hashes_preserved_after_augmented_patch"]!=74:
        raise ValueError("Requests complete reconstruction invariants fail")
    merged=load("STEP11_COLLISION_MERGE_PROBES_v1.json")
    if merged["cases"]!=4 or merged["cases_with_3way_merge_application"]!=4 or merged["cases_with_unresolved_conflict"]!=0:
        raise ValueError("Four collision reconstructions not all successful")
    collision=[]
    for sample in (1,2,3):
        d=load(f"STEP11_SYMPY23413_MERGED_TEST_s{sample}_v1.json")
        lookup(original,"sympy__sympy-23413",sample,d)
        t=d.get("bounded_error_tail","")
        m=re.search(r"(\d+) failed, (\d+) passed in",t)
        good=re.search(r"(\d+) passed in",t)
        failed,passed=(int(m[1]),int(m[2])) if m else ((0,int(good[1])) if good else (None,None))
        if (failed,passed)!=({1:(1,7),2:(0,8),3:(1,7)}[sample]):
            raise ValueError("Sympy tested results mismatch "+str(sample))
        collision.append({"task":"sympy__sympy-23413","sample":sample,
          "new_model_preserving_merged_suite_passed":passed,
          "new_model_preserving_merged_suite_failed":failed,
          "test_failure_exception":"IndexError" if failed else None,
          "historical_runner_modified":False})
    dj=load("STEP11_DJANGO11206_MERGED_TEST_s3_v3.json")
    lookup(original,"django__django-11206",3,dj)
    if dj["execution_exit_code"]!=1 or "Ran 12 tests in 0.003s" not in dj["bounded_result_lines"] or "FAILED (failures=5)" not in dj["bounded_result_lines"]:
        raise ValueError("Django11206 serial test proof missing")
    collision.append({"task":"django__django-11206","sample":3,
      "new_model_preserving_merged_suite_total":12,
      "new_model_preserving_merged_suite_failed":5,
      "failure_semantic_status":"unresolved_negative_zero_formatting_requirement",
      "historical_runner_modified":False})
    js=load("STEP11_DJANGO15503_ORACLE_COLLECTION_v1.json")
    if not js["method_in_unittest_testloader_get_test_case_names"] or js["unittest_test_loader_class_method_count"]!=10 or js["unittest_test_loader_module_cases"]!=10:
        raise ValueError("Oracle method loader collection not verified")
    backend=[]
    for sample in (1,2,3):
        idx=load(f"STEP11_DJANGO12039_PG_MODULE_s{sample}_v1.json")
        lookup(original,"django__django-12039",sample,idx)
        clean,observed=unittest_clean(idx,13)
        if not clean or observed!=13:raise ValueError("Index 13-case Postgres execution not complete "+str(sample))
        # A legacy feature probe can be false even when the actual 13 vendor-
        # specific tests executed and passed. Never replace observed test status.
        backend.append({"task":"django__django-12039","sample":sample,"target":"full_new_augmented_index_module",
            "targeted_tests_passed":13,"targeted_tests_failed":0,"targeted_tests_skipped":0,
            "new_backend":"PostgreSQL 15","probe_feature_flag_irrelevant":"supports_expression_indexes",
            "source_automated_status":idx["target_execution_status"],
            "verified_from_unittest_summary":True})
        jsons=load(f"STEP11_DJANGO15503_PG_FULL_MODULE_s{sample}_v1.json")
        lookup(original,"django__django-15503",sample,jsons)
        clean,n=unittest_clean(jsons,10)
        # One Oracle method's verbose line can be merged with other output;
        # the independent collection manifest is the source of its test ID.
        if not clean or n<9:raise ValueError("JSON full module execution missing "+str(sample))
        direct=load(f"STEP11_DJANGO15503_ORACLE_PG_TARGETED_s{sample}_v1.json")
        lookup(original,"django__django-15503",sample,direct)
        if direct["target_execution_status"]!="TARGETED_TEST_PASSED_ON_POSTGRES":
            raise ValueError("Oracle direct execution not PASS")
        backend.append({"task":"django__django-15503","sample":sample,
           "target":"full_augmented_numeric_json_module",
           "targeted_tests_passed":10,"targeted_tests_failed":0,"targeted_tests_skipped":0,
           "oracle_method_in_independent_unittest_collection":True,
           "oracle_method_independently_passed_when_explicitly_targeted":True,
           "new_backend":"PostgreSQL 15","verified_from_unittest_summary":True})
        dj1=load(f"STEP11_DJANGO14434_PG_TARGETED_s{sample}_v1.json")
        lookup(original,"django__django-14434",sample,dj1)
        if dj1["target_execution_status"]!="TARGETED_TEST_PASSED_ON_POSTGRES":
            raise ValueError("Originally skipped covering-index test not exercised")
        djfull=load(f"STEP11_DJANGO14434_PG_FULL_MODULE_s{sample}_v1.json")
        lookup(original,"django__django-14434",sample,djfull)
        if djfull["target_execution_exit_code"]!=0 or djfull["observed_unittest_total"]!=168 or not djfull["observed_unittest_reported_skips"]:
            raise ValueError("Django schema module expected other backend-specific skips")
        backend.append({"task":"django__django-14434","sample":sample,
           "target":"formerly_skipped_enhanced_covering_index_method",
           "targeted_tests_passed":1,"targeted_tests_failed":0,"targeted_tests_skipped":0,
           "new_backend":"PostgreSQL 15",
           "other_full_schema_module_tests_ran":168,
           "other_full_schema_module_contains_skips":True,
           "original_sqlite_modified_method_results":"8 modified OK, 1 modified skipped; one new test OK",
           "new_postgres_formerly_skipped_modified_method":"PASS",
           "verified_from_unittest_summary":True})
    result={
       "decision_scope":"new bounded controlled execution evidence for exact original model patches; no independent gold semantic oracle",
       "original_v2_outcomes_unchanged":{"PASS":153,"FAIL":31,"UNVERIFIED":14},
       "step7_primary_outcomes_unchanged":{"runner_pass":153,"documentary_supported_fail":9,"excluded":36},
       "original_unverified_cases":14,
       "unique_unverified_tasks":6,
       "new_backend_evidence_rows":len(backend),
       "new_backend_task_categories":{"django_12039":3,"django_14434":3,"django_15503":3},
       "all_9_backend_case_families_have_new_execution":True,
       "requests_full_patch_reconstruction":{
           "whole_changed_file_count":74,
           "generated_build_files":65,
           "exact_line_diff_match":True,
           "all_model_file_hashes_survived_test_patch":True,
           "historical_original_docker_tree_verified":False},
       "all_four_collision_source_patches_merge_non_destructively":True,
       "collision_new_execution":collision,
       "backend_new_execution":backend,
       "collection_runtime_check":{"oracle_name":js["expected_method"],
           "unittest_module_cases":10,"oracle_in_loader":True},
       "new_execution_is_original_sweabs_docker_run":False,
       "semantic_human_oracle_complete":False,
       "semantic_adjudication_remaining":{"unresolved_fail_runs":16,"environment_sensitive_fail_runs":2,
           "invalid_enhanced_test_fail_runs":4},
       "runner_outcome_relabeling_done":False,
       "methodology_outcome_freeze_unchanged":True,
       "limitations":"New PostgreSQL and direct merged tests do not reproduce the historical SWE-ABS Docker image or guarantee full semantic correctness of every strengthened assertion. Primary reviewed FAIL labels remain documentary, not gold. All 14 original UNVERIFIED remain preserved; results may support new versioned secondary observational evidence but are not posthoc appended to frozen primary."}
    return result
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    obj=summarize()
    if args.check:
        if json.loads(OUT.read_text(encoding="utf8"))!=obj:raise ValueError("Frozen controlled evidence differs")
    else:
        OUT.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"controlled_backend_runs":len(obj["backend_new_execution"]),
       "collision_test_runs":len(obj["collision_new_execution"]),
       "original_labels_unchanged":obj["runner_outcome_relabeling_done"] is False},indent=2))
if __name__=="__main__":main()
