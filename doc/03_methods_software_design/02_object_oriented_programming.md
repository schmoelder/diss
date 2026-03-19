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

- *Inheritance* refers to a hierarchy in which subclasses inherit all procedures and data definitions of the parent class and can extend their functionality with additional properties and methods. It enables the reuse of code and helps to organize classes in a logical manner.
- *Polymorphism* refers to the ability of objects to have different functionality while sharing a common interface. It enables code to be written in a more general way, making it easier to reuse and maintain.
- *Abstraction* refers to hiding internal complexity in the background and providing a simple interface that requires only essential information to use the class's functionality. It simplifies the use of complex functionality by providing only what is necessary for the user.
- *Encapsulation* refers to restricting access to certain properties and methods to ensure a consistent internal state of the object, preventing unintended side effects or errors. It enables developers to control how objects are used, providing security and reducing errors that can arise from unintended manipulation.

## Example

To demonstrate these principles, consider a generic `Shape` class which defines that an object of this type has a `color` attribute, as well as two getter functions for accessing the values of its `area` and `perimeter`.
Note that this parent class does not actually implement any methods but instead, the `area` and `perimeter` methods have to be provided by concrete implementations (i.e. sub-classes) of the interface.
For this example, the programming language *Python3* is used.

```{code-cell} ipython3
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    def __init__(self, color):
        self.color = color

    @property
    @abstractmethod
    def area(self):
        pass

    @property
    @abstractmethod
    def perimeter(self):
        pass

```

By defining an abstract `Shape` class with common attributes and methods, more specialized classes can inherit from `Shape` and share common functionality.
These child classes can add their own attributes and methods as needed to specialize their behavior.

```{code-cell} ipython3
class Circle(Shape):
    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius**2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, length, width, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.length = length
        self.width = width

    @property
    def area(self):
        return self.length * self.width

    @property
    def perimeter(self):
        return 2 * (self.length + self.width)
```

`Circle` and `Rectangle` both inherit from `Shape`, which already provides a common interface for accessing the `color`, `area`, and `perimeter` attributes.
To correctly compute `area` and `perimeter`, specific attributes are used (e.g. `radius` for `Circle`, `width` and `height` for `Rectangle`) to ensure that the correct value is always returned, even if the value of the specific attributes changes.
This also demonstrates the principle of *Polymorphism*, where objects of different classes can share a common interface (in this case, the `Shape` class) but have different behavior based on their specific attributes and methods.
This simplifies the code and makes it more modular, as objects of different classes can be treated as if they were the same type of object, thanks to inheritance.

The `@property` decorator is used to define the `area` attribute as an abstract read-only property in the `Shape` class and as concrete read-only properties in the `Circle` and `Rectangle` classes.
This encapsulates the computation of the area attribute within each class and restricts access to it in a controlled way.
By using `@property`, read-only properties can be defined that can be accessed using dot notation, as if they were instance variables.
However, setting these values is restricted which helps to ensure that the `Shape` object remains in a consistent and valid state, and reduces the risk of errors or unexpected behavior.

Now that the classes are defined, instances of these classes can be instantiated and

```{code-cell} ipython3
circle = Circle(radius=1, color='red')
print(circle.color)
print(circle.area)
```

```{code-cell} ipython3
another_circle = Circle(radius=2, color='blue')
print(another_circle.color)
print(another_circle.area)
```

```{code-cell} ipython3
rectangle = Rectangle(length=2, width=1, color='black')
print(rectangle.color)
print(rectangle.area)
print(rectangle.perimeter)
```

The objects `circle` and `another_circle` are instances of the `Circle` class; `rectangle` is an instance of a `Rectangle`.
They use the class templates that were previously defined and independently store values of their properties.

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
