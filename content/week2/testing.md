# Intro to testing

Tests are crucial to writing reliable software. A good test suite allows you to:

- Immediately know if a new platform or software version works,
- Refactor and cleanup your code with confidence,
- Evaluate the effect of additions and changes.

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

> ### What about other choices?
>
> The alternative library, `nose`, has been abandoned in favor of `pytest`,
> which can run nose-style tests. The standard library has a test suite as well,
> but it's extremely verbose and complex; and since "developers" run tests, your
> test requirements don't affect users. And `pytest` can run stdlib style
> testing too. So just use `pytest`. All major packages use it too, including
> `NumPy`. Most other choices, like [Hypothesis][], are related to `pytest` and
> just extend it.

# Test Driven Development

# Parametrizing

# Fixtures

[hypothesis]: https://hypothesis.readthedocs.io
[pytest]: https://docs.pytest.org
[pytest-mock]: https://pypi.org/project/pytest-mock/
[unittest.mock]: https://docs.python.org/3/library/unittest.mock.html
