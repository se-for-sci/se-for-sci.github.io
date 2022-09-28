- Level Up Your Python minicourse this Friday at 4:30 PM
- Include "APC 524 in emails, please
- Let's use ED Discussions (class request) - I'll move to there.

Functional Programming

- Mutability and state
  - Truly immutable - a few CPython builtins (well, unless you fiddle with raw
    pointers and bits, but let's not do that)
  - Declared to be immutable by adding hash
    - Hash is a consistent number that allows an object to be placed in a set or
      as the key of a dict
    - Lookup is fast because you can do much faster lookups on a sorted set of
      hashes
- Why Mutable?
  - Easy to change small part
    - But we can use tricks like `dataclasses.replace` or replace methods on
      signatures/code objects, etc.
    - Showed dataclasses example
  - Memory saving
    - But this is actually an implementation detail if you do not access the
      original object again - some languages/libraries can take advantage of
      this to optimize the copy out.
  - You can make a mutable API
    - But functional style chains can be nearly as easy to _use_ (not always
      write), and provide tab completion / correctness benefits
    - Think about _state_ - methods that mutate state incompatibly are generally
      bad (but sometimes necessary)
- Why Immutable?
  - Copy vs. Reference
    - The signature is your contract with the user - input in, output out
    - Mutable arguments (and even mutable default arguments) are surprising if
      you mutate them!
    - You don't need to worry about copy vs. reference if you don't mutate!
    - `self` is special - we sometimes expect to mutate that
  - Easier on compiler (if you are using one) - can optimize
  - Chaining APIs can be nice
- Notice the requirement is "functions don't mutate", not "immutable data
  structure"
- Pure functions
  - No mutation
  - No state (self mutation)
  - No side effects (printing, file IO)
- Map, Filter, Reduce
  - Example using idiomatic Python & comprehensions instead
  - Example in vanilla Python
  - Example with a little wrapper to give "chaining style"
  - Looking at other languages. Sometimes map -> apply or transform, sometimes
    reduce -> fold.
- Currying
  - `functools.partial` example
- Why Functional?
  - Can be lazy
  - Can be parallelized (not in Python)
  - Easier to optimize or work with
- Example: JAX (Google's functional successor of sorts to TensorFlow)
  - NumPy like API except no mutation allowed
  - Can use special methods to make copies with small changes
  - Can use `jax.jit` to fuze together and prepare code for CPU, GPU, and TPU
  - Can use `jax.grad` to compute gradients from functions
  - Not the only choice for machine-level performance from Python or GPUs! See
    Numba, CuPy, PyTorch, and others. This one is just functional.
