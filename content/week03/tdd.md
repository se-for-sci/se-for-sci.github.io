# Test Driven Development (TDD)

## When to write tests?

Fundamentally, unit tests provide documentation about what you expect functions
to do and a mechanism to automatically check the tests are passing. _When_ you
write tests affects how you write your tests and source code.

When source code is written first, you focus on the implementation. When, and
if, you write unit tests, you trace your source code to ensure every branch is
exercised. Your ability to determine corner cases and possible errors is
anchored to the implementation you have. Consider this code to find the largest
element in a list:

```python
def my_max(input_list):
    maxval = input_list[0]
    for val in input_list:
        if val > maxval:
            maxval = val
    return maxval
```

Some obvious corner cases to test include an empty list (which would raise an
unhandled exception here). What may not be apparent is what to do when a
non-list object is passed as an argument. Such errors from corner cases may not
come up until they are encountered as bugs during runtime.

Writing tests first allows you to focus instead on the interface you expect a
function to support. Consider the following `pytest` functions:

```python
import pytest


def test_my_max():
    assert my_max([1, 2, 3]) == 3
    assert my_max([3, 2, 1]) == 3
    assert my_max([3]) == 3


def test_my_max_empty():
    assert my_max([]) is None


def test_my_max_non_list():
    with pytest.raises(ValueError) as e:
        my_max(1)
    assert str(e.value) == "Non-list argument passed to my_max"
```

Now you know exactly what you expect to happen when an empty or non-list object
is passed to `my_max`. These tests fail, but now you know what behavior the
function should have and when to _stop_ coding.

## TDD

TDD is a fundamental apsect of agile software development where no code is
written without first having a test covering the feature. Development proceeds
through a cycle of red, green, refactor.

### Red

The red stage represents writing a failing unit test for a feature that is not
currently implemented. A red color is commonly used by unit testing frameworks
when a test suite is failing. This is the test that drives development.

### Green

Next, the developer adds just enough code to make the failing test pass, with
green indicating all tests passing. Often, the hardest part of the green stage
is to not add any more code than necessary to pass failing tests.

### Refactor

Before moving to the next feature/test, the developer makes a concerted effort
to try and improve the codebase. Separating refactoring as a step of TDD helps
compartmentalize and emphasize the importance of making code DRY and readable.
When in the red or green stage, you can copy/paste, use one letter variables,
and make giant methods to focus solely on adding a new feature. Since the
feature is tested, you are free to change the code in the refactor stage to
focus on readability and clean code. Refactoring also applies to test code, if
setup code is repeated in several methods, promote it to a fixture to eliminate
duplication. Don't forget to document test functions to specify what the test is
trying to uncover.

### Fully tested codebases by induction

Almost by definition, if you don't add a feature until a unit test is in place,
the code you add will be fully tested. If all developers utilize TDD through the
entirety of a project, the project will be fully tested. This is a powerful
guarantee when refactoring that any changes, anywhere, will not break the
system.

## Example TDD workflow

Let's demonstrate TDD with `my_max`, with the tests in the same file as the
method for simplicity. Start with the red stage:

```python
# red
def test_my_max():
    my_max()
```

Which will fail, because `my_max` is not defined. Why is this an important step
in the red stage? When starting TDD, it can seem silly to write tests like these
which will obviously fail and are fixed with simple, obvious additions. But
think about what it would mean if the above test _passed_. Since the intention
was to write a failing test, having the test pass means that you have failed to
test what you intended! In this case, it would indicate a name conflict,
`my_max` already exists and another name should be used. It's also possible the
test file is not located in the correct directory to be run.

Even failing this test provides important information. You have pytest
installed, it is finding your file, and if it is failing at the expected line,
you know any dependencies are correctly installed.

Back to the example, to move to green:

```python
# green
def my_max():
    pass


def test_my_max():
    my_max()
```

And we don't have to refactor since we don't have much code. Now for a return
value and argument

```python
# red
def my_max():
    pass


def test_my_max():
    assert my_max([3]) == 3
```

To pass this test, we can just accept an argument and return 3.

```python
# green
def my_max(input):
    return 3


def test_my_max():
    assert my_max([3]) == 3
```

Let's test some more inputs

```python
# green?
def my_max(input):
    return 3


def test_my_max():
    assert my_max([3]) == 3
    assert my_max([1, 2, 3]) == 3
    assert my_max([3, 2, 1]) == 3
```

