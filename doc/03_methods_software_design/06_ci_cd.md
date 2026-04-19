(ci_cd)=
# Continuous Integration/Continuous Deployment

Continuous Integration/Continuous Deployment (CI/CD) is a software development methodology that enables teams to build, test, and deploy code changes more quickly and reliably.
By automating the process of merging new code into the main development branch, formatting standards are enforced, and the software's functionality is verified through automated testing, which helps to identify issues early on and speeds up the release cycle.

In practice, services like [*Github Actions*](https://github.com/features/actions) or [*Travis CI*](https://www.travis-ci.com/) can be used to automate the CI/CD process.
For example, in CADET-Process, *Github Actions* is used to enforce formatting, run tests, and update documentation for every commit.
Additionally, a new version is uploaded to the *Python Package Index (PyPI)* for every release, enabling users to easily install and use the latest version of the software.

By automating the build, test, and deployment process, CI/CD makes it easier to detect and fix bugs, ensure consistency across the codebase, and reduce the time and effort required to release new software versions.
It also increases productivity, as developers can focus on writing code rather than manually managing the build and deployment process.
