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

Tests actually _save_ time --- You are probably already writing tests when you
write your code, you are just likely deleting them. If you record them instead,
they will continue to be useful, and will cut hours of debugging and problem
solving. If you are manually running a few known inputs, recording those in a
framework that runs automatically can be a huge time saver.

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

### Frequency of testing

How often do you run tests? Unit tests are generally run every commit (more on
that later). Integration tests might be less frequent. System tests will be much
less frequent.

The faster your tests run, the more often you can run them.

### What do you test?

Here's a non-exhaustive list of some types of testing:

- **Functional testing**: Does this code unit do what it's supposed to? You give
  some inputs, you get some outputs e.g. numerical results, create an object of
  a specific type, etc. You can hard code input/output, or use the next item in
  this list...
- **Property based testing** uses random inputs and verifies properties of the
  output. The Python tool for this is
  [Hypothosis](https://hypothesis.readthedocs.io/en/latest/), which works with
  pytest. This also may be called "fuzzing".
- **Smoke testing**: Making sure the code won't "catch fire". Checking an
  end-to-end ground truth.
- **Performance testing**: Testing to see if code gets slower/faster. Can be
  tricky on publicly available resources. Good tools can test previous
  _revisions_ (using version control) and produce a trend on a single machine.
- **Confirmation testing**: Did your bugfix work?
- **Regression testing**: Make sure refactoring/bug-fix/new feature doesn't
  cause code that used to work to break.
- **Compliance testing**: Does this comply to regulatory standards, etc? Can be
  important for human/animal subjects, etc.

### How do you test?

- Static "testing" (**static checking** is the more common term) will be covered
  later. With this, you do not need to run the code. Dynamic testing (often just
  called **testing**) runs your code.

- **Black box**: You can't "see inside" the unit you are testing, and have to
  just test input/output.
- **White box** (really a bright box or clear box, IMO): You can "see inside",
  and mock components.

### When do you write tests?

We won't discuss details of development methodologies, but we should probably at
least mention them once.

- **Waterfall**: Linear development: Requirements -> Design -> Implementation ->
  Verification -> Maintenance.
- **AGILE**: Iterative an incremental development, based on feedback.

More interesting for us is **Test Driven Development** (TDD), which we'll cover
in a later section. This tends to be more common / easier with AGILE
development, since you are writing smaller portions at a time.

#### Test Driven Development (TDD)

Test driven development flips the tables on test vs. code; instead of writing
the code then testing it, you write the tests and then make them pass by writing
the code. It may seem unnatural at first, but is has some significant benefits:

- Forces you to think about and design the _interface_ first. How should this be
  used? It's easier to answer that question when making a change doesn't require
  rewriting _anything_ (since no code has been written, only the _usage_ of the
  interface itself, in a test).
- Encourages thinking about edge and corner cases _before_ you implement the
  code. If you do it after, knowing the implementation, you might be biased to
  thinking only of working examples based on your implementation.
- Helps you not add unnecessary features too early. You should write code to
  make the test pass, then stop - you write more tests before you write more
  code.
- Encourages high or complete coverage of your code by tests.

The most important reason: If you write code first, you are much less likely to
go back and test it. Writing tests is important, so treat it as such!

#### Other styles

You don't have to lead with tests. You can write a new feature, then test it.
Most of the time, you'll develop one thing at a time (feature, refactor,
dependency upgrade, etc), and then submit it as a Pull Request (even to
yourself), and the only requirement is any new code also has new tests.

I'd recommend trying TDD, then deciding on a style that's right for you - it
might even be problem specific (in fact, it almost surely is).

### How much do you test?

As close to 100% coverage as you reasonably can. If you are measuring coverage
using a tool, there's a huge benefit to getting 100% coverage, even if you have
to explicitly mark a few tiny sections to be ignored by coverage (due to special
platform or hardware requirements, perhaps).

You can do even better. Just because a line of code is tested once, it doesn't
mean every possible path through it is tested. Just because units are tested,
that doesn't mean the whole integrated system works. So you can still add tests.

There are some things that are hard to test. Code that needs hardware (like data
acquisition), graphical user interfaces, remote networking, plotting, slow
computations, or large volumes of data can be challenging. We'll be discussing
some ways to test these sorts of things later!

How important is it that your code work? How many users do you have? Will
someone die if there's a bug (a real worry in some areas like medical /
automotive fields!)

We'll also cover static checking, which is not as powerful, but generally
doesn't need explicit tests and so can more easily cover every line of code.
It's not a replacement, but it can help.

### Testing strategies

- Every new feature needs test(s)
- If you (or someone else) finds a bug, write a test. Before the fix if you
  can - that way you can verify the bug is reproducible, the fix does in fact
  fix it, and that it stays fixed in the future.
- If you find a bug in someone else's code, it's nice to write a failing (unit)
  test and include it in the report.
- Run tests automatically, in CI, on all PRs (we'll show how to do this later).
- You have to maintain test too! You don't do as much with them over time, but
  don't treat them like throw-away code. Keep them clean(ish) if you can.

## Testing frameworks

Let's be honest: no one likes writing tests (at least I know I don't). And the
last thing I want to do is write a lot of boiler-plate code that makes the tests
runnable & easy to use. Specifically, I want these features:

- Easy to run all tests.
- Good readable output if tests fail
- Some output if they pass
- Various common needs (setup/teardown, mocking, parameterization, etc.)

A testing framework adds these things without requiring extensive per-test
boilerplate. Early testing frameworks were often "x-unit" style, which came from
a generalization of J-unit, a framework for Java. It solved the above
requirements, but was very verbose (okay, so is Java). Modern testing frameworks
utilize the languages they are in to provide a lower boilerplate, cleaner
experience.

Some C++ testing frameworks:

- **Catch2**: A powerful and modern C++ framework. Highly recommended. Use
  version 2 if you need \< C++14. (Yes, Catch2 is on version 3. Go figure.)
- **DocTest**: A rewrite of Catch2 focused on speed and simplicity. But not as
  tested as Catch2, and Catch2 has been doing a great job at improving speed.
- **GoogleTest**: If you don't mind Google's "live at head" philosophy (rare/non
  existent actual releases) and rather strict compiler policy (nothing older
  than 5 years), this is also a good option, slightly less modern of a design.
  The (powerful) mocking library (GoogleMock) is separate and contains some
  things you (at least I) often need that are testing and not related to
  mocking, which is mildly annoying.
- **Boost.Test**: Good if you are using Boost heavily and don't mind the less
  beginner friendly syntax.

Note that none of these are true x-unit style, because C++ doesn't have
reflection, making C++ one of the few languages without x-unit style test
frameworks.

Some Python testing frameworks:

- **pytest**: The gold standard. You can stop reading now. Has a thriving plugin
  family, too.
- **unittest**: Built in. Follows the x-unit style, so is very verbose. But
  pytest can run it.
- **nose**: Not an option anymore, died in 2016. But pytest can run it.
- **doctest**: Also built in, but tests docstrings instead of normal tests.
  Tricky to use for non-trivial anything. Not related to the C++ library of the
  same name.
- **xdoctest**: a better version of the standard library module that might even
  be usable in some cases.
- **Hypothosis**: Property based testing (is an add-on to pytest)
- [**ward**](https://github.com/darrenburns/ward): A rather new library that
  tries to rethink pytest to be even more modern. Interesting, at least.

In short: Use pytest, unless you are writing a Python standard library module.
Which I assume you are not.

Ruby has a couple of popular frameworks. Matlab has integrated frameworks
(everything is integrated in Matlab, though). Look around and see what others
are using in your favorite language.
