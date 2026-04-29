from __future__ import annotations

from pathlib import Path


class ImplementationAgent:
    def add_regression_test_for_divide_zero(self, repo: Path) -> None:
        test_path = repo / "tests" / "test_calculator.py"
        content = test_path.read_text(encoding="utf-8")

        if "test_divide_by_zero_raises_value_error" in content:
            return

        insertion = """
    def test_divide_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            divide(10, 0)
"""

        marker = '\n\nif __name__ == "__main__":'
        if marker in content:
            content = content.replace(marker, "\n" + insertion + marker, 1)
        else:
            content = content.rstrip() + "\n" + insertion + "\n"
        test_path.write_text(content, encoding="utf-8")

    def repair_divide_zero_behavior(self, repo: Path) -> None:
        src_path = repo / "src" / "calculator.py"
        content = src_path.read_text(encoding="utf-8")

        old = """def divide(a, b):
    return a / b
"""
        new = """def divide(a, b):
    if b == 0:
        raise ValueError("division by zero is not allowed")
    return a / b
"""
        if "division by zero is not allowed" in content:
            return
        if old not in content:
            raise RuntimeError("Could not locate expected divide implementation.")
        src_path.write_text(content.replace(old, new), encoding="utf-8")
