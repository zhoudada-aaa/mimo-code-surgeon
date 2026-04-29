# Issue: divide zero behavior is unclear

`calculator.divide` currently does not define a clear API contract when the divisor is 0.

Expected:

- Add a regression test.
- Make the behavior explicit.
- Keep normal division behavior unchanged.
