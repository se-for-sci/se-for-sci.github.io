# Vector example

This example is intended for Test Driven Development. You should start by
implementing some tests, then adding functionality to make the tests pass.

## Running instructions

Since we haven't covered packaging, we'll just use `python -m pytest` to run the
tests from this directory. You cannot use `pytest` directly, as that will not
add the current directory to the import path. Normally that's good, and you
normally should be testing the installed version of the library, but this
requires less setup and explanation for now. If you do know enough packaging to
install this as a package, a bare-bones `pyproject.toml` has been provided to
make that easier.
