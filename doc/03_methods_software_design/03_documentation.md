(software_documentation)=
# Documentation

Extensive documentation is a crucial aspect of software development that enhances the maintainability and reusability of code.
However, documentation that simply restates the mechanics of the code is of limited use.
Instead, documentation should provide an overview of the code's purpose and instructions on its usage, including explanations of design decisions, architectural structures, and interfaces.
It is important to note that if the code is too complex, it should be simplified before documentation is added (see {numref}`programming_principles`).
Good documentation should also include user manuals with installation instructions, tutorials for beginners, and troubleshooting guides.
By following these documentation practices, developers can create software that is more easily understandable, maintainable, and reusable.

In the following sections, the usage of docstrings in Python to document functions, classes, and modules will be discussed.
Docstrings are special string literals that can be used to provide documentation for Python code.
Additionally, the usage of documentation generation tools like Sphinx to automatically generate documentation from docstrings will be covered.

## Docstrings

Most programming languages have conventions for writing string literals in the source code that can be used to document a specific segment of code.
Unlike conventional source code comments, docstrings are retained throughout the runtime of the program and can be used for interactive help systems.
In Python, docstrings conventions were defined with *PEP-257* {cite}`PEP257`, which specifies how modules, functions, classes, or methods should be documented so they can be accessed with the special `__doc__` attribute of that object.

There are several conventions for structuring docstrings into sections that describe different aspects of the function.
To structure docstrings into sections that describe different aspects of a function, a one-line summary should first provide a brief description of the corresponding source code.
Relevant details of the code segment are then described in subsequent sections.
In the following, some of the most important sections are presented using *Numpy*'s formatting convention {cite}`numpy_docstring`.

**Parameters**

Description of the function arguments, keywords and their respective types.

```
Parameters
----------
x : type
    Description of parameter `x`.
y
    Description of parameter `y` (with type not specified).

```

**Returns**

Explanation of the returned values and their types.

```
Returns
-------
int
    Description of integer return value.
```

**Raises**

Details on which errors get raised and under what conditions:

```
Raises
------
ValueError
    If value has an invalid value.
```

In addition to the previously mentioned sections, there are several other commonly used sections in docstrings.
The "See Also" section is used to reference related code, while the "References" section is used for citing relevant literature.
The "Examples" section is used to provide usage examples of the code segment, and the "Notes" section can be used for additional explanation or comments related to the code.

## Documentation generator tools

In order to make the documentation readily available for both developers and users, documentation generator tools such as *Sphinx* have been developed to extract the docstrings from the source code and create reference manuals in readable forms such as HTML or PDF.
*Sphinx* is widely used in the Python community and allows for the creation of rich and informative documentation.
*Sphinx* can be customized with themes and extensions, enabling the embedding of additional materials such as images, diagrams, and mathematical notation to enhance the comprehensiveness of the documentation.

By combining background information, tutorials, and advanced examples with the extracted docstrings, these reference manuals become a useful starting point for new users of a software package.
For example, in the case of **CADET-Process**, the documentation can be found on [Read The Docs](https://readthedocs.org/projects/cadet-process), an online platform for hosting and publishing software documentation that also supports *Sphinx*.
The documentation is automatically updated when changes are made to the source code, ensuring that the documentation is always up-to-date and accurate (see {numref}`section %s<ci_cd>`).
This makes it easier for both new and experienced users to access the information they need, ultimately leading to better code quality and more efficient development.
