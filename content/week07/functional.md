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

# Functional programming

[Slides](https://henryiii.github.io/se-for-sci/slides/week-07-1)

## Mutability and state

```{code-cell} python3
:tags: [remove-cell]

from rich.console import Console

console = Console(width=80)
print = console.print
```

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

#### Mutable is easy to change a small part

It's conceptually and syntactically easy to change a small part of a structure.
For example:

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

If we wanted to change this without mutation, we'd have to do:

```{code-cell} python3
@dataclasses.dataclass(frozen=True)
class Immutable:
    x: int
    y: int

immutable_1 = Immutable(1, 2)
immutable_2 = Immutable(2, immutable_1.y)
print(immutable_2)
```

Imagine if the class was larger! Dataclasses can really help us here in the
immutable case write something that is quite reasonable instead of having to
manually call the constructor ourselves with the replaced values and forwarding
in all the rest:

```{code-cell} python3
immutable_1 = Immutable(1, 2)
immutable_2 = dataclasses.replace(immutable_1, x=2)
print(immutable_2)
```

This scales much better to larger dataclasses. But it's still a bit easier /
more natural, and much easier if you are not dealing with something like
dataclasses (though as we'll see, things that tend heavily toward immutability
will provide tools similar to `dataclasses.replace`)

#### Memory saving

If you have a large structure, you can simply change part in place, avoiding
copying the entire thing. This is nice - but it could be seen as an
implementation detail if you never were to touch the original structure again.
If the language was smart enough to detect this, it could do the mutation for
you even when you asked for a new copy. That is, the difference the examples
above is really an implementation detail if `immutable_1` is never used again. A
smart compiler (not Python, which doesn't have a compiler) could learn to
rewrite the immutable example into the first behind the scenes.

We'll get into why we think the immutable versions may be better in some cases
soon!

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
its contents (or contents of its contents) are not changed. For example, this
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

- Does not mutate its arguments
- Does not contain internal state (doesn't mutate itself or a global, basically)
- Has no side effects (like printing to the screen)

Functors are not pure functions (they mutate themselves). `print` is not a pure
function (it mutates the screen). And many of the methods on lists and dicts are
not pure functions (they mutate the first argument, self). But there are lots of
pure functions, like most built-ins and most non-method functions, and methods
of tuples and such.

Put simply, a pure function produces the same output whenever given the same
inputs. Its behavior is determined solely by the inputs.

### Map, filter, reduce

Functional programming often involves passing functions to functions. Three very
common ones are `map` (apply a function to each item of a sequence), `filter`
(remove items from a sequence based on a function), and `reduce` (apply a
function to successive pairs of a sequence). You'll sometimes see map called
`apply`, and reduce called `fold`.

Let's take the following Pythonic code using a comprehension:

```{code-cell} python3
items = [1, 2, 3, 4, 5]
sum_sq_odds = sum(x**2 for x in items if x % 2 == 1)
print(sum_sq_odds)
```

And instead write it following in a functional style:

```{code-cell} python3
import functools


items = [1, 2, 3, 4, 5]
sum_sq_odds = functools.reduce(lambda x, y: x + y, filter(lambda x: x % 2 == 1, map(lambda x: x**2, items)))
print(sum_sq_odds)
```

Notice the data structure I chose was a list, which is mutable - but that's
okay, I didn't mutate it - the functions were pure.

Notice how horribly this reads; our operations are in reverse order (right to
left). In a more functional language, you can chain these left to right instead.
Or with a library.

We'll write a little wrapper that will allow us to chain operations as if we
were in a proper functional language:

```{code-cell} python3
class FunctionalIterable:
    def __init__(self, this, /):
        self._this = this
    def __repr__(self):
        return repr(self._this)
    def map(self, func):
        return self.__class__(map(func, self._this))
    def filter(self, func):
        return self.__class__(filter(func, self._this))
    def reduce(self, func):
        return functools.reduce(func, self._this)
```

Now, let's compare readability:

```{code-cell} python3
items = FunctionalIterable([1, 2, 3, 4, 5])
sum_sq_odds = items.map(lambda x: x**2).filter(lambda x: x % 2).reduce(lambda x,y: x + y)
print(sum_sq_odds)
```

Notice that we now read this left to right. Our items are squared then filtered
then reduced. Compare that to some languages with support for functional
programming:

`````{tab-set}
````{tab-item} Ruby
```ruby
items = [1,2,3,4,5]
sum_sq_odds = items.map{_1**2}.filter{_1 % 2 == 1}.reduce{_1 + _2}
puts items
```

This looks very nice, especially with Ruby 2.7's lambda shortcut notation. If you
didn't want to use that, classic lambdas would be `|x| x**2`, etc.
````
````{tab-item} Scala
```scala
val arr = (1 to 5)
val sum_sq_odds = arr.map(x => x*x).filter(_ % 2 == 1).reduce(_ + _)
println(sum_sq_odds)
```

This is often considered a highly functional language, so I've included it here for completeness.
````
````{tab-item} Hascal
```
foldl (+) 0 . filter ((==) 1 . flip mod 2) . map (^2) $ [1..5]
```

Hascal is a purely functional language. It's also a bit odd in that idiomatic
Hascal reads right to left (from mathematics).  However, as of 4.8 it does have
reverse function application operator (also using a lambda to match the other
examples more closely):

```
[1..5] & map (^2) & filter (\x -> x `mod` 2 == 1) & foldl (+) 0
```

I've left of variable assignment & printing since those are a bit different in online playgrounds.
````
````{tab-item} C++20 Ranges
```cpp
#include <iostream>
#include <vector>
#include <ranges>
#include <numeric>

int main() {
    std::vector<int> items {1, 2, 3, 4, 5};
    auto odd_sq = items | std::views::transform([](int i){return i*i;})
                        | std::views::filter([](int i){return i%2==1;});
    auto sum_sq_odds = std::accumulate(std::begin(odd_sq), std::end(odd_sq), 0, [](int a, int b){return a + b;})
    std::cout << sum_sq_odds << std::endl;
    return 0;
}
```

Not that C++ is slowly gaining support; `std::fold_left` is in C++23, but for
C++20, we have to drop back to a classic `std::accumulate` algorithm & begin
and end iterators.

````
````{tab-item} C++23 Ranges
```cpp
import std;

int main() {
    std::vector items {1, 2, 3, 4, 5};
    auto odd_sq = items | std::views::transform([](int i){return i*i;})
                        | std::views::filter([](int i){return i%2==1;});
    auto sum_sq_odds = std::ranges::fold_left(odd_sq, 0, [](int a, int b){return a + b;});
    std::println("{}", sum_sq_odds);
    return 0;
}
```

Not that stdlib module support is not available yet.

````
````{tab-item} Rust
```rust
fn main() {
    let items = [1,2,3,4,5];
    let sum_sq_odds = items.iter()
                      .map(|x| x*x)
                      .filter(|&x| x%2==1)
                      .fold(0, |acc, x| acc + x);
    println!("{}", sum_sq_odds);
}
```
````

````{tab-item} Swift
```swift
let items = [1, 2, 3, 4, 5]
let sum_sq_odds = items.map { $0 * $0 }
                       .filter { $0 % 2 == 1 }
                       .reduce(0, +)
print(sum_sq_odds)
```
````
`````

Notice how many of the languages use similar terms and try to read well when
chained. Map (or transform for C++, odd one out here) applies a function to an
iterator and returns an iterator of the returned values. Filter removes
iterations based on the truthiness of the return value. And reduce (or fold)
does a binary reduction (most languages also have sum for this common
reduction).

Most templating languages like Liquid and Jinja have "filters", which are
applied left to right in a similar style. Hugo's templating system is
functional, too.

#### Currying

Another common feature of functional languages is currying. Let's say a function
takes two arguments. Currying means that if you give it one argument, you now
have a function that requires one argument. Purely functional or heavily
functional languages will often curry by default; in Python, you have to
manually curry with `functools.partial`.

Here's an example of a two argument function:

```{code-cell} python3
def power(y, x):
    return x**y
```

Now, we can "curry it":

```{code-cell} python3
import functools


pow2 = functools.partial(power, 2)
pow3 = functools.partial(power, 3)
```

Now we have two new functions that have `y` pre-specified:

```{code-cell} python3
print(f"{pow2(10) = }")
print(f"{pow3(10) = }")
```

Note that this is a (better) way to do a subset of Functors (from the previous
chapter on OOP). If you are using a Functor to capture state, then you can use
currying with `partial` to be much more explicit as to your intent _and_ curried
methods will capture the current value, not a reference that could change later.

### So what do you get?

Why worry about pure functions? It turns out, they have a lot of properties
related to optimization. Some libraries make use of these properties to do some
very impressive things.

#### Lazy

When you have pure functions, the programming language or library can decide
when to run them - and often it can decide to do it at some later time. For
example, we can observe this if we break our promise about pure functions:

```{code-cell} python3
def not_pure(x):
    print("computing x")
    return x

values = [1,2,3]
results = map(not_pure, values)
```

Notice nothing ran? If you look at the type of `results`, it's an iterator. The
mapping only happens when you do the iteration. We can also filter:

```{code-cell} python3
filtered_results = filter(lambda x: x%2==0, results)
```

Still nothing. A reduction does iterate over the results:

```{code-cell} python3
print(sum(filtered_results))
```

Now you see the side effects; this is when it ran.

:::{admonition} Python & lazy iterators

You can do this without the functional spellings above - generator
comprehensions (the ones with `()` instead of `[]`) are also lazy, as is `range`
and quite a few other methods in Python 3. There also is good support for
coroutines via generator functions. You can use those to write things that look
like they apply to a list and return a list but still ensure code only runs once
though a final iteration, saving memory. However, this is not useful for most
numeric work - see array programming.

:::

#### Parallelization

While not used in Python, functional programming is easy to optimize for
parallel execution. Since things like external state are not allowed, you can
not just run later, you can also run concurrently.

#### Easier to optimize

Some languages and libraries can do a lot of optimization if you have pure
functions and no mutability. There are a lot of assumptions you can make that
help with optimization. Again, not in Python itself, but we will look at a
library that takes advantage of these things.

### Example: JAX

```{admonition} No JAX in our environment

We will not be including or running JAX since it is quite large and would slow down setting up an environment. All
examples will be pre-computed, and we'll not be using it in homework.
```

A library that makes use of this is JAX. JAX is a ML inspired library that is a
bit of a spiritual successor to TensorFlow. TensorFlow focused on symbolic
computation, while JAX is functional.

JAX provides a NumPy-like interface:

```python
import jax
import jax.numpy as jnp

arr = jnp.array([1, 2, 3])
```

However, _you can't modify a jax array_. Having read the above, I would expect
you could have guessed that JAX is functional. They provide a shortcut for
setting a value; for example, `arr[0] = 4` can be written:

```python
arr = arr.at[0].set(4)
```

But what do you get?

- You can fuse functions together with `jax.jit` & they get compiled into
  machine code
- You can target CPU, GPU, and TPU (Google's tensor processing units)
- You can compute gradients of functions

For example, we can define a pure function and get a fast version and get a
gradient function as well:

```python
@jax.jit
def f(x):
    return x**3 + x**2 + x


dfdx = jax.grad(f)
```

And we can use it:

```python
dfdx(1.0)
```

```output
DeviceArray(6., dtype=float32, weak_type=True)
```

(That's $\frac{df}{dx} = 3x^2 + 2x + 1$ if you were to compute it by hand.)

There are quite a few rules to follow when making JAX functions (control flow is
a common issue), but you get a lot for your efforts!

```{admonition} Other ways to go faster
You don't have to use JAX to write code faster than NumPy. There are other
tools that sometimes are better in some situations, including the excellent
Numba library, which is imperative. PyTorch is a great ML-focused library. CuPy
is a great GPU NumPy replacement. Etc. JAX here is just intended to be an
example of what thinking in a functional mindset can do.
```

```

```
