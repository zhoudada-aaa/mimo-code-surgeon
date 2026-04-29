from __future__ import annotations

from .models import RepoScan


def rough_tokens_from_text(text: str) -> int:
    return max(1, int(len(text) / 3.5))


def build_token_estimate(scan: RepoScan, issue: str) -> dict:
    repo_tokens = rough_tokens_from_text(scan.tree + "\n" + "\n".join(f.content for f in scan.files))
    issue_tokens = rough_tokens_from_text(issue)

    multi_agent_multiplier = 8
    repair_multiplier = 4
    estimated_single_issue = (repo_tokens + issue_tokens) * multi_agent_multiplier * repair_multiplier

    return {
        "local_demo_api_tokens": 0,
        "rough_scanned_repo_tokens": repo_tokens,
        "rough_issue_tokens": issue_tokens,
        "estimated_single_issue_tokens_for_real_model": {
            "lower_bound": max(1_000_000, estimated_single_issue),
            "upper_bound": max(5_000_000, estimated_single_issue * 2),
            "unit": "tokens"
        },
        "application_level_estimate": {
            "repo_initialization": "500,000 - 2,000,000 tokens per medium/large repository",
            "single_issue_full_loop": "1,000,000 - 5,000,000 tokens per real issue",
            "daily_processing_20_to_50_issues": "30,000,000 - 200,000,000 tokens per day"
        },
        "why_tokens_are_needed": [
            "Repository-wide long-context reading",
            "Multi-agent planning and context passing",
            "Patch generation",
            "Test log analysis",
            "Failure repair",
            "Regression verification",
            "PR documentation"
        ]
    }
