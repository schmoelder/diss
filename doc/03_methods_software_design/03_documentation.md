(software_documentation)=
# Documentation

Documentation makes software accessible: it communicates the purpose of a codebase, explains design decisions, and describes how components fit together and how to use the provided interfaces.
Documentation that merely restates what the code does is of limited value; what matters is the context and reasoning that the code itself cannot express.
If code is too complex to document clearly, this is a signal to simplify it first (see {numref}`programming_principles`).
Effective documentation also extends beyond the API: user manuals, installation guides, and tutorials are essential for onboarding new users.
The following sections discuss docstrings, Python's built-in mechanism for embedding documentation in source code, and Sphinx, a tool for generating reference documentation from them {cite}`sphinx`.

Documentation makes software accessible: it communicates the purpose of a codebase, explains design decisions, and describes how components fit together and how to use the provided interfaces.
Documentation that merely restates what the code does is of limited value; what matters is the context and reasoning that the code itself cannot express.
If code is too complex to document clearly, that is a signal to simplify first (see {numref}`programming_principles`).
Good documentation also extends beyond the API: user manuals, installation guides, and tutorials are essential for making software accessible to new users.
The following sections discuss docstrings, Python's built-in mechanism for embedding documentation in source code, and Sphinx, a tool used to generate reference documentation from them {cite}`sphinx`.

## Docstrings

Most programming languages have conventions for writing string literals in the source code that can be used to document a specific segment of code.
In Python, docstrings are string literals placed at the beginning of a module, class, or function that serve as its documentation.
Unlike regular comments, docstrings are retained at runtime and accessible via the `__doc__` attribute, enabling interactive help systems and documentation generators.
Their conventions are defined in *PEP-257* {cite}`PEP257`.
A one-line summary should first provide a brief description of the corresponding source code.
Relevant details of the code segment are then described in subsequent sections.
In the following, some of the most important sections are presented using *Numpy*'s formatting convention {cite}`numpy_docstring`:

**Parameters**

Description of the function arguments and their semantic meaning.
When type annotations are present in the function signature (see {numref}`type_annotations`), the type does not need to be repeated here.

```
Parameters
----------
state
    Current concentration in mol/m^3.
flow_rate
    Volumetric flow rate in m^3/s.
c_in
    Inlet concentration in mol/m^3.
```

**Returns**

Description of the return value and its type.

```
Returns
-------
float
    Residual of the mass balance.
```

**Raises**

Details on which errors get raised and under what conditions:

```
Raises
------
ValueError
    If the argument has an invalid value.
```

The examples above correspond directly to the `residual` method of the `CSTR` class introduced in {numref}`oop`.
In addition to these sections, docstrings commonly include "See Also" for related code, "References" for literature citations, "Examples" for usage demonstrations, and "Notes" for supplementary remarks.

## Documentation generator tools

*Sphinx* is a documentation generator widely used in the Python community that extracts docstrings from source code and produces reference manuals in formats such as HTML or PDF.
It can be customized with themes and extensions to embed images, diagrams, and mathematical notation.
Its *autodoc* extension reads type annotations (see {numref}`type_annotations`) directly from the source code, integrating them into the generated reference documentation without manual duplication.

By combining background information, tutorials, and advanced examples with the extracted docstrings, these reference manuals become a useful starting point for new users.
*Sphinx* integrates naturally with Read The Docs, an online platform for hosting and publishing documentation: https://readthedocs.org.
In CADET-Process, all public classes and functions include docstrings following the NumPy convention, and the reference documentation is hosted at https://cadet-process.readthedocs.io and automatically rebuilt whenever changes are made to the source code (see {numref}`ci_cd`).
