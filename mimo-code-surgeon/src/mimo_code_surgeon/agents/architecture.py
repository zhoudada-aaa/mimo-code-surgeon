from __future__ import annotations

from mimo_code_surgeon.models import RepoScan


class ArchitectureAgent:
    def run(self, scan: RepoScan, issue: str) -> str:
        py_files = [f.path for f in scan.files if f.path.endswith(".py")]
        test_files = [f.path for f in scan.files if "test" in f.path.lower()]
        dep_files = [f.path for f in scan.files if f.path.endswith((".toml", ".txt", ".yaml", ".yml"))]

        return f'''# Architecture Report

## Project tree

```text
{scan.tree}
```

## Detected Python files

{chr(10).join(f"- `{p}`" for p in py_files) or "- None"}

## Detected test files

{chr(10).join(f"- `{p}`" for p in test_files) or "- None"}

## Detected dependency/config files

{chr(10).join(f"- `{p}`" for p in dep_files) or "- None"}

## Issue impact analysis

Issue: {issue}

The task appears to affect business logic and tests. In the sample repository,
`src/calculator.py` contains the target behavior and `tests/test_calculator.py`
contains the regression tests.
'''
