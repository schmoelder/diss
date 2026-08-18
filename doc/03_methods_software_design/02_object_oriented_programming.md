---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

(oop)=
# Object oriented programming

The principles introduced in the previous section operate at the level of individual functions.
At a larger scale, object-oriented programming (OOP) provides a paradigm for structuring entire systems around objects, instances of classes that bundle data and behavior together, improving reusability, extensibility, and maintainability.
Classes serve as blueprints that define the structure, properties, and methods of their instances.

Four general principles characterize object oriented languages:

- *Inheritance* refers to a hierarchy in which subclasses inherit all attributes and methods of a parent class and can extend them with additional functionality.
  This promotes code reuse and helps organize classes in a logical hierarchy.
- *Polymorphism* refers to the ability of objects from different classes to share a common interface while providing different behavior.
  Code can thus be written against a common interface rather than specific implementations, improving reuse and maintainability.
- *Abstraction* refers to exposing only the essential interface of a class while hiding its internal implementation details.
  This simplifies both human usage and programmatic interaction, as callers need only know what a class can do, not how it does it.
- *Encapsulation* refers to restricting direct access to an object's internal state, exposing it only through defined methods.
  This prevents unintended manipulation and reduces errors arising from uncontrolled access to internal data.

## OOP-Example

To demonstrate these principles, consider an illustrative `UnitOperationBase` class, inspired by the structure of unit operations in CADET-Process and implemented in Python, which is also used throughout the framework.
The class defines a common interface: every unit operation has a name and must be able to compute its residual.
This is *abstraction* in practice: any code interacting with a `UnitOperationBase` subclass only needs to know that it can compute residuals, without needing to know the specific implementation details.
The code also includes docstrings, which document the interface contract and are discussed in detail in {numref}`software_documentation`.

```{code-cell} ipython3
import math
from abc import ABC, abstractmethod

class UnitOperationBase(ABC):
    """Base class for unit operation models."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def residual(self, state: float, flow_rate: float, c_in: float) -> float:
        """Compute the residual of the unit operation model.

        Parameters
        ----------
        state
            Current internal concentration in mol/m^3.
        flow_rate
            Volumetric flow rate in m^3/s.
        c_in
            Inlet concentration in mol/m^3.

        Returns
        -------
        float
            Residual of the mass balance.
        """
        pass
```

By defining an abstract `UnitOperationBase` class, more specialized unit operation classes can inherit from it and extend it with model-specific parameters and behavior.

```{code-cell} ipython3
class CSTR(UnitOperationBase):
    """
    Continuously stirred tank reactor.
    """

    def __init__(self, name: str, v_init: float, c_init: float):
        """
        Parameters
        ----------
        name
            Name of the unit operation.
        v_init
            Initial volume in m^3.
        c_init
            Initial concentration in mol/m^3.
        """
        super().__init__(name)
        self.v_init = v_init
        self.c_init = c_init

    def residual(self, state: float, flow_rate: float, c_in: float) -> float:
        """Compute residual of the CSTR mass balance with constant volume.

        Parameters
        ----------
        state
            Current concentration in mol/m^3.
        flow_rate
            Volumetric flow rate in m^3/s.
        c_in
            Inlet concentration in mol/m^3.

        Returns
        -------
        float
            Residual of the CSTR mass balance.
        """
        c = state
        return flow_rate * (c_in - c)
```

The `CSTR` class inherits from `UnitOperationBase`, which defines the common interface for all unit operations.
Its `__init__` method calls `super().__init__()` to delegate initialization of the shared `name` attribute to the parent class, and stores `v_init` and `c_init` as fixed model parameters.
Time-varying inputs (`flow_rate` and `c_in`) are passed directly to `residual` at each evaluation, reflecting that these quantities can change over the course of a simulation.
Inside `residual`, `c = state` identifies the internal state variable as the current concentration, and the CSTR mass balance is evaluated accordingly.
This demonstrates *Polymorphism*: while only one subclass is shown here, any number of unit operation classes — each implementing a different physical model — can share the same `UnitOperationBase` interface and be treated interchangeably by the surrounding simulation code.
The `@abstractmethod` decorator enforces that every subclass must implement `residual`, while the base class itself does not provide an implementation.
This encapsulates the model-specific computation within each subclass and ensures a consistent interface across all unit operations.
```{raw} latex
\needspace{6\baselineskip}
```
With the class hierarchy defined, a `CSTR` can be instantiated and its residual evaluated:

```{code-cell} ipython3
cstr = CSTR(name="reactor", v_init=10.0, c_init=0.0)
print(cstr.residual(state=0.5, flow_rate=1.0, c_in=1.0))
```

```{code-cell} ipython3
large_cstr = CSTR(name="large_reactor", v_init=50.0, c_init=0.0)
print(large_cstr.residual(state=0.5, flow_rate=1.0, c_in=1.0))
```

