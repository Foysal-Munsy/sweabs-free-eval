import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import sys

from scripts.pilot import (
    build_prediction, changed_lines, collect_result, generate_plan, pretest_diff,
    resolved_rows, sha256, build_test_record, merge_results,
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
        src = '''GIT_APPLY_CMDS = [
    "git apply --verbose",
    "patch --batch -p1 -i",
]
def run():
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
        compile(patched, "patched.py", "exec")

    def test_pinned_augmented_test_record(self):
        fake = SimpleNamespace(load_dataset=lambda *a, **k: [
            {"instance_id": "repo__repo-1", "test_patch": PATCH, "extra": "ok"}])
        with patch.dict(sys.modules, {"datasets": fake}):
            record, manifest = build_test_record("d" * 40, "repo__repo-1")
        self.assertEqual(len(record), 1)
        self.assertEqual(manifest["test_patch_sha256"], sha256(PATCH))
        self.assertEqual(manifest["test_dataset_revision"], "d" * 40)

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
        self.folder = self.root / "pilot_101" / "openhands-gemini3-flash-sample-1" / self.instance
        self.folder.mkdir(parents=True)
        (self.folder / "patch.diff").write_text(PATCH, encoding="utf-8")
        (self.folder / "run_instance.log").write_text(DIFF_LOG, encoding="utf-8")
        (self.folder / "test_output.txt").write_text("PASSED test_x\n", encoding="utf-8")
        self.meta = {"instance_id": self.instance, "sample": 1, "patch_sha256": sha256(PATCH),
                     "dataset_revision": "a" * 40}

    def run_with_report(self, resolved, failures=None):
        (self.folder / "report.json").write_text(json.dumps({self.instance: {
            "patch_successfully_applied": True, "resolved": resolved,
            "tests_status": {"FAIL_TO_PASS": {"success": ["x"], "failure": failures or []},
                             "PASS_TO_PASS": {"success": [], "failure": []}},
        }}), encoding="utf-8")
        return collect_result(self.meta, self.root, "pilot_101")

    def test_pass_requires_validated_patch_and_report(self):
        r = self.run_with_report(True)
        self.assertEqual(r["outcome"], "PASS")
        self.assertEqual(r["patch_diff_check"], "CHANGE_LINES_MATCH")

    def test_fail_requires_explicit_failed_tests(self):
        self.assertEqual(self.run_with_report(False, ["x"])["outcome"], "FAIL")
        self.assertEqual(self.run_with_report(False)["outcome"], "UNVERIFIED")

    def test_missing_report_is_unverified(self):
        r = collect_result(self.meta, self.root, "pilot_101")
        self.assertEqual(r["outcome"], "UNVERIFIED")

    def test_mismatched_patch_is_unverified_even_if_report_passed(self):
        self.run_with_report(True)
        (self.folder / "run_instance.log").write_text(DIFF_LOG.replace("+new", "+wrong"), encoding="utf-8")
        r = collect_result(self.meta, self.root, "pilot_101")
        self.assertEqual(r["outcome"], "UNVERIFIED")
        self.assertEqual(r["patch_diff_check"], "MISMATCH")

    def test_patched_harness_patch_diff_tamper_detected(self):
        self.run_with_report(True)
        (self.folder / "patch.diff").write_text(PATCH + "more", encoding="utf-8")
        self.assertEqual(collect_result(self.meta, self.root, "pilot_101")["outcome"], "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
