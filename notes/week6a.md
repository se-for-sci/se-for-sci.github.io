Structural subtyping

- Protocols (Interfaces in Java, Concepts in C++20)
- Formalized duck typing
- Example: PlottableHistogram from https://uhi.readthedocs.io
  - Boost-histogram/hist & uproot can produce histograms, but can't depend on
    each other
  - Histoprint & mplhep can visualize histograms, but don't want to be dependent
    on either/both & have multiple implementations for each
  - A `PlottableHistogram` protocol was decided on and provided in the UHI
    package.
  - Huge win! No interdependencies, more libraries have joined.
- Protocols (as "concepts") were a huge win for C++ error messages!
  - Ranges waited for concepts entirely due to error messages. Results of better
    error messages will be slow, due to C++20 taking time to take hold.
- Example: `.do_something()`
  - Writing a Protocol
  - Using a Protocol
  - Implementing a Protocol
- Standard Protocols in `collections.abc`/`typing`
  - Sized just means it has `__len__`
  - Others like `Itereable`, `Collection`, `Sequence`, `Mapping`, `Callable`
- Rule: Accept as general as you can, return as specific as you know.
- Generics: Possible with `TypeVar` (like templating in C++) - can "forward"
  through types, or implement new parametrized types!
- Bonus: if you fully statically type, maybe try `mypyc` and see if you get a
  2-5x speedup? Worth checking.

Git: see class notes

- A bit about why version control
- A discussion of the history of git
  - Older systems (Centralized Version Control) used incrementing numbers and a
    single source of truth.
  - Git uses SHA's, and is fully Distributed Version Control
- Branching is lightweight and easy
- Example of building a good git history (DAG)
- Quick example of making a PR via a web interface, and a quick look at GitHub's
  "period key" WebAssembly VSCode instance.
