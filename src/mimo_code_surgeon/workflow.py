from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .agents import ArchitectureAgent, DocumentationAgent, ImplementationAgent, RetrievalAgent, ReviewAgent
from .models import WorkflowArtifacts
from .patch_utils import snapshot_files, unified_diff, write_text
from .repo_scanner import scan_repo
from .test_runner import run_tests
from .token_estimator import build_token_estimate


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _copy_repo(src: Path, dst: Path) -> None:
    ignore = shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache", "runs")
    shutil.copytree(src, dst, ignore=ignore)


def run_workflow(
    repo_path: str | Path,
    issue: str,
    test_command: str,
    output_dir: str | Path | None = None,
    mode: str = "auto",
) -> WorkflowArtifacts:
    source_repo = Path(repo_path).resolve()
    if output_dir is None:
        output_dir = Path.cwd() / "runs" / _timestamp()
    run_dir = Path(output_dir).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    working_repo = run_dir / "working_repo"
    if working_repo.exists():
        shutil.rmtree(working_repo)
    _copy_repo(source_repo, working_repo)

    artifacts = WorkflowArtifacts(run_dir=run_dir)

    scan = scan_repo(working_repo)
    architecture = ArchitectureAgent().run(scan, issue)
    retrieval = RetrievalAgent().run(scan, issue)
    implementer = ImplementationAgent()
    reviewer = ReviewAgent()
    documenter = DocumentationAgent()

    write_text(run_dir / "input_issue.md", f"# Input Issue\n\n{issue}\n")
    write_text(run_dir / "repo_summary.md", _build_repo_summary(scan))
    write_text(run_dir / "architecture.md", architecture)
    write_text(run_dir / "retrieval_result.json", json.dumps(retrieval, indent=2, ensure_ascii=False))

    plan = _build_plan(issue, retrieval, mode)
    write_text(run_dir / "plan.md", plan)

    before_result = run_tests(test_command, working_repo)
    write_text(run_dir / "test_before.log", before_result.to_log())

    tracked_files = sorted(set(retrieval["source_files"] + retrieval["test_files"]))
    before_first_patch = snapshot_files(working_repo, tracked_files)
    implementer.add_regression_test_for_divide_zero(working_repo)
    after_first_patch = snapshot_files(working_repo, tracked_files)
    write_text(run_dir / "first_patch.diff", unified_diff(before_first_patch, after_first_patch))

    first_result = run_tests(test_command, working_repo)
    write_text(run_dir / "test_first_attempt.log", first_result.to_log())

    repair_notes = reviewer.analyze_failure(first_result)
    write_text(run_dir / "repair_notes.md", repair_notes)

    before_repair = snapshot_files(working_repo, tracked_files)
    if not first_result.passed:
        implementer.repair_divide_zero_behavior(working_repo)
    after_repair = snapshot_files(working_repo, tracked_files)
    write_text(run_dir / "repair_patch.diff", unified_diff(before_repair, after_repair))

    final_result = run_tests(test_command, working_repo)
    write_text(run_dir / "test_after.log", final_result.to_log())

    pr_description = documenter.build_pr_description(issue, final_result)
    write_text(run_dir / "pr_description.md", pr_description)

    token_estimate = build_token_estimate(scan, issue)
    write_text(run_dir / "token_estimate.json", json.dumps(token_estimate, indent=2, ensure_ascii=False))

    manifest = {
        "project": "MiMo Code Surgeon",
        "mode": mode,
        "source_repo": str(source_repo),
        "working_repo": str(working_repo),
        "issue": issue,
        "test_command": test_command,
        "final_status": "passed" if final_result.passed else "failed",
        "artifacts": [
            "input_issue.md",
            "repo_summary.md",
            "architecture.md",
            "retrieval_result.json",
            "plan.md",
            "test_before.log",
            "first_patch.diff",
            "test_first_attempt.log",
            "repair_notes.md",
            "repair_patch.diff",
            "test_after.log",
            "pr_description.md",
            "token_estimate.json",
        ],
    }
    write_text(run_dir / "manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))

    for item in manifest["artifacts"]:
        artifacts.add(item, run_dir / item)
    return artifacts


def _build_repo_summary(scan) -> str:
    return f'''# Repository Summary

Root: `{scan.root}`

## File tree

```text
{scan.tree}
```

## Scanned files

{chr(10).join(f"- `{item.path}` ({len(item.content)} chars)" for item in scan.files)}

## Total scanned characters

{scan.total_chars}
'''


def _build_plan(issue: str, retrieval: dict, mode: str) -> str:
    return f'''# Execution Plan

## Mode

`{mode}`

## Issue

{issue}

## Selected source files

{chr(10).join(f"- `{p}`" for p in retrieval.get("source_files", []))}

## Selected test files

{chr(10).join(f"- `{p}`" for p in retrieval.get("test_files", []))}

## Steps

1. Run baseline tests.
2. Add a regression test that captures the expected divide-by-zero behavior.
3. Run tests and collect failure logs.
4. Analyze failure with Review Agent.
5. Apply minimal source repair.
6. Run regression tests again.
7. Generate PR description and token estimate.
'''
