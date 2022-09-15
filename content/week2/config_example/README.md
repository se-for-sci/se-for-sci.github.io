# Config example

This is an example of testing setting up a little configuration reader. The goal
of the "library" is to read a JSON format configuration file like this:

```json
{
  "size": 100,
  "name": "Test",
  "simulation": true,
  "path": "data/somewhere",
  "duration": 10.0
}
```

Into a little class that has those values as members:

```python
Configuration(
    size=100,
    name="Test",
    simulation=True,
    path="data/somewhere",
    duration=10.0,
)
```

In real code, this is an ideal use case for `dataclasses` (or the third-party
library it was based on, `attrs`), and a conversion/validation library like
`cattrs`. Or you could use `pydantic`, which combines both. An example of what
it would look like is also provided - feel free to experiment with refactoring!

It still should be tested, though, and testing is the reason for the example.

## Running instructions

Since we haven't covered packaging, we'll just use `python -m pytest` to run the
tests from this directory. You cannot use `pytest` directly, as that will not
add the current directory to the import path. Normally that's good, and you
normally should be testing the installed version of the library, but this
requires less setup and explanation for now. If you do know enough packaging to
install this as a package, a bare-bones `pyproject.toml` has been provided to
make that easier.
