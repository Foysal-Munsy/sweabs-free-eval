#!/usr/bin/env python3
"""Generate a reproducible SWE-ABS evaluation pilot and conservatively collect labels.

Uses the same trajectory source as the repository's smoke test. External
packages (datasets/huggingface_hub) are imported only by prepare commands,
so result collection and local tests work offline with the standard library.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

DATASET_ID = "tarsur385/swe-verified-gemini3-flash-trajectories"
SPLIT = "train"
TEST_DATASET_ID = "OpenAgentLab/SWE-Bench_Verified_ABS"
SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")


def sha256(data: str | bytes) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def load_rows(revision: str) -> list[dict[str, Any]]:
    from datasets import load_dataset
    return list(load_dataset(DATASET_ID, split=SPLIT, revision=revision))


def resolved_rows(rows: list[dict[str, Any]], sample: int) -> list[dict[str, Any]]:
    selected = [r for r in rows if r.get("sample") == sample and r.get("resolved") is True]
    for r in selected:
        ident = r.get("instance_id")
        if not isinstance(ident, str) or not SAFE_ID.fullmatch(ident):
            raise ValueError(f"Invalid instance_id in sample {sample}: {ident!r}")
        if not isinstance(r.get("patch"), str) or not r["patch"].strip():
            raise ValueError(f"Missing submitted patch for {ident!r}")
    counts = Counter(r["instance_id"] for r in selected)
    duplicates = [x for x, n in counts.items() if n > 1]
    if duplicates:
        raise ValueError(f"Sample {sample} contains duplicate instance IDs: {duplicates[:5]}")
    return sorted(selected, key=lambda r: r["instance_id"])


def generate_plan(rows: list[dict[str, Any]], revision: str, sample: int, offset: int, count: int,
                  test_revision: str = "UNVERIFIED") -> dict[str, Any]:
    if sample not in (1, 2, 3) or offset < 0 or not 1 <= count <= 10:
        raise ValueError("Require sample=1..3, offset>=0 and count=1..10")
    selected = resolved_rows(rows, sample)
    window = selected[offset: offset + count]
    if len(window) != count:
        raise ValueError(f"Requested {count} rows at offset {offset}, but sample has {len(selected)}")
    include = [
        {"instance_id": r["instance_id"], "sample": sample, "index": offset + i,
         "patch_sha256": sha256(r["patch"])}
        for i, r in enumerate(window)
    ]
    return {"dataset": DATASET_ID, "split": SPLIT, "dataset_revision": revision,
            "test_dataset": TEST_DATASET_ID, "test_dataset_revision": test_revision,
            "sample": sample, "total_originally_resolved_in_sample": len(selected),
            "selection_order": "lexical_instance_id", "offset": offset, "count": count,
            "matrix": {"include": include}}


def build_prediction(rows: list[dict[str, Any]], revision: str, sample: int,
                     instance_id: str, expected_hash: str) -> tuple[dict[str, Any], dict[str, Any]]:
    selected = [r for r in resolved_rows(rows, sample) if r["instance_id"] == instance_id]
    if len(selected) != 1:
        raise ValueError(f"Expected exactly one original PASS run for {sample}/{instance_id}; found {len(selected)}")
    patch = selected[0]["patch"]
    got_hash = sha256(patch)
    if got_hash != expected_hash:
        raise ValueError("Patch SHA-256 mismatch between plan and fetched revision")
    model = f"openhands-gemini3-flash-sample-{sample}"
    prediction = {"instance_id": instance_id, "model_name_or_path": model, "model_patch": patch}
    manifest = {"dataset": DATASET_ID, "split": SPLIT, "dataset_revision": revision,
                "instance_id": instance_id, "sample": sample, "model_name_or_path": model,
                "original_resolved": True, "patch_sha256": got_hash,
                "patch_bytes": len(patch.encode("utf-8")),
                "sweabs_commit": os.environ.get("SWE_ABS_SHA", "UNVERIFIED")}
    return prediction, manifest


def build_test_record(revision: str, instance_id: str) -> tuple[list[dict[str, Any]], dict[str, str]]:
    from datasets import load_dataset
    rows = load_dataset(TEST_DATASET_ID, split="test", revision=revision)
    selected = [r for r in rows if r.get("instance_id") == instance_id]
    if len(selected) != 1:
        raise ValueError(f"Expected one SWE-ABS task for {instance_id}; found {len(selected)}")
    row = dict(selected[0])
    if not isinstance(row.get("test_patch"), str) or not row["test_patch"].strip():
        raise ValueError(f"No augmented SWE-ABS test patch for {instance_id}")
    target_paths = sorted({m.group(1) for m in re.finditer(
        r"(?m)^diff --git a/[^\n]+ b/([^\n]+)$", row["test_patch"])
        if "/tests/" in m.group(1) and Path(m.group(1)).name.startswith("test_")})
    return [row], {"test_dataset": TEST_DATASET_ID, "test_dataset_revision": revision,
                   "test_patch_sha256": sha256(row["test_patch"]),
                   "base_commit": row["base_commit"],
                   "augmented_test_files": target_paths}


def changed_lines(text: str) -> Counter[tuple[str, str, str]] | None:
    """Conservatively match repository-file code edits, not agent runtime traces.

    Paths under workspace/bash_events and workspace/conversations are local
    agent trace artifacts shipped in the supplied prediction diff. They are
    not source-code changes in the target project. All OTHER changed paths
    remain subject to exact added/removed line matching. Mode-only/rename/
    binary patches are deliberately not supported by this small pilot.
    """
    counts: Counter[tuple[str, str, str]] = Counter()
    filename = None
    in_hunk = False
    excluded = False
    had_diff = False
    for line in text.splitlines():
        if line.startswith("diff --git "):
            had_diff = True
            in_hunk = False
            m = re.fullmatch(r"diff --git a/(\S+) b/(\S+)", line)
            if not m or m.group(1) != m.group(2):
                return None
            filename = m.group(2)
            if filename.startswith("/") or ".." in Path(filename).parts:
                return None
            excluded = filename.startswith(("workspace/bash_events/", "workspace/conversations/"))
        elif line.startswith(("GIT binary patch", "Binary files ", "rename from ", "rename to ")):
            return None
        elif line.startswith(("new file mode ", "deleted file mode ", "old mode ", "new mode ")):
            # Require review for source-file mode changes. Ignore modes on
            # excluded agent-runtime trace files only.
            if not excluded:
                return None
        elif line.startswith("@@ "):
            if filename is None:
                return None
            in_hunk = True
        elif in_hunk and line.startswith(("+", "-")) and not excluded:
            counts[(filename, line[0], line[1:])] += 1
        elif line.startswith("\\ No newline"):
            continue
    return counts if had_diff and counts else None


def pretest_diff(log: str) -> str | None:
    start_token = "Git diff before:\n"
    end_token = "Eval script for "
    start = log.find(start_token)
    if start == -1:
        return None
    end = log.find(end_token, start + len(start_token))
    if end == -1:
        return None
    return log[start + len(start_token):end].strip()


def parse_augmented_pytest(output: str, expected_files: list[str]) -> tuple[str | None, dict[str, Any]]:
    """Conservative parser for one augmented pytest invocation in an eval.sh log.

    This is NOT the standard SWE-bench resolved metric; it reads only the
    strengthened test block. Any ambiguity stays UNVERIFIED.
    """
    text = re.sub(r"\x1b\[[0-9;]*m", "", output)
    begin, end = ">>>>> Start Test Output", ">>>>> End Test Output"
    if text.count(begin) != 1 or text.count(end) != 1:
        return None, {"reason": "augmented_pytest_markers_missing_or_multiple"}
    segment = text.split(begin, 1)[1].split(end, 1)[0]
    runs = re.findall(r"(?m)^\+ pytest -rA (.+)$", segment)
    if len(runs) != 1:
        return None, {"reason": "expected_one_augmented_pytest_command"}
    targets = runs[0].strip().split()
    if not expected_files or not set(expected_files).intersection(targets):
        return None, {"reason": "augmented_pytest_command_does_not_target_test_patch"}
    collected = re.findall(r"(?m)^collected (\d+) items?\s*$", segment)
    summaries = [line.strip() for line in segment.splitlines()
                 if re.search(r"={3,}.*\b(?:passed|failed|error|skipped)\b.*\bin\s+\d", line)]
    if len(collected) != 1 or len(summaries) != 1:
        return None, {"reason": "augmented_pytest_collection_or_summary_ambiguous"}
    n = int(collected[0])
    summary = summaries[0]
    def count(name: str) -> int:
        m = re.search(r"\b(\d+)\s+" + name + r"\b", summary)
        return int(m.group(1)) if m else 0
    passed = count("passed")
    failed = count("failed")
    skipped = count("skipped")
    errors = count("error") + count("errors")
    extra = any(re.search(r"\b\d+\s+" + cat + r"\b", summary)
                for cat in ("xfailed", "xpassed", "deselected", "warnings"))
    details = {"augmented_collected": n, "augmented_passed": passed,
               "augmented_failed": failed, "augmented_skipped": skipped,
               "augmented_errors": errors, "augmented_pytest_targets": targets}
    if n == 0 or skipped or errors or extra or passed + failed != n:
        details["reason"] = "augmented_pytest_incomplete_or_ambiguous"
        return None, details
    return ("FAIL" if failed else "PASS"), details


def collect_result(metadata: dict[str, Any], logs_root: Path, run_id: str) -> dict[str, Any]:
    instance_id = metadata["instance_id"]
    result: dict[str, Any] = {
        **metadata, "run_id": run_id, "outcome": "UNVERIFIED",
        "reason": "missing_run_directory", "patch_diff_check": "NOT_CHECKED",
        "harness_report_resolved": None,
        "label_source": "augmented_pytest_not_original_swebench_report",
    }
    base = logs_root / run_id
    folders = [p for p in base.glob("*/" + instance_id) if p.is_dir()]
    if len(folders) != 1:
        result["reason"] = f"expected_one_run_directory_found_{len(folders)}"
        return result
    folder = folders[0]
    prediction_patch = folder / "patch.diff"
    log_path, report_path, output_path = (folder / "run_instance.log",
                                          folder / "report.json", folder / "test_output.txt")
    if not prediction_patch.exists() or sha256(prediction_patch.read_bytes()) != metadata.get("patch_sha256"):
        result["reason"] = "evaluator_patch_sha256_missing_or_mismatch"
        return result
    if not log_path.exists():
        result["reason"] = "run_instance_log_missing"
        return result
    log_text = log_path.read_text(encoding="utf-8", errors="replace")
    marker = re.findall(r"PREPATCH_BASE_COMMIT_VERIFIED: ([a-f0-9]{40})", log_text)
    if len(marker) != 1 or marker[0] != metadata.get("base_commit"):
        result["reason"] = "prepatch_base_commit_not_verified"
        return result
    result["base_commit_check"] = "VERIFIED"
    parsed_before = pretest_diff(log_text)
    if parsed_before is None:
        result["reason"] = "pretest_diff_not_logged"
        return result
    expected = changed_lines(prediction_patch.read_text(encoding="utf-8", errors="replace"))
    observed = changed_lines(parsed_before)
    if expected is None or observed is None:
        result["reason"] = "unsupported_patch_format_or_empty_diff"
        return result
    if expected != observed:
        result["reason"] = "pretest_repository_change_lines_mismatch"
        result["patch_diff_check"] = "MISMATCH"
        return result
    result["patch_diff_check"] = "REPOSITORY_CHANGE_LINES_MATCH"
    if not report_path.exists() or not output_path.exists():
        result["reason"] = "missing_report_or_test_output"
        return result
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))[instance_id]
    except (ValueError, KeyError, TypeError):
        result["reason"] = "malformed_report_json"
        return result
    # The official report's resolved field scores original FAIL_TO_PASS/PASS_TO_PASS
    # names, not the newly added tests in the SWE-ABS test_patch. Preserve it as
    # provenance but DO NOT use it as the stronger-test success label.
    result["harness_report_resolved"] = report.get("resolved")
    if report.get("patch_successfully_applied") is not True:
        result["reason"] = "harness_did_not_parse_test_log"
        return result
    output_text = output_path.read_text(encoding="utf-8", errors="replace")
    setup_segment = output_text.split(">>>>> Start Test Output", 1)[0]
    result["environment_setup_warning"] = any(marker in setup_segment for marker in (
        "error: subprocess-exited-with-error", "ModuleNotFoundError:",
    ))
    if "would be overwritten by checkout" in output_text or "Aborting" in output_text:
        result["reason"] = "checkout_failed_during_augmented_evaluation"
        return result
    status, details = parse_augmented_pytest(output_text, metadata.get("augmented_test_files", []))
    result.update(details)
    if status is None:
        result["reason"] = details["reason"]
        return result
    result.update(outcome=status, reason="verified_augmented_pytest_with_base_and_repository_patch")
    return result


def merge_results(path: Path, output: Path) -> None:
    paths = sorted(path.rglob("result.json"))
    if not paths:
        raise RuntimeError(f"No result.json files in {path}")
    results = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    keys = [(x.get("sample"), x.get("instance_id")) for x in results]
    if len(keys) != len(set(keys)):
        raise RuntimeError("Duplicate sample/instance ID in collected results")
    fields = ["sample", "instance_id", "original_resolved", "patch_sha256", "dataset_revision", "test_dataset_revision", "test_patch_sha256",
              "sweabs_commit", "run_id", "outcome", "reason", "base_commit", "base_commit_check",
              "patch_diff_check", "augmented_collected", "augmented_passed", "augmented_failed",
              "augmented_skipped", "augmented_errors", "environment_setup_warning",
              "label_source", "harness_report_resolved"]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted(results, key=lambda x: (x.get("sample", 0), x.get("instance_id", ""))))
    counts = Counter(x["outcome"] for x in results)
    (output.parent / "pilot_summary.json").write_text(json.dumps({"total": len(results), "outcomes": dict(counts),
        "warning": "PASS and FAIL labels are provisional; manually validate setup warnings and source-state evidence before publication"}, indent=2) + "\n")
    print(f"Merged {len(results)} outcomes: {dict(counts)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    subs = ap.add_subparsers(dest="cmd", required=True)
    plan = subs.add_parser("plan")
    for p in (plan,):
        p.add_argument("--sample", type=int, required=True)
        p.add_argument("--offset", type=int, required=True)
        p.add_argument("--count", type=int, required=True)
        p.add_argument("--output", type=Path, required=True)
    pred = subs.add_parser("prediction")
    for arg in ("revision", "instance-id", "expected-hash"):
        pred.add_argument("--" + arg, required=True)
    pred.add_argument("--sample", type=int, required=True)
    pred.add_argument("--output", type=Path, required=True)
    pred.add_argument("--metadata", type=Path, required=True)
    test = subs.add_parser("test-record")
    test.add_argument("--revision", required=True)
    test.add_argument("--instance-id", required=True)
    test.add_argument("--output", type=Path, required=True)
    test.add_argument("--metadata", type=Path, required=True)
    collect = subs.add_parser("collect")
    collect.add_argument("--metadata", type=Path, required=True)
    collect.add_argument("--logs-root", type=Path, required=True)
    collect.add_argument("--run-id", required=True)
    collect.add_argument("--instance-id", required=True)
    collect.add_argument("--sample", type=int, required=True)
    collect.add_argument("--output", type=Path, required=True)
    merge = subs.add_parser("merge")
    merge.add_argument("--input-dir", type=Path, required=True)
    merge.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.cmd == "plan":
        from huggingface_hub import HfApi
        revision = HfApi().dataset_info(DATASET_ID).sha
        test_revision = HfApi().dataset_info(TEST_DATASET_ID).sha
        if not re.fullmatch(r"[a-f0-9]{40}", revision) or not re.fullmatch(r"[a-f0-9]{40}", test_revision):
            raise RuntimeError(f"Expected both revisions to be 40-character commit SHAs: {revision}, {test_revision}")
        out = generate_plan(load_rows(revision), revision, args.sample, args.offset, args.count, test_revision)
        args.output.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        print(f"Prepared {args.count} tasks, sample {args.sample}, trajectory SHA {revision}, SWE-ABS test SHA {test_revision}")
    elif args.cmd == "prediction":
        prediction, manifest = build_prediction(load_rows(args.revision), args.revision,
                             args.sample, args.instance_id, args.expected_hash)
        args.output.write_text(json.dumps(prediction, ensure_ascii=False) + "\n", encoding="utf-8")
        args.metadata.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote prediction for {args.instance_id}, SHA256={manifest['patch_sha256']}")
    elif args.cmd == "test-record":
        rows, manifest = build_test_record(args.revision, args.instance_id)
        args.output.write_text(json.dumps(rows, ensure_ascii=False) + "\n", encoding="utf-8")
        old = json.loads(args.metadata.read_text(encoding="utf-8"))
        old.update(manifest)
        args.metadata.write_text(json.dumps(old, indent=2) + "\n", encoding="utf-8")
        print(f"Pinned SWE-ABS test patch: {args.instance_id}, SHA256={manifest['test_patch_sha256']}")
    elif args.cmd == "collect":
        if args.metadata.exists():
            meta = json.loads(args.metadata.read_text(encoding="utf-8"))
        else:
            meta = {"instance_id": args.instance_id, "sample": args.sample,
                    "patch_sha256": None, "dataset_revision": os.environ.get("DATASET_REVISION", "UNVERIFIED"),
                    "sweabs_commit": os.environ.get("SWE_ABS_SHA", "UNVERIFIED")}
        result = collect_result(meta, args.logs_root, args.run_id)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"{result['instance_id']}: {result['outcome']} ({result['reason']})")
    elif args.cmd == "merge":
        merge_results(args.input_dir, args.output)


if __name__ == "__main__":
    main()
