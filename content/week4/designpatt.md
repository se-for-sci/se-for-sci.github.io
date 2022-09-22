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

## Mutability and state

We talked a bit about mutability in Python already. Python's concept of
mutability has two aspects:

- Some built-in (implemented in C) objects are immutable. You can't really
  imitate this in only Python with custom classes - all user classes make
  mutable objects.
- Immutable objects have a hash (`__hash__` is not None). This is the actual
  property checked most of the time - so you can make classes that can be put in
  sets and dict keys by making them hashable. It is up to you to make them
  immutable by convention (you can make it pretty hard to do).

Notice the second point: immutability really is by convention, not forced by the
language - and that's okay. Immutability / mutability is a design pattern!

### Why do we tend toward mutable?

#### Memory saving (implementation detail)

If you have a large structure, you can simply change part in place, avoiding
copying the entire thing. This is nice - but it could be seen as an
implementation detail. If the language was smart enough to detect that you never
used the "original" object again, it could do the mutation for you even when you
asked for a new copy. That is, the difference here:

```{code-cell} python3
import dataclasses

@dataclasses.dataclass
class Mutable:
    x: int
    y: int

mutable = Mutable(1, 2)
mutable.x = 2
print(mutable)
```

Verses:

```{code-cell} python3
import dataclasses

@dataclasses.dataclass
class Immutable:
    x: int
    y: int

immutable_1 = Immutable(1, 2)
immutable_2 = dataclasses.replace(immutable_1, x=2)
print(immutable_2)
```

is really an implementation detail if "immutable_1" is never used again. A smart
compiler (not Python, which doesn't have a compiler) could learn to rewrite the
second example into the first behind the scenes.

We'll get into why we think the second version is better in some cases soon!

#### Mutable is easy to change a small part

As you saw above, it's easy to change a small part of code. Dataclasses really
helped us in the immutable case write something that was quite reasonable
instead of having to manually call the constructor ourselves with the replaced
values and forwarding in all the rest. But it's still a bit easier / more
natural, and much easier if you are not dealing with something like dataclasses.

#### Easy to build API in a way that you maybe shouldn't

Some APIs just don't fit well with immutable designs (we'll see some solutions,
though). Things with a non-linear progression, for example. Something like:

```python
data = Data()
data.load_data()
data.prepare()
data.do_calculations()
data.plot()
```

That's easy and simple. **Unless you forget a step.** Oh, yeah, and static
analysis tools can't tell you if you forget a step, the API doesn't statically
"know" that `.prepare()` is required, for example. Tab completion tells you that
`.plot()` is valid immediately. The problem is that `Data` has a changing state,
and not all operations are valid in all possible states.

If we replaced the single `Data` with multiple immutable classes, then our
problem would be solved:

```python
empty_data = EmptyData()
loaded_data = empty_data.load_data()
prepared_data = loaded_data.prepare()
computed_data = prepared_data.do_calculations()
computed_data.plot()
```

These classes don't have to be immutable. Maybe you can load more data to loaded
data. But they are harder to use incorrectly when they at least not have a
mutating state that makes subsets of operations invalid. Note that tab
completion in this case would show exactly the allowed set of operations each
time.

We could avoid naming the temporaries, too:

```python
computed_data = EmptyData().load_data().prepare().do_calculations()
computed_data.plot()
```

This "chaining" style is a hallmark of functional programming (which is where we
are headed).

### Copy vs. reference

As you might already know, everything in Python is copied by reference. If you
have a mutable object, you have to make a copy (or a deepcopy) to ensure that
it's contents (or contents of it's contents) are not changed. For example, this
function is evil:

```{code-cell} python3
def evil(x):
    x.append("Muhahaha")

mutable = []
evil(mutable)
print(mutable)
```

A function should be of the form `name(input, ...) -> output`, but instead, this
function is mutating the argument it was given! If we used a immutable object
instead, we would have been forced to use the return value of the function,
making it much easier to understand when you are using it. Functions are much
nicer when arguments are not mutated. `self` is kind of a special case - a
programmer is much more likely to expect `x.do_something()` to modify `x` than
`do_something(x)`. But as we've seen above, there are limits/drawbacks.

### What do we get with immutability?

Let's summarize above:

- Optimization choices for the compiler (if you have one) - it's much simpler to
  reason about.
- Chaining of methods
- No worry about copying

Notice I didn't actually require immutability on the points, I simply required
_we don't mutate_. The fact that we can or can't mutate it is less important
than if we do mutate it.

## Functional programming

Let's define a **pure function**. This is a function that:

- Does not mutate it's arguments
- Does not contain internal state (doesn't mutate itself or a global, basically)
- Has no side effects (like printing to the screen)

Functors are not pure functions (they mutate themselves). `print` is not a pure
function (it mutates the screen). And many of the methods on lists and dicts are
not pure functions (they mutate the first argument, self). But there are lots of
pure functions, like most built-ins and most non-method functions, and methods
of tuples and such.

### Map, filter, reduce

Functional programming often involves passing functions to functions. Three very
common ones are `map` (apply a function to each item of a sequence), `filter`
(remove items from a sequence based on a function), and reduce (apply a function
to successive pairs of a sequence).

Let's take the following Pythonic code using a comprehension:

```{code-cell} python3
items = [1, 2, 3, 4, 5]
sum_sq_evens = sum(x**2 for x in items if x % 2)
print(sum_sq_evens)
```

And instead write it following in a functional style:

```{code-cell} python3
import functools


items = [1, 2, 3, 4, 5]
sum_sq_evens = functools.reduce(lambda x, y: x + y, filter(lambda x: x % 2, map(lambda x: x**2, items)))
print(sum_sq_evens)
```

Notice the data structure I chose was a list, which is mutable - but that's
okay, I didn't mutate it - the functions were pure.

Notice how horribly this reads; our operations are in reverse order (right to
left). In a more functional language, you can chain these left to right instead.
Or with a library.

## Type dispatch

## Memory safety

## Modularity

## Refactoring
