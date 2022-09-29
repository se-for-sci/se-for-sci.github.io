Announcements

- Projects descriptions due next week, aiming to post on Friday
- HW1 due tomorrow
- AI office hour moved to tomorrow (see Canvas announcement for details)

Type Dispatch

- A bit forced in Python, common in C++ & the basis for Julia
- Python: single dispatch, opt-in
  - Example from notes
  - Tips:
    - First argument only
    - Type annotations work too (3.7+)
    - Unions work too (3.11+)
    - Duck typing via Protocols works too (next week)
- This is modular and can be partial (implemented at different times / in
  different files), unlike OOP

Coroutines - Generators - Iterators

- Example: my_range from notes
- Empty generator
  - You have to check the function body for "yield"
  - This was done better when async coroutines were added to the language
- Iterator as a programming model
  - Example reading a file two ways, then converted to iterators
  - Can refactor iterators with `yield from`, Python 3.3+
- Iterators are fine for things like IO, Python's not fast at per-array
  operations, though
  - But we have array based programming up next!
- C++20 has `co_yield` and C++23 has `std::generator`.

Array based programming

- NumPy array -> dense memory store
- Imperative square example
- Functional square example
- Array based square example
  - The looping is done in C, precompiled into NumPy
  - Downside: memory usage and lots of separate calls and memory allocations
    (note: NumPy can do a tiny bit of operation fusion for simple code)
- mgrid simple computation example
- Array based programming started in APL, also used in Matlab and many others
- Easy to read, little less so to write (sometimes)
- Loops often become dimensions in an ND array

Memory - garbage collector

- Simple `class Boom: def __del__(self): print("Boom")` example.
- Deleting the instance only calls the destructor if the refcount goes to 0
- Multiple ways to increase the refcount, including IPython's history storage
- The garbage collector is supposed to solve reference cycles, like a inside b,
  b inside a.
- You can manually run the garbage collector, and it runs with some frequency.
- You can use weakref.ref to solve cycles yourself (rare, tricky)

Memory - compiled language

- We'll use online compilers - cpp.sh is one I thought looked good for this,
  godbolt.org is a famous one but to complicated for my simple examples.
- The stack: local linear storage for function frames
  - Loaded at the start of a block (function, usually) and unloaded at the end
  - Static, can't request an arbitrary amount
  - Not shared (can't use after the frame is unloaded)
  - Limited in size (usually 1MB, though if you find this out you are likely
    misusing it!)
- The heap: OS managed memory pool
  - New/delete pattern in C++ (malloc/dealoc in C, and you have to count bytes
    in C!)
    - Lots of ways this could go wrong. Forget to call delete, call delete
      twice, use after delete, etc.
  - C++ syntax
    - `int*` is a pointer, compiler ensures it's to an int (type safety)
    - `*x` gets the address `x` points at
  - Setting the pointer to `nullptr` after delete is good practice
- Pattern 1: Class to manage the heap with the stack
  - New in constructor, delete in destructor
  - Since this is the stack (and not a garbage collector), it's safe to use
  - Doesn't solve the sharing problem, we'll get there
  - We also ignored copying. One step at a time!
