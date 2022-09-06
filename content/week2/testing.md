# Intro to testing

Tests are crucial to writing reliable software. A good test suite allows you to:

- Immediately know if a new platform or software version works,
- Refactor and cleanup your code with confidence,
- Evaluate the effect of additions and changes.

It also does a few things you might not have expected:

- Document bugs --- if every time you find a bug, you write a test that captures
  the bug, it helps mark development history of the code, and it assures that
  bug (or similar bugs) won't creep in again
- To force you to make requirements and expectations _explicit_ (**adversarial
  view** of testing --- you are trying to break the code, albeit in a "safe
  space").
- To grow _confidence_ in the code (both for you and other users) --- this is
  why it's important for tests to be _recorded_ and, to the extent feasible,
  runnable _automatically_.

In short: **tests serve as a form of documentation about your expectations of
the code**.

```{admonition} Verification vs. validation
* **Verification** --- the code is meeting the requirements you set (is this code correct?)
* **Validation** --- the requirements you set made sense in the first place (is this the correct code?)

We'll be focusing almost exclusively on verification, though validation is also
important even in science/engineering for code that you want others to use and
rely on.
```

## Intro to pytest

Python used to have three major choices for tests; but now [pytest][] is used
almost exclusively. Testing is never an install requirement, so there's no harm
in using pytest. The goals of writing good tests are:

- Simplicity: the easier / nicer your tests are to write, the more you will
  write.
- Coverage: using as many inputs as possible increases the chances of finding
  something that breaks.
- Performance: the faster the tests, the more situations you can run your tests
  in CI.
- Reporting: when things break, you should get good information about what
  broke.

```{admonition} What about other choices?
The alternative library, `nose`, has been abandoned in favor of `pytest`,
which can run nose-style tests. The standard library has a test suite as well,
but it's extremely verbose and complex; and since "developers" run tests, your
test requirements don't affect users. And `pytest` can run stdlib style
testing too. So just use `pytest`. All major packages use it too, including
`NumPy`. Most other choices, like [Hypothesis][], are related to `pytest` and
just extend it. One new take is [ward](https://github.com/darrenburns/ward),
but the same basic ideas and structure still follow there, just with some
lightly changed syntax.
```

```{admonition} What about other languages?
While the details are fairly specific to Python + pytest, the concepts are
general. You can look for similar tools in other languages. Catch2, doctest,
GoogleTest, and Boost::Test for C++, for example, are all somewhat similar,
but adapted for C++ and its lack of reflection.[^1]
```

<!-- prettier-ignore-start -->
[^1]: Reflection is the ability of a programming language to inspect and process
      itself. "Please give me every function that starts with `test_`" is an
      example of a question you can ask in a language that supports reflection.
<!-- prettier-ignore-end -->

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
inputs. But there are a few problems with this, especially related to scaling
out:

- The test does not report that it passed, it's silent.
- If the test fails, you get very little helpful output, just the line which
  failed. You can't see what `f(x)` actually returned.
- You have to add each test manually to be run (duplication).
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

We can by using pytest. While pytest _can_ run unittest code, it has it's own
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

# Test Driven Development (TDD)

# Parametrizing

# Fixtures

[hypothesis]: https://hypothesis.readthedocs.io
[pytest]: https://docs.pytest.org
[pytest-mock]: https://pypi.org/project/pytest-mock/
[unittest.mock]: https://docs.python.org/3/library/unittest.mock.html
