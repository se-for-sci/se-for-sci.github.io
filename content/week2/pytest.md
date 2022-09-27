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

## Floating point comparisons

What is the result of this code:

```python
0.1 + 0.2 == 0.3
```

You can run it in your favorite language. Is the result what you thought it
would be?

As a general rule, avoid `==` and `!=` with floating point numbers. It's much
better to test approximate ranges - and most testing frameworks have a mechanism
to make this easy. Pytest's is `pytest.approx`.

```python
import pytest

assert 0.1 + 0.2 == pytest.approx(0.3)
```

This will check a range around the value. The default is good for a few
operations on floating point numbers, and you can customize it via keyword
arguments.

```{admonition} Correct calculations
If this bothers you, there are two libraries in the standard library
that help with exact calculations: `decimal.Decimal` and `fraction.Fraction`. These
do exact arithmetic, but are many times slower and bulkier than normal floating point calculations.
99% of the time, you just learn to work around floating point limitations.
```

## Fixtures

One of the key features of x-unit style tests is setup/teardown code. Often you
need to do something like open files, prepare resources, precompute an expensive
input, etc. The classes had overridable methods for this. Pytest offers
something even better: **fixtures**. A fixture is:

- **Modular**: It is not tied to a class. You can reuse fixtures however you
  want.
- **Scoped**: You can make a fixture that is class level, but you can also make
  function level, module level, and session level fixtures too! Want to do
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

Notice the argument, `capsys` - you never "call" tests, so pytest looks up
fixtures by the name of the argument you are requesting and passes them in.

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

Fixtures are great for keeping your tests DRY.  If you notice you setup the
same object for multiple tests, extract it to a fixture.  Combined with
parameterizing, you can generate tests suites from collections of fixtures
easily.

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

You can see how you can build these into powerful, composable tools for testing
hard-to-test functionality!

## Skipping tests

You can put any arbitrary marks on any test, and use them to select a subset of
tests very quickly from the command line. There a couple of other really
important built-in marks: `skipif` will skip a test if a condition is True,
`skip` will always skip a test, and `xfail` will tell pytest that failing the
test is okay (or even required with `strict=True`) - this one also optionally
supports a condition.

```python
import pytest
import sys


@pytest.mark.skip
def test_never_runs():
    assert False


@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10 to run")
def test_py310_plus():
    assert True


@pytest.mark.xfail(strict=True, reason="This is currently expected to fail")
def test_xfail():
    assert False
```

There are a few other options for these marks; they are very useful if you have
not yet implemented a feature or fixed a bug, or if you have a flaky test, or if
you have tests that don't apply to all systems.

One more really common need is skipping a test if an import is missing. You can
do that with `pytest.importorskip`:

```python
np = pytest.importorskip("numpy")
```

This will skip everything after it in a module, or the test if placed inside a
test.

If you want to apply a mark to the entire test module, assign it to the global
variable `pytestmark=`; pytest will look for this when it reads the module.

## Organizing tests

Pytest allows quite a bit of organization: you have a test folder (or more), any
number of subfolders, any number of test files, an optional class, and then test
functions (or methods in the class case). Unlike x-unit style testing, the test
class is simply a normal class and is just used for organization (the self
arguments are useless). One benefit of the class is that you can apply a mark to
the whole class without applying it to the whole file. You could also use
subclassing, etc. like normal. But 95% of tests in pytest are better as simple
test functions.

Every test folder can have a `conftest.py`, and that's where you put fixtures
and pytest hooks. This also helps you avoid adding a `__init__.py`, which is not
ideal for tests - they don't have to be importable. The fixtures are available
for any tests in that folder, and any subfolders.

## Plugins

