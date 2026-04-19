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
- Timely: Tests should be written before the code is included in the production code.

One effective way to apply these principles in practice is through a programming practice called *test-driven development* (TDD)
In TDD, the usual programming workflow is inverted: first, a test is written that clearly defines the interface and tests for use cases to cover all requirements and exception conditions.
Only if the corresponding function passes the test will it be included in the working branch of the software {cite}`Martin2008`.

To demonstrate these principles, consider a function that calculates the area of a circle using the radius as an input argument.
The functionality of this function can be verified by writing a script for automated testing.
Templates for `TestCases` and assertion methods to write tests are provided by the `unittest` module in *Python*'s standard library.
In this case, the `assertAlmostEqual` method can be used to limit the number of significant figures and prevent false positive errors due to limited numerical precision.

When writing the test, it may become apparent that the `circle_area` function should not be called with a negative radius argument, and an exception should be raised in such cases.
Additionally, the function should only accept floats and integers as input arguments to yield valid results.
Tests can be written to validate these requirements, ensuring that the function works correctly and preventing potential errors in the code.

```{code-cell} ipython3
import unittest

class TestCircleArea(unittest.TestCase):
    def test_area(self):
        self.assertAlmostEqual(circle_area(1), math.pi)
        self.assertAlmostEqual(circle_area(0), 0)
        self.assertAlmostEqual(circle_area(math.e), math.pi * math.e**2)

    def test_values(self):
        self.assertRaises(ValueError, circle_area, -2)

    def test_types(self):
        self.assertRaises(TypeError, circle_area, 3+1.4j)
        self.assertRaises(TypeError, circle_area, 'radius')
```

After the interface (i.e. the input and output parameters) of the function is enforced by the tests, the function can be implemented with proper documentation (see {numref}`software_documentation`).

```{code-cell} ipython3
import math

def circle_area(r):
    """Calculate the area of a circle.

    Parameters
    ----------
    r : float or int
        Radius of the circle.

    Returns
    -------
    A : float
        Area of the circle.

    Raises
    ------
    TypeError
        If the radius is not a float or int
    ValueError
        If the radius is negative.

    """
    if not isinstance(r, (float, int)):
        raise TypeError("The radius has to be float.")
    if r < 0:
        raise ValueError("The radius cannot be negative.")

    return math.pi * r**2
```

Writing these kinds of tests incentivizes programmers to think about code modularization, programming towards cleaner interfaces (see {numref}`programming_principles`), and writing proper documentation (see {numref}`software_documentation`).
Tests are essential for ensuring a working code base and identifying problems when they occur.

In this project, tests for various functions can be found in the root directory of the *Git* repository.
Using *Github Actions*, these tests are automatically run whenever the code is updated (see also sections {numref}`version_control` and {numref}`ci_cd`).

By enforcing the "F.I.R.S.T." principles of testing, it can be ensured that the code is efficient, reliable, and maintainable.
Writing tests as an integral part of the development process helps to catch bugs early on and saves time in the long run.
