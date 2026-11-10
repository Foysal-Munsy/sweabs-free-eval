import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import sys

from scripts.pilot import (
    build_prediction, changed_lines, collect_result, generate_plan, pretest_diff,
    resolved_rows, sha256, build_test_record, merge_results, parse_augmented_pytest, parse_augmented_django, parse_augmented_suite,
)
from scripts.patch_harness import patch_source

PATCH = '''diff --git a/foo.py b/foo.py
index 1234567..2345678 100644
--- a/foo.py
+++ b/foo.py
@@ -1 +1 @@
-old
+new
'''
DIFF_LOG = '2026-11-09 12:00 INFO Git diff before:\n' + PATCH + '\n2026-11-09 12:01 INFO Eval script for task-1 written to ...\n'


class DataTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"instance_id": "repo__repo-2", "sample": 1, "resolved": True, "patch": PATCH},
            {"instance_id": "repo__repo-1", "sample": 1, "resolved": True, "patch": PATCH},
            {"instance_id": "repo__repo-3", "sample": 1, "resolved": False, "patch": PATCH},
            {"instance_id": "repo__repo-1", "sample": 2, "resolved": True, "patch": PATCH},
        ]

    def test_plan_sorts_selects_preserves_samples(self):
        plan = generate_plan(self.rows, "a"*40, 1, 0, 2)
        self.assertEqual([x["instance_id"] for x in plan["matrix"]["include"]], ["repo__repo-1", "repo__repo-2"])
        self.assertEqual(len(resolved_rows(self.rows, 2)), 1)
        self.assertEqual(plan["matrix"]["include"][0]["patch_sha256"], sha256(PATCH))

    def test_invalid_ranges_and_duplicates_rejected(self):
        with self.assertRaises(ValueError):
            generate_plan(self.rows, "a"*40, 1, 0, 11)
        with self.assertRaises(ValueError):
            generate_plan(self.rows, "a"*40, 1, 1, 2)
        with self.assertRaises(ValueError):
            resolved_rows(self.rows + [self.rows[0]], 1)

    def test_exact_revision_prediction_hash(self):
        prediction, manifest = build_prediction(self.rows, "a"*40, 1, "repo__repo-1", sha256(PATCH))
        self.assertEqual(prediction["model_patch"], PATCH)
        self.assertTrue(manifest["original_resolved"])
        with self.assertRaises(ValueError):
            build_prediction(self.rows, "a"*40, 1, "repo__repo-1", "b"*64)


