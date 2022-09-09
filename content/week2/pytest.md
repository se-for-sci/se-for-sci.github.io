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

## Parametrizing

## Fixtures

[hypothesis]: https://hypothesis.readthedocs.io
[pytest]: https://docs.pytest.org
[pytest-mock]: https://pypi.org/project/pytest-mock/
[unittest.mock]: https://docs.python.org/3/library/unittest.mock.html
