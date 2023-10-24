---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# APC 524

## Design patterns

---

## Prelude

To keep the slides simple, I will assume the following imports:

```python
import dataclasses
import functools
import numpy as np
```

---

## Type Dispatch

Can be alternative (Julia) or used in conjunction with OOP.

```python
@functools.singledispatch
def generic(x):
    raise NotImplementedError("General implementation")


@generic.register(int)
def _(x):
    print(f"I know how to compute {x}, it's an int!")


@generic.register(float)
def _(x):
    print(f"I know how to compute {x}, it's an float!")
```

---

## Type Dispatch: Python specific tips

- Only the first argument used (single dispatch)
- You can use type annotations instead
- You can stack multiple registers
- Or use Unions (Python 3.11+)
- Duck typing is supported through Protocols
- Methods start with self - so there’s a singledispatchmethod too

---

## Type Dispatch: language support

- Python: opt-in, first argument only (single dispatch)
- Julia: The language is designed around multiple dispatch
- C: Not supported
- C++: Supported
- Rust: Possible via Traits

Type dispatch tends to be modular, but doesn't have some code reuse & discovery features of OOP.

---

## Coroutines

AKA Generators / Iterators.

```python
def my_range(n):
    for i in range(n):
        yield i
```

The presence of a yield anywhere in the body changes this to a generator (bad design, by the way).

Try to make an empty generator. :)

---

## Coroutines (2)

- To start iteration, call `y = iter(x)`, which calls `y = x.__iter__()`.
- To increment, call `next(y)`, which calls `y.__next__()`.
- To stop, raise `StopIteration` (yes, an exception is required).

Lots of places in Python do this for you, like `for` loops, `list(...)`, etc.

---

## Coroutines (3)

Two way communication is possible (though not as nicely supported via syntax). Call `y.send(...)` instead of `next(y)`. The `yield` expression returns the sent value.

`yield from` lets you factor out generators.

Python's `async`/`await` are also generators, just specialized for asyncio.

---

## Coroutines as a design pattern

### Non-generator version

```python
with open(name, encoding="utf-8") as f:
    lines = list(f)

stripped_lines = [line.strip() for line in lines]
words_lines = [line.split() for line in stripped_lines]
words_per_line = [len(words) for words in words_lines]
print("Total words:", sum(words_per_line))
```

Make many unneeded lists!

---

## Coroutines as a design pattern

### Non-generator version (2)

```python
with open(name, encoding="utf-8") as f:
    total = 0
    for line in f:
        stripped_line = line.strip()
        words_line = stripped_line.split()
        words_per_line = len(words_line)
        total += words_per_line
```

May not want to write this way!

---

## Coroutines as a design pattern

### Generator version (1)

```python
with open(name, encoding="utf-8") as f:
    stripped_lines = (line.strip() for line in f)
    words_lines = (line.split() for line in stripped_lines)
    words_per_line = (len(words) for words in words_lines)
    print("Total words:", sum(words_per_line))
```

---

## Coroutines as a design pattern

### Generator version (1)

```python
def word_counter(name):
    with open(name, encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            words_line = stripped_line.split()
            words_per_line = len(words_line)
            yield words_per_line


print("Total words:", sum(word_counter(name)))
```

---

## Generators in other languages

You could always make your own, but nicer with language support.

- Python: Generators and Async, generator comprehensions
- C++: Coroutines new in C++20 and `std::generator` added in C++23. Various libraries like `boost::async`
- Rust has third-party libraries implementing coroutines

Iterators are similar, though a bit less powerful (one directional):

- C++ also has iterators (with begin/end)
- Rust has a `std::iter::IntoIterator` Trait

---

## Array programming

Not always considered, but it's an important one for the sciences.

```python
input_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

# Imperative version
output_data = np.zeros_like(input_data)
for i in range(len(input_data)):
    output_data[i] = input_data[i] ** 2

# Functional version
output_data = np.fromiter(map(lambda x: x**2, input_data), int)

# Array-at-a-time version
output_data = input_data**2
```

---

## Array programming (2)

Originally a language feature (APL, Matlab), it is a library feature in modern languages (Python, C++, Rust).

```python
x, y = np.mgrid[0:5:501j, 0.5:3.5:301j]
radius = np.sqrt(x**2 + y**2)
```

