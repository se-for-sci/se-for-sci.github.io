- Homework 1 posted, notes on it, collaborations rules
- Office hours will be in Fine 206, after class. AI office hours on Thursday,
  same room, 4:30-6
- I'm not allowed to give out the Zoom link to Princeton students. But I can
  provide recordings on request (even if I said no before, the answer is now
  yes, please ask again)
- White box vs. black box testing in HW - we are doing black box testing, avoid
  anything different between List and Matrix classes. We'll formalize this
  (twice) in later classes
- Pytest
  - Importorskip
  - Class based organization
  - Configuring pytest - `pyproject.toml`'s `tool.pytest.ini_options` section
    - `addopts`
    - strictness settings
    - `testpaths`
  - `conf.py` - home for fixtures and more, per test directory
  - Plugins can add fixtures and more to pytest, highlighted a few
- Running pytest
  - `pytest` vs. `python -m pytest` (local directory included in search path for
    `python -m`, and we haven't made it to packaging yet)
  - Can request a dir, a file, or even a specific test
  - `-k regexp`
  - `-m markers`
  - `-l/--showlocals`
- Logging
  - Print with a global level switch
  - Tell a story with `"INFO"`
  - Provide debugging details with `"DEBUG"`
  - Pytest can include logging on failures (`log_cli_level="INFO"`)
- Debugging
  - Running with python -m pdb
  - PDB minilanguage (`hpnswudcq` are useful letters) - similar to compiled
    debuggers (gdb, lldb)
  - Adding breakpoint() triggers the current debugger (pdb, or
    pycharm/ipdb/other)
  - Also integrated with JupyterLab visual debugger in modern IPython versions
  - Playing with code in a debugger can help you understand how the call stack
    works
  - You can jump into the debugger on pytest failures with `--pdb`
  - You can start with the debugger using `--trace` (often combine with `--lf`
    or manually specifying the interesting test)

Intro to classes

- Objects
  - Are a bag of "things" (functions and data)
  - Only useful if consistent
    - Using a "template function" to "construct" objects ensures consistency
  - Example of `home_dir` with `string_location` & `exists()`
- Classes
  - Shared functions and constructor for instances of objects
  - Real world example: Bluey is an instance of a dog. Dog is the class, Bluey
    is an object of that class.
  - Template function: `__init__` constructor in Python
  - Objects have a `__class__` - Python looks in the object first, then in the
    class
  - And it keeps going if there are parent classes
    - You can look at the `__mro__` of a class to see what the look up order is
  - Shortcut: Path.exists(`home_dir`) can be written as `home_dir.exists()` -
    Python include "self" as the first argument when calling from the instance.
    - Most languages do this, but they way they provide access to "self" varies
  - `__class__` has a `__name__` - `self.__class__.__name__` is a common
    shortcut for the current class name.
- Subclassing
  - `Animal` can `eat()`, `Dog` is an animal, so `Dog` can `eat()`.
    - You can add or override attributes, but you can't remove them, since it's
      really just a lookup chain.
  - A subclass can override by providing the same thing - the first think in the
    lookup chain (`__mro__`) is the one returned.
  - You can get at the function you are overriding with `super()`
  - Subclassing is heavily used for Exceptions, often the class body is empty!
    - Look at `KeyError.__mro__`
  - Multiple Inheritance: more of a good thing?
    - Hard to use, but a limited subset will be in the next class (mixins
      pattern)
    - Still has a linear `__mro__`, `super()` really means "one up the
      `__mro__`"
- Special methods: canonical source is the Python Data Model
  - Also some books like Dive into Python have great chapters on special methods
- Dataclasses vs. classic classes
