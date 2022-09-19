---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python [conda env:se-for-sci] *
  language: python
  name: conda-env-se-for-sci-py
---

# Object Oriented Design

## Intro

Let's define some terminology we've been seeing, along with a bit of new stuff:

- **Encapsulation** (meaning 1): The idea of bundling data & operations together
  under one roof.
- **Encapsulation** (meaning 2): Isolating the implementation and only providing
  access to a minimal "public" part.
- **Object** or **instance** -- A variable holding data with a type holding
  functions.
- **Attribute**: Something accessible on an object.
- **Member**: A data attribute stored in each object.
- **Method**/**Member function**: A callable attribute stored in a class and
  callable from an object
- **Constructor**/**Initializer**: A function that creates instances of a class
- **Destructor**: A function that runs with an instance is destroyed. Much more
  interesting in non-garbaged collected languages (C++); they tend to be rather
  useless when combined with a garbage collector, because you can't guarantee
  when or if they will be called.
- **Inheritance**: When one class uses another as a starting point, and just
  **extends** by adding or **overrides** existing methods.
- **Composition** (meaning 1): Adding instances of classes as members of a new
  class.
- **Composition** (meaning 2): Combining non-overlapping classes via multiple
  inheritance.
- **Interface**: A collection of methods/members that need to be provided in
  order to be used.

### Why should we use classes and objects?

- Pass around and keep related values together.
- **Inheritance** and **Composition** can be used to keep code DRY.
- Clean way to establish interfaces (via Abstract Base Classes (ABCs) or
  Protocols (see static typing))

```{admonition} Interfaces
Python refers to an Interface (Java terminology, technically) as a Protocol. C++20
calls it a Concept. The basic idea is simply that a set of methods/members are
required in order for a class to be used, without requiring formal inheritance.
We'll save this until we look at static typing, however.
```

### Why Inheritance?

If you want two classes both to have a set of data or methods specified by the
same code, you can put the code in class A and have class B "inherit" that code.
We then say that A is the **parent class** or **super class** of B, and that B
is the child class or subclass of A.

- Provides the concept of "is a" (`isinstance` / `issubclass` in Python).
- Provides a way to "Realize" or "Implement" a specified interface (ABC or
  Protocol).

For example, in `content/week3/geom_example/geometry/classic.py`, `Shape` is a
base class with `area()` and `parameter()` methods. It doesn't know how to
compute those - they are abstract. This means you can't instantiate `Shape()`,
doing so would give you an error (from the `abc` module). However, the
subclasses of `Shape` like `Rectangle` and `Circle` do know how to compute this,
so they can be instantiated.

When you use it, you can take any concrete (no abstract methods left) subclass
of `Shape`. Again, when we get to static typing, we'll learn how to formalize
this, for now, we have to trust duck typing and willpower to avoid using
anything that's not in `Shape` when we accept it as an argument.

### Why Composition/Aggregation?

- Provides the concept of "has a", or "inherent part of". `Kidney` is a part of
  `Human`, for example.
- **Composition** is generally when the contained object's lifetime is tied to
  the parent object (one can't exist without the other). **Aggregation** is more
  "has a" or "is in a"; like Ducks in a Pond. The Pond can dry up and the Ducks
  persist, and the Ducks can move between Ponds.

You can use composition as a replacement for inheritance in some cases. For
example, in our geometry example, we could have made Square inherit from Shape
instead, and hold a Rectangle as an attribute, and then use that Rectangle to
compute the methods of the Square. The benefit is that we now control the
interface Square provides completely; adding something to Rectangle does not add
it to Square unless we also wrap it there. For this case, it's not a great
design, but imagine if Rectangle was from somewhere we didn't control (and if
square was not as conceptually a variation of a rectangle is it really is!).

An important contributor to designing good classes is this: A child class cannot
remove attributes from a parent. It can override them or add new ones, but not
remove. Be very careful if you are exposing more public API than you want to!

### UML diagrams

