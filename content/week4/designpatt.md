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

## Coroutines

A powerful flow control scheme is Generators / Iterators / Coroutines. These are
objects that can stop and resume. In Python, a Generator looks like this:

```{code-cell} python3
def my_range(n):
    for i in range(n):
        yield i
```

The presence of a `yield` causes this to become a generator. The return value of
this function is not an int, it's an iterable object. So expressions like
`for i in my_range(3)` or `list(my_range(3))` are valid ways to use this.

````{admonition} Empty generator
The presence of a `yield` anywhere in a function causes a function to be a generator. So
this is actually an empty generator:

```python
def empty():
    return
    yield
```

The yield in the body forces a generator, which then never yields, but simply
returns immediately, making an empty iterator. That's probably a bit less readable
than this alternative, though:

```python
def empty():
    yield from ()
```
````

The examples above are a subset of generators often called "iterators", because
they only produce values, and do not take values in. There is a way to "send"
values into a generator, though it doesn't really have a special in-language
syntax like a `for` loop or `list`/`tuple`.

There is a second sort of coroutine in Python called an `async` function. It is
conceptually the same sort of thing as a generator, except with `yield from`
being written as `await`. They also fixed the language issue with a single word
being found in the body changing the return type by replacing `def` with
`async def`. If generators were written today, there probably would be some
keyword before `def` for them, removing the "empty generator" weirdness and
keeping the reader from having to manually look at the body of the entire
function for any yields. If you've had experience with compiled languages, you
know that the signature of a function is supposed to be the public interface of
the function, and users should not have to look into the body! This issue in
Python will be corrected when we cover static types.

Generators can be used as a programming model. For example, you might have the
following imperative code to counts the words in a file:

```python
with open(name, encoding="utf-8") as f:
    lines = list(f)

stripped_lines = [line.strip() for line in lines]
words_lines = [line.split() for line in stripped_lines]
words_per_line = [len(words) for words in words_lines]
print("Total words:", sum(words_per_line))
```

This has a problem: every line in the file gets stored in memory (multiple
times!). The lists `lines`, `stripped_lines`, `words_lines`, and
`words_per_line` are all intermediate copies we don't want. Now we could
redesign this doing all the computation in one go:

```python
with open(name, encoding="utf-8") as f:
    total = 0
    for line in f:
        stripped_line = line.strip()
        words_line = stripped_line.split()
        words_per_line = len(words_line)
        total += words_per_line

print("Total words:", total)
```

But this might not match the problem very well. Also we might want the
words-per-line list, which would be harder to get from the second example.

We could rewrite this using a generator:

`````{tab-set}
````{tab-item} Inline generators
```python
with open(name, encoding="utf-8") as f:
    stripped_lines = (line.strip() for line in f)
    words_lines = (line.split() for line in stripped_lines)
    words_per_line = (len(words) for words in words_lines)
    print("Total words:", sum(words_per_line))
```
````
````{tab-item} Generator function
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
````
`````

In both examples above, _a list is never made_. You never store more than one
line of a file in memory. Notice how in the inline version, we needed to keep
the file open, since at each step we were building a generator that had not yet
iterated over the source material. In both cases, the iteration only happens
when we call `sum`.

```{admonition} Refactoring
When programming with functions, a key feature is we can always take a
subsection of the function out and place it in a new function. With generators,
if that section of code includes one or more `yield`s, you can do the same thing
with `yield from` starting in Python 3.3, which made generators fully
refactorable.
```

This syntax is really just a shortcut for making iterable objects, which is done
through magic methods. Iterators can be restartable and have an estimated length
(neither of which is available on the shortcut syntax using `yield`).

Reading a file is a particularly good use case for this, as Python's performance
is about equal or faster than file IO, meaning the most optimized file read and
a Python program that runs Python code on each line of a file are likely to be
competitive. One terrible use case for this style is array programming, due to
the extreme overhead of an interpreted language. An alternative is array based
programming, which is up next.

Other languages have this concept (and it's not that hard to write it yourself
with objects, it's just better to have a standard). C++ traditionally prefers
"start/end iterators" which are objects that can be +1'd and eventually compare
equal, but modern C++ has coroutines (C++20) and a helper to make iterators
(`std::generator`, C++23). The C++ version was designed to be general enough to
back async support, too, in a single concept.

## Array programming

This is not always mentioned as a programming paradigm, but it is one, and an
important one for the sciences. Consider the following square of an array in
imperative code:

```python3
import numpy as np


input_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
output_data = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

for i in range(len(input_data)):
    output_data[i] = input_data[i]**2
```

This describes what happens to each element. We could have chosen a functional
procedure instead:

```python3
output_data = np.fromiter(map(lambda x: x**2, input_data), int)
```

This still describes what happens on each element in Python. Python has to loop
over the array, doing a lot of work like checking the types, looking up methods,
creating and destroying Python objects, when really this could be done much more
efficiently if you just had a pre-compiled function to do this.

Interpreted languages (like Matlab) as well as a library for Python (NumPy) came
upon a solution to this problem, from the original APL: array-at-a-time
calculations. It looks like this:

```python3
output_data = input_data**2
```

NumPy has overloaded most of the special methods for arrays so that actions on
an array run a pre-compiled routine that does not have to do all the checks
Python does to be general and dynamic. This means you get full compiled like
performance for simple operations. It's also a different paradigm when working
with arrays; it's short and concise, and can read very well (though sometimes
it's a bit harder to write).

See
[this SciPy tutorial: loopy programming](https://github.com/jpivarski-talks/2022-07-11-scipy-loopy-tutorial/blob/main/narrative.ipynb)
for more about array based languages & NumPy.

## Memory safety

## Modularity

## Refactoring
