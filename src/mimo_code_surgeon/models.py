from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class FileSnapshot:
    path: str
    content: str


@dataclass
class RepoScan:
    root: Path
    files: List[FileSnapshot]
    tree: str
    readme: str | None = None

    @property
    def total_chars(self) -> int:
        return sum(len(item.content) for item in self.files)


@dataclass
class TestResult:
    command: str
    cwd: str
    exit_code: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.exit_code == 0

    def to_log(self) -> str:
        status = "PASSED" if self.passed else "FAILED"
        return (
            f"Command: {self.command}\n"
            f"Working directory: {self.cwd}\n"
            f"Exit code: {self.exit_code}\n"
            f"Status: {status}\n\n"
            f"--- STDOUT ---\n{self.stdout}\n\n"
            f"--- STDERR ---\n{self.stderr}\n"
        )


@dataclass
class WorkflowArtifacts:
    run_dir: Path
    files: Dict[str, Path] = field(default_factory=dict)

    def add(self, name: str, path: Path) -> None:
        self.files[name] = path
