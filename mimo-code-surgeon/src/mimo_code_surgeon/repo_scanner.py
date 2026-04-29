from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .models import FileSnapshot, RepoScan

DEFAULT_EXTENSIONS = {
    ".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".json",
    ".ini", ".cfg", ".sh", ".js", ".ts", ".go", ".java"
}
IGNORED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    "node_modules", "dist", "build", ".mypy_cache", ".ruff_cache"
}


def _should_read(path: Path, root: Path, extensions: set[str]) -> bool:
    rel_parts = path.relative_to(root).parts
    if any(part in IGNORED_DIRS for part in rel_parts):
        return False
    if not path.is_file():
        return False
    if path.stat().st_size > 300_000:
        return False
    return path.suffix.lower() in extensions or path.name in {"Dockerfile", "Makefile"}


def build_tree(root: Path, max_entries: int = 300) -> str:
    entries: list[str] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        depth = len(rel.parts) - 1
        prefix = "  " * depth + ("- " if depth else "")
        marker = "/" if path.is_dir() else ""
        entries.append(f"{prefix}{rel.name}{marker}")
        if len(entries) >= max_entries:
            entries.append("... tree truncated ...")
            break
    return "\n".join(entries)


def scan_repo(repo_path: str | Path, extensions: Iterable[str] | None = None) -> RepoScan:
    root = Path(repo_path).resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Repository path does not exist or is not a directory: {root}")

    ext_set = set(extensions or DEFAULT_EXTENSIONS)
    files: list[FileSnapshot] = []
    readme: str | None = None

    for path in sorted(root.rglob("*")):
        if not _should_read(path, root, ext_set):
            continue
        rel = path.relative_to(root).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="utf-8", errors="replace")

        files.append(FileSnapshot(path=rel, content=content))
        if path.name.lower().startswith("readme") and readme is None:
            readme = content

    return RepoScan(root=root, files=files, tree=build_tree(root), readme=readme)