Note we are not in the red stage because our new tests are still passing. The
problem is not the code, but the tests not exercising the behavior we want.
Let's try again:

```python
# red
def my_max(input):
    return 3


def test_my_max():
    assert my_max([3]) == 3
    assert my_max([1, 2, 3]) == 3
    assert my_max([3, 2, 1]) == 3
    assert my_max([3, 5]) == 5
```

It is almost always best to leave passing assert statements, even if they seem
pointless. They are usually cheap to run and if they start to fail it can help
uncover bugs. In this case, notice how the location of the max value changes.
Now we need to implement the function:

```python
# green
def my_max(input):
    maxval = input[0]
    for val in input:
        if val > maxval:
            maxval = val
    return maxval


def test_my_max():
    assert my_max([3]) == 3
    assert my_max([1, 2, 3]) == 3
    assert my_max([3, 2, 1]) == 3
    assert my_max([3, 5]) == 5
```

As a refactor, we can change the argument name to something descriptive that
won't shadow the built-in `input` function of python. `maxval` should be
`max_val` and we can add types hints, restricting our code to ints for now:

```python
# refactor
def my_max(input_list: list[int]) -> int:
    max_val = input_list[0]
    for val in input_list:
        if val > max_val:
            max_val = val
    return max_val


def test_my_max():
    assert my_max([3]) == 3
    assert my_max([1, 2, 3]) == 3
    assert my_max([3, 2, 1]) == 3
    assert my_max([3, 5]) == 5
```

Finally, let's add a test for empty and non-list objects. In ideal TDD, this
would be two cycles.

```python
# red
import pytest


def my_max(input_list: list[int]) -> int:
    max_val = input_list[0]
    for val in input_list:
        if val > max_val:
            max_val = val
    return max_val


def test_my_max():
    assert my_max([3]) == 3
    assert my_max([1, 2, 3]) == 3
    assert my_max([3, 2, 1]) == 3
    assert my_max([3, 5]) == 5


def test_my_max_empty():
    assert my_max([]) is None


def test_my_max_non_list():
    with pytest.raises(ValueError) as e:
        my_max(1)
    assert str(e.value) == "Non-list argument passed to my_max"
```

And to pass

```python
# green
import pytest


def my_max(input_list: list[int]) -> int:
    if not isinstance(input_list, list):
        raise ValueError("Non-list argument passed to my_max")

    if not input_list:
        return None

    max_val = input_list[0]
    for val in input_list:
        if val > max_val:
            max_val = val
    return max_val


def test_my_max():
    assert my_max([3]) == 3
    assert my_max([1, 2, 3]) == 3
    assert my_max([3, 2, 1]) == 3
    assert my_max([3, 5]) == 5


def test_my_max_empty():
    assert my_max([]) is None


def test_my_max_non_list():
    with pytest.raises(ValueError) as e:
        my_max(1)
    assert str(e.value) == "Non-list argument passed to my_max"
```

Notice that each stage of TDD is short, usually just a few minutes. It doesn't
take much time to write a failing test. Since you stop after the first failure,
there aren't many features to add before the test starts passing. Refactoring
can take longer, up to several days, but you will want to run tests after each
small change to ensure bugs and typos don't "pile up".

## TDD in practice

For TDD to work, tests must be run frequently, ideally after each write of any
source or test file. Some IDEs can do this for you and on the command line
tools, like [entr](https://eradman.com/entrproject/), can help. As a
consequence, tests and building should be fast, less than about 10 seconds.
Tests that run slowly disrupt the flow of the TDD cycle and tempt developers to
skip running tests. Slow tests or building also can indicate a problem. Try to
decouple dependencies to accelerate building in compiled languages. For tests,
options include injecting mocks to skip creating expensive objects, connecting
to databases, or file IO. You can `mark` tests as slow with pytest and only run
tests that are not slow during active development, saving the full test suite
for just before committing to VCS.

Ideally TDD follows the red, green, refactor cycle in order and without
exception. In practice, while adding a feature to source code, you may identify
a corner case that should be tested. You could leave a comment to test it, or
add the feature now and add the test next. Beware the dangers of writing tests
that pass the first time. Depending on your previous training, it may be
difficult to decide on an interface without writing some of the implementation
first. This is all fine, the important part is to have full test coverage as
often as possible and make an effort to refactor code frequently and without
worry that code is breaking.
