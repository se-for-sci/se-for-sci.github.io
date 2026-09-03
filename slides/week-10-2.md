---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Object Oriented Programming

---

## Why design classes?

We want an interface that is:

- Easy to use correctly
- Hard to use incorrectly

We don't want to give up on our principles, like _modularity_!

You absolutely can design a spaghetti mess of code with OOP!

---

- **Encapsulation** (1): Bundling data & operations together
- **Encapsulation** (2): Isolating implementation & minimal public part
- **Object**/**Instance**: A variable holding data with a type holding
- **Attribute**/**Property**: Something accessible on an object
- **Member**: A data attribute stored in each object
- **Method**/**Member function**: A callable attribute stored in a class
- **Constructor**/**Initializer**: A function that creates instances
- **Destructor**: A function that runs when an instance is destroyed
- **Inheritance**: When one class uses another as a starting point
- **Composition** (1): Adding instances of classes as members
- **Composition** (2): Combining classes via multiple inheritance

---

## Why use classes?

- Keep related values tother
- **Inheritance** and **Composition** can be used to keep code DRY
- Clean way to establish interfaces (ABCs/Protocols)
- Ensure required code is run
- Associate functions to a specific type (varies by language)

---

## Why inheritance?

A: **Parent class** / **super class** B: **Child class**

```python
class A:
    pass


class B(A):
    pass
```

- Provides the concept of "is a" (`isinstance` / `issubclass` in Python)
- Provides a way to "realize" or "implement" a specified interface

---

## Why composition/aggregation?

```python
class A:
    pass


class B:
    def __init__(self):
        self.a = A()
```

- Provides the concept of "has a", or "inherent part of".
- **Composition**: contained object's lifetime is tied to the parent
- **Aggregation** parent holds objects, but they exist separately too
- "Wrapped" class can re-expose (some) of contained methods (remember inheritance can't remove attributes!)

---

## UML diagrams

UML, or Unified Modeling Language, is a method of displaying class diagrams [(read more here)](https://www.lucidchart.com/pages/what-is-UML-unified-modeling-language), or read about it for [mermaid](https://mermaid-js.github.io/mermaid/#/classDiagram), which is supported quite a lot of places these days, including GitHub.

---

## SOLID

- **S**ingle responsibility: classes should do one thing (modular)
- **O**pen-closed principle: API stable (closed) but extensible (open)
- **L**iskov substitution: children work where parents expected
- **I**nterfaces should be specific and segregated
- **D**ependency inversion
  - High level code _should not_ depend on low level code details
  - Low level code _should_ depend on high level abstractions

---

## Interfaces example

- Xerox makes a mutlifunction machine
  - `Stapler` and `Printer` are subclasses of `Job`
  - `Job` holds _everything_ for interacting with the machine
  - `Printer` can access stapling functions since they are in `Job`
- Now they want to make a coper that can't staple
  - But `Job` still knows about stapling!
- Testing is also much harder

---

<!--
_class: lead
-->

# Design principles & patterns

---

## Minimal public API

```python
class Container:
    def __init__(self, x):
        self.x = x


c = Container(1)
c.x = 2
```

Since we allow setting `x` after creation, we have to design the class assuming a user can manually change it at any time!

---

## Minimal public API (2)

```python
class Container:
    def __init__(self, x):
        self._x = x

    @property
    def x(self):
        return self._x
```

Now a user can't change `x`, only set it

- `frozen=True` does this with dataclasses
- We can also make this hashable now (usable in dict keys and sets)
- The underscore means it's "hidden" (some languages have private)

---

## Pattern: code reuse

```python
# fmt: off
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
# fmt: on
SteppedCode().run()
```

---

## Pattern: code reuse (2)

Now you can replace one step via inheritance:

```python
class NewSteps(SteppedCode):
    def step_2(self):
        print("Replaced step 2")


NewSteps().run()
```

---

## Pattern: code reuse (3)

Or inject code around an existing step:

```python
class SurroundedSteps(SteppedCode):
    def step_2(self):
        print("Before step 2")
        super().step_2()
        print("After step 2")


SurroundedSteps().run()
```

---

## Required interface

- Require an implementer to provide one or methods
- Often via `@abstractmethod` and ABCs

Extended "Integrator" example in class notes.

---

## Functors: the problem

```python
_start = 0


def incr():
    global _start
    _start += 1
    return _start


print(f"{incr() = }")  # incr() = 1
print(f"{incr() = }")  # incr() = 2
print(f"{incr() = }")  # incr() = 3
```

This is _global_, there can only by one.

---

## Functors: the problem (2)

```python
def make_incr():
    _start = 0

    def incr():
        nonlocal _start
        _start += 1
        return _start

    return incr


incr1 = make_incr()
print(f"{incr1() = }")  # incr1() = 1
print(f"{incr1() = }")  # incr1() = 2
```

Not global anymore, but still ugly. `_start` is kept around via reference counting.

---

## Functors: the solution

```python
class Incr:
    start: int = 0

    def __call__(self):
        self.start += 1
        return self.start


incr = Incr()
print(f"{incr() = }")  # incr() = 1
print(f"{incr() = }")  # incr() = 2
```

- **Functor**: A callable object that holds state

---

## Separation of concerns

Each class should address a specific concern.

Some languages allow you to define classes in multiple places (Ruby, Rust), and just load the part you need or extend it without subclassing. Python does not (at least not officially/nicely), neither does C++. Multiple inheritance, type dispatch (C++, Julia), or Traits (Rust) can provide similar benefits, though.

---

## eDSLs: embedded Domain Specific Languages

```python
class Path(str):
    def __truediv__(self, other):
        return self.__class__(f"{self}/{other}")


print(Path("one") / Path("two"))
```

You can use operator overloading (and a few other things) to make something for a domain specific purpose instead of a new language.

Don't do this exact thing, `pathlib.Path` already exists. :)

---

## Mixins

A very specific form of multiple inheritance.

### Rules:

- No `__init__`
- No members (those need `__init__`)
- No `super()`
- No overloading the class they are to mix into

You _can_ bend these rules a bit, but then you are moving into multiple inheritance territory, so be very careful.

---

## Mixins (2)

```python
class PathMixin:
    def __truediv__(self, other):
        return self.__class__(f"{self}/{other}")


class Path(str, PathMixin):
    pass


print(Path("one") / Path("two"))
```

- Example: a drag-and-drop mixin for a GUI framework
- FYI, Python specific simi-alternative: new class keywords
