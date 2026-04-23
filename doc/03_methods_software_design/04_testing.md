---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

(software_tests)=
# Software tests

Most programs are dynamic in nature, with features constantly being added and code being restructured.
In this process, functionality that is required by other parts of the codebase might be broken, even if the modified function itself works as intended.
One effective way to check for such problems is to write automated tests.
*Unit tests* verify that a specific unit of the code meets its design criteria.
*Integration tests*, on the other hand, are designed to validate that interfaces between components work as intended {cite}`Hamill2004`.

In his book "Clean Code: A Handbook of Agile Software Craftsmanship", Robert Martin summarizes the important aspects of software testing in the "F.I.R.S.T." principle {cite}`Martin2008`:

- Fast: Tests should be fast enough to be run many times during development.
- Independent: Tests should not depend on the output of other tests.
- Repeatable: Tests should be independent of the programming environment.
- Self-Validating: Tests should not depend on manual checks by the developer but instead either pass or fail.
- Timely: Tests should be written before or alongside the production code, not added as an afterthought.

One effective way to apply these principles in practice is through a programming practice called *test-driven development* (TDD).
In TDD, the usual programming workflow is inverted: first, a test is written that clearly defines the interface and tests for use cases to cover all requirements and exception conditions.
Only if the corresponding function passes the test will it be included in the working branch of the software {cite}`Martin2008`.

To demonstrate these principles, consider a function that computes the steady-state residual of a continuously stirred tank reactor (CSTR), building on the example from {numref}`oop`.
The functionality of this function can be verified by writing a script for automated testing.
Templates for `TestCases` and assertion methods to write tests are provided by the `unittest` module in *Python*'s standard library.
The `assertAlmostEqual` method limits the number of significant figures and prevents false positive errors due to limited numerical precision.

When writing the test, it may become apparent that the function should raise an exception if a non-numeric argument is passed.
Tests can be written to validate these requirements before the function itself is implemented.

```{code-cell} ipython3
import unittest

class TestCSTRResidual(unittest.TestCase):
    def test_equilibrium(self):
        self.assertAlmostEqual(cstr_residual(flow_rate=1.0, c_in=1.0, state=1.0), 0.0)

    def test_value(self):
        self.assertAlmostEqual(cstr_residual(flow_rate=1.0, c_in=1.0, state=0.5), 0.5)

    def test_types(self):
        self.assertRaises(TypeError, cstr_residual, '1.0', 1.0, 0.5)
```

After the interface (i.e. the input and output parameters) of the function is enforced by the tests, the function can be implemented with proper documentation (see {numref}`software_documentation`).

```{code-cell} ipython3
def cstr_residual(flow_rate: float, c_in: float, state: float) -> float:
    """Compute the steady-state mass balance residual of a CSTR.

    Parameters
    ----------
    flow_rate
        Volumetric flow rate in m^3/s.
    c_in
        Inlet concentration in mM.
    state
        Current concentration in mM.

    Returns
    -------
    float
        Residual of the steady-state mass balance.

    Raises
    ------
    TypeError
        If any argument is not a float.

    """
    if not isinstance(flow_rate, float):
        raise TypeError("flow_rate must be a float.")
    return flow_rate * (c_in - state)
```

Writing these kinds of tests incentivizes programmers to think about code modularization, programming towards cleaner interfaces (see {numref}`programming_principles`), and writing proper documentation (see {numref}`software_documentation`).

In CADET-Process, tests are located in the `tests/` directory of the repository and cover both unit and integration tests using a combination of *Python*'s standard `unittest` module and *pytest* {cite}`pytest`.
Using *Github Actions*, these tests are automatically run whenever the code is updated (see {numref}`ci_cd`), ensuring that new contributions do not break existing functionality.
Test coverage, i.e. the fraction of source code executed by the test suite, is tracked using [*Codecov*](https://app.codecov.io/github/fau-advanced-separations/CADET-Process/tree/dev) and currently stands at approximately 73\% (as of April 2026).
