- Project: due Friday, feel free to discuss of ED discussions, single page
  submission for groups of 3

Memory management

- Review: stack vs. heap
- Code from last time
  - Addition of templating
  - `nullptr` addition
  - Copy (just deleting it explicitly - will not handle in example)
  - Move constructor addition
- In the standard library: Smart pointers
  - `unique_ptr` is very close to our example - movable, not copyable
  - `shared_ptr` has a refcount, is a little slower for thread safety (refcount
    only) - very Python like
    - You are responsible for not making or cleaning up cyclic references - no
      garbage collector here!
- Common needs: these things don't need pointers (C++17 or use Boost libraries)
  - `std::optional`: for when something could be "None". On the stack.
  - `std::variant`: A union, can hold one of several options. Sized on the stack
    to the largest member.
  - `std::any`: Can hold any type, similar to objects in Python. On the heap.

A new approach (in Rust)

- Small string example
  - `fn` is like `def` in Python (searchable keyword for function definition)
  - `let` makes a variable, type is inferred, "const" by default! (Mutable
    default in C++ seen as mistake)
- Broken! Because Rust _moves_ by default!
  - Can fix by being explicit about ownership - take reference, make clone, or
    use view (which is also a reference)

Other patterns

- Singleton
- Registries
- Factories
- State machine
- Event loop / Async

Static Typing

- Python best feature: no static typing
- Python worst problem: no static typing
- Python has gained _optional_ static typing in the last few years
- Run a function with bad types - no error
- Compare to compiled language - types are caught "at compile time"
  - So we need to add a "compile time", or "static check" run to Python!
  - This is done with a "type checker", which is like a compiler that doesn't...
    compile.
- Why Python? This is not a Python course.
  - Familiar, simple, gradual, and a useful skill if you do need it in Python
- Pick a type checker - we'll pick MyPy (lowest common denominator, heavily
  used, from the Python team)
- Running a type checker
  - Running on example code with `mypy <filename>`
  - Strict mode `--strict` adds a few dozen "strictness" flags
    - Gradual typing - designed for untyped large code bases slowly adding types
  - `reveal_type` is like `print()` but for type checkers (now standardized in
    `typing`/`typing_extensions`, but available by default inside the type
    checker)
  - `from __future__ import annotaitons` turns all annotations into strings! Can
    use future syntax in older Pythons
  - Example using "Optional" -> `float | None`
  - `type: ignore` escape hatch (not available in compiled language!)
  - You can lie about types
