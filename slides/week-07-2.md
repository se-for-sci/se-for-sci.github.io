---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# APC 524

## Design patterns

Besides Functional Programming, here are more patterns to be aware of.

---

## Prelude

To keep the slides simple, I will assume the following imports:

```python
import dataclasses
import functools
import numpy as np
```

---

## Type Dispatch

Can be alternative (Julia) or used in conjunction with OOP.

Single dispatch is supported in Python:

```python
@functools.singledispatch
def generic(x):
    raise NotImplementedError("General implementation")


@generic.register(int)
def _(x):
    print(f"I know how to compute {x}, it's an int!")


@generic.register(float)
def _(x):
    print(f"I know how to compute {x}, it's an float!")
```

---

## Type Dispatch: Python specific tips

- Only the first argument used
- You can use type annotations instead
- You can stack multiple registers
- Or use Unions (Python 3.11+)
- Duck typing is supported through Protocols
- Methods start with self - so there’s a singledispatchmethod too

---

## Type Dispatch: language support

- Python: opt-in, first argument only (single dispatch)
- Julia: The language is designed around type dispatch
- C: Not supported
- C++: Supported
- Rust: Possible via Traits

Type dispatch tends to be modular, but doesn't have some code reuse & discovery features of OOP.

---

## Coroutines

AKA Generators / Iterators.

```python
def my_range(n):
    for i in range(n):
        yield i
```

The presence of a yield anywhere in the body changes this to a generator (bad design, by the way).

Try to make an empty generator. :)

---

## Coroutines (2)

- To start iteration, call `y = iter(x)`, which calls `y = x.__iter__()`.
- To increment, call `next(y)`, which calls `y.__next__()`.
- To stop, raise `StopIteration` (yes, an exception is required).

Lots of places in Python do this for you, like `for` loops, `list(...)`, etc.

---

## Coroutines (3)

Two way communication is possible (though not as nicely supported via syntax). Call `y.send(...)` instead of `next(y)`. The `yield` expression returns the sent value.

`yield from` lets you factor out generators.

Python's `async`/`await` are also generators, just specialized for asyncio.

---

## Coroutines as a design pattern

### Non-generator version

```python
with open(name, encoding="utf-8") as f:
    lines = list(f)

stripped_lines = [line.strip() for line in lines]
words_lines = [line.split() for line in stripped_lines]
words_per_line = [len(words) for words in words_lines]
print("Total words:", sum(words_per_line))
```

Make many unneeded lists!

---

## Coroutines as a design pattern

### Non-generator version (2)

```python
with open(name, encoding="utf-8") as f:
    total = 0
    for line in f:
        stripped_line = line.strip()
        words_line = stripped_line.split()
        words_per_line = len(words_line)
        total += words_per_line
```

May not want to write this way!

---

## Coroutines as a design pattern

### Generator version (1)

```python
with open(name, encoding="utf-8") as f:
    stripped_lines = (line.strip() for line in f)
    words_lines = (line.split() for line in stripped_lines)
    words_per_line = (len(words) for words in words_lines)
    print("Total words:", sum(words_per_line))
```

---

## Coroutines as a design pattern

### Generator version (1)

```python
def word_counter(name):
    with open(name, encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            words_line = stripped_line.split()
            words_per_line = len(words_line)
            yield words_per_line


print("Total words:", sum(word_counter(name)))
```

---

## Generators in other languages

You could always make your own, but it's nicer if the language supports it.

- Python: Generators and Async, generator comprehensions
- C++: Coroutines new in C++20 and `std::generator` added in C++23. Various libraries like `boost::async`
- Rust has third-party libraries implementing coroutines

Iterators are similar, though a bit less powerful (one directional):

- C++ also has iterators (with begin/end)
- Rust has a `std::iter::IntoIterator` Trait

---

## Array programming

Not always considered a programming paradigm, but it's an important one for the sciences.

```python
input_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

# Imperative version
output_data = np.zeros_like(input_data)
for i in range(len(input_data)):
    output_data[i] = input_data[i] ** 2

# Functional version
output_data = np.fromiter(map(lambda x: x**2, input_data), int)

# Array-at-a-time version
output_data = input_data**2
```

---

## Array programming (2)

Originally a language feature (APL, Matlab), it is a library feature in modern languages (Python, C++, Rust).

```python
x, y = np.mgrid[0:5:501j, 0.5:3.5:301j]
radius = np.sqrt(x**2 + y**2)
```

In the above example, we compute the radius for plotting.

---

## TODO

- Memory safety
  - Garbage collected languages
  - Memory management and moves

---

## Interfaces

- Java: Interfaces
- C++: Concepts
- Python: Protocols
- Rust: Traits (partial parametric polymorphism, technically)

We'll see Protocols in detail next week.

---

## Traits

One of Rust's two key features (besides the memory model and borrow checker).

Differences vs. normal Interfaces:

- Must explicitly opt-in to a trait, not just simple name matching
- Only the library defining the Trait or the library defining the type can opt-in to a trait
- Trait methods can overlap, including with struct methods!
- Lookup will use the trait method if available and non-overlapping

---

## Traits (2)

```rust
foo = Foo::new();
foo.bar();
```

If there's a `Foo::bar()`, call that. If not, if there's a Trait with a `.bar()` implemented on `Foo`, call that.

---

## Other patterns

- **Singleton pattern**: There can only be one instance of a class. Like `None`, `True`, `False`.
- **Registries**: logging uses this design.
- **State machine**: this is used heavily by Matlab.
- **Factory pattern**: We've touched on this lightly, classes `__init__` method, for example.
- **Ascync patterns**: Lightly touched on during generators.
- **Event loop**: A common pattern for reacting to multiple possible inputs.
