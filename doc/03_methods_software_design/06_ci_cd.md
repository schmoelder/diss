(ci_cd)=
# Continuous Integration/Continuous Deployment

As software projects grow, manually verifying that every change leaves the codebase in a working state becomes impractical.
Continuous Integration/Continuous Deployment (CI/CD) addresses this by automating the processes of validation and delivery through two complementary practices.
*Continuous Integration* (CI) refers to the automatic building and testing of the codebase on every push to a pull request, allowing issues to be identified and resolved before changes are merged into the master branch.
*Continuous Deployment* (CD) extends this by automatically deploying tested, release-ready code to end-users, for example by publishing a new package version to a package repository.

In practice, services like [*Github Actions*](https://github.com/features/actions) or [*Travis CI*](https://www.travis-ci.com/) can be used to automate the CI/CD process by defining workflows that are triggered by specific events such as pull requests or releases.
In CADET-Process, *Github Actions* is used to implement the following pipeline:

- On every pull request push: code formatting, the presence of docstrings, and type annotations are checked and enforced using *pre-commit* and *ruff* (see {ref}`Language and domain specific aspects <style>` and {numref}`software_documentation`), and the test suite is executed using *pytest* (see {numref}`software_tests`).
- On every release: the reference documentation is rebuilt and published via *Sphinx* and Read The Docs (see {numref}`software_documentation`), and the package is uploaded to the *Python Package Index (PyPI)*, making the new version immediately available for installation (see {numref}`version_control`).

By automating both validation and delivery, the pipeline ensures that no change reaches the master branch without passing all quality checks, and that every release corresponds to a fully tested, documented state of the codebase.
The following chapter discusses software licensing, which determines under what conditions this software may be used and distributed by others.
