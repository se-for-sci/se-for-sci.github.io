---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Static Typing

---

## Prelude

To keep the slides simples, I will assume the following imports:

```python
import typing
```

---

## Static typing

- What is the best thing about Python? No explicit typing

- What is the worst thing about Python? No explicit typing

---

## Static typing

- What is the best thing about Python? No explicit typing
  - Easy to read a little code
  - Easier to learn

- What is the worst thing about Python? No explicit typing
  - Hard to read a larger codebase
  - Breakage always happens at runtime
  - Lots of pitfalls even with good tests (like forgetting `None`)

---

## Optional static typing

Python has been gaining _optional_ static typing!

```python
def times_three(x: float) -> float:
    return x * 3
```

What happens when we do this:

```python
times_three(["hi"])
```

---

## Optional static typing (2)

Python doesn't care about type annotations! Some are accessible to libraries, but using that is not as common.

How do you use the type annotations? With a type checker!

- MyPy: The original type checker, from the CPython authors.
- PyRight: Microsoft's type checker. Powers PyLance in VSCode.
- PyRE: Meta's type checker, written for Instagram. In OCaml.
- PyType: Google's type checker with inference. Python + UNIX.
- PyCharm also has a built-in one.

---

## Why study this?

- Final step toward compiled languages
- Type checker is basically a compiler (that doesn't compile)
- MyPyC actually can compile, by the way
- Valuable skill in Python, too!

We can study types, generics, Protocols, etc. All without leaving Python!

---

## Runtime usage

- Type annotations are evaluated & stored on class/module/function
- Type annotations are thrown away inside functions
- A string is identical to it's evaluated contents
- If you `from __future__ import annotations` (Python 3.7), then unevaluated strings are stored instead

Some libraries that use runtime annotations are Pydantic and beartype. They should still be types, though.

The stdlib uses them in a couple of places (dataclasses look for `typing.ClassVar` and single dispatch can use them)

---

## Demo `simple.py`

Run MyPy with:

```bash
mypy simple.py
```

You can also use pre-commit, nox, etc.

This is "gradual" typing. You can enable strict mode:

```bash
mypy --strict simple.py
```

---

## Demo: Optional example

MyPy is great at checking for None handling. See if you can spot the error in `optional.py`. MyPy can!

---

## Revealing the type

You can use `reveal_type(x)` or `typing.reveal_type(x)` (newer versions of Python) like a type-checker "print" statement.

## Ignoring errors

You can ignore errors with `type: ignore` statements!

```python
x: str = f()
x.nonexistent()  # type: ignore[attr-defined]
```

---

## Lying about types

You can lie about typing in Python, since it's not actually using them.

Doesn't work in a compiled language!

But a useful escape hatch sometimes, or a way to deprecate code.

---

## Typing basics

```python
# Variable annotation (3.6+)
x: int = 2

# No assignment is allowed ("declaration")
y: int


# Function annotation
def f(x: int) -> int:
    return x


# Class annotations
class X:
    a: int  # Declares instance variable, use typing.ClassVar otherwise
```

---

## Basic types

Note you don't need types if they can be inferred.

```python
a: int = 1
b: str = "hi"
c: bytes = b"hi"
d: float = 1.0
e: complex = 1 + 1j
f: bool = True
g: None = None  # is it's own type
```

---

## Catchall types

```python
from typing import Any

x: Any = could_return_anything()  # Everything valid
y: object = could_return_anything()  # Nothing assumed
```

Operations on `object` are restricted to only things that work on _all_ objects (like `str(y)`).

`Any` is an escape hatch allowing a mix of static and dynamic code.

---

## Generics

Generics are parametrized types. Python has several built-in:

```python
a: list[int] = [1, 2, 3]
b: tuple[int, int, int] = (1, 2, 3)
c: tuple[int, ...] = (1, 2, 3)
d: dict[str, int] = {"one": 1, "two": 2}
```

Lists have a single parameter, the type the list holds. Tuples either take one parameter each, or have a `...`. And dicts take one for the key and one for the value.

---

## Unions

```python
w: int | str = "hi"  # Either string or int
x: list[int | str] = [1, "hi"]  # Mix of strings and ints
y: list[int] | list[str] = [1, 2]  # All strings or all ints
```

Uses the `A|B` (Python 3.10+, 3.7+ annotations only with future import) or `typing.Union[A,B]`.

Very commonly used for "Nonable" (`typing.Optional`)

```python
x: int | None = None
```

---

## Other types

These are things common in compiled languages.

- `Literal[X]`: Only this value (or values) exactly. Enum-like
- `Final[X]`: Not allowed to be replaced later
- `@final`: A decorator for methods that can't be overridden
- `enum.Enum`: An enum type (subclass to make one)
- `TypedDict`: A string keyed dict with types per key
- `NamedTuple`: A tuple with names for items (and types, of course)
- `Self`: The current class (3.11+)

---

## Typing backports

If something was added in a newer version of Python, it is also in `typing_extensions` for older versions of Python.

```python
import sys

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self
```

And then only require `typing-extensions; python_version<"3.11"`.

---

## Type narrowing

How do type checkers work? One key feature is _type narrowing_.

```python
def f(x: str | None) -> str:  # x is str | None
    if x is None:
        return ""  # x must be None here
    return x  # x must be str here
```

The `if` statement "guards" against the None case, so after the if, the type has been narrowed to just `str`.

---

## Type narrowing: question

What would this print?

```python
def f(x: str | None) -> None:
    if x:
        reveal_type(x)
    else:
        reveal_type(x)
```

---

## Type narrowing: a little help

You can help narrow with `assert`:

```python
def could_be_none(y: bool) -> int | None:
    return 42 if y else None


y = could_be_none(True)
assert y is not None
print(f"Bitcount: {y.bit_count()}")
```

FYI, for the above, it would be better to use overloads with literals, we'll see that later.

---

## Literals

Literals are often useful with type narrowing. Taking the following example:

```python
from typing import Literal


def run(action: Literal["start", "stop"]) -> bool:
    if action == "start":
        return True
    return False
```

We'd like to be able to a) run this on `str` too, and b) get a literal True/False out if we put a literal in.

---

## Overloads

```python
@typing.overload
def run(action: Literal["start"]) -> Literal[True]: ...


@typing.overload
def run(action: Literal["stop"]) -> Literal[False]: ...


def run(action: str) -> bool:
    if action == "start":
        return True
    return False
```

Now if we use a literal, the type system will know the actual value!

---

## Exhaustiveness checking

```python
class Direction(enum.Enum):
    up = enum.auto()
    down = enum.auto()


def handle_direciton(direction: Direction) -> str:
    if direction == Direction.up:  # direction contains [up, down]
        return "up"
    if direction == Direction.down:  # direction contains [down]
        return "down"
    assert_never(direction)  # direction is the empty Union
```

If you add a new enum item later, this will fail until you handle it!

---

## Structural subtyping

This is basically formalized ducktyping

- Python: Protocol
- C++: Concepts
- Java: Interface
- Rust: Traits (_partial parametric polymorphism_, but similar)

---

## Protocols

What is the type of `x` in this function?

```python
def f(x) -> None:
    x.quack()
```

We could look up the actual type(s) this is called on.

Or we could formalize what we know what a Protocol!

---

## Protocols (2)

```python
class Duck(typing.Protocol):
    def quack(self) -> None: ...  # This is actually part of the syntax


def f(x: Duck) -> None:
    x.quack()
```

Now, `f` can be called on any object that has a `.quack()` method, and the type checker will be happy!

---

## Runtime protocols

Opt-in, though types are not checked.

```python
@typing.runtime_checkable
class Duck(typing.Protocol):
    def quack(self) -> None: ...


class MyDuck:
    def quack(self) -> None:
        print("Quack!")


# Works at runtime
assert isinstance(MyDuck, Duck)
```

---

## Verify you pass a Protocol

Here's a (slightly weird) trick to see if you pass a Protocol:

```python
if typing.TYPE_CHECKING:
    _: Duck = typing.cast(MyDuck, None)
```

When running the type checker, you pretend (`cast`) that `None` is an instance of a `MyDuck`, and then see if you can assign it to a variable of type `Duck`. If you can, it's a valid `Duck`.

Note that `typing.assert_type` (3.11) only checks exact types, not structural subtypes, so it's not useful for this.

---

## Standard ABCs

- `Iterable[T]`: Something that can be iterated (has `__iter__`)
- `Iterator[T]`: Something that is being iterated (has `__next__`)
- `Sized`: Something that has a `__len__`
- `Collection[T]`: This can be iterated over and is `Sized`
- `Sequence[T]`: `Collection` with random access (`list`, `tuple`)
- `Generator[T, None, None]`: This is what a `yield` function returns
- `Mapping[K, V]`: Something that acts like a `dict`
- `Callable[[Args, ...], RetValue]`: Something that is callable
- `Set[T]` A `set` or `frozenset`, or similar

---

## When to use Protocols vs. concrete types

- Input parameters should be as general as possible
- Output should be as specific as possible

```python
from collections.abc import Sequence, Sized


def match_ints(a: Sequence[int], b: Sized) -> list[int]:
    return list(a[: len(b)])
```

In this case, we might want to "pass-through" the type of `a`...

---

## Generics: TypeVar

Let's type this trivial function:

```python
def f(x):
    return x
```

We need to "pass-through" the type of x.

---

## Generics: TypeVar (Python 3.12+)

```python
def f[T](x: T) -> T:
    return x
```

In Python 3.12, we could do it as shown. But that is _not_ valid at runtime in older versions, since it's new syntax, and not only an annotation.

This also handles covariance/contravariance for you!

---

## Generics: TypeVar

```python
T = typing.TypeVar("T")


def f(x: T) -> T:
    return x
```

- `TypeVar`'s must be used in the input of a function.
- `TypeVar` can be inside another type
- You can constrain `TypeVar` to certain types & subclasses (`bound=`)
- Or just to specific types (positional arguments)
- TypeVar's can be covariant, contravariant, or invariant (more later)

---

## Type theory: Contravariant or Covariant

TL;DR: Do whatever the type checker tells you

```
                               A -> B -> C
```

Let's say the typevar is `B`. Accepting `C` would be covariant and `A` would be contravariant.

Unions/immutable collections are covariant. `B | None` would accept `C`. Lists (or anything mutable) are invariant.

---

## Going further

Try `mypyc`; it can compile your Python, giving a 2-5x speedup on a fully typed codebase.

- [Awesome Python Typing](https://github.com/typeddjango/awesome-python-typing): A curated list of links to Python typing related things
- [Adam Johnson's Typing series](https://adamj.eu/tech/tag/mypy/)
- [MyPy's cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
