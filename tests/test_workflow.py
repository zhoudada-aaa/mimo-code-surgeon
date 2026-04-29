from pathlib import Path
import shutil
import tempfile
import unittest

from mimo_code_surgeon.workflow import run_workflow


class WorkflowTest(unittest.TestCase):
    def test_mock_workflow_passes(self):
        project_root = Path(__file__).resolve().parents[1]
        source_repo = project_root / "examples" / "sample_repo"

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            repo_copy = td_path / "repo"
            shutil.copytree(source_repo, repo_copy)

            artifacts = run_workflow(
                repo_path=repo_copy,
                issue="修复 calculator.divide 在除数为 0 时行为不清晰的问题，并补充测试",
                test_command="python -S -m unittest discover -s tests",
                output_dir=td_path / "run",
                mode="mock",
            )

            first_log = (artifacts.run_dir / "test_first_attempt.log").read_text(encoding="utf-8")
            self.assertIn("Status: FAILED", first_log)

            final_log = (artifacts.run_dir / "test_after.log").read_text(encoding="utf-8")
            self.assertIn("Status: PASSED", final_log)

            pr = (artifacts.run_dir / "pr_description.md").read_text(encoding="utf-8")
            self.assertIn("PR:", pr)


if __name__ == "__main__":
    unittest.main()
