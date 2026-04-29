from __future__ import annotations

import argparse

from .workflow import run_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mimo-surgeon",
        description="Multi-agent automated code refactoring and verifiable PR generation demo.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run the multi-agent workflow.")
    run.add_argument("--repo", required=True, help="Path to local repository.")
    run.add_argument("--issue", required=True, help="Issue text to solve.")
    run.add_argument("--test", required=True, help="Test command to execute inside the repository.")
    run.add_argument("--output", default=None, help="Output run directory. Default: runs/<timestamp>.")
    run.add_argument("--mode", default="auto", choices=["auto", "mock", "real"], help="Agent mode.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        artifacts = run_workflow(
            repo_path=args.repo,
            issue=args.issue,
            test_command=args.test,
            output_dir=args.output,
            mode=args.mode,
        )
        print(f"MiMo Code Surgeon run completed: {artifacts.run_dir}")
        print("Key artifacts:")
        for name in [
            "plan.md",
            "test_first_attempt.log",
            "repair_notes.md",
            "test_after.log",
            "pr_description.md",
            "token_estimate.json",
        ]:
            path = artifacts.files.get(name)
            if path:
                print(f"- {name}: {path}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
