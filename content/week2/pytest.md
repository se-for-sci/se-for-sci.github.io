# Intro to pytest

## Basics of writing a test

### Starting your first test

The simplest possible test doesn't need a framework or anything extra. You could
just start with this:

```python
def f(x):
    return x**2


def test_f():
    assert f(0) == 0
    assert f(1) == 1
    assert f(2) == 4


if __name__ == "__main__":
    test_f()
```

This is a working unit test for the function `f(x)`. If you were to run this
file, you would be running a test which will verify that f does square a few
inputs. But there are a few problems with this, especially related to scaling:

- The test does not report that it passed, it's silent.
- If the test fails, you get very little helpful output, just the line which
  failed. You can't see what `f(x)` actually returned.
- You have to add each test manually to be run (duplication).
- Only the first test fails, if you were to put in multiple test function; it
  would be better to see all failures at the end of the test run.
- You have no controls over what tests run, or what to do if one fails.
- You are giving up running the file to running tests - maybe you want to run
  the file and run `f(sys.argv[1])` or something like that.

### Why not x-unit style testing?

There is a framework built into Python for testing. It's based on the Java
x-unit style framework. While this fixes all the problems listed above, it loses
a lot of simplicity. Now our code looks like this:

```python
import unittest


def f(x):
    return x**2


class TestFunction(unittest.testcase):
    def test_f(self):
        self.assertEqual(f(0), 0)
        self.assertEqual(f(1), 2)
        self.assertEqual(f(2), 4)
```

Now you can run `python -m unittest` and that will pick up and run the test,
with nice reporting, etc. However, this is a lot of boiler plate code. You have
to subclass and come up with class names (which do group the code, at least).
You have to look up dozens of `assert*` methods. You have to pass `self` around.
Setup and teardown code (not shown above) is also hard to reuse. _Nobody (that I
know) enjoys writing tests_; the simpler and nicer you can make them, the more
fun they are to write, the more tests you will write. Wouldn't it be nice if we
could have both the simple syntax _and_ nice running features?

### Writing pytest tests

We can by using pytest. While pytest _can_ run unittest code, it has its own
preferred native testing style:

```python
def f(x):
    return x**2


def test_f():
    assert f(0) == 0
    assert f(1) == 1
    assert f(2) == 4
```

You can run this (after installing `pytest`) with `python -m pytest` or
`pytest`. Pytest will rewrite the assert statements before handing the code over
to Python so that you can get useful error messages! It will automatically find
`*test*` functions. It will report successes. It will hide output unless there's
a failure. And it has a lot of useful flags. From here on, we will be using
pytest for Python testing.

```{admonition} Test location
For the moment, for simplicity, we are putting the code and the test in the same
file. In the future, it's usually better to put your tests into separate files
in a separate directories, like `tests/`. Pytest will look everywhere for tests,
though you can configure it to only look in certain directories if you wish.
```

## Fixtures

One of the key features of x-unit style tests is setup/teardown code. Often you
need to do something like open files, prepare resources, precompute an expensive
input, etc. The classes had overridable methods for this. Pytest offers
something even better: **fixtures**. A fixture is:

- **Modular**: It is not tied to a class. You can reuse fixtures however you
  want.
- **Scoped**: You can make a fixture that is class level, but you can also make
  function level, module level, and session level fixtures too! Want do do
  something every test? Or something once for the whole testing session?
  Fixtures can do that.
- **Composable**: You can make a new fixture using an old one. You can use as
  many fixtures as you want.
- **Optionally Automatic**: You can activate "autouse" on a fixture, which
  causes it to always apply to all tests where it's defined. This is great for
  fixtures that mock expensive or dangerous system calls.
- **Easy to add Teardown**: There's a simple way to add teardown to any fixture.
- **Easy to Parametrize**: You can parametrize tests via fixtures too.

This is an example of _using_ a built-in fixture:

```python
def test_printout(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert "hello" in captured.out
```

Notice the argument - you never "call" tests, so pytest looks up fixtures by the
name of the argument you are requesting and passes them in.

The `capsys` fixture captures the system level text output. The `print` call is
captured. Then we can call `.readouterr()` on the fixture and that gives us the
stdout and stderr streams.

