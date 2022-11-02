Homework due today

Projects approved! Projects should have:

- Tests
- Classes (at least 2, if you have to force them, check with us, you can use a
  different design paradigm if better for your problem)
- Several pre-commit and/or some other runner (nox, tox, etc) based checks
- CI
- Docs (depending on how much we cover Thursday)

Pre-commit checks (a few more added on to last time)

- A C++ check listed on scikit-hep.org/developer (and many checks are language
  agnostic, full list on pre-commit.com)
- PyUpgrade: upgrades old syntax based on your minimum supported version
- Extra examples of things not as ideal for pre-commit checks
  - Refurb (too many checks that might need to be ignored, rather new)
  - Pylint: noisy but you can configure, but works best with the package
    "installed" - pre-commit checks usually shouldn't require you to install
    your package
- Nox/Tox best for slower, dynamic testing, pre-commit for many small fast
  checks

Continuous Integration

- What is it for?
  - Running tests (consistent / multiple environments)
  - Building documentation
  - Building static websites
  - Building packages and releasing binaries (called artifacts)
- Basics
  - Adding the simplest workflow doing tests
  - Using a matrix
  - Using variables
- Dependabot: a service for keeping actions (or other things) up to date via PRs
  (owned by GitHub these days) .