In the above example, we compute the radius for plotting.

---

## Memory safety: garbage collection

Garbage collected languages include most interpreted languages as well as C#, D, Java, Go.

Pros:

- easy

Cons:

- Unpredictable performance
- Counting reference cycles can take time
- Objects may never be deleted (implementation defined).

---

## Reference counting

```python
class CheckDestruct:
    def __del__(self):
        print("Bye!")


a = CheckDestruct()
del a
```

This should print `Bye!`

---

## Reference counting (2)

```python
a = CheckDestruct()
b = a
del a
```

Does this print `Bye!`?

---

## Reference counting (3)

```python
b = "something else"
```

How about now?

---

## Reference counting (4)

There are other ways to get a reference. Like:

- The REPL keeps the last expression (`_`)
- IPython keeps every output (in `Out[...]`)

If you miss one, `__del__` gets called during Python shutdown, and even `sys.modules` might not be reliable!

Use `sys.getrefcount` to see how many refs you have (remember it takes one, so 2 is the smallest value).

---

## Garbage collector

We haven't really seen the garbage collector; Python immediately cleaned those up due to the refcount going to 0. Try this:

```python
a = CheckDestruct()
b = CheckDestruct()
a.other = b
b.other = a
del a, b
```

---

## Garbage collector (2)

If you need to force a run:

```python
import gc

gc.collect()
```

You can disable it:

```python
gc.disable()
```

Don't leave it off!

---

## A valid garbage collector

A garbage collected is _only required_ to delete objects to keep memory from running out.

Infinite system memory is a valid implementation of a garbage collector!

---

## Manually fixing reference cycles

```python
import weakref

a = CheckDestruct()
b = CheckDestruct()
a.other = b
b.other = weakref.ref(a)
del a, b
```

This is rarely used with a GC, and `del a` would invalidate `b`!

---

## Memory management in compiled languages

We'll be moving to a compiled language (C++20) for this part, since we can't talk about stack vs. heap in an interpreted language, and we can't talk about memory management without a garbage collector if we have one!

Feel free to use godbolt.org, cpp.sh, wandbox.org, or similar online C++ compilation.

---

## Stack vs. heap

Stack:

- Pre-allocated when you run your program
- Fast
- A function (frame) has a set stack usage

Heap:

- Can be requested during runtime
- Can be any size
- Requested in consecutive chunks
- Can leak (forget to deallocate)

---

## Stack and frame

```cpp
int main() {  // The variables (x) pushed onto the stack
    int x = 2;
    return 0;
} // Stack values (x) dropped here
```

C used to require all variable at the top of a function.

---

## The heap: manual management

```cpp
int main() {
    int* x = new int;  // Request 32 bits on heap, store 64 bit pointer on stack
    *x = 2;            // Put 2 in the location in the heap
    delete x;          // Release 32 bits on heap back to OS
    x = nullptr;       // Protect against mistakes later
    return 0;
}
```

Don't do this, especially in C++!

What happens if the middle line throws an error and you catch it later>

---

## RAII

We can use a classes and the stack to help us with the heap!

RAII: Resource Allocation Is Initialization pattern.

---

## RAII code

```cpp
class HeapInt {
  private:
    int* value;

  public:
    HeapInt(int init) : value(new int(init)) {}  // Constructor
    HeapInt(const HeapInt&) = delete;  // Copy constructor
    HeapInt& operator=(const HeapInt&) = delete;  // Copy assignment
    ~HeapInt() {  // Destructor
        delete value;
    }
    void set_value(int val) {
        *value = val;
    }
    int get_value() const {
        return *value;
    }
};
```

---

## RAII code (2)

```cpp
int main() {
    HeapInt three{3};  // Memory allocated here

    std::cout << three.get_value() << std::endl;
    return 0;  // Memory removed here
}
```

We could even overload `operator*` to make this more pointer like!

---

## RAII in the standard library

Obviously, don't do this yourself. This is used in the standard library heavily:

- `std::unique_ptr<T>`: Basically what we just wrote
- `std::shared_ptr<T>`: Also has reference counting
- `std::vector<T>`: Stores sequence of values
- `std::string`: Stores letters

---

## Moves

What if you want to use something outside of the current frame?

C++11 added the idea of moves (and Rust moves by default). You can't "move" the stack, but you can _transfer ownership_.

