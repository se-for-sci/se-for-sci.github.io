Forgot to start the receding today. As a reminder, Princeton doesn't want
students to connect to classes or watch recordings, but I'll try to provide
recordings all-at-once at the end of class. A few (4-5) students from other
universities through a special program are connecting via Zoom, as well.

- Homework 1 being posted tomorrow. Will be in notebook format, with
  `%%writefile` used to write multiple files (set up for you).
- Survey results:
  - Python most commonly known language, Matlab a strong second
  - C++ language most interested in learning, with Python strong second
  - Testing is new to 80%+ of the class or so.
- Frequency of testing: run often, every "commit" if possible
- What do you test:
  - Functional testing
  - Property based testing
  - Smoke testing
  - Performance testing
  - Confirmation testing
  - Regression testing
  - Compliance testing
- Static "checks" vs. Dynamic testing
- Black (hidden) box vs. white (visible) box testing
- Waterfall vs. AGILE - two common methodologies
- Test Driven Development, Example 1: vector_example (code in content/week2
  folder)
  - `tests/test\_simple.py` -> add test
  - `vector/__init__.py` -> add file, add class, add constructor, fix
    constructor, add `__add__()`, add `mag()`
  - Starting with tests gives you a different perspective
  - Try TDD, find balance that works for you - but test and code should be
    written close together, harder to add long after the fact
- How much do you test?
  - Try for 100%
  - Is 100% bug free? No:
    - Bad tests
    - Branches
    - Combinatorics
    - Invalid inputs
    - Different system/deps/OS
  - But it's better than low or no coverage! Just not a magic bullet (nothing
    is, though)
- Strategies - add a test when:
  - If you add a new feature
  - If you find a bug
    - Test should fail first, to verify you can see the bug, then fix it.
  - If something is untested, to slowly raise coverage
- Refactoring
  - Change code or tests, but be very careful when changing both!
    - Unless you are intentionally breaking users

pytest example w/fixtures: content/week2/vector_example

- Copied in code to run, and json file for testing
- We used vscode for this example, with GitHub CoPilot providing AI assisted
  code completion to help write tests (it's really good for that, except when
  it's not)
- Wrote a test reading file
- Wrote a test writing then reading a file, using a fixture (`tmp_path`)
- Wrote a test parametrizing over "size"
- Wrote a fixture parametrizing "simulation"
- Customized the ids of the "simulation" to say "simulation/no-simulation"

Pytest section

- Fixtures
  - Modular
  - Scalar
  - Composable
  - Optionally Automatic
  - Teardown
  - Parametrization
- capsys example
- Writing a simple fixture
- Teardown (cleanup) code in a fixture using yield
- Monkeypatching
- Parametrization (without fixtures then with fixtures)
- Skipping tests with skipif or using xfail

Next time we will look at debuggers & running pytest with debuggers, then we'll
start object oriented design.
