from __future__ import annotations

from mimo_code_surgeon.models import RepoScan


class RetrievalAgent:
    def run(self, scan: RepoScan, issue: str) -> dict:
        lower_issue = issue.lower()
        source_files: list[str] = []
        test_files: list[str] = []

        for item in scan.files:
            path = item.path.lower()
            content = item.content.lower()
            if "calculator" in lower_issue and "calculator" in path:
                if "test" in path:
                    test_files.append(item.path)
                else:
                    source_files.append(item.path)
            elif "divide" in lower_issue and "divide" in content:
                if "test" in path:
                    test_files.append(item.path)
                else:
                    source_files.append(item.path)

        if not source_files:
            source_files = [f.path for f in scan.files if f.path.endswith(".py") and "test" not in f.path.lower()][:3]
        if not test_files:
            test_files = [f.path for f in scan.files if "test" in f.path.lower()][:3]

        return {
            "source_files": source_files,
            "test_files": test_files,
            "reason": "Selected files by matching issue keywords against file paths and code content."
        }
