Announcement

- Project notes
  - 1 page, pass/try-again, idea of scope
  - Groups of 5 -> make two groups (maybe closely connected groups?)
- Git -> install for next time if not already installed
- If using brew + mypy, update (4x faster now, just like the one you pip
  install)

Typing

- Simple types
  - A string of a type is the type
- Catch-all types
  - Any vs. object
  - No known type == Any
- Generics (angle brackets in C++)
  - list
  - tuple
  - dict
- Unions (`|`)
  - Optional pattern
  - MyPy show old syntax
- Final (not really const)
  - final for class methods, too
- Enums
- TypedDict (if tempted to use, consider a normal class...)
  - One of the few places you get to see class keyword arguments used, so I
    guess that's something.
  - Finally getting "better" in 3.11 and typing_extensions (but then no need for
    class keyword `total=False` argument 😡 )
- NamedTuple (typed replacement for `collections.namedtuple`)

Structural Subtyping

- Protocols (like Java Interfaces, C++ Concepts (and older SFINAE ideas))
- "isinstance" type checks based on _structure_, not inheritance - formalized
  duck typing!
