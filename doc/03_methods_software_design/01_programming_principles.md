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

The time spent modifying an existing codebase typically far exceeds the time spent writing it in the first place.
Moreover, code is rarely read with the same context in which it was written: the design decisions, constraints, and goals that were clear to the author are not available to future readers, when collaborators or the even original author return to the code months later.
Clear, concise code that is easy to navigate is therefore essential for long-term maintainability.
A key strategy is to limit the amount of information required to understand any given piece of logic, as human working memory can hold only a handful of facts at a time {cite}`Baddeley2015`.
Practices such as modularization, clear naming, and documentation all serve this goal, and they simultaneously make code easier to test and less error-prone.
The following sections present some of the most widely applicable principles, drawn from software engineering practice and experience.

(sro)=
**Single responsibility principle**

Decomposing large programs into smaller, well-defined functions is the most direct way to make code understandable and extensible.
This approach is commonly referred to as the *Single Responsibility Principle*: each function or module should have exactly one reason to change.
The *Unix philosophy* captures the same idea concisely: "Write programs that do one thing and do it well" {cite}`Raymond2003`.
Beyond readability, the principle has a practical benefit: functions with a single responsibility are straightforward to test in isolation, as will be discussed in {numref}`software_tests`.

(dry)=
**Don't repeat yourself**

Code duplication is a common issue in software development that can lead to maintenance problems when modifications have to be made to the duplicated logic.
To address this issue, developers should follow the "Don't Repeat Yourself" (DRY) principle, which recommends encapsulating common logic in functions or abstract interfaces and replacing all occurrences with function calls.
By doing so, modifications to the logic will be automatically reflected in all relevant places, reducing the risk of errors and inconsistencies.
As formulated in "The Pragmatic Programmer": every piece of knowledge must have a single, unambiguous, authoritative representation within a system {cite}`Hunt1999`.

(kiss)=
**KISS principle**

The "keep it simple, stupid" principle (KISS) is a fundamental principle of software development that encourages programmers to keep code as simple as possible.
This principle recognizes that often there are multiple ways to implement the same functionality.
Focusing on an implementation with the fewest lines of code, or maximum efficiency often sacrifices readability and increases complexity.
Instead, developers should strive to write clear, concise, and understandable code that is easy to maintain and modify over time.
As Knuth famously observed, "premature optimization is the root of all evil" {cite}`Knuth1974`.
Unless efficiency is a genuine bottleneck, a simpler implementation is preferable: it will rarely affect overall performance significantly, but will be substantially easier to understand and modify.
Moreover, if a function does more than one thing, its logic is more likely to be reimplemented elsewhere in the codebase, violating the DRY principle.
Adhering to the KISS principle therefore enhances both maintainability and extensibility.

(interface_vs_implementation)=
**Program to the interface not to the implementation**

In software development, it is crucial to design flexible code to accommodate changes in requirements.
One technique for achieving this is to program to an interface, not to an implementation.
An interface can be thought of as an abstract representation of the behavior that a piece of code is supposed to exhibit.
It is a contract that specifies *what* a piece of code can do, but not *how* it does it.
An implementation, on the other hand, is the actual code that provides the behavior specified by the interface.
This allows different implementations with equivalent behavior to be substituted without modifying the surrounding code, promoting a clear separation of concerns.
By designing with interfaces, the code can focus on the essential behavior, making it easier to understand, maintain, and test.


(style)=
**Language and domain specific aspects**

In addition to syntax, every programming language has its own philosophy that users should adhere to.
Following these conventions enables better communication within the community.
When sharing code or seeking assistance, the coding style will be evaluated, even if the program produces correct results.

Guido van Rossum, the creator of the Python programming language, introduced a style guide with best practices and guidelines in the Python Enhancement Proposal 8 (*PEP-8*) {cite}`PEP8`.
*PEP-8* includes specific recommendations regarding naming conventions, whitespace, and other aspects of code formatting to promote consistency and readability.
Alongside *PEP-8*, the "Zen of Python" (*PEP-20*) condenses the same attitude into 19 aphorisms, several of which restate the principles discussed above in compressed form.
Their phrasing is deliberately light, and one entry is an in-joke about Van Rossum's Dutch nationality, but the collection is not decorative: it records the design consensus of the community that maintains the language, and it is the standard against which Python code is judged in review.

::::{container} zenquote
:::{line-block}
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one, and preferably only one, obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea; let's do more of those!
:::

— Tim Peters, *PEP 20: The Zen of Python* {cite}`PEP20`
::::

None of these principles is enforceable in the way a compiler enforces syntax.
They decide between implementations that are all technically correct, and they hold because the community applies them in review and in discussion, which makes them a matter of culture rather than of rules.
What can be checked mechanically is the narrower style layer of *PEP-8*, and several tools are available for it.
In this work, the *pre-commit* package is employed to automatically execute scripts on each commit {cite}`pre-commit`.
This includes using the *ruff* package to auto-format code according to *PEP-8* and to perform supplementary checks, such as verifying the presence of docstrings and type annotations {cite}`ruff`.
Together, these tools ensure that the codebase remains consistent in style, readable, and compliant with *PEP-8* recommendations.
The following chapter discusses how these principles are applied at a higher level of abstraction through object-oriented programming.