UML, or Unified Modeling Language, is a method of displaying class diagrams
[(read more here)](https://www.lucidchart.com/pages/what-is-UML-unified-modeling-language).
Let's see what our simple Geom example looks like:

```{mermaid}
classDiagram
    Shape <|-- Rectangle
    Rectangle <|-- Square
    Shape <|-- Triangle
    Shape <|-- Circle
    class Shape {
        +area()* float
        +parameter()* float
    }
    class Rectangle {
        +height: float
        +width: float
        +area() float
        +parameter() float
    }
    class Triangle {
        +a float
        +b float
        +c float
        +area() float
        +parameter() float
    }
    class Circle {
        +radius float
        +area() float
        +parameter() float
    }
    class Square {
        +side: float
    }
```

All the supported relationships are:

```{mermaid}
classDiagram
    classA --|> classB : Inheritance
    classC --* classD : Composition
    classE --o classF : Aggregation
    classG --> classH : Association
    classI -- classJ : Link(Solid)
    classK ..> classL : Dependency
    classM ..|> classN : Realization
    classO .. classP : Link(Dashed)
```

## Design principles

### Provide minimal public API

You should try to limit the Public API as much as possible. Everything you add
as public API means something someone might depend on and something you can't
easily refactor. Some languages provide ways to forcibly lock down access;
Python only provides convention with an `_` at the start of names, but that's
fine - use it.

In some languages, you should avoid/limit direct access to members, as this
could limit you from ever adding an operation that occurs when setting or
getting that value. This is _not_ an issue with Python, since the following
class:

```{code-cell} python3
class Container:
    def __init__(self, x):
        self.x = x

c = Container(1)
print(f"{c.x = }")
c.x = 2
print(f"{c.x = }")
```

Can be refactored and still provide the same user API:

```{code-cell} python3
class Container:
    def __init__(self, x):
        self._x = x

    @property
    def x(self):
        print("Accessing x")
        return self._x

    @x.setter
    def x(self, value):
        print("Setting x")
        self._x = value

c = Container(1)
print(f"{c.x = }")
c.x = 2
print(f"{c.x = }")
```

## Object Oriented Programming design patterns

The following are a collection of design patterns for OOP.

### Code reuse

This is not the most common use, but is a really simple one, so let's start with
it.

If we have some code that has many steps:

```{code-cell} python3
class SteppedCode:
    def step_1(self):
        print("Working on step 1")
    def step_2(self):
        print("Working on step 2")
    def step_3(self):
        print("Working on step 3")
    def run(self):
        self.step_1()
        self.step_2()
        self.step_3()

SteppedCode().run()
```

You can then use inheritance to swap out arbitrary steps:

```{code-cell} python3
class NewSteps(SteppedCode):
    def step_2(self):
        print("Replaced step 2")

NewSteps().run()
```

We can also inject code around a step:

```{code-cell} python3
class SurroundedSteps(SteppedCode):
    def step_2(self):
        print("Before step 2")
        super().step_2()
        print("After step 2")

SurroundedSteps().run()
```

Real code likely will pass values around or use class attributes, but the idea
remains. That leads into the next, more common pattern.

### Required interface

This allows you to request a user specify an interface to use your code. For
example:

#### integrator_example/integrator/**init**.py

```{literalinclude} ./integrator_example/integrator/__init__.py
:language: python
:end-before: class EulerIntegrator(IntegratorBase)
```

To implement an integrator, we have to provide `compute_step`:

```{literalinclude} ./integrator_example/integrator/__init__.py
:language: python
:start-at: class EulerIntegrator(IntegratorBase)
:end-before: class RK4Integrator(IntegratorBase)
```

We can implement more:

```{literalinclude} ./integrator_example/integrator/__init__.py
:language: python
:start-at: class RK4Integrator(IntegratorBase)
```

Now we can use it:

```{code-cell} ipython3
:tags: [hide-cell]

import sys
sys.path.append("integrator_example")
```

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np

from integrator import EulerIntegrator, RK4Integrator


def f(t, y):
    "Y has two elements, x and v"
    return np.array([-1 * y[1], y[0]])

ts = np.linspace(0, 40, 1000 + 1)
euler = EulerIntegrator()
y_euler = euler.integrate(f, [1, 0], ts)
rk4 = RK4Integrator()
y_rk4 = rk4.integrate(f, [1, 0], ts)

fig, ax = plt.subplots()
ax.plot(ts, y_euler[:, 0], "--", label="Euler")
ax.plot(ts, y_rk4[:, 0], ":", lw=5, label="RK4")
ax.plot(ts, np.cos(ts), label="Analytical")
ax.legend()
plt.show()
```

### Separation of concerns

### Overloading

### Mixins