Pytest supports plugins, and there's a thriving ecosystem - there are nearly 1K
plugins according to
[pytest's automated page](https://docs.pytest.org/en/7.0.x/reference/plugin_list.html).
A few plugins of note:

- `pytest-mock`: Makes the excellent `unittest.mock` built-in library nicer to
  use from pytest as native fixtures.
- `pytest-ascyncio`: Allows pytest to natively test ascync functions.
- `pytest-xdist`: Distributed testing, loop on failing.
- `pytest-subprocess`: Mocks subprocess calls.
- `pytest-benchmark`: Compute benchmarks as part of testing (also see
  [ASV](https://github.com/airspeed-velocity/asv) if interested in
  benchmarking).

## Running and configuring pytest

### Configuring pytest

pytest supports configuration in `pytest.ini`, `setup.cfg`, or, since version 6,
`pyproject.toml`. If you can require pytest 6 (in other words, if Python 3.6+ is
fine - pytest is a developer requirement, not a user one, so limiting it is
fine), then use `pyproject.toml`. This is an example configuration:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = ["-ra", "--strict-markers", "--strict-config"]
xfail_strict = true
filterwarnings = ["error"]
log_cli_level = "info"
testpaths = ["tests"]
```

The `minversion` will print a nicer error if your `pytest` is too old (though,
ironically, it won't read this is the version is too old, so setting "6" or less
in `pyproject.toml` is rather pointless). The `addopts` setting will add
whatever you put there to the command line when you run; `-ra` will print a
summary "r"eport of "a"ll results, which gives you a quick way to review what
tests failed and were skipped, and why. `--strict-markers` will make sure you
don't try to use an unspecified fixture. And `--strict-config` will error if you
make a mistake in your config. `xfail_strict` will change the default for
`xfail` to fail the tests if it doesn't fail - you can still override locally in
a specific xfail for a flaky failure. `filter_warnings` will cause all warnings
to be errors (you can add allowed warnings here too). `log_cli_level` will
report `INFO` and above log messages on a failure. Finally, `testpaths` will
limit `pytest` to just looking in the folders given - useful if it tries to pick
up things that are not tests from other directories.
[See the docs](https://docs.pytest.org/en/stable/customize.html) for more
options.

pytest also checks the current and parent directories for a `conftest.py` file.
If it finds them, they will get run outer-most to inner-most. These files let
you add fixtures and other pytest configurations (like hooks for test discovery,
etc) for each directory. For example, you could have a "mock" folder, and in
that folder, you could have a `conftest.py` that has a mock fixture with
`autouse=True`, then every test in that folder will get this mock applied.

In general, do not place a `__init__.py` file in your tests; there's not often a
reason to make the test directory importable, and it can confuse package
discovery algorithms.

Python hides important warnings by default, mostly because it's trying to be
nice to users. If you are a developer, you don't want it to be "nice". You want
to find and fix warnings before they cause user errors! Locally, you should run
with `-Wd`, or set `export PYTHONWARNINGS=d` in your environment. The `pytest`
warning filter "error" will ensure that `pytest` will fail if it finds any
warnings.

### Running pytest

You can run pytest directly with `pytest` or `python -m pytest`. You can
optionally give a directory or file to run on. You can also select just some
subset of tests with `-k <expression>`, or an exact test with
`filename.py::test_name`.

If a test fails, you have lots of options to save time in debugging. Adding
`-l`/`--showlocals` will print out the local values in the tracebacks (and can
be added by default, see above). You can run `pytest` with `--pdb`, which will
drop you into a debugger on each failure. Or you can use `--trace` which will
drop you into a debugger at the start of each test selected (so probably use the
selection methods above). `pytest` also supports `breakpoint()` in Python 3.7+.
You can also start out in your debugger at the beginning of the last failed test
with `--trace --lf`.
[See the docs](https://docs.pytest.org/en/stable/usage.html) for more running
tips.

```{admonition} Further reading and useful links
* [Scikit-HEP Develoepr Pages](https://scikit-hep.org/developer/pytest)
* [Test and Code](https://testandcode.com): a podcast on testing and related topics
* [The Good Research Code Handbook](https://goodresearch.dev): General resource with a strong focus on testing
* [Research Software Engineering with Python](https://merely-useful.tech/py-rse/): Also has a testing section.
```

[hypothesis]: https://hypothesis.readthedocs.io
[pytest]: https://docs.pytest.org
[pytest-mock]: https://pypi.org/project/pytest-mock/
[unittest.mock]: https://docs.python.org/3/library/unittest.mock.html
