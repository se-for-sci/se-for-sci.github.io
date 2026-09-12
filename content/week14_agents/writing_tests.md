# Writing tests

Writing tests is considered by many to be one of the most "boring" parts of
software development. However, it is also one of the most important. Tests are
the safety net that allows developers to make changes with confidence, ensuring
that new code does not break existing functionality, and that the code does what
it's supposed to do.

Agentic AI has made it even more important to have a robust test suite, since
the agent gets immediate feedback on whether its changes broke something or are
not implemented correctly. This allows for an iterative development process
where the agent writes code, runs the test suite, and repeats until everything
works as intended (make sure the testing commands are mentioned in the
[AGENTS.md](./agents_md.md)). It also gives you peace of mind that the agent's
work is correct, especially if you are not painstakingly reviewing every line of
code it writes.

## Test-driven development

Test-driven development (TDD) is a software development approach where tests are
written before the code. This approach is valuable with agentic AI, since it
allows the agent to clearly understand the requirements of the code that is
needed. A test is a more stringent way to specify how you want the code to
behave than simply describing it in plain text. By manually writing a few simple
tests, you explicitly enforce the interface and the behavior of the code. The
agent will then be constrained to make these tests pass, and will be able to
iterate on its implementation until it does.

However, we already mentioned that writing tests can be one of the most boring
parts, and this approach ends up focusing most of our work exactly on this.
Thankfully, agentic AI can help us here as well. After writing only a few simple
tests, we can ask the agent to write more tests for us (see
[Repetitive work](./repetitive_work.md)) or to make the tests we wrote more
general or robust (for example with a property-based testing tool like
[Hypothesis](https://hypothesis.readthedocs.io/en/latest/)).

## Coverage-driven test writing

As we discussed, a good test suite is useful for agentic AI. Such a suite covers
most of the codebase, ideally all of it. Getting to 100% coverage is a tedious
task, especially if you didn't write tests as the code was being developed.
Agentic AI can help with this as well, but you need to be careful. After all,
100% coverage does not automatically mean that the test suite is good!

Coverage-driven test writing is the process in which you use a coverage
reporting tool to identify which parts of the codebase are not covered by the
tests. An agent can then use this information to write new tests, or adapt
existing ones, so that all of the missing parts are also covered. Generally,
this is done as an iterative process, where the agent will write tests, produce
a coverage report again, and repeat until the coverage is satisfactory.

This process can occur in two different contexts:

- **When you have an existing codebase with incomplete test coverage.**

  This case can be a little tricky, depending on the size of the codebase and
  the existing test coverage. The agent may have to write a lot of tests, and
  may not have a good reference for how to properly structure the tests or make
  sure they test the right things. For an untested part of the code, an agent
  may derive its expectations from the existing implementation, so it can
  accidentally end up locking in a bug by adding a test that asserts the buggy
  behavior instead of the correct one. Additionally, it will be difficult to
  review the tests that the agent wrote to make sure that they are correct and
  meaningful. You will likely need a good model in this case, so that it can
  better understand the codebase and write good tests.

- **When you are in the process of developing a new feature.**

  This is the ideal case. Having a solid testing suite, and writing new tests as
  each feature is added will make things much easier for you and the agent. The
  agent will have a good reference for how to write tests, how to structure
  them, what kind of things they should check, and how to have them be
  meaningful. Additionally, it will be easier to review the new tests, since
  they will be constrained to the context of the new feature being developed. A
  simple prompt like `"Add tests for the change I just made"` usually works well
  in this case, even with small models.

```{note} Model choice matters when writing tests
Writing a good test requires a model that understands the codebase and the requirements. Small models may be able to write simple tests, but often they will not be able to write a meaningful test, in the sense that it checks for the right things. Larger models are also much better at identifying edge cases and weak points, and at writing tests to check them.
```

## Improving the test suite

These are some ways to improve the test suite of a codebase.

- **Test the examples in the documentation.**

  This is a great way to ensure that the information you are conveying to your
  users is correct and up-to-date. But it is also a good way for an agent to
  make sure that new changes won't break the contract that you have made with
  your users.

- **Add issue reproducers as tests.**

  Every time a bug is found, either by you, a user of your package, or the
  agent, use the code that reproduces the bug as one of your regression tests.
  Confirm that the test fails before the fix, but passes afterwards.

- **Keep the test suite lean, but robust.**

  If the test suite is too slow, it will slow down agentic development. You can
  ask the agent to run only a relevant portion of the tests (smart models might
  do this for you). Also, if there are flaky tests they can confuse the agent
  into thinking it broke something. If the flakiness comes from within your
  code, then you should fix it. If the flakiness is external, then you should
  avoid it and find an alternative.

- **Remove overlap in the test suite.**

  An agent can help you look for duplicate tests, or for simplifications that
  don't sacrifice robustness. It can do mechanical adaptations to make things
  faster, like swapping an expensive C++ test for a faster-to-compile C one,
  mocking an expensive external dependency, or reducing the size of example
  data.

- **Hold tests up to the same standards as the rest of your code.**

  Having the test suite be composed of high-quality code will help an agent
  continue to write good tests and respect the existing structure. Since an
  agent makes it much easier to have polished testing code, you should aim to do
  so. For example, in Python it can make sense to add type annotations to tests,
  even though it is not common, because an agent can do it easily and it will
  help future readers of the tests.

- **Look for edge cases, not more tests for the sake of more tests.**

  There's no reason to test something multiple times if there's nothing
  different between the tests. You can use agents to look for coverage of corner
  cases (like behavior around 0, None handling, etc). It's easy to forget
  something like adding a negative value in your tests, but agents can look for
  these sorts of omissions.

- **Adopt new types of tests.**

  An agent lowers the cost of trying a kind of test you do not use yet, like the
  property-based testing mentioned above, or a benchmarking suite.

## Common pitfalls

- **A passing test does not necessarily mean the code is correct.**

  The test might be too narrow or it may not be testing the right thing at all.
  This is something to be aware of with TDD, as the agent will iterate until a
  test passes, but it may have implemented the wrong thing. Maybe it only works
  for the particular case in the test, but not more general ones. Or maybe the
  test is checking something unrelated, and the code the agent wrote just
  happened to make it work. Good tests should check the right things, and be as
  general as possible.

- **100% test coverage doesn't mean everything is tested properly.**

  Just because some line of code is executed during some test, it doesn't mean
  that the line is correct. Its result may never be checked, or may not affect
  the things being checked in the test. This is the difference between a smoke
  test (i.e. checking if the code runs) and a proper test (i.e. checking if the
  code does what it is supposed to do). A test is meaningful if it checks that
  all of the outputs the code produces are correct, and that the code behaves
  correctly in all cases.

- **An agent may edit an existing test to make it pass.**

  An agent may weaken a test by tweaking an assert, wrapping something in a
  `try/except`, or by adding a marker to skip it. It's good to tell the agent to
  ask before it modifies tests, unless there is an intentional behavior or API
  change. You can also ask it to revert test changes after the fact, or split
  commits.

## Exercise

Improve the test coverage of `agentic-ai-example` and inspect which generated
tests are worth keeping.