- Copy the stack items
- Invalidate the old value

---

```cpp
template<typename T>
class HeapHolder {
  private:
    T* value;

  public:
    HeapHolder(T init) : value(new T(init)) {}  // Constructor
    HeapHolder(const HeapHolder& init) = delete;  // Copy constructor
    HeapHolder(HeapHolder&& init) noexcept : value(init.value) {   // Move constructor
        init.value = nullptr;
    }
    HeapHolder& operator=(const HeapHolder& other) = delete;  // copy assignment
    HeapHolder& operator=(HeapHolder&& other) noexcept { // move assignment
        return *this = HeapHolder(std::move(other));
    }
    ~HeapHolder() { if(value != nullptr) delete value; }
    T& operator*() { return *value; }
};
```

---

## Moves (2)

```cpp
int main() {
    HeapHolder<int> start{3};
    HeapHolder<int> middle{std::move(start)}; // a
    HeapHolder<int> moved = std::move(middle); // b
    std::cout << *moved << std::endl;
    return 0;
}
```

---

## Smart pointers

```cpp
#include <memory>
#include <iostream>

int main() {
    std::unique_ptr<int> heap_int_a{new int(3)};  // Original C++11
    auto heap_int_b = std::make_unique<int>(3);  // C++14 required

    std::cout << *heap_int_a << " " << *heap_int_b << std::endl;
    return 0;
}
```

These also support moves.

---

## Replacements for pointers

Let's cover some common needs that pointers used to solve, but have a type safe alternative now.

---

## Optional items

```cpp
// Bad
int* x = int_or_nullptr_func();
if(x)
    use(*x);

// Good
std::optional<int> x = optional_int_func();
if(x) {
  use(*x);
}
```

---

## Union (Enum in Rust)

```cpp
std::variant<int, float> int_or_float;
int_or_float = 12;
int i = std::get<int>(int_or_float);  // i is now 12
```

---

## Type erasure

```cpp
std::any a = 1;
std::cout << a.type().name() << " " << std::any_cast<int>(a) << std::endl;
```

---

## A new approach to memory (Rust)

```rust
fn main() {
  let s1 = "Hello world".to_string();
  let s2 = s1;
  println!("{} {}", s, s2);  // BROKEN!
}
```

---

## Rust: Reference

```rust
fn main() {
  let s1 = "Hello world".to_string();
  let s2 = &s1;
  println!("{} {}", s, s2);
}
```

Note you are allowed as many const references as you want without `mut` references, but only one `mut` reference at a time!

---

## Rust: Clone

```rust
fn main() {
  let s1 = "Hello world".to_string();
  let s2 = s1.clone();
  println!("{} {}", s, s2);
}
```

---

## Rust: View

```rust
fn main() {
  let s1 = "Hello world";
  let s2 = s1;
  println!("{} {}", s, s2);
}
```

Like `std::string_view` in C++17. Already a reference, so safe to copy (string in static storage).

## Example of a buggy C++ code

```cpp
val = std::vector {1, 2, 3};
first_element = &val[0];
val.push_back(4);
std::cout << first_element << std::endl;
```

This can't happen in Rust!

---

## Interfaces

- Java: Interfaces
- C++: Concepts
- Python: Protocols
- Rust: Traits (partial parametric polymorphism, technically)

We'll see Protocols in detail next week.

---

## Traits (Rust)

One of Rust's two key features (besides the memory model and borrow checker).

Differences vs. normal Interfaces:

- Must explicitly opt-in to a trait, not just simple name matching
- Only the library defining the Trait or the library defining the type can opt-in to a trait
- Trait methods can overlap, including with struct methods!
- Lookup will use the trait method if available and non-overlapping

---

## Traits (2)

```rust
foo = Foo::new();
foo.bar();
```

If there's a `Foo::bar()`, call that. If not, if there's a Trait with a `.bar()` implemented on `Foo`, call that.

---

## Other patterns

- **Singleton pattern**: There can only be one instance of a class. Like `None`, `True`, `False`.
- **Registries**: logging uses this design.
- **State machine**: this is used heavily by Matlab.
- **Factory pattern**: We've touched on this lightly, classes `__init__` method, for example.
- **Ascync patterns**: Lightly touched on during generators.
- **Event loop**: A common pattern for reacting to multiple possible inputs.
