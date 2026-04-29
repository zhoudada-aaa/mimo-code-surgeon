from __future__ import annotations

import difflib
from pathlib import Path
from typing import Dict


def snapshot_files(root: Path, paths: list[str]) -> Dict[str, str]:
    snap: Dict[str, str] = {}
    for rel in paths:
        path = root / rel
        snap[rel] = path.read_text(encoding="utf-8") if path.exists() else ""
    return snap


def unified_diff(before: Dict[str, str], after: Dict[str, str]) -> str:
    chunks: list[str] = []
    for rel in sorted(set(before) | set(after)):
        before_lines = before.get(rel, "").splitlines(keepends=True)
        after_lines = after.get(rel, "").splitlines(keepends=True)
        chunks.extend(
            difflib.unified_diff(
                before_lines,
                after_lines,
                fromfile=f"a/{rel}",
                tofile=f"b/{rel}",
                lineterm="",
            )
        )
        if chunks and not chunks[-1].endswith("\n"):
            chunks[-1] += "\n"
    return "".join(chunks)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
