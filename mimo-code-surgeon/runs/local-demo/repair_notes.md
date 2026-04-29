# Review Notes

## Test status

The first attempt failed.

## Failure summary

```text
..E
======================================================================
ERROR: test_divide_by_zero_raises_value_error (test_calculator.CalculatorTest.test_divide_by_zero_raises_value_error)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/mnt/data/mimo-code-surgeon/runs/local-demo/working_repo/tests/test_calculator.py", line 16, in test_divide_by_zero_raises_value_error
    divide(10, 0)
    ~~~~~~^^^^^^^
  File "/mnt/data/mimo-code-surgeon/runs/local-demo/working_repo/src/calculator.py", line 6, in divide
    return a / b
           ~~^~~
ZeroDivisionError: division by zero

----------------------------------------------------------------------
Ran 3 tests in 0.004s

FAILED (errors=1)

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
