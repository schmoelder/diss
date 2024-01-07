---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(programming_principles)=
# Programming principles

When writing code, it is crucial to consider the time and effort required to modify it, which often exceeds the time spent on writing the code in the first place.
Moreover, the context in which code is read can be vastly different from the one in which it was written.
Especially for collaborative projects where multiple developers work on the same codebase, as unclear code can lead to confusion and errors that can be difficult to fix.
In such cases, clear and concise code that is easy to understand and navigate becomes critical for maintaining code quality and ensuring its longevity.

To improve the readability and understandability of code, it is recommended to limit the amount of information necessary to understand a piece of logic, as human memory can only hold a handful of facts at a time {cite}`Baddeley2015`.
By adopting best practices such as modularization and documentation, developers can ensure that code remains understandable and maintainable over time.
Additionally, good coding practices can help prevent errors and facilitate testing, ultimately saving valuable time and resources in the long run.

There are multiple measures that can be taken to improve the quality of code, ranging from design patterns to coding standards.
In this chapter, we present some of the most important techniques, albeit this list is far from complete.
While these design patterns may aid the programmer in making informed decisions during development, there are always compromises and fair balances to be made.
Ultimately, the goal is to produce code that is maintainable, reliable, and efficient, while minimizing errors and maximizing productivity.

(sro)=
**Single responsibility principle**

Breaking down large programs into smaller, easily understood functions is an essential measure to ensure understandable and extendable code.
This approach is commonly referred to as the *Single Responsibility Principle*, which involves designing functions with a single, well-defined responsibility.
The *Unix philosophy* encapsulates this principle, advocating that each program should do one thing well and that the output of every program should become the input to another, as yet unknown, program {cite}`Raymond2003`.

Applying the *Single Responsibility Principle* not only improves the quality of code but also makes it easier to test functions, as will be discussed in {numref}`software_tests`.

(dry)=
**Don't repeat yourself**

Code duplication is a common issue in software development that can lead to maintenance problems when modifications have to be made to the duplicated logic.
To address this issue, developers should follow the "Don't Repeat Yourself" (DRY) principle, which recommends encapsulating common logic in functions or abstract interfaces and replacing all occurrences with function calls.
By doing so, modifications to the logic will be automatically reflected in all relevant places, reducing the risk of errors and inconsistencies.
As stated in the book "The Pragmatic Programmer", every piece of knowledge or logic should have a single, unambiguous representation within a system to avoid confusion and ensure maintainability {cite}`Hunt1999`.

(kiss)=
**KISS principle**

The "keep it simple, stupid" principle (KISS) is a fundamental principle of software development that encourages programmers to keep code as simple as possible.
This principle recognizes that often there are multiple ways to implement the same functionality.
Focusing on an implementation with the fewest lines of code, or maximum efficiency often sacrifices readability and increases complexity.
Instead, developers should strive to write clear, concise, and understandable code that is easy to maintain and modify over time.
Don Knuth famously wrote: "Premature optimization is the root of all evil." {cite}`Knuth1974`
Unless efficiency is critical, a suboptimal implementation will not severely affect the performance of the program but will make it harder to understand. Moreover, if a complicated function does more than one thing, it is more likely that at some point logic has to be reimplemented in another part of the code base, violating the DRY principle. Therefore, adhering to the KISS principle can greatly enhance the maintainability and extendability of code.

(interface_vs_implementation)=
**Program to the interface not to the implementation**

In software development, it is crucial to design flexible code to accommodate changes in requirements.
One technique for achieving this is to program to an interface, not to an implementation.

An interface can be thought of as an abstract representation of the behavior that a piece of code is supposed to exhibit.
It is a contract that specifies *what* a piece of code can do, but not *how* it does it.
An implementation, on the other hand, is the actual code that provides the behavior specified by the interface.

This technique allows for the creation of adaptable code, where different implementations providing the similar behavior can be easily substituted without the need to modify the code that depends on that behavior which promotes a clearer separation of concerns in the code.
By designing with interfaces, the code can focus on the essential behavior, making it easier to understand, maintain, and test.

(style)=
**Language and domain specific aspects**

In addition to syntax, every programming language has its own philosophy that users should adhere to.
Following these conventions enables better communication within the community.
When sharing code or seeking assistance, the coding style will be evaluated, even if the program produces correct results.

Guido van Rossum, the creator of the Python programming language, introduced a style guide with best practices and guidelines in the Python Enhancement Proposal 8 (*PEP-8*) {cite}`PEP8`.
*PEP-8* includes specific recommendations regarding naming conventions, whitespace, and other aspects of code formatting to promote consistency and readability.

Moreover, the "Zen of Python" was introduced in *PEP-20*, which includes 19 guiding principles for writing maintainable code {cite}`PEP20`:

1. Beautiful is better than ugly.
1. Explicit is better than implicit.
1. Simple is better than complex.
1. Complex is better than complicated.
1. Flat is better than nested.
1. Sparse is better than dense.
1. Readability counts.
1. Special cases aren't special enough to break the rules.
1. Although practicality beats purity.
1. Errors should never pass silently.
1. Unless explicitly silenced.
1. In the face of ambiguity, refuse the temptation to guess.
1. There should be one-- and preferably only one --obvious way to do it.
1. Although that way may not be obvious at first unless you're Dutch.
1. Now is better than never.
1. Although never is often better than *right* now.
1. If the implementation is hard to explain, it's a bad idea.
1. If the implementation is easy to explain, it may be a good idea.
1. Namespaces are one honking great idea -- let's do more of those!

While these principles serve as general guidelines, adhering to the specific coding conventions introduced in *PEP-8* are crucial to be followed to ensure consistency and readability.
To enforce these conventions when writing code, several tools and packages exist.
In this work, the [*pre-commit*](https://pre-commit.com/) package is utilized to automatically run scripts on every commit {cite}`precommit`.
During this process, the [*black*](https://black.readthedocs.io/en/stable/the_black_code_style/index.html) package auto-formats the code according to *PEP-8* guidelines {cite}`black`.
Finally, [*flake8*](https://flake8.pycqa.org/en/latest/) performs a final check on the code {cite}`flake8`.
These packages help ensure that the code adheres to *PEP-8* recommendations and is consistent in style and readability.