A few good built-in fixtures
([full list in pytest 7](https://docs.pytest.org/en/7.1.x/reference/fixtures.html)):

- `capsys`: Capture stdout/stderr (most Python printing)
- `capfd`: Capture using file descriptors (C extensions, etc) - use this if
  `capsys` doesn't get it.
- `monkeypatch`: temporarily modify pretty much anything (undoes the mod after
  running the test)
- `request`: Used when making new fixtures
- `tmp_path`: Provide a temporary, unique path (test scope)
- `tmp_path_factory`: Session scoped temporary path creation
- `cache`: Store and access values across multiple runs.

Plugins often add fixtures. It's also easy to write your own! Fixtures can be
added to a test file, or they can be placed in `conftest.py`, where they will be
available to all files in the same directory or any subdirectories.

Here's a simple fixture:

```python
import pytest


@pytest.fixture
def something():
    return "world"


def test_something(something):
    assert something == "world"
```

Notice that we told pytest we were making a fixture by adding the
`pytest.fixture` decorator. We can return anything we want. We use the fixture
in a test (function with `test` in the title) by putting in the name as an
argument. Inside the function, we get the value the fixture returns.

This is not quite the x-unit style setup yet - the fixture return will be rerun
for every test (which is sometimes handy). If we want to change the scope, we
can just tell the fixture what scope we want:

```python
import pytest
import time


@pytest.fixture(scope="session")
def slow():
    time.sleep(5)
    return "world"


def test_a(something):
    assert something == "world"


def test_b(something):
    assert something == "world"
```

Fixtures support setup _and_ teardown, and they do so using the same "trick"
`contextlib.contextmanager` uses:

```python
@pytest.fixture
def before_after():
    print("Setting up")
    yield "world"
    print("Tearing down")
```

Just swap "return" for "yield", and place teardown code after the yield. That's
it. If you have multiple fixtures with different scopes, they all setup and
teardown correctly.

One really powerful built-in fixture is monkeypatch. Let's say you have code
like this:

```python
import sys


def some_function():
    if sys.platform.startswith("linux"):
        ...
```

If the contents of the function work on any os, you can actually test it on any
os! We can monkeypatch `sys.platform` to be something that it's not.

```python
import sys


def test_some_function_linux(monkeypatch):
    monkepatch.setattr(sys, "platform", "linux")
    # stuff here will think it's on linux
    ...
    # after the test, the monkeypatching is removed!
```

## Parametrizing

Now let's say we want to test all three OS's on our little function. Assuming
the logic inside works on all os's, and it doesn't call anything that breaks if
we lie about the os (monkeypatching is best on what you own!), we can
parametrize:

```python
import pytest
import sys


@pytest.mark.parametrize("platform", ["linux", "win32", "darwin"])
def test_some_function_linux(monkeypatch, platform):
    monkepatch.setattr(sys, "platform", platform)
    ...
```

This is a "mark" in pytest. It's really just a way to add arbitrary metadata to
a test, but pytest recognizes a few marks by default during test collection, and
this is one of them. You give it the name of the argument(s), and the values
(and optionally an `id=` for nice names). It generates three test functions,
each runs and is reported separately.

This is great for one-off parametrization, but if we want to do this on several
tests, we can use a fixture! Let's rewrite this as a fixture:

```python
import pytest
import sys


@pytest.fixture("platform", ["linux", "win32", "darwin"])
def platform(request):
    return request.param


def test_some_function_linux(monkeypatch, platform):
    monkepatch.setattr(sys, "platform", platform)
    ...
```

Anything that asks for "platform" will run three times. However, we can go one
step further in this case, and combine the monkeypatching into our platform
fixture:

```python
import pytest
import sys


@pytest.fixture("platform", ["linux", "win32", "darwin"])
def platform(request, monkeypatch):
    monkepatch.setattr(sys, "platform", platform)
    return request.param


def test_some_function_linux(monkeypatch, platform):
    ...
```

Now we automatically get the monkeypatching each time, too!

You can move your fixture to a file called `conftest.py` in the same test
directory (or above), and it will still be usable, no import needed. This allows
you to easily share fixtures between test modules.

You can see how you can build these into powerful composable tools for testing
hard-to-test functionality!

[hypothesis]: https://hypothesis.readthedocs.io
[pytest]: https://docs.pytest.org
[pytest-mock]: https://pypi.org/project/pytest-mock/
[unittest.mock]: https://docs.python.org/3/library/unittest.mock.html
