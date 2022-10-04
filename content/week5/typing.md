# Static Typing

What is the best thing about Python? One of the first things you'll hear: no
explicit typing.

What is the worst thing about Python? That's pretty unanimous (only the
occasional whitespace-hater might disagree): no explicit typing.

It's great to be able to pick up Python and not have to worry about types. You
don't have to learn how to write types, you might even find it easier to focus
on what matters without all the extra characters that adding types would bring.
But as your program size grows, you'll quickly find it is much _harder_ to read
code without types, and you'll start wishing a compiler would give you errors
immediately instead of having your code crash half an hour into a job because
you forgot to handle a variable being None.

Over the last few years, Python has been gaining an _optional_ type system. It
looks like this:

```python
def times_three(x: float) -> float:
    return x * 3
```

We can call it with something that's not a float, and `python` doesn't care or
check:

```python
times_three(["Hi"])
```

```output
["Hi", "Hi", "Hi"]
```

This is good, as checking this could be very expensive (imagine a huge list that
supposed to be filled with ints - Python would have to loop over the entire
list! How about a generator that can only be iterated over once? Etc.)

But how do we verify our types look correct? The key to this is to look at a
compiled language. Runtime is not when a compiled language verifies its types -
it does it when you _compile_ - a "pre-running" step. A required pre-running
step, but still, that's what it is. If we want to add this to Python, we need an
_optional_ pre-running step that checks types - it serves the same purpose that
compiling the compiled language does, minus compiling and making machine code,
of course.

With Python, this equates to running a type checker. This is a static check you
run over your code, very similar to testing. It checks the validity of your
types (which can catch many common and uncommon errors) over your entire code
base without needing to write a single test. It's usually very fast, as well.
The downside is that it's not as powerful as testing, so ideally you have both
good tests and static types.

```{admonition} Why learn Python types?
This is not a course about Python. So why learn Python types? Almost everything
you do with Python types applies to compiled code too - it's just required,
rather than optional. Hopefully by learning it now you'll be able to focus on
compiling and adapting to the other parts of the compiled lanague - and you'l
have a new valuable Python skill too!
```

While the language defines types and the Python developers provide types for the
standard library and some major third party dependencies, there are multiple
type checkers to pick from.

- MyPy: The original type checker, from the CPython authors. Written in Python.
  Often trails the other type checkers in adding new typing feature support,
  largely due to the age of the code base and being the first and rather
  home-grown.
- PyRight: Microsoft's type checker. Powers PyLance, which is the language
  server used in VSCode. Written in TypeScript. Very fast, very good. Targets
  running on large codebases and doing incremental live typechecking.
- PyRE: Meta's type checker, written for Instagram. Written in OCaml (FYI,
  Rust's syntax borrows heavily from OCaml). Focused on Security.
- PyType: Google's type checker. Written in Python, requires a unix-like system.
  Differs in that it does inference on untyped functions, and tries not to be
  more strict than runtime.

Together, these form the "big four" type checkers, and representatives from all
four projects are part of the typing mailing lists for Python, and have say on
all new features related to typing.

If you don't know which to pick, use mypy. It's the easiest to run, often the
"lowest common denominator" for features, and it's what your dependencies are
most likely checking against. If you are using VSCode, you'll also get PyRight
underlining things live. PyCharm also has it's own built-in type checker - it
can't be run standalone, but it's similar in importance to the four listed
above.

```{admonition} Runtime typing
There are libraries that do forms of runtime typing as well. You can inspect the
types and act on them if you want, so libraries like `beartype`, `typeguaurd`,
and `strongtyping` will give you something (usually a decorator) that adds
runtime validation based on your type annotations.

Python just by default doesn't do anything with the annotations, and that's for
the best.
```

## Running a type checker

Let's say we have the following `simple.py`:

```{literalinclude} ./mypy_examples/simple.py
:language: python
```

