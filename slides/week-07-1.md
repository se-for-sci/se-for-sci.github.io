---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# APC 524

## Design Patterns - Functional programming

---

## Prelude

TO keep the slides simple, I will assume the following imports:

```python
import dataclasses
import functools
```

## Python is a multi-paradigm language

But it favors OO programming pretty heavily. We may reach out to other languages to learn lessons about different paradigms.

---

## Mutability and state

First we need to talk about **mutability** and **state**. Functional programming is all about _avoiding_ them.

---

## Mutability in Python

- Some built-in objects are truly immutable (like `int`). You can't mutate them.
- Immutable objects have a hash (`__hash__` is present and not None)

Immutability by convention more than language.

---

## Why do we introduce mutability?

- Easy to change
- Saves memory
- Easy API (but maybe not a good one!)

---

## Easy to change

```python
@dataclasses.dataclass
class Mutable:
    x: int
    y: int


mutable = Mutable(1, 2)
mutable.x = 2
print(mutable)
```

```output
Mutable(x=2, y=2)
```

---

## Easy to change (2)

```python
@dataclasses.dataclass(frozen=True)
class Immutable:
    x: int
    y: int


immutable_1 = Immutable(1, 2)
immutable_2 = Immutable(2, immutable_1.y)
print(immutable_2)
```

```output
Immutable(x=2, y=2)
```

---

## Easy to change (3)

```python
@dataclasses.dataclass(frozen=True)
class Immutable:
    x: int
    y: int


immutable_1 = Immutable(1, 2)
immutable_2 = dataclasses.replace(immutable_1, x=2)
print(immutable_2)
```

```output
Immutable(x=2, y=2)
```

---

## Easy to build API

```python
data = Data()
data.load_data()
data.prepare()
data.do_calculations()
data.plot()
```

What happens if you forget a step?

---

## Immutable API + classes

We could replace a mutating state with (immutable) classes:

```python
empty_data = EmptyData()
loaded_data = empty_data.load_data()
prepared_data = loaded_data.prepare()
computed_data = prepared_data.do_calculations()
computed_data.plot()
```

Now mistakes can be detected statically! Tab completion will tell you what you can do. Etc.

---

## Chained style

We could also use a chained style:

```python
computed_data = EmptyData().load_data().prepare().do_calculations()
computed_data.plot()
```

This style is common in functional programming (which is where we are headed).

---

## Copy vs. reference

```python
def evil(x):
    x.append("Muhahaha")


mutable = []
evil(mutable)
print(mutable)
```

What will this output?

---

## Design suggestion

A function should be of the form

```
name(input, ...) -> output
```

We tend to allow:

```python
x.do_something()
```

Though that also mutates an argument (`self`).

---

## What does immutability give us?

- Optimization by the compiler (if you have one)
- Chaining of methods
- No issues with copying vs. references
- Avoid one mutable reference breaking another

These don't require immutability, they require _we don't mutate_.

---

## Functional programming

Defining **pure function**:

- Does not mutate arguments
- Does not contain internal state
- No side effects (like printing to screen!)

Think about some functions and see which ones are pure.

---

## map, filter, reduce

Functional programming often involves passing functions to functions.

Here's Pythonic code running on `items = [1, 2, 3, 4, 5]`:

```python
sum_sq_odds = sum(x**2 for x in items if x % 2 == 1)
```

Written in a functional style:

```python
sum_sq_odds = functools.reduce(
    lambda x, y: x + y, filter(lambda x: x % 2 == 1, map(lambda x: x**2, items))
)
```

---

## Improving the syntax

Python isn't a functional language. Let's try adding chaining:

```python
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

---

## Improving the syntax (2)

```python
items = FunctionalIterable([1, 2, 3, 4, 5])
sum_sq_odds = (
    items.map(lambda x: x**2).filter(lambda x: x % 2).reduce(lambda x, y: x + y)
)
```

---

## Other languages: Ruby

```ruby
items = [1,2,3,4,5]
sum_sq_odds = items.map{_1**2}.filter{_1 % 2 == 1}.reduce{_1 + _2}
puts items
```

---

## Other languages: Rust

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

---

## Other languages: C++23 (not supported yet)

```cpp
import std;

int main() {
    std::vector items {1, 2, 3, 4, 5};
    auto result = items | std::views::transform([](int i){return i*i;})
                        | std::views::filter([](int i){return i%2==1;});
    sum_sq_odds = std::fold_left(odd_sq, 0, [](int a, int b){return a + b;});
    std::println("{}", result);
    return 0;
}
```

---

## Currying

```python
def power(y, x):
    return x**y


pow2 = functools.partial(power, 2)
pow3 = functools.partial(power, 3)

print(f"{pow2(10) = }")
print(f"{pow3(10) = }")
```

```output
pow2(10) = 100
pow3(10) = 1000
```

Subset of functors!

---

## So what can you get?

### Lazy evaluation

```python
def not_pure(x):
    print("computing x")
    return x


values = [1, 2, 3]
results = map(not_pure, values)
filtered_results = filter(lambda x: x % 2 == 0, results)
print(sum(filtered_results))
```

Where does the print statement run?

---

## So what can you get?

### Parallelization

(Not Python) Can run in parallel, since when you run doesn't matter.

### Easy to optimize

(Not Python) Easy to reason about.

Not Python only means not the _language_, libraries can implement!

---

## JAX

A library that makes use of this is JAX. Let's look at it:

```python
import jax
import jax.numpy as jnp

arr = jnp.array([1, 2, 3])
```

Looks like NumPy right? Try to modify the array. ;)

---

## JAX (2)

Here's how you write `arr[0] = 4`:

```python
arr = arr.at[0].set(4)
```

### What you get:

- You can fuse functions together with `jax.jit` & they get compiled into machine code
- You can target CPU, GPU, and TPU (Google’s tensor processing units)
- You can compute gradients of functions

---

## JAX (3)

```
@jax.jit
def f(x):
    return x**3 + x**2 + x


dfdx = jax.grad(f)
print(f"{dfdx(1.0) = }")
```

```output
dfdx(1.0) = DeviceArray(6., dtype=float32, weak_type=True)
```
