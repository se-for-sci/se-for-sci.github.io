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

```{code-cell} python3
def times_three(x: float) -> float:
    return x*3
```

We can call it with something that's not a float, and `python` doesn't care or
check:

```{code-cell} python3
times_three(["Hi"])
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

By default, mypy supports "gradual typing"; that is, it tries to do things that
it can, but it doesn't complain when types are missing or for using untyped
code. You can turn on flags one by one to make mypy stricter, or you can do it
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

## Type narrowing

## Protocols (& interfaces)

## Generics

```{admonition} Useful links
* [Awesome Python Typing]https://github.com/typeddjango/awesome-python-typing): A curated list of links to Python typing related things
```
