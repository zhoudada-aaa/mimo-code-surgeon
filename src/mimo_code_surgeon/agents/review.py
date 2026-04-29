from __future__ import annotations

from mimo_code_surgeon.models import TestResult


class ReviewAgent:
    def analyze_failure(self, result: TestResult) -> str:
        if result.passed:
            return "# Review Notes\n\nTests passed. No repair is required.\n"

        return f'''# Review Notes

## Test status

The first attempt failed.

## Failure summary

```text
{(result.stdout + result.stderr)[-4000:]}
```

## Root cause

The new regression test expects `calculator.divide(10, 0)` to raise `ValueError`.
The current implementation delegates directly to Python division, which raises
`ZeroDivisionError`. The public behavior is therefore unclear and not aligned
with the new API contract.

## Repair plan

Update `src/calculator.py` so `divide(a, b)` explicitly checks `b == 0` and
raises `ValueError("division by zero is not allowed")` before performing the
division.
'''