Once you have type annotations, you can run a type checker on your code. This
generally involves installing your type checker (we'll use mypy exclusively),
and then running it on your Python code:

```bash
mypy simple.py
```

```output
simple.py:8: error: Argument 1 to "simple_typed_function" has incompatible type "List[str]"; expected "float"
Found 1 error in 1 file (checked 1 source file)
```

This shows typing problem: we claimed that `simple_typed_function` took only
floats, but we then tried to use it with a list of strings. Either we should
expand our types to include lists of strings, or we should not call the function
with lists of strings! It happens that this one works at runtime - you can be
more strict & clear in your types than you are at runtime. It's _probably_ just
a coincidence this happens to work on lists; you probably never considered this
when you wrote the function.

```{admonition} Where do types go?
There are three possible locations to place types in Python:
* Inline annotations, like we are doing - recommended.
* Type comments - mostly there as a holdover from Python 2.
* Stub files (`.pyi`) - used if you can't add to the source.

Packages of stub files are available for popular untyped libraries using
`<name>-stubs` names on PyPI. You can also add local stubs for a library that's
missing stub files, or add stubs for compiled / generated files in your own
code.
```

By default, MyPy supports "gradual typing"; that is, it tries to do things that
it can, but it doesn't complain when types are missing or for using untyped
code. You can turn on flags one by one to make MyPy stricter, or you can do it
all in one flag `--strict`:

```bash
mypy --strict simple.py
```

```output
simple.py:4: error: Function is missing a type annotation
simple.py:8: error: Argument 1 to "simple_typed_function" has incompatible type "List[str]"; expected "float"
simple.py:9: error: Call to untyped function "simple_untyped_function" in typed context
```

Now MyPy tells us exactly what we need to do to fully type this code and give us
the best results: we need to add types to our untyped function. Notice we do
_not_ need to add types to `input_value`; your type checker will infer most
variables for you. It's only interfaces (function parameters and return values)
that need typing usually.

```{admonition} Inspecting Python types
MyPy gives you a `reveal_type(x)` function that will cause MyPy to print
the type of `x`. Think of it like a `print` statement, but for MyPy! You
can also use `reveal_types()` to show the types for all locals at once. These
functions are very useful for inspecting the types and learning how it works.
And occasionally figuring out the type of something you aren't sure of.
```

````{admonition} Using modern typing annotations even in older languages
If a Python 3.7+ file starts with:
```python
from __future__ import annotations
```
Then all type annotations in the file will be unevaluated strings. This means
you can use Python 3.11 syntax in them, and even Python 3.7 will happily work!
This is great, as every version up to 3.10 has had some large improvements for
typing.  We will be using this new syntax exclusively; use the above import to
follow along on older Python versions.

Also, features added to `typing` (stdlib) are also added to `typing_extensions`,
which you can pip install / add to your requirements. So it's very common to
conditionally pull things from `typing` or `typing_extensions` - we will be
doing that in this material.
````

One case MyPy is very good at is validating "optional" values (things that can
be a value or None). For example:

```{literalinclude} ./mypy_examples/optional.py
:language: python
```

Do you see the error? MyPy does:

```bash
mypy optional.py
```

```output
optional.py:4: error: Item "None" of "Optional[List[str]]" has no attribute "__iter__" (not iterable)
Found 1 error in 1 file (checked 1 source file)
```

Ignoring the old style syntax (it should say
`Item "None" of "list[str] | None"`), it did find the problem. If someone does
not pass `prefix=`, our function will not work - it will try to iterate over
None, which throws an error! We might have forgotten to add a test case for
this, but MyPy can detect it.

The fix is simple - just use `for prefix in prefixes or []:`. Once we learn
about Protocols, another fix would be to replace the `list[str]` with something
that allows tuples too, then `()` could be a default argument instead of
allowing `None`. Note: never make a _list_ a default argument - the list is
bound when the function is created, so any mutation on it will mutate the
default argument itself!

### Escape hatch

You can force your type checker to ignore a bit of code with a `type: ignore`
comment, like this:

```python
x: str = f()
x.nonexistent()  # type: ignore[attr-defined]
```

Only use this as a last resort, but here are places where you need to use this,
especially if your code is not fully typed yet. The reason is optional, but
recommended.

```{admonition} Lying about types
In a compiled language, you have to make the types work. But since they are
optional in Python and only checked by an optional step, you can simply disable
them on a line or a file if you need to. In fact, you can even lie about types.
You can claim something only takes fewer types than it really could take, you
can not include something that only exists for backward compatibility or is
deprecated, etc - all things you could not do in a compiled language. In
general, you should be more strict with typing that with runtime.
```

## Typing basics

### Typing syntax

The following places are places you can add type annotations:

```python
# Variable annotation (3.6+)
x: int = 2

# No assignment is allowed ("declaration")
y: int

# Function annotation
def f(x: int) -> int:
    return x
```

Python type checkers consider a string to be identical to the type itself:

```python
x: "int" = 2
```

This allows you to use classes that have not yet been defined as types, for
example. If you put `from __future__ import annotations` at the top, then all
type annotations are automatically strings, and you don't have to worry about
adding quotes.

You do not need to add types to most variable declarations; they can be deduced.
You do not need to add a type to the `self` or `cls` parameter of a method.

### Simple types

The type of a variable is generally it's class. So these are all types:

```python
a: int = 1
b: str = "hi"
c: bytes = b"hi"
d: float = 1.0
e: complex = 1 + 1j
f: bool = True
g: None = None
```

Notice that `None` is it's own type. If you have a custom or standard library
class, that is also it's type.

The relationship between `int`, `float`, and `complex` is special; `float` can
also be `int`, for example. This keeps the types from being annoying about
matching floats with float operations. Though enforcing the dot might have made
Python 3.11 run faster, as it optimizes float-float and int-int operations, but
not float-int. (A similar special case is setup between `bytes`, `bytearray`,
and `memoryview`, if you were curious. All other cases can be handled correctly
via Protocols, see below.)

### Catch-all types

There are two catch all types in Python. The first is `Any`. This is the "fully
dynamic" type:

```python
from typing import Any

x: Any = could_return_anything()
```

This is basically untyped - the type checker will not catch anything with `Any`.
Everything is allowed. There are places you have to (at least temporarily) use
it, like when reading an data structure from a file. You should generally try to
assign a type as soon as you know one.

The other is `object`. This is also valid on every type, since every type in
Python inherits from object. The difference is that the type checker will allow
nothing on `object` that does not work with every object - hint: `is` and
`str`/`repr` work on all objects! Try to use `object` instead of `Any` if you
can. A great use for `object` is for forwarding args:

```python
def wrap(*args: object, **kwargs: object) -> int:
    return compute_int(*args, **kwargs)
```

Note that the type of `args` then is `tuple[object, ...]` and the type of
`kwargs` is `dict[str, object]`; this is how the `*` and `**` was defined in
Python. Using `object` is a bit safer than `Any` and doesn't require an import.
Obviously, if you know the fixed type of these, it's better to use that.

### Generics

Python also as the idea of generic classes (template classes in C++, the reason
C++'s standard library is called the "stl", standard template library). This is
a class that is parametrized on a "contained" type. Let's look at one:

```python
a: list[int] = [1, 2, 3]
```

The parameters of the type are provided using `[]` syntax (`<>` in C++). List's
have a parameter that takes the contents of the list. You can have 0 or more of
those items. (Note: list is generic starting in Python 3.9, so either use future
annotations or Python 3.9 for the above syntax; before that you had to use
`from typing import List` and `List[int]`). The `set` collection works the same
way.

Now let's look at `tuple`; it has a design that's rather unique (most other
containers are more like `list`):

```python
b: tuple[int, int, int] = (1, 2, 3)
c: tuple[int, ...] = (1, 2, 3)
```

You'll see `tuple`'s design is customized based on the fact tuple is more often
a heterogeneous container. You can chose to type it by each item, or you can use
`...` to indicate there are 0 or more of the last item. If your type checker
infers the type of tuple, it will select the "one each" method.

Now let's look at `dict`:

```python
d: dict[str, int] = {"one": 1, "two": 2}
```

Dictionaries take two arguments, the key and the value. Dictionaries are such an
important structure that there's a second way to add types to them, `TypedDict`,
that allows you to assign specific types to specific keys. We won't cover that
here, but it is available if you need it. If you do have different types for
different entries, you often should be using a (data)class instead of a
dictionary - dicts are best homogeneous.

That's the built-in collections. We'll see a better way to type _input_
collections in a later section.

### Unions

What if you want to have multiple types? Whenever two or more types are allowed,
that's a Union. For example, this is a list that can take either ints or
strings:

```python
x: list[int | str] = [1, "hi"]
```

This is a list that is either full of ints, or strings, but not mixed:

```python
x: list[int] | list[str] = [1, 2]
y: list[int] | list[str] = ["hello", "world"]
```

One of the most common unions is the "optional" pattern, probably better called
"Nonable":

```python
x: int | None = None
```

This can then be set to an `int` later. This is very common for optional
arguments.

## Other types

### Final

You can add special features to Python typing that are normally only found in
compiled languages. One example of this is `Final`:

```python
x: Final = 3
```

You are now not allowed to reassign this:

```python
# Type checker will error here
x = 4
```

This is very useful for global constants - they should not be modified, now you
can ensure that via the type checker. Note that this is not a "true" `const`
variable; you can still mutate the variable if it's mutable. At least the Python
authors were better at naming this - C++ `const` pointers and variables have the
same problem if they hold a reference/pointer that is mutable.

`Final` is a shorthand for `Final[Literal[3]]` in this case. You can explicitly
include the type if you want (and this is not considered an unspecified generic
when you turn on the matching flag in MyPy, since it's not assuming `Any` for
the parameter). Some type checkers (PyLance) treat this a little differently
when unspecified, so specifying the type when you have a container is mildly
recommended.

Another example is `@typing.final`, which is a decorator that marks a method as
un-overridable.

### Enums

Python's enums are handled by type checkers as well; they act like literals and
unions.

```python
from enum import Enum


class Direction(Enum):
    up = "up"
    down = "down"


reveal_type(Direction.up)  # Revealed type is "Literal[Direction.up]?"
reveal_type(Direction.down)  # Revealed type is "Literal[Direction.down]?"
```

Note that the `?` from `reveal_type` tells you that a type was inferred. The
type checker is allowed to treat `Literal[Direction.up]?` as `Direction` later
since it was inferred.

### TypedDict

Python provides `TypedDict`, which allows you to customize the types of values
based on string keys.

```python
class VersionDict(typing.TypedDict):
    major: int
    minor: int
    patch: int


d: VersionDict = {"major": 1, "minor": 2, "patch": 3}
```

If you want these keys to be optional, you can add `total=False` to the _class
definition_ (since version 3, Python has supported keyword arguments here too).
Since Python 3.11 (or using `typing_extensions`) you can mark fields as required
or potentially missing as well. (before this, you had to do this by making two
classes with different `total=` settings and using inheritance, but it was
cumbersome).

```python
class VersionDictExtra(VersionDict, total=False):
    build: int
```

### NamedTuple

Python didn't handle `collections.namedtuple` very well when it came to adding
types, so `typing.NamedTuple` provides a new, simpler syntax that also allows
you to specify the types:

```python
# Classic
Version = collections.namedtuple("Version", "major", "minor", "patch")

# New
class Version(typing.NamedTuple):
    major: int
    minor: int
    patch: int
```

This syntax is often nicer for runtime as well, and supports default values a
bit more naturally.

## Type narrowing

One of the most important features to running a type checker is type narrowing.
This tracks a union and removes entries if something is excluded, often in
branching. For example:

```python
def f(x: str | None) -> str:
    if x is None:
        return ""
    return x
```

This passes a type check. The `if` statement narrows the union `str | None` to
just `None` inside the body of the if. Once the `if` has passed, then the type
of `x` is now just `str`, since if it was `None` the function execution could
not have reached this point. (FYI, this style is called a "guard".)

What do you think this would print?

```python
def f(x: str | None) -> None:
    if x:
        reveal_type(x)
    else:
        reveal_type(x)
```

The first `reveal_type` will print `str`, since `None` can not be in this
branch; it can't be truthy. The second `reveal_type` will print `str | None`,
since `None` must be falsey, and `str` might be if it's the empty string.
Technically, since MyPy shows the old syntax, this is exactly what it prints:

```output
tmp.py:3: note: Revealed type is "builtins.str"
tmp.py:5: note: Revealed type is "Union[builtins.str, None]"
Success: no issues found in 1 source file
```

Usually your type checker can narrow correctly, but occasionally it might need
help. For example,

```python
def could_be_none(y: bool) -> int | None:
    return 42 if y else None


y = could_be_none(True)
print(f"Bitcount: {y.bit_count()}")
```

This won't pass a typecheck, since `None.bit_count()` is not supported. If you
know this is not going to be None based on the situation, you can force a
narrowing using `assert`:

```python
y = could_be_none(True)
assert y is not None
print(f"Bitcount: {y.bit_count()}")
```

Now this passes the type check, because `y` is no longer `None`, it was narrowed
out by the assert.

If you had this exact situation, it would be be better to teach the type checker
that the literal `True` forces a non-None return value - this can be done with
`overload`s, which we'll cover later.

### Literals

There are cases were you want to control the types based on the exact value of
an input. Given we already have unions, we can use that to include literal
values (other than None, which is already only a single value). The easiest
literal are the bool values. You could see `bool` as `Literal[True, False]`,
which is basically how type checkers see it. Strings can have literal values
too:

```python
from typing import Literal


def run(action: Literal["start", "stop"]) -> bool:
    if action == "start":
        return True
    return False
```

This will require `"start"` or `"stop"` to be used; `run("begin")` will fail a
type check. Note that `Literal["a", "b"]` is a shorthand for
`Literal["a"] | Literal["b"]`.

Note for backwards compatibility (and probably generally less surprising), the
inferred type of `x = True` is `bool`, not `Literal[True]`. If type checkers did
this, then `x = False` could not be set later, that would change the type (at
least as some strictness level, variables should not be reassigned with a
different type, just like a compiled language).

### Overloads

You can specify overloads with the type checker. These are _typing_ overloads;
similar to `functools.singledispatch`, but you are responsible for setting up
the dispatch or returns; this is just telling the type checker that different
patterns of input types produce different output types.

Here's an example:

```python
import typing
from typing import Literal


@typing.overload
def could_be_none(y: Literal[True]) -> int:
    ...


@typing.overload
def could_be_none(y: Literal[False]) -> None:
    ...


# This is optional, but allows passing an unknown bool in too
@typing.overload
def could_be_none(y: bool) -> int | None:
    ...


def could_be_none(y: bool) -> int | None:
    return 42 if y else None


x: bool = return_a_bool()
a: int = could_be_none(True)
b: None = could_be_none(False)
c: int | None = could_be_none(x)
```

Note the `...` above are the actual syntax - these are used in typing to
indicate the body is somewhere else. (Unlike `pass`, which indicates there is no
body or it's not implemented yet.) These overloads are type overloads only -
they can't contain a body, they do nothing at runtime.

### Exhaustiveness checking

If you have an enum or a union, often you want to handle all possibilities.
Something like this runtime code:

`````{tab-set}
````{tab-item} Classic if statements
```python
class Direction(Enum):
    up = "up"
    down = "down"


def handle_direciton(direction: Direction) -> str:
    if direction == Direction.up:
        return "up"
    if direction == Direction.down:
        return "down"
    raise AssertionError(f"Unhandled direction {direction}")
```
````
````{tab-item} Pattern matching (Python 3.10+)
```python
class Direction(Enum):
    up = "up"
    down = "down"


def handle_direction(direction: Direction) -> str:
    match direction:
        case Direction.up:
            return "up"
        case Direction.down:
            return "down"
        case _:
            raise AssertionError(f"Unhandled direction {direction}")
```
````
`````

If you add a new direction, you will not be notified about `handle_direction`
not handling the new direction until you hit it at runtime (hopefully by adding
a test, not by your code breaking in the wild!). This can be handled by the type
checker; it's called exhaustiveness checking:

`````{tab-set}
````{tab-item} Classic if statements
```python
from typing_extensions import assert_never  # typing in 3.11+


def handle_direciton(direction: Direction) -> str:
    if direction == Direction.up:
        return "up"
    if direction == Direction.down:
        return "down"
    assert_never(direction)
```
````
````{tab-item} Pattern matching (Python 3.10+)
```python
from typing_extensions import assert_never  # typing in 3.11+


def handle_direction(direction: Direction) -> str:
    match direction:
        case Direction.up:
            return "up"
        case Direction.down:
            return "down"
        case _:
            assert_never(direction)
```
````
`````

The way this works is that `assert_never` takes `Never` as an input type. The
`Never` input type is an empty (fully narrowed) union. If the thing you give it
has not been fully narrowed, it will be a typing error. (It also throws a
runtime error for you similar to the one we used above). Now your type checker
will immediately notify you if you add an item to Direction but forget to update
the usage!

````{admonition} Historical note
The implementation of `NoReturn`, the type for a function that never makes it to a
return statement, is also an empty union, so in the past this was how we could
implement this feature:

```python
from typing import NoReturn

Never = NoReturn


def assert_never(val: Never) -> NoReturn:
    assert False, f"Unhandled value: {value} ({type(value).__name__})"
```
The actual `Never` return type gives a better type checker error, so it's nice
that it's directly available now.
````

## Structural subtyping

We've already covered inheritance and ABCs. Now let's cover a different form,
called structural subtyping, that fixes several shortcomings of that method.
Namely, we lost modularity when we stared forcing inheritance structures.
Structural subtyping trades code reuse for modularity. In Python, it's called a
Protocol. C++ calls it Concepts. Java called it Interfaces. In essence, it's
formalized duck typing.

Rust implements _partial parametric polymorphism_ as Traits, which is somewhat
similar but more explicit and controlled.

### Protocols

Let's look at the following function:

```python
def f(x):
    x.do_something()
```

What is the type of `x`? If I haven't spoiled your Python duck typing sense yet
by the previous sections, hopefully you'll answer "something that has
`do_something()`"[^1] or "anything that has `do_something()`". Up until now,
we've been trading Python duck typing for known types. But we don't have to!
Let's just formalize what we have:

[^1]: If you answered this, you might like Rust Traits better than Protocols.

```python
from typing import Protocol  # typing_extensions before 3.8


class DoesSomething(Protocol):
    def do_something(self) -> None:
        ...


def f(x: DoesSomething) -> None:
    x.do_something()
```

Like before, the `...` is part of the syntax; Protocols have no bodies. Any
class that has a `.do_something()` method that matches this signature can be
passed to this function! We now have duck typing that MyPy can report on.

In C++20, doing this is a huge win for compiler error messages on templated
code. This allows the compiler to instantly quit and tell the user exactly what
is required, rather than producing a massive bunch of unreadable error messages
at the first place an error is encountered inside the function (and this can be
nested, making it really hard to see where you broke an unspecified assumption).
It's also a much easier and more readable way of doing overloads on templated
arguments in C++20.

Most things available for classes (methods, members, properties, settable
properties, etc.) are available. You just leave all bodies as `...`.

#### Runtime protocols

You can make protocols runtime checkable, as well:

```python
import typing


@typing.runtime_checkable
class DoesSomething(Protocol):
    def do_something(self) -> None:
        ...


assert isinstance(MyThing, DoesSomething)
```

This will pass if `MyThing` has a `do_something` method. Unlike the static
version, this will only check for the existence of that method; it will not
check the type signature (it's a runtime construct, after all).

If you use a `hasattr(x, "do_something")` pattern, a runtime checkable Protocol
can replace it and type checkers will correctly narrow as well. Though if it is
a performance critical section of code, the `runtime_checkable` `Protocol` is a
little slower that then `hasattr` and a `type: ignore` comment, sadly.

### Verifying a Protocol

Notice the main difference between a Protocol and an ABC is that you are
required to inherit from the ABC (subtyping), which the Protocol simply requires
the structure of the class to look like a subtype of the Protocol. You _can_
explicitly inherit from the Protocol if you want to, but there's much much
reason to - a better trick that doesn't require the Protocol to be present at
runtime is this:

```python
class MyDoesSomething:
    def do_something(self) -> None:
        print("Yep")


if typing.TYPE_CHECKING:
    _: DoesSomething = typing.cast(MyDoesSomething, None)
```

There's a bit to unpack here, so let's go over it left to right. We are putting
this inside a block only the type checker will analyze; it is skipped at
runtime. We are making a variable, but we don't care about it, so we name it
`_`. Then we tell the type checker this is going to be the desired Protocol. We
then assign and instance of our class to this variable that is typed as the
Protocol; if the type checker can't do this, we didn't successfully implement
the Protocol. The `typing.cast` takes a value (just None in this case) and tells
the type checker to treat it like `MyDoesSomething`. This is to avoid
constructing the class - there's no constructor involved here. In this example,
we could have just used `MyDoesSomething()` instead.

Note that we couldn't use `assert isinstance`, which would require
`@runtime_checkable` (even in a `TYPE_CHECKING` block) or `typing.assert_type`,
which will only check exact type equivalence, not structural subtypes.

### Standard ABC's

There are a large number of standard protocols in Python. These were initially
added to `typing`, but were merged with `collections.abc` once runtime generics
were added to the standard library in Python 3.9. You can import them from
either place if you use Python 3.9+ or the annotations import. These are both
ABCs and Protocols; if you subclass from them, you can sometimes get a few free
mix-in methods[^2]; if you don't, you have to implement all of the required
methods.

[^2]: Mix-in's in these ABCs are not provided separately as mixin classes.

Here are some of the most useful ones - a full list including required methods
is in the [Python docs](https://docs.python.org/3/library/collections.abc.html):

- `Iterable[T]`: This is something that can be iterated over (has `__iter__`)
- `Iterator[T]`: This is something that is being iterated (has `__next__`)
- `Sized`: Something that has a `__len__`.
- `Collection[T]`: This can be iterated over and is `Sized`.
- `Sequence[T]`: This is a `Collection` with random access, like `list` or
  `tuple`.
- `MutableSequence[T]`: Basically a list. Why are you mutating input arguments,
  though?
- `Generator[T, None, None]`: This is what a `yield` function returns. It can
  also be written as `Iterator[T]`, but this is not quite correct.
- `Mapping[K, V]`: Something that acts like a `dict`.
- `Callable[[Args, ...], RetValue]`: Something that is callable, like a
  function.
- `Set[T]` A `set` or `frozenset`, or similar.

As a general rule: _take the most general from possible_, and _return the
specific form_. For example:

```python
from collections.abc import Sequence, Sized


def match_ints(a: Sequence[int], b: Sized) -> list[int]:
    return list(a[: len(b)])
```

This takes two lists and returns the first list sliced to match the second list.
By using generics, we can also swap these lists out for anything else that would
work, like tuples or user defined classes with the right special methods. We
always return a `list`, so we stay as specific as possible in the return.

## More about generics

### TypeVar

You've seen overload, which lets you change the output type based on the input
type. One very common use case is passing though a type. For example, take the
trivial function:

```python
def f(x):
    return x
```

How would you type this? You want to tell the type checker the output type is
the same as the input type. This is done using `TypeVar`:

```python
from typing import TypeVar

T = TypeVar("T")


def f(x: T) -> T:
    return x
```

TypeVar's do not hold a type by themselves. They always occur at least once in
the _input_ of a of function. They may occur multiple times, or in the output,
but they must occur in the input, since that's how they pick up a type. They can
only be used in a function where they are in the input types. Above, when you
call `f`, then `T` will be the type you call `f` with. So the above will pass
through any types. You can use this inside other types, as well:

```python
def make_a_list(*args: T) -> list[T]:
    return list(args)


def default_construct(cls: type[T]) -> T:
    return cls()
```

`TypeVar`'s have a few other options. You can use `bound=` to force them to only
bind to a type or it's subclasses (it picks the most specific possible) - unions
are also supported. You can constrain to a preset collection of types, and it
will only match those types exactly.

### Custom Generics

Another use for TypeVar is for creating custom Generic classes. Let's say you
wanted to make a custom container that holds arbitrary types, called MyList.
Here's how you'd do it:

```python
class MyList(Generic[T]):
    def __init__(self, items: Iterable[T]) -> None:
        self.items = list(items)

    def append(self, element: T) -> None:
        self.append(element)

    ...
```

This will then be usable as `MyList[int]`, for example.

### Contravariant or Covariant TypeVar? (advanced)

You can also specify `covariant=True` or `contravariant=True` when you make a
TypeVar; this changes the invariance of a generic type. Simple TL;DR solution:
if the type checker tells you to add one of these, add it.

The longer explanation is based on parents and children. If you have an
inheritance diagram `A -> B -> C` and your TypeVar `T` resolves to `B`, what is
also allowed? If nothing is allowed except `B`, your TypeVar is **invariant**
(the default). If you do allow children, then your TypeVar needs to be
**covariant** and `*_co` is recommended for the name. If you allow parents, then
it is **contravariant**, and `*_contra` is recommended for the name.

Unions are covariant. `B | None` would also accept `C`.

Lists (generally anything mutable) are invariant. If you have a `list[B]`, it is
invalid to append either `A` or `C` to it.

### Self

A special, very common need is to return a type that is related to `self`.
There's a very easy way to do it in `typing_extensions` (and typing in Python
3.11), but it's not yet supported by MyPy (as of 0.982) although all the other
major type checkers have added support.

The "chaining" pattern is a common use case, as are factory methods
(classmethods). Here's how you'd do it:

`````{tab-set}
````{tab-item} Manual
```python
Self = TypeVar("Self", bound="Vector")


@dataclass
class Vector:
    x: float
    y: float

    @classmethod
    def origin(cls: type[Self]) -> Self:
        return cls(0, 0)

    def inplace_unit(self: Self) -> Self:
        mag = (self.x**2 + self.y**2) ** 0.5
        self.x /= mag
        self.y /= mag
        return self
```
````
````{tab-item} Self
```python
from typing import Self  # or typing_extensions before 3.11


@dataclass
class Vector:
    x: float
    y: float

    @classmethod
    def origin(cls) -> Self:
        return cls(0, 0)

    def inplace_unit(self) -> Self:
        mag = (self.x**2 + self.y**2) ** 0.5
        self.x /= mag
        self.y /= mag
        return self
```
````
`````

Notice with the manual version, we ideally should bind the TypeVar to the class,
so it's not reusable (new TypeVar for each class), and we have to annotate
`self` or `cls` so the TypeVar will be usable.

Note: don't just return `"Vector"`. That will be incorrect if someone subclasses
`Vector`.

## Going further

If you fully statically type your codebase, then you can try `mypyc`. This
compiles your Python into a compiled language and can give you a speed boost,
ranging from 2-5x. This is used on MyPy itself, and on the black code formatter.
Results may vary, and it's not as fast as normal compiled code, but it could be
very useful and basically free once you are statically typed.

```{admonition} Useful links
* [Awesome Python Typing](https://github.com/typeddjango/awesome-python-typing): A curated list of links to Python typing related things
* [Adam Johnson's Typing series](https://adamj.eu/tech/tag/mypy/)
* [MyPy's cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
```
