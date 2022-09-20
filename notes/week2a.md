Today's notes, starting with intro stuff:

- Note about using the repo link to the course material for saving links (just
  in case URLs change)
- Links to the course updated on <https://iscinumpy.dev> &
  <https://github.com/henryiii>
- More code, less text today (and probably in the future) - course website can
  be studied offline (no official book for the course)
- Added binder as another option for running the course material for now (we'll
  be setting up locally more later)
- Ping me on the course chat if I promise something and forget to do it! (or
  anything else)

Added material to Python overview:

- Decorators
  - `lru_cache`/`cache` example
  - Some in-class discussion about writing a decorator. We shouldn't have to do
    that this semester. :)
- Context manager - writing one using a decorator (we made a timer)

Final bit of cleanup best practices:

- Optimize late
- Avoid globals / minimize capture

Code cleanup example:

- Run through Black to get initial cleanup
- Avoiding importing all (`from numpy import *` -> `import numpy as np`)
- Variable naming conventions
- Cleanup titles
- Drop keywords on limits (opinionated, not required)
- Avoid capture of "start" in function
- Rename arguments to x, order, start
- Move plotting code closer together (added in class, not in notes example yet)
- Add a doctoring
- Move comments to separate lines and remove useless ones
- Factor out `np.arange`
- Use list comprehension or np.vectorize instead of plotting one dot at a time
- Fully vectorize code (optional, requires more numpy knowledge than required
  for this class)

Intro to testing (first half):

- Why test?
  - Document bugs
  - Document expectations
  - Monitor regressions
  - Assist in refactoring
  - Give confidence and warm fuzzy feelings
- Verification vs. validation
- Tests are code, too
- Test lines may outnumber code lines (by up to 608x times for SQLite)
- Let's be honest: designing is fun. Writing a lot of tests is not.
- Tests save time in the long run
- You are already writing tests if you are writing code! Let's just formalize
  them and record them.
- Scope of tests
  - Unit tests
  - Integration tests
  - System tests

Intro to pytest:

- Example tests
  - Problems?
    - Silent successes
    - Poor failure message
    - Manual additions per test
    - No control
    - Can't also run the file for other things
    - Only get the first failure
  - I added a second test function (not in class notes yet)
- Move to x-unit style (unittest)
  - Solves the problems above
  - But adds new ones:
    - Verbose, lots of boilerplate
    - Many methods to remember / lookup
    - Have to deal with OOP and self when it's not helpful
- Using pytest
  - Using the simple code with pytest as the runner instead of python
  - We can have our cake and eat it too!
- Tests are normally in a test folder. But we are using notebooks since you can
  see what's going on.
