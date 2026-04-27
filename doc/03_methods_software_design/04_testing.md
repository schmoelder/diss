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

Most code bases are dynamic in nature, with features constantly being added and code being restructured.
In this process, functionality that is required by other parts of the codebase might be broken, even if the modified function itself works as intended.
One effective way to check for such problems is to write automated tests.
*Unit tests* verify that a specific unit of the code meets its design criteria.
*Integration tests* validate that interfaces between components work as intended.
*System tests* verify end-to-end behavior of the complete software {cite}`Hamill2004`.
Beyond these, other test categories exist, including performance tests and security tests, which address non-functional requirements.
Martin summarizes the important aspects of software testing in the "F.I.R.S.T." principle {cite}`Martin2008`:

- Fast: Tests should be fast enough to be run many times during development.
- Independent: Tests should not depend on the output of other tests.
- Repeatable: Tests should be independent of the programming environment.
- Self-Validating: Tests should not depend on manual checks by the developer but instead either pass or fail.
- Timely: Tests should be written before or alongside the production code, not added as an afterthought.

A programming practice that directly applies these principles is *test-driven development* (TDD).
In TDD, the usual programming workflow is inverted: first, a test is written that clearly defines the interface and covers all requirements and exception conditions.
Only if the corresponding function passes the test will it be included in the working branch of the software {cite}`Martin2008`.

To demonstrate these principles, consider the `CSTR` class introduced in {numref}`oop`.
Templates for `TestCases` and assertion methods to write tests are provided by the `unittest` module in *Python*'s standard library.
The `assertAlmostEqual` method limits the number of significant figures and prevents false positive errors due to limited numerical precision.
When writing the test, it may become apparent that `residual` should raise an exception if a non-numeric argument is passed.
Tests can be written to validate these requirements before the implementation is finalized.

```{code-cell} ipython3
:tags: [remove-cell]

import unittest
from abc import ABC, abstractmethod

class UnitOperationBase(ABC):
    """Base class for unit operation models."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def residual(self, state: float, flow_rate: float, c_in: float) -> float:
        pass

class CSTR(UnitOperationBase):
    """Continuously stirred tank reactor."""

    def __init__(self, name: str, v_init: float, c_init: float):
        super().__init__(name)
        self.v_init = v_init
        self.c_init = c_init

    def residual(self, state: float, flow_rate: float, c_in: float) -> float:
        """Compute the mass balance residual of a CSTR.

        Parameters
        ----------
        state
            Current concentration in mM.
        flow_rate
            Volumetric flow rate in m^3/s.
        c_in
            Inlet concentration in mM.

        Returns
        -------
        float
            Residual of the mass balance.

        Raises
        ------
        TypeError
            If any argument is not a float.

        """
        if not isinstance(flow_rate, float):
            raise TypeError("flow_rate must be a float.")
        c = state
        return flow_rate * (c_in - c)
```

```{code-cell} ipython3
class TestCSTR(unittest.TestCase):
    def setUp(self):
        self.cstr = CSTR(name="reactor", v_init=10.0, c_init=0.0)

    def test_zero_flow(self):
        self.assertAlmostEqual(self.cstr.residual(state=0.5, flow_rate=0.0, c_in=1.0), 0.0)

    def test_value(self):
        self.assertAlmostEqual(self.cstr.residual(state=0.5, flow_rate=1.0, c_in=1.0), 0.5)

    def test_types(self):
        self.assertRaises(TypeError, self.cstr.residual, 0.5, '1.0', 1.0)
```

Writing these kinds of tests incentivizes programmers to think about code modularization, cleaner interfaces (see {numref}`programming_principles`), and proper documentation (see {numref}`software_documentation`).

In CADET-Process, tests are located in the `tests/` directory of the repository and cover both unit and integration tests using a combination of *Python*'s standard `unittest` module and *pytest* {cite}`pytest`.
Using *Github Actions*, these tests are automatically run whenever the code is updated (see {numref}`ci_cd`), ensuring that new contributions do not break existing functionality.
Test coverage, i.e. the fraction of source code executed by the test suite, is tracked using *Codecov* and currently stands at approximately 73\% (as of April 2026).
The following chapter discusses how version control enables structured collaboration and tracks the full history of these changes.
