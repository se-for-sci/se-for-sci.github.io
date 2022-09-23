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

```{code-cell} python3
:tags: [remove-cell]

from rich.console import Console

console = Console(width=80)
print = console.print
```

# Design patterns

Let's move beyond OO and learn from other paradigms and patterns. These are not
exclusive - you may use some or all of the ideas here to inform your class
design. You might use OOP ideas to help your functional patterns. Etc.

## Functional Programming

In it's own section.

## Type dispatch

Type dispatch can be seen as an alternative to OOP, though it's often used in
conjunction with it (unless you are in Julia). Type dispatch is a bit
"non-Pythonic" in that it's a bit problematic with duck typing, but you can use
it.

First we start with the "general" implementation; this will get called if none
of the types match:

```{code-cell} python3
import functools

@functools.singledispatch
def generic(x):
    raise NotImplementedError("General implementation")
```

Now we can register one or more types:

```{code-cell} python3
@generic.register(int)
def _(x):
    print(f"I know how to compute {x}, it's an int!")

@generic.register(float)
def _(x):
    print(f"I know how to compute {x}, it's an float!")
```

Now we can call this with ints or floats, but nothing else. It dispatches
different versions depending on the types it sees.

```{admonition} Python specific tips
* Only the first argument will be used for the dispatch. Other arguments are ignored.
* You can use type annotations instead (Python 3.7+)
* You can stack multiple registers
    * Or use Unions (Python 3.11+)
* Duck typing supported through Protocols (Python 3.8+ or `typing_extensions` backport)
```

Other languages have varying levels of support for type dispatch. C++ supports
it, while C does not. Julia is designed around it. It's a key part of Rust
(though in a rather different form).

A benefit of type dispatch over OOP is that it tends to be more modular. A
drawback is that some patterns of code reuse are not available.

## Array programming

## Memory safety

## Modularity

## Refactoring
