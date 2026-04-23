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

Object-oriented programming (OOP) aims to simplify software organization and structure while improving reusability, extendibility, and security.
In OOP, data and functionality are encapsulated into units called objects, which provide methods for accessing and modifying their associated data.
Objects are created from classes, which serve as blueprints defining the structure, properties, and methods of the object.

Four general principles characterize object oriented languages:

- *Inheritance* refers to a hierarchy in which subclasses inherit all procedures and data definitions of the parent class and can extend their functionality with additional attributes and methods. It enables the reuse of code and helps to organize classes in a logical manner.
- *Polymorphism* refers to the ability of objects to have different functionality while sharing a common interface. It enables code to be written in a more general way, making it easier to reuse and maintain.
- *Abstraction* refers to hiding internal complexity in the background and providing a simple interface that requires only essential information to use the class's functionality. It simplifies the use of complex functionality by providing only what is necessary for the user.
- *Encapsulation* refers to restricting access to certain properties and methods to ensure a consistent internal state of the object, preventing unintended side effects or errors. It enables developers to control how objects are used, providing security and reducing errors that can arise from unintended manipulation.

## Example

To demonstrate these principles, consider the `UnitOperationBase` class from CADET-Process, which defines the common interface for all unit operations.
Each unit operation must implement a method to compute the process residuals.
Note that this parent class does not actually implement the residual computations but instead, concrete subclasses must provide these methods.
This is *abstraction* in practice: a user interacting with any `UnitOperationBase` subclass only needs to know that it has parameters and can compute residuals, without needing to know the specific implementation details.
For this example, the programming language *Python3* is used.

```{code-cell} ipython3
import math
from abc import ABC, abstractmethod

class UnitOperationBase(ABC):
    """
    Base class for unit operation models.
    """

    def __init__(self, name: str, flow_rate: float):
        self.name = name
        self.flow_rate = flow_rate  # mL/min

    @abstractmethod
    def residual(self, state: float) -> float:
        """Residual of the unit operation model."""
        pass
```

By defining an abstract `UnitOperationBase` class with common attributes and methods, more specialized unit operation classes can inherit from it and share common functionality.
These child classes can add their own parameters and methods as needed to specialize their behavior.

```{code-cell} ipython3
class CSTR(UnitOperationBase):
    """
    Continuously stirred tank reactor.
    """

    def __init__(self, name: str, flow_rate: float, volume: float, c_in: float):
        super().__init__(name, flow_rate)
        self.volume = volume  # m^3
        self.c_in = c_in      # mol/m^3

    @property
    def tau(self) -> float:
        """Residence time in min."""
        return self.volume / self.flow_rate

    def residual(self, state: float) -> float:
        """Compute residuals for the CSTR."""
        c_out = state
        return self.flow_rate * (self.c_in - c_out)
```

The `CSTR` class inherits from `UnitOperationBase`, which defines the common interface for computing process residuals.
The concrete `CSTR` implementation adds its own parameters (`volume`, `c_in`) and implements the steady-state mass balance specific to a continuously stirred tank reactor.
This demonstrates *Polymorphism*: objects of different unit operation classes share a common interface (`UnitOperationBase`) but provide different behavior based on their specific model equations.
Different unit operations can therefore be treated interchangeably by the surrounding simulation code, making the framework modular and extensible.

The `@abstractmethod` decorator enforces that every subclass must implement `residual`, while the base class itself does not provide an implementation.
This encapsulates the model-specific computation within each subclass and ensures a consistent interface across all unit operations.

Now that the classes are defined, instances can be created and used as follows:

```{code-cell} ipython3
cstr = CSTR(name="reactor", flow_rate=1.0, volume=10.0, c_in=1.0)
print(cstr.tau)
print(cstr.residual(state=0.5))
```

```{code-cell} ipython3
fast_cstr = CSTR(name="reactor_fast", flow_rate=5.0, volume=10.0, c_in=1.0)
print(fast_cstr.tau)
print(fast_cstr.residual(state=0.5))
```

The objects `cstr` and `fast_cstr` are instances of the `CSTR` class.
They use the same class template but independently store their own parameter values, producing different residence times and residuals.

(type_annotations)=
## Type annotations

Type annotations, introduced in *PEP-484* {cite}`PEP484`, allow developers to declare the expected types of function arguments and return values directly in the function signature.
Building on the class definitions above, they serve as a precise specification of the interface contract: rather than relying on documentation or convention, the signature itself states what a method accepts and what it returns.

This is particularly valuable for abstract base classes.
In the `UnitOperationBase` example above, the annotation `-> float` on the abstract `residual` method makes the required contract of any subclass explicit:

```python
@abstractmethod
def residual(self, state: float) -> float:
    pass
```

A concrete subclass that returns an incorrect type (e.g., a string instead of a float) violates this contract, and tools such as *mypy* or *ruff* can detect this statically, before the code is even run.
Beyond abstract classes, annotations improve the readability of any method signature by making the expected input and output types immediately apparent without having to consult the implementation or documentation.
In CADET-Process, type annotations are enforced throughout the codebase and verified as part of the CI/CD pipeline (see {numref}`ci_cd`).

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
This pattern is useful when existing classes should be reused but their interfaces does not match the ones required.
In this work, an *Adapter Pattern* is used to translate the internal `Process` configuration into the API of an external simulator.

**Behavioral patterns** are a category of design patterns that focus on defining the interactions between objects and how they work together.
One of the most commonly used behavioral patterns is the Strategy pattern.
This pattern allows related algorithms for a particular action to be grouped under one abstraction, which can be switched out at runtime without modifying the client code.
The key to the Strategy pattern is the definition of a common interface or abstraction for a family of algorithms, which allows them to be used interchangeably while ensuring consistent behavior of the overall system.
An example of the Strategy pattern in CADET-Process is when different binding models are associated with unit operations.
In this case, the binding model is configured independently and then associated with the unit.
By defining a common interface for binding models, different models can be swapped in and out at runtime without affecting the behavior of the unit operation.
This results in a more flexible and maintainable codebase.

By applying established design patterns, software developers can create more adaptable and maintainable code that is more amenable to modifications and extensions over time.
However, it is important to note that design patterns are not a universal solution and their use should be carefully considered in each specific context.
Overusing design patterns can result in creating complex and less comprehensible code, which could impede software development and maintenance efforts.
Therefore, it is crucial for developers to strike a balance between leveraging design patterns and maintaining code simplicity and readability.

In CADET-Process, OOP principles are applied throughout the framework.
Unit operations, binding models, and optimization algorithms each share common base classes that define their interfaces, allowing them to be combined and exchanged without modifying the surrounding code.
This modularity is what enables the flexible process configurations described in {numref}`implementation`.
