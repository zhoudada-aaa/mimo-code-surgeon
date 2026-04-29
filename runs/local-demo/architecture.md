# Architecture Report

## Project tree

```text
README.md
src/
  - __init__.py
  - calculator.py
tests/
  - test_calculator.py
```

## Detected Python files

- `src/__init__.py`
- `src/calculator.py`
- `tests/test_calculator.py`

## Detected test files

- `tests/test_calculator.py`

## Detected dependency/config files

- None

## Issue impact analysis

Issue: 修复 calculator.divide 在除数为 0 时行为不清晰的问题，并补充测试

The task appears to affect business logic and tests. In the sample repository,
`src/calculator.py` contains the target behavior and `tests/test_calculator.py`
contains the regression tests.
