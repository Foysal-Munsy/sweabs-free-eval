#!/usr/bin/env python3
"""Step 11: collect exact Django-15503 module test IDs without executing tests.

Run AFTER step11_django_backend_probe.prepare on sample1, with Python3.9 and
the pinned source installed editable. Distinguish artifact verbose-formatting
absence from actual unittest collection omission, with no label relabeling.
"""
from __future__ import annotations
import argparse,ast,hashlib,importlib,json,os,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TASK="django__django-15503"
CLASS="JSONFieldNumericKeyLookupsTests"
METHOD="test_oracle_json_path_final_key_is_quoted_for_numeric_strings"
MOD="model_fields.test_jsonfield_numeric_keys"
def flatten(suite):
    for case in suite:
        if isinstance(case,unittest.TestSuite):
            yield from flatten(case)
        else:yield case.id()
def main():
    pa=argparse.ArgumentParser();pa.add_argument("--sample",type=int,default=1)
    args=pa.parse_args()
    root=ROOT/"scratch"/("step11-django-15503-sample"+str(args.sample))/"django"
    path=root/"tests"/"model_fields"/"test_jsonfield_numeric_keys.py"
    source=path.read_bytes()
    tree=ast.parse(source.decode("utf8"),filename=str(path))
    nodes=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==CLASS]
    if len(nodes)!=1:raise ValueError("Expected exactly one source class")
    methods=[n.name for n in nodes[0].body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    if METHOD not in methods:raise ValueError("Pinned merged source lacks target Oracle method")
    sys.path.insert(0,str(root/"tests"));sys.path.insert(0,str(root))
    os.environ["DJANGO_SETTINGS_MODULE"]="test_sqlite"
    import django
    from django.conf import settings
    # The stock test_sqlite example has no INSTALLED_APPS; the regular
    # runtests.py setup() would populate these before importing test models.
    settings.INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "model_fields"]
    django.setup()
    mod=importlib.import_module(MOD)
    cls=getattr(mod,CLASS)
    loader=unittest.TestLoader()
    classnames=loader.getTestCaseNames(cls)
    module_suite=loader.loadTestsFromModule(mod)
    ids=list(flatten(module_suite))
    hits=[x for x in ids if x.endswith(CLASS+"."+METHOD)]
    result={
      "task":TASK,"sample":args.sample,
      "patched_file":"tests/model_fields/test_jsonfield_numeric_keys.py",
      "patched_source_sha256":hashlib.sha256(source).hexdigest(),
      "expected_method":METHOD,"class":CLASS,
      "method_present_in_pinned_patched_ast":METHOD in methods,
      "method_function_definitions_in_ast":methods.count(METHOD),
      "method_present_in_runtime_class":callable(getattr(cls,METHOD,None)),
      "method_in_unittest_testloader_get_test_case_names":METHOD in classnames,
      "unittest_test_loader_class_method_count":len(classnames),
      "unittest_test_loader_module_cases":len(ids),
      "unittest_test_loader_target_case_ids":hits,
      "all_class_test_method_names":classnames,
      "test_methods_actually_executed":False,
      "original_runner_relabelled":False,
      "limitation":"Python unittest.TestLoader collection from pinned patched module is not identical proof of SWE-ABS/Django DiscoverRunner execution. Compare with controlled full-module run and original verbose logs."
    }
    print("STEP11_COLLECTION_RESULT_BEGIN")
    print(json.dumps(result,sort_keys=True))
    print("STEP11_COLLECTION_RESULT_END")
if __name__=="__main__":main()
