# Intro to testing

## Why Test?

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
* **Verification** --- the code is meeting the requirements you set (is this
  code correct?)
* **Validation** --- the requirements you set made sense in the first place (is
  this the correct code?)

We'll be focusing almost exclusively on verification, though validation is also
important even in science/engineering for code that you want others to use and
rely on.
```

## Overarching principles to keep in mind

The adversarial view --- don't be wishful. Try to find defects. Document for the
user things that could cause problems but that you are not guarding against
(a.k.a. make explicit caveat emptors). We'll discuss documentation later.

Write code that's amenable to atomic testing --- modularity, DRY vs. WET, etc
all help (as we'll see). The better your design and workflow play with Git, then
generally the more amenable your code will be to systematic testing.

An ounce of prevention is worth a pound of cure --- test early, test often, and
review code.

You can't test everything --- code will have bugs or use-cases it didn't
anticipate. Your goals are to minimize the incidence of the unforeseen and to
have a framework that lets you incorporate previously unanticipated scenarios
into your future testing easily.

Tests are themselves code --- it should adhere to good development principles
(modularity, DRY not WET, etc), and it should grow alongside your actual code
(i.e. writing more and more tests is part of the code authoring process).

Test code often outnumbers real code --- or at least it should. SQLite famously
has 608 times more test code than source code.

Testing well isn't trivial --- tools can help, but it's a skill and an art.

Code that passes all tests may still suck --- verification vs validation;
Quality Assurance (QA) is also important.

## Types of tests

There are several levels / types of tests:

- **Unit tests**: These verify small, atomic units of code work. If you write
  highly modular code, you should be able to write lots of unit tests.
- **Integration tests**: These verify a larger chunk of many units to make sure
  all the parts work together. The main drawbacks over unit tests are that they
  are usually slower and often produce much poorer information if the test
  fails. They may catch problems a unit test can't, though, and look more like
  normal usage.
- For a large application, a distinction might be made for **System tests**,
  with integration tests being a mid-point between unit and system.
