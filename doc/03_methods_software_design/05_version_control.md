(version_control)=
# Version control

% Requirements for version control
In scientific software development, code evolves continuously as models are refined, numerical methods are extended, and new features are added.
Keeping track of what changed, when, who made the change, and why quickly becomes difficult without systematic management of this history.
Authorship tracking is also relevant beyond debugging: in collaborative projects, a clear record of contributions matters for questions of credit, intellectual property, and patent claims (see {numref}`software_licenses`).
A version control system (VCS) addresses this by maintaining a structured history of commits, each recording a snapshot of the code alongside a message describing the change and its motivation.
Rather than commenting out deprecated code, developers can delete it outright and restore it from history if needed, keeping the codebase clean.
When a bug is introduced, the commit history makes it straightforward to pinpoint exactly when the regression appeared.
When code runs on multiple machines or is developed collaboratively, file-sharing tools like *Dropbox* or *Google Drive* quickly reach their limits: simultaneous edits cause conflicts, and there is no mechanism for maintaining stable and development versions in parallel.
A VCS handles all of this through a single, well-structured workflow.

## Version control systems

Version control systems start with a base version of the document and then record all subsequent changes as a sequence of commits.
Each developer works on a local copy of the project; once changes are complete, they are committed with a message describing what was changed and why, providing context for future readers.
The complete history of commits makes up a repository, which can be kept in sync across different machines to facilitate collaboration.

VCSs allow maintaining multiple versions of the code simultaneously through branches.
Branches enable developers to work on separate features without compromising the integrity of the master branch.
Different branches can be easily compared, and changes can be merged back into the master branch once a feature is complete.
Modern version control systems automatically merge changes from files edited simultaneously by different users and include tools to resolve conflicts when they arise.
Because of this, version control is most effective with text files, while its use with binary files, such as PDFs or JPGs, is limited.
However, solutions like large file storage (LFS) systems help mitigate some of these limitations.

VCSs have been in use since the early 1980s, with early systems like *RCS* and *CVS*.
*SVN* later introduced centralized server-based collaboration, while *Git*, developed by Linus Torvalds in 2005, introduced a fully distributed model in which every developer holds a complete copy of the repository.
According to Open Hub, *Git* has a market share of $\gt 70~\%$ {cite}`openhub` and is the system used for developing CADET-Process.

## Collaborative development

Modern VCS platforms such as *GitHub* or *GitLab* build on top of the core VCS functionality to support structured collaboration.
*Issues* provide a lightweight mechanism for reporting bugs, requesting features, or discussing proposed changes.
Each issue is tracked with a title, description, and status, and can be assigned to specific developers, labeled by category, and linked to the commits that resolve it.
*Pull requests* (PRs) extend this by providing a structured process for proposing and reviewing code changes before they are merged into the master branch.
A PR bundles a set of commits from a feature branch with a description of the changes and their motivation, and opens them for review by other contributors.
Reviewers can leave inline comments, request revisions, and approve the changes once satisfied.
In CADET-Process, every change to the codebase goes through a pull request, ensuring that new contributions are reviewed and automatically tested before they are merged (see {numref}`ci_cd`).
The repository is hosted on GitHub at https://github.com/fau-advanced-separations/CADET-Process.

## Software releases

While a VCS tracks every change to the source code, end-users typically do not interact with the full development history.
Instead, the development team periodically publishes *releases*: snapshots of the codebase that are considered stable and ready for general use.
In *Git*, a release is associated with a tag that marks a specific commit as a named, stable version.
These releases are published to package repositories such as *PyPI* (Python Package Index) or *conda-forge*, allowing users to install the software without needing access to the source code repository.
For example, CADET-Process can be installed with a single command that also resolves all dependencies automatically:

```bash
pip install cadet-process
```

To install a specific version, for instance to reproduce results from a previous study, the version number can be specified explicitly:

```bash
pip install cadet-process==0.11.1
```

Different conventions exist for naming releases.
One widely used scheme is *Semantic Versioning* {cite}`semantic`, which encodes the nature of changes in a three-component version number of the form MAJOR.MINOR.PATCH.
The MAJOR version is incremented when incompatible changes are made to the API, the MINOR version for backwards-compatible new functionality, and the PATCH version for backwards-compatible bug fixes.
From a user perspective, updating to a new PATCH or MINOR version is generally safe, whereas a new MAJOR version may require changes to existing scripts or workflows.

All releases of CADET-Process, together with a changelog describing new features or API changes, are published on GitHub (https://github.com/fau-advanced-separations/CADET-Process/releases) and on PyPI.
The release process itself is automated as part of the CI/CD pipeline, described in the following chapter.
