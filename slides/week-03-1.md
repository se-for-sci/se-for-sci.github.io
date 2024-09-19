---
marp: true
theme: gaia
class: lead
style: |
  :root {
    font-size: 30px;
  }
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Testing

---

## Why test?

- Know if new platform/versions work
- Refactor / cleanup
- Evaluate changes

Also:

- Document bugs
- Requirements and expectations _explicit_
- Confidence in code

**Tests serve as documentation about your expectations**.

---

## Verification vs. validation

- **Verification** The code is meeting the requirements you set (is this code correct?)
- **Validation** The requirements you set made sense in the first place (is this the correct code?)

We will focus on verification, but both are important.

---

## Principles

- Try to find defects
- Modular, DRY code is best for testing
- Test early, test often, review
- Minimize incidence of the unforeseen
- Tests are code too
- Tests can outnumber code (SQLite: 608x)
- Tools help, still can be a skill/art

---

## Doesn't it take time?

- You are already writing tests when developing (usually)
- Debugging broken code is slow
- Bugs in production is slow

---

## Size of tests

- **Unit tests**: Small, atomic pieces of code
- **Integration tests**: Large chunks work together (like the whole app)

You may see **system tests**, one more step up for large applications.

---

## Types of tests

Here's a non-exhaustive list of some types of testing:

- **Functional testing**: Does this code unit do what it's supposed to?
- **Property based testing** uses random inputs and verifies properties. See [Hypothosis](https://hypothesis.readthedocs.io/en/latest/). AKA "fuzzing"
- **Smoke testing**: Checking an end-to-end ground truth.
- **Performance testing**: Test previous revisions perf.
- **Confirmation testing**: Did your bugfix work?
- **Regression testing**: Make sure something continues to work.
- **Compliance testing**: Does this comply to regulatory standards?

---

## How do you test?

Static "testing" (**static checking**) will be covered later. Dynamic testing (often just called **testing**) runs your code.

- **Black box**: You can't "see inside" the unit you are testing, and have to just test input/output.
- **White box** (really a bright box or clear box, IMO): You can "see inside", and mock components.

---

## When do you write tests?

- **Waterfall**: Linear development: Requirements -> Design -> Implementation -> Verification -> Maintenance.
- **AGILE**: Iterative an incremental development, based on feedback.

---

## Test Driven Development (TDD)

Write tests _before_ writing the code it tests.

- Good for thinking about the _interface_
- Encourages thinking about edge/corner cases _before_ implementation
- Helps avoid adding unnecessary features too soon
- Good for code _coverage_

---

## Other styles

I'd recommend trying TDD, then deciding on a style that's right for you - it might even be problem specific (in fact, it almost surely is).

---

## How much do you test?

- More is better
- 100% coverage is much better than even missing it by a little
- Just because a line is covered, can still do better (branching, integration, etc)
- Some things are hard (plots, GUIs, networking, big data), some tricks though!
- How important is your code?

---

## Testing strategies

- Every new feature needs test(s)
- Every bug needs a test - show it fails, show fix works
- Write a test in the report if you find a bug in other's code
- Run tests automatically on all PRs (later)
- Try to write clean tests - they are maintained too!

---

## Testing frameworks

- Easy to run all tests
- Good readable output if tests fail
- Some output if they pass
- Various common needs (setup/teardown, mocking, parameterization, etc.)

Many early frameworks were "x-unit" style. High boilerplate.

---

## C++ frameworks

- **Catch2**: A powerful and modern C++ framework. Recommended.
- **DocTest**: A rewrite of Catch2 focused on speed and simplicity.
- **GoogleTest**: Google's. Normal drawbacks (like only 5 year compiler support).
- **Boost.Test**: Good if you are using Boost, less beginner friendly syntax.

Note that none of these are true x-unit style, because C++ doesn't have reflection, making C++ one of the few languages without x-unit style test frameworks.

---

## Python frameworks

- **pytest**: The gold standard.
- **unittest**: Built in. Follows the x-unit style. Pytest can run it.
- **nose**: Died in 2016. But pytest can run it.
- **doctest**: Also built in, but tests docstrings instead of normal tests.
- **xdoctest**: a better version of the standard library module that might even be usable in some cases.
- **Hypothosis**: Property based testing (is an add-on to pytest)
- [**ward**](https://github.com/darrenburns/ward): Abandoned but interesting ideas.