class PatchTests(unittest.TestCase):
    def test_change_signature(self):
        self.assertEqual(changed_lines(PATCH), changed_lines(PATCH.replace("index 1234567..2345678", "index abc..def")))
        self.assertNotEqual(changed_lines(PATCH), changed_lines(PATCH.replace("+new", "+different")))
        self.assertIsNone(changed_lines('diff --git a/old.py b/new.py\n@@ -1 +1 @@\n-a\n+b'))
        self.assertEqual(changed_lines(pretest_diff(DIFF_LOG)), changed_lines(PATCH))

    def test_preserved_smoke_harness_backport_compiles(self):
        src = '''import json
GIT_APPLY_CMDS = [
    "git apply --verbose",
    "patch --batch -p1 -i",
]
def run():
    if True:
        container.start()
    applied_patch = False
    for git_apply_cmd in GIT_APPLY_CMDS:
        pass
    if not applied_patch:
        raise ValueError("bad")
    before = "git -c core.fileMode=false diff"
    after = "git -c core.fileMode=false diff"
'''
        patched = patch_source(src)
        self.assertIn("git apply --check --reverse", patched)
        self.assertIn("git checkout -- . ; git clean -fd", patched)
        self.assertIn("PREPATCH_BASE_COMMIT_VERIFIED", patched)
        self.assertIn("git checkout --force {base_commit}", patched)
        compile(patched, "patched.py", "exec")

    def test_pinned_augmented_test_record(self):
        fake = SimpleNamespace(load_dataset=lambda *a, **k: [
            {"instance_id": "repo__repo-1", "test_patch": PATCH,
             "base_commit": "c" * 40, "extra": "ok"}])
        with patch.dict(sys.modules, {"datasets": fake}):
            record, manifest = build_test_record("d" * 40, "repo__repo-1")
        self.assertEqual(len(record), 1)
        self.assertEqual(manifest["test_patch_sha256"], sha256(PATCH))
        self.assertEqual(manifest["test_dataset_revision"], "d" * 40)
        self.assertEqual(manifest["base_commit"], "c" * 40)

    def test_top_level_django_test_patch_paths_are_detected(self):
        diff = """diff --git a/tests/utils_tests/test_numberformat.py b/tests/utils_tests/test_numberformat.py
@@ -1 +1 @@
-old
+new
"""
        fake = SimpleNamespace(load_dataset=lambda *a, **k: [
            {"instance_id": "repo__repo-1", "test_patch": diff,
             "base_commit": "c" * 40, "extra": "ok"}])
        with patch.dict(sys.modules, {"datasets": fake}):
            _, manifest = build_test_record("d" * 40, "repo__repo-1")
        self.assertEqual(manifest["augmented_test_files"], ["tests/utils_tests/test_numberformat.py"])

    def test_base_commit_with_test_paths_is_accepted(self):
        import re
        expr = r"(?m)^git checkout ([0-9a-f]{40})(?=[ \t]|$)"
        script = f"git checkout {'a' * 40} tests/t1.py tests/t2.py\ngit checkout {'a' * 40} tests/t1.py tests/t2.py"
        self.assertEqual(set(re.findall(expr, script)), {'a'*40})

    def test_merge_keeps_sample_run_identity(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            for n in (1, 2):
                target = folder / str(n)
                target.mkdir()
                (target / "result.json").write_text(json.dumps({
                    "sample": n, "instance_id": "repo__repo-1", "outcome": "UNVERIFIED",
                    "reason": "test", "patch_sha256": sha256(PATCH)}))
            merge_results(folder, folder / "out.csv")
            self.assertIn("2", (folder / "pilot_summary.json").read_text())
            self.assertEqual(len((folder / "out.csv").read_text().splitlines()), 3)


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.instance = "repo__repo-1"
        self.base = "c" * 40
        self.folder = self.root / "pilot_101" / "openhands-gemini3-flash-sample-1" / self.instance
        self.folder.mkdir(parents=True)
        (self.folder / "patch.diff").write_text(PATCH, encoding="utf-8")
        (self.folder / "run_instance.log").write_text(
            "PREPATCH_BASE_COMMIT_VERIFIED: " + self.base + "\n" + DIFF_LOG,
            encoding="utf-8")
        self.pass_output = """Applied patch foo/tests/test_new.py cleanly.
+ : '>>>>> Start Test Output'
+ pytest -rA foo/tests/test_new.py
collected 1 item
==================== 1 passed in 0.02s ====================
+ : '>>>>> End Test Output'
"""
        (self.folder / "test_output.txt").write_text(self.pass_output)
        self.meta = {"instance_id": self.instance, "sample": 1, "patch_sha256": sha256(PATCH),
                     "dataset_revision": "a" * 40, "base_commit": self.base,
                     "augmented_test_files": ["foo/tests/test_new.py"]}

    def report(self, standard_resolved=False):
        (self.folder / "report.json").write_text(json.dumps({self.instance: {
            "patch_successfully_applied": True, "resolved": standard_resolved,
            "tests_status": {"FAIL_TO_PASS": {"success": [], "failure": ["old_test"]}},
        }}), encoding="utf-8")
        return collect_result(self.meta, self.root, "pilot_101")

    def test_pass_uses_augmented_test_and_checked_patch_even_if_standard_unresolved(self):
        r = self.report(standard_resolved=False)
        self.assertEqual(r["outcome"], "PASS")
        self.assertEqual(r["patch_diff_check"], "REPOSITORY_CHANGE_LINES_MATCH")
        self.assertFalse(r["harness_report_resolved"])

    def test_fail_requires_augmented_test_failure_even_if_standard_report_is_resolved(self):
        (self.folder / "test_output.txt").write_text(self.pass_output.replace(
            "1 passed in 0.02s", "1 failed in 0.02s"))
        self.assertEqual(self.report(standard_resolved=True)["outcome"], "FAIL")

    def test_checkout_conflict_invalidates_pass(self):
        (self.folder / "test_output.txt").write_text(self.pass_output +
             "error: Your local changes would be overwritten by checkout\nAborting\n")
        r = self.report()
        self.assertEqual(r["outcome"], "UNVERIFIED")
        self.assertEqual(r["reason"], "checkout_failed_during_augmented_evaluation")

    def test_missing_base_commit_invalidates_pass(self):
        (self.folder / "run_instance.log").write_text(DIFF_LOG)
        self.assertEqual(self.report()["reason"], "prepatch_base_commit_not_verified")

    def test_missing_report_is_unverified(self):
        self.assertEqual(collect_result(self.meta, self.root, "pilot_101")["outcome"], "UNVERIFIED")

    def test_mismatched_patch_is_unverified_even_if_report_passed(self):
        (self.folder / "run_instance.log").write_text(
            ("PREPATCH_BASE_COMMIT_VERIFIED: " + self.base + "\n" + DIFF_LOG).replace(
                "+new", "+wrong"))
        r = self.report(True)
        self.assertEqual(r["outcome"], "UNVERIFIED")
        self.assertEqual(r["patch_diff_check"], "MISMATCH")

    def test_patch_hash_tamper_detected(self):
        self.report()
        (self.folder / "patch.diff").write_text(PATCH + "more", encoding="utf-8")
        self.assertEqual(self.report()["outcome"], "UNVERIFIED")

    def test_runtime_trace_paths_do_not_affect_repository_code_comparison(self):
        model = PATCH + '''diff --git a/workspace/bash_events/foo b/workspace/bash_events/foo
new file mode 100644
--- /dev/null
+++ b/workspace/bash_events/foo
@@ -0,0 +1 @@
+log
'''
        self.assertEqual(changed_lines(model), changed_lines(PATCH))
        self.assertIsNone(changed_lines("diff --git a/foo b/foo\nold mode 100644\nnew mode 100755\n"))

    def test_django_unittest_success_and_failure(self):
        output = """Applied patch tests/utils_tests/test_http_example.py cleanly.
+ : '>>>>> Start Test Output'
+ ./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_http_example
test_one (utils_tests.test_http_example.ExampleTests) ... ok
test_two (utils_tests.test_http_example.ExampleTests) ... ok
----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK
+ : '>>>>> End Test Output'
"""
        expected = ["tests/utils_tests/test_http_example.py"]
        status, info = parse_augmented_django(output, expected)
        self.assertEqual(status, "PASS")
        self.assertEqual(info["augmented_collected"], 2)
        self.assertEqual(parse_augmented_suite(output, expected)[0], "PASS")
        failure = output.replace("test_two (utils_tests.test_http_example.ExampleTests) ... ok",
                                 "test_two (utils_tests.test_http_example.ExampleTests) ... FAIL")
        failure = failure.replace("\nOK\n", "\nFAILED (failures=1)\n")
        status, info = parse_augmented_django(failure, expected)
        self.assertEqual(status, "FAIL")
        self.assertEqual(info["augmented_passed"], 1)
        self.assertEqual(info["augmented_failed"], 1)
        self.assertIsNone(parse_augmented_django(output, ["tests/other/test_other.py"])[0])

    def test_django_error_requires_review(self):
        output = """Applied patch tests/utils_tests/test_example.py cleanly.
+ : '>>>>> Start Test Output'
+ ./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_example
Ran 2 tests in 0.002s
FAILED (errors=1)
+ : '>>>>> End Test Output'
"""
        result, details = parse_augmented_django(output, ["tests/utils_tests/test_example.py"])
        self.assertIsNone(result)
        self.assertEqual(details["reason"], "augmented_django_test_errors_require_review")

    def test_augmented_test_patch_application_is_required(self):
        (self.folder / "test_output.txt").write_text(
            self.pass_output.replace("Applied patch foo/tests/test_new.py cleanly.", ""))
        r = self.report()
        self.assertEqual(r["outcome"], "UNVERIFIED")
        self.assertEqual(r["reason"], "augmented_test_patch_application_not_proven")

    def test_pytest_parser_aborts_on_incomplete_or_wrong_target(self):
        good, detail = parse_augmented_pytest(self.pass_output, ["foo/tests/test_new.py"])
        self.assertEqual(good, "PASS")
        self.assertEqual(detail["augmented_collected"], 1)
        self.assertIsNone(parse_augmented_pytest(self.pass_output, ["other/test.py"])[0])
        self.assertIsNone(parse_augmented_pytest(self.pass_output.replace("1 passed", "1 skipped"),
                                                  ["foo/tests/test_new.py"])[0])


if __name__ == "__main__":
    unittest.main()