The objects `cstr` and `large_cstr` are instances of the same `CSTR` class but store different initial volumes, while receiving the same time-varying inputs at evaluation time.

(uml)=
## UML class diagrams

Object-oriented designs are commonly visualized using *Unified Modeling Language* (UML) class diagrams, which provide a standardized notation for classes, their attributes and methods, and the relationships between them {cite}`Rumbaugh2010`.
{numref}`uml_unit_operation_oop` shows the diagram for the example above.
Attributes are listed with their types, reflecting the type annotations in the code; visibility may optionally be indicated using UML conventions (e.g. `+` for public, `-` for private), though this distinction is less strict in Python.
More complex diagrams additionally include associations, aggregations, or compositions, which are omitted here for clarity.
This pattern of abstract base classes and concrete subclasses recurs throughout CADET-Process, and UML diagrams are used in {numref}`implementation` to document its architecture.

```{figure} ./figures/uml_unit_operation.png
:name: uml_unit_operation_oop
:width: 45%

UML class diagram of `UnitOperationBase` and `CSTR`.
The abstract base class defines the common interface; `CSTR` inherits from it and adds model-specific parameters.
```

(type_annotations)=
## Type annotations

Type annotations, introduced in *PEP-484* {cite}`PEP484`, allow developers to declare the expected types of function arguments and return values directly in the function signature.
Building on the class definitions above, they serve as a precise specification of the interface contract: rather than relying on documentation or convention, the signature itself states what a method accepts and what it returns.
This is particularly valuable for abstract base classes.
In the `UnitOperationBase` example above, the annotation `-> float` on the abstract `residual` method makes the required contract of any subclass explicit:

```python
@abstractmethod
def residual(self, state: float, flow_rate: float, c_in: float) -> float:
    pass
```

A concrete subclass that returns an incorrect type (e.g., a string instead of a float) violates this contract, and tools such as *mypy* or *ruff* can detect this statically, before the code is even run.
Note that Python does not enforce type annotations at runtime; they are a static analysis aid, particularly valuable in IDEs and CI pipelines.
Beyond abstract classes, annotations improve the readability of any method signature by making the expected input and output types immediately apparent without having to consult the implementation or documentation.
In CADET-Process, type annotations are enforced throughout the codebase and verified as part of the CI/CD pipeline (see {numref}`ci_cd`).

(design_patterns)=
## Design patterns

Design patterns are a set of solutions to recurring software design problems, and they provide best practices and templates for designing flexible, reusable, and maintainable code.
Since these patterns are programming language agnostic, they provide a shared vocabulary and best practices for solving common problems in software design {cite}`Gamma1994`.
While there are dozens of different design patterns, they can be grouped into three categories: Creational, Structural, and Behavioral patterns.

**Creational patterns** are patterns that provide various object creation mechanisms, which increase flexibility and reuse of existing code.
The *Factory method* is an example of a creational design pattern that separates the process of object creation from the code that uses the objects when the exact types and dependencies of the objects are not known beforehand.
It is often used when the process of object creation is complex and requires different steps or when objects are created dynamically.
For example, CADET-Process provides a {class}`~CADETProcess.modelBuilder.CarouselBuilder` class which facilitates the creation of complex multi-column processes.

**Structural patterns** are patterns that deal with object composition and allow developers to create more complex objects by combining simpler ones.
For example, the *Adapter pattern* is a structural design pattern that allows incompatible classes to work together by implementing a converter acting as a translator which enables communication without having to change the classes themselves.
This pattern is useful when existing classes should be reused but their interfaces do not match the ones required.
In this work, an *Adapter pattern* is used to translate the internal `Process` configuration into the API of an external simulator.

**Behavioral patterns** are a category of design patterns that focus on defining the interactions between objects and how they work together.
One of the most commonly used behavioral patterns is the Strategy pattern.
This pattern allows related algorithms for a particular action to be grouped under one abstraction, which can be switched out at runtime without modifying the client code.
The key to the Strategy pattern is the definition of a common interface or abstraction for a family of algorithms, which allows them to be used interchangeably while ensuring consistent behavior of the overall system.
In CADET-Process, binding models are an example of the Strategy pattern: each binding model implements a common interface (computing the adsorption isotherm), and any binding model can be assigned to a unit operation and swapped at runtime without modifying the unit operation itself.
This decoupling is precisely what makes the framework extensible — adding a new isotherm model requires no changes to the surrounding transport equations.

Design patterns are not a universal solution: overuse leads to unnecessary abstraction that obscures rather than clarifies, and a balance with the KISS principle is crucial.
In CADET-Process, this balance is reflected in how OOP principles are applied: unit operations, binding models, and optimization algorithms each share common base classes that define their interfaces, allowing them to be combined and exchanged without modifying the surrounding code, as described in {numref}`implementation`.
