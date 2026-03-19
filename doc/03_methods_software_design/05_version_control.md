(version_control)=
# Version control

% Requirements for version control
A version control system (VCS) is a software tool that allows developers to manage changes to source code.
There are several reasons why using a VCS is essential in software development.
First and foremost, it provides developers with access to the entire version history of a project.
This is crucial when introducing new features or improving existing code, which may involve deleting old or deprecated functionality.
With a VCS, developers can easily revert changes if files are accidentally deleted or if new development approaches turn out to be infeasible.
Instead of simply commenting out the code, which can severely impact readability, having the ability to restore older versions of a file or the entire code base increases the confidence of developers to experiment with alternative implementations while maintaining a clean and functional code base.

In addition, when fixing bugs, having access to a granular file history is important.
A common approach is to find the last working version of the code and then move forward through the changes to quickly pinpoint when issues were introduced.

Moreover, the need for VCSs emerges when code is used on multiple machines, such as a development PC and a server, or when other people start contributing to the code base.
Although file sharing solutions like *Dropbox* or *Google Drive* may initially work well, they are often limited in practice.
Issues arise as soon as the same files are edited by more than one person simultaneously or if changes are synchronized before they are finished.

Finally, managing multiple versions of the code is a challenge.
There are usually stable versions used in productive environments, such as a server running simulations, and development versions for work in progress, including bug fixes, new features, or experimental implementations.
However, applying an elaborate naming scheme for these different versions only works for small projects.
Keeping changes in sync becomes increasingly difficult as the project grows, emphasizing the importance of using a VCS to manage code versions effectively.

## Version control systems

Version control systems start with a base version of the document and then sequentially record all changes made.
The master copy of the code is never modified directly.
Instead, changes are made to a local copy of the project, and once they are completed, they are committed to the master copy.
Commit messages should include a description of the changes made and the reason for the modification to provide context for future readers.
This way, context is provided that helps the reader (often the same developer some time later) to follow the development history.
The complete history of commits for a project makes up a repository, which can be kept in sync across different computers, facilitating collaboration among different people.

VCS also allow maintaining multiple versions of the code simultaneously through branches.
Branches enable developers to work on separate features without compromising the integrity of the main branch, often called the master branch.
Different branches can be easily compared, and changes can be merged back into the main branch once a feature is complete.

Repositories enable synchronization across multiple computers, facilitating collaboration among teams.
Collaborators can update their local working copies to get current versions of the codebase.
Modern version control systems automatically merge changes from files edited simultaneously by different users and include tools to resolve conflicts when they arise.
Because of this, version control is most effective with text files, while its use with binary files, such as PDFs or JPGs, is limited.
However, solutions like large file storage (LFS) systems help mitigate some of these limitations.

VCS have been in use since the early 1980s, with early systems like *RCS* and *CVS*.
However, more modern systems like *Git* and *SVN* have become the new standard due to their distributed architecture and advanced features.
According to Open Hub, *Git* has a market share of $\gt 70~\%$ {cite}`openhub` and is also the system used in this work.

## Software releases

Although using a version control system is crucial for developing stable software, it may not be convenient for end-users.
Instead, it is useful to periodically create software releases - deployable software versions that are considered stable enough to be made available for a wider audience to download and use.
These versions can be deployed to package managers like *PyPI* or *conda*, making it easier to install the software.
For example, to install CADET-Process, users can use the following command which will automatically install the package along with all its dependencies:

```bash
pip install cadet-process
```

Different conventions exist for naming releases.
One commonly used scheme is called "Semantic Versioning" {cite}`semantic`.
Semantic Versioning is a three-component number in the format of MAJOR.MINOR.PATCH.
The MAJOR version number is incremented when incompatible changes are made to the API, the MINOR version number is incremented for backwards compatible functionality, and the PATCH version number is incremented for backwards compatible bug fixes.

All releases of CADET-Process can be found on *[GitHub](https://github.com/fau-advanced-separations/CADET-Process/releases)*.
The page also includes a changelog describing new features or changes in the API introduced with that version.
