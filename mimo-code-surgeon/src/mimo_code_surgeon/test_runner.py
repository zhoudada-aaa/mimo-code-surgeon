from __future__ import annotations

import subprocess
from pathlib import Path

from .models import TestResult


def run_tests(command: str, cwd: str | Path, timeout: int = 120) -> TestResult:
    cwd_path = Path(cwd).resolve()
    proc = subprocess.run(
        command,
        cwd=str(cwd_path),
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return TestResult(
        command=command,
        cwd=str(cwd_path),
        exit_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )
