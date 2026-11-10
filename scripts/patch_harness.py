#!/usr/bin/env python3
"""Apply the safe patch fallback backport from the existing successful smoke test.

Fails closed if the pinned upstream harness no longer has the expected source
structure. Do not treat this transform as a generic SWE-bench monkeypatch.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def patch_source(source: str) -> str:
    lines = source.splitlines()
    cmd_start = next(i for i, line in enumerate(lines) if line.strip() == "GIT_APPLY_CMDS = [")
    cmd_end = next(i for i in range(cmd_start + 1, len(lines)) if lines[i].strip() == "]")
    base_indent = lines[cmd_start][: len(lines[cmd_start]) - len(lines[cmd_start].lstrip())]
    lines[cmd_start : cmd_end + 1] = [
        base_indent + "GIT_APPLY_CMDS = [",
        base_indent + '    "git apply --verbose",',
        base_indent + '    "git apply --verbose --3way",',
        base_indent + '    "git apply --verbose --reject",',
        base_indent + '    "patch --batch --forward --fuzz=5 -p1 -i",',
        base_indent + "]",
    ]

    loop_index = next(
        i for i, line in enumerate(lines) if line.strip() == "for git_apply_cmd in GIT_APPLY_CMDS:"
    )
    loop_indent = lines[loop_index][: len(lines[loop_index]) - len(lines[loop_index].lstrip())]
    child_indent = loop_indent + "    "
    lines[loop_index] = loop_indent + "for attempt, git_apply_cmd in enumerate(GIT_APPLY_CMDS):"
    reset_block = [
        child_indent + "if attempt:",
        child_indent + "    container.exec_run(",
        child_indent + '        ["/bin/bash", "-c", "git checkout -- . ; git clean -fd"],',
        child_indent + "        workdir=DOCKER_WORKDIR,",
        child_indent + "        user=DOCKER_USER,",
        child_indent + "    )",
    ]
    lines[loop_index + 1 : loop_index + 1] = reset_block

    fail_index = next(
        i for i in range(loop_index + len(reset_block) + 1, len(lines))
        if lines[i].strip() == "if not applied_patch:"
    )
    fail_indent = lines[fail_index][: len(lines[fail_index]) - len(lines[fail_index].lstrip())]
    reverse_block = [
        fail_indent + "if not applied_patch:",
        fail_indent + "    reverse_check = container.exec_run(",
        fail_indent + '        f"git apply --check --reverse {DOCKER_PATCH}",',
        fail_indent + "        workdir=DOCKER_WORKDIR,",
        fail_indent + "        user=DOCKER_USER,",
        fail_indent + "    )",
        fail_indent + "    if reverse_check.exit_code == 0:",
        fail_indent + "        logger.info(",
        fail_indent + '            f"{APPLY_PATCH_PASS}: verified already applied")',
        fail_indent + "        applied_patch = True",
    ]
    lines[fail_index:fail_index] = reverse_block

    modified = "\n".join(lines) + "\n"
    old_diff = '"git -c core.fileMode=false diff"'
    new_diff = '"git -c core.fileMode=false diff HEAD"'
    if modified.count(old_diff) != 2:
        # Both before- and after-test diffs are expected by the current harness.
        raise RuntimeError(f"Expected 2 diff commands; found {modified.count(old_diff)}")
    modified = modified.replace(old_diff, new_diff)

    required = [
        '"git apply --verbose --3way"',
        '"git apply --verbose --reject"',
        '"patch --batch --forward --fuzz=5 -p1 -i"',
        "git checkout -- . ; git clean -fd",
        "git apply --check --reverse",
        "git -c core.fileMode=false diff HEAD",
    ]
    for marker in required:
        if marker not in modified:
            raise AssertionError(f"Patch safety marker missing: {marker}")
    compile(modified, "patched_run_evaluation.py", "exec")
    return modified


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True, type=Path)
    args = p.parse_args()
    before = args.file.read_text(encoding="utf-8")
    after = patch_source(before)
    args.file.write_text(after, encoding="utf-8")
    print("Safe patch backport and Python syntax check: OK")


if __name__ == "__main__":
    main()
