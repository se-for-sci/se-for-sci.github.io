---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python [conda env:se-for-sci] *
  language: python
  name: conda-env-se-for-sci-py
---

```{code-cell} python3
:tags: [remove-cell]

from rich.console import Console

console = Console(width=80)
print = console.print
```

# Design patterns

Let's move beyond OO and learn from other paradigms and patterns. These are not
exclusive - you may use some or all of the ideas here to inform your class
design. You might use OOP ideas to help your functional patterns. Etc.

## Functional Programming

In its own section, see following page.

## Type dispatch

Type dispatch can be seen as an alternative to OOP, though it's often used in
conjunction with it (unless you are in Julia). Type dispatch is a bit
"non-Pythonic" in that it's a bit problematic with duck typing, but you can use
it.

First we start with the "general" implementation; this will get called if none
of the types match:

```{code-cell} python3
import functools

@functools.singledispatch
def generic(x):
    raise NotImplementedError("General implementation")
```

Now we can register one or more types:

```{code-cell} python3
@generic.register(int)
def _(x):
    print(f"I know how to compute {x}, it's an int!")

@generic.register(float)
def _(x):
    print(f"I know how to compute {x}, it's an float!")
```

Now we can call this with ints or floats, but nothing else. It dispatches
different versions depending on the types it sees.

```{admonition} Python specific tips
* Only the first argument will be used for the dispatch. Other arguments are ignored.
* You can use type annotations instead (Python 3.7+)
* You can stack multiple registers
    * Or use Unions (Python 3.11+)
* Duck typing supported through Protocols (Python 3.8+ or `typing_extensions` backport)
* Methods start with `self` - so there's a `singledispatchmethod` too (Python 3.8+)
```

Other languages have varying levels of support for type dispatch. C++ supports
it, while C does not. Julia is designed around it. It's a key part of Rust
(though in a rather different form).

A benefit of type dispatch over OOP is that it tends to be more modular. A
drawback is that some patterns of code reuse are not available.

## Coroutines

A powerful flow control scheme is Generators / Iterators / Coroutines. These are
objects that can stop and resume. In Python, a Generator looks like this:

```{code-cell} python3
def my_range(n):
    for i in range(n):
        yield i
```

The presence of a `yield` causes this to become a generator. The return value of
this function is not an int, it's an iterable object. So expressions like
`for i in my_range(3)` or `list(my_range(3))` are valid ways to use this.

````{admonition} Empty generator
The presence of a `yield` anywhere in a function causes a function to be a generator. So
this is actually an empty generator:

```python
def empty():
    return
    yield
```

The yield in the body forces a generator, which then never yields, but simply
returns immediately, making an empty iterator. That's probably a bit less readable
than this alternative, though:

```python
def empty():
    yield from ()
```
````

The examples above are a subset of generators often called "iterators", because
they only produce values, and do not take values in. There is a way to "send"
values into a generator, though it doesn't really have a special in-language
syntax like a `for` loop or `list`/`tuple`.

There is a second sort of coroutine in Python called an `async` function. It is
conceptually the same sort of thing as a generator, except with `yield from`
being written as `await`. They also fixed the language issue with a single word
being found in the body changing the return type by replacing `def` with
`async def`. If generators were written today, there probably would be some
keyword before `def` for them, removing the "empty generator" weirdness and
keeping the reader from having to manually look at the body of the entire
function for any yields. If you've had experience with compiled languages, you
know that the signature of a function is supposed to be the public interface of
the function, and users should not have to look into the body! This issue in
Python will be corrected when we cover static types.

Generators can be used as a programming model. For example, you might have the
following imperative code to counts the words in a file:

```python
with open(name, encoding="utf-8") as f:
    lines = list(f)

stripped_lines = [line.strip() for line in lines]
words_lines = [line.split() for line in stripped_lines]
words_per_line = [len(words) for words in words_lines]
print("Total words:", sum(words_per_line))
```

This has a problem: every line in the file gets stored in memory (multiple
times!). The lists `lines`, `stripped_lines`, `words_lines`, and
`words_per_line` are all intermediate copies we don't want. Now we could
redesign this doing all the computation in one go:

```python
with open(name, encoding="utf-8") as f:
    total = 0
    for line in f:
        stripped_line = line.strip()
        words_line = stripped_line.split()
        words_per_line = len(words_line)
        total += words_per_line

print("Total words:", total)
```

But this might not match the problem very well. Also we might want the
words-per-line list, which would be harder to get from the second example.

We could rewrite this using a generator:

`````{tab-set}
````{tab-item} Inline generators
```python
with open(name, encoding="utf-8") as f:
    stripped_lines = (line.strip() for line in f)
    words_lines = (line.split() for line in stripped_lines)
    words_per_line = (len(words) for words in words_lines)
    print("Total words:", sum(words_per_line))
```
````
````{tab-item} Generator function
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
````
`````

In both examples above, _a list is never made_. You never store more than one
line of a file in memory. Notice how in the inline version, we needed to keep
the file open, since at each step we were building a generator that had not yet
iterated over the source material. In both cases, the iteration only happens
when we call `sum`.

```{admonition} Refactoring
When programming with functions, a key feature is we can always take a
subsection of the function out and place it in a new function. With generators,
if that section of code includes one or more `yield`s, you can do the same thing
with `yield from` starting in Python 3.3, which made generators fully
refactorable.
```

This syntax is really just a shortcut for making iterable objects, which is done
through magic methods. Iterators can be restartable and have an estimated length
(neither of which is available on the shortcut syntax using `yield`).

Reading a file is a particularly good use case for this, as Python's performance
is about equal or faster than file IO, meaning the most optimized file read and
a Python program that runs Python code on each line of a file are likely to be
competitive. One terrible use case for this style is array programming, due to
the extreme overhead of an interpreted language. An alternative is array based
programming, which is up next.

Other languages have this concept (and it's not that hard to write it yourself
with objects, it's just better to have a standard). C++ traditionally prefers
"start/end iterators" which are objects that can be +1'd and eventually compare
equal, but modern C++ has coroutines (C++20) and a helper to make iterators
(`std::generator`, C++23) - it looks about like you'd expect, with `co_yield`
instead of `yield`. The C++ version was designed to be general enough to back
async support, too, in a single concept.

## Array programming

This is not always mentioned as a programming paradigm, but it is one, and an
important one for the sciences. Consider the following square of an array in
imperative code:

```{code-cell} python3
import numpy as np


input_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
output_data = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

for i in range(len(input_data)):
    output_data[i] = input_data[i]**2
```

This describes what happens to each element. We could have chosen a functional
procedure instead:

```python3
output_data = np.fromiter(map(lambda x: x**2, input_data), int)
```

This still describes what happens on each element in Python. Python has to loop
over the array, doing a lot of work like checking the types, looking up methods,
creating and destroying Python objects, when really this could be done much more
efficiently if you just had a pre-compiled function to do this.

Interpreted languages (like Matlab) as well as a library for Python (NumPy) came
upon a solution to this problem, from the original APL: array-at-a-time
calculations. It looks like this:

```python3
output_data = input_data**2
```

NumPy has overloaded most of the special methods for arrays so that actions on
an array run a pre-compiled routine that does not have to do all the checks
Python does to be general and dynamic. This means you get full compiled like
performance for simple operations. It's also a different paradigm when working
with arrays; it's short and concise, and can read very well (though sometimes
it's a bit harder to write).

Here's a quick example:

```{code-cell} python3
x, y = np.mgrid[0:5:501j, 0.5:3.5:301j]
radius = np.sqrt(x**2 + y**2)
print(f"{x.shape=}, {y.shape=}\n{radius[400,250] = }")
```

Here, we make a grid of values that represent `x` and `y` over a fixed grid.
Then we can work with the values much like we'd write math, and everything
happens element-wise. We can also take these values, mask out values more than
5, then plot the result:

```{code-cell} python3
import matplotlib.pyplot as plt

mradius = np.ma.masked_where(radius > 5, radius)
fix, ax = plt.subplots()
ax.pcolormesh(x, y, mradius)
ax.set_aspect("equal")
plt.show()
```

See
[this SciPy tutorial: loopy programming](https://github.com/jpivarski-talks/2022-07-11-scipy-loopy-tutorial/blob/main/narrative.ipynb)
for more about array based languages & NumPy.

## Memory safety

### Garbage collected languages

Many higher level languages have a garbage collector (most interpreted
languages, and languages like C#, D, Java, Go). These work by keeping a
reference count, and tracking how many ways you can reference an object. Once
that hits zero, the garbage collector is allowed to remove the object to free
memory.

This means we almost don't have to think about memory management. But it also
means we can't think about memory management very much. We don't have much
control over "when" the garbage collector runs (at least as a library
developer).

The problems with garbage collection:

- Performance unpredictable: you might have a garbage collector running in the
  middle of what you are doing.
- Reference cycles can take time to detect.
- Objects may never be deleted: implementation defined.

The last point is an important one. One useful way to think of it: A valid
garbage collector implementation could be a computer with infinite memory. Real
implementations instead usually run the collector at some frequency and detect
some number of reference cycles. Take the following class:

```{code-cell} python3
class CheckDestruct:
    def __del__(self):
        print("Bye!")

a = CheckDestruct()
del a
```

First, note that `del` does not call `__del__`. It simply removes `a`, which
decreases the refcount by one. If the refcount was 2, this will not be deleted.

```{code-cell} python3
a = CheckDestruct()
b = a
del a
```

You have to delete all ways of accessing the object for the refcount to reach
zero:

```{code-cell} python3
b = "something_else"
```

Notice we didn't need `del`, any way of removing the way to access the object
through `b` works.

There are multiple ways you can avoid the word "Bye" showing up. If this gets
referenced in IPython's history, it is really hard to get the refcount down to
zero. If you turn down the frequency of the garbage collector, it will happen
later (defaults to once per line). If you use PyPy instead of CPython, the
garbage collector runs less.

A second problem occurs if this is in globals, and gets cleaned up during
interpreter shutdown. At that point, the interpreter may have started deleting
`sys.modules`, so using something that was imported from elsewhere can be
problematic. In general, very few classes have `__del__` in Python, and they are
very defensively programmed when they do, and only used for emergency cleanup.
For required cleanup, context managers (`with` blocks) are used instead. Python
3.4 also significantly improved finalization, making `__del__` less dangerous.

Reference cycles are the main reason for the garbage collector running. Let's
say you have two of these objects and they reference each other:

```{code-cell} python3
a = CheckDestruct()
b = CheckDestruct()
a.other = b
b.other = a
del a, b
```

Let's import the `gc` and force a full collection:

```{code-cell} python3
import gc
gc.collect()
```

There we go. It detected the reference cycle, and cleaned it up for us. Note:
there is a chance the collection will run by itself; if you try this yourself,
you might see it happen before you can make it to the collect call.

```{admonition} Garbage collector vs. refcount
CPython will automatically delete anything that has a refcount that drops to 0
when that happens. The garbage collector is there to detect reference cycles and
also delete those. You can disable the garbage collector with `gc.disable()`, and
you will only lose reference cycle deletion.

If you ask `sys.getrefcount(...)` for the refcount of an object, it will start
at 2; the use of it as a parameter increases it by one during the `getrefcount`
call!
```

You can avoid the cycle manually if you want (this is extremely rare in Python):

```{code-cell} python3
import weakref

a = CheckDestruct()
b = CheckDestruct()
a.other = b
b.other = weakref.ref(a)
del a, b
```

Now `b.other` does not keep `a` alive, so deleting `a` is enough to delete it
completely. But, on the flipside, if you do delete only `a` and not `b`, then
`b.other` will be invalid!

### Memory management and moves

Let's look at C++ (& Rust in a minute) so that we can see manual memory
management. All C++ examples can be run on public compiler services, like
<https://wandbox.org>, which allows you to load files and create shareable
links, and <https://cpp.sh>, which compiles on a server using Emscripten then
runs the code in your webbrowser using the WebAssembly output. The most famous
online compilers is <https://godbolt.org>, which supports a massive number of
compilers and has the most advanced interface. "Godbolting" is a term you'll
sometimes hear when it comes to testing something out quickly.

You can find similar online tools for most of the other languages (all snipits
in this course work on online playgrounds). For example, Rust has
<https://play.rust-lang.org>.

Later we'll compile things ourselves. But this works for quick example demos.
Unless specified, all examples use C++20.

For a compiled language, you have access to two types of memory:

#### The stack

The stack is pre-allocated when you start your program. The stack is local - you
can only access it in the scope (frame) that it is in, and not above - unloading
the current frame unloads the stack associated with it. It is automatically
reclaimed at the end of scope. In C or C++, defining a local variable places it
on the stack:

```cpp
int main() { // The stack is allocated here
    int x = 2;
} // The stack is removed here
```

In C, you used to have to declare all variables at the top of a function,
because it's preparing the stack for the current function. In modern C and C++,
you can define variables anywhere, and the compiler will prepare the appropriate
stack for you. It's still placed at the top, because the stack is contagious.

The biggest problem with the stack is it's not dynamic. You can request a
runtime dependent amount of it. It's also limited (you can adjust the limit in
the linker); each program gets a free continuous block of memory equal to the
maximum stack size, around 1MB by default on most systems. It's (mostly) hard to
run out of it unless you try. And of course, since it's loaded/unloaded with the
function you are in, it's not shared between different parts of your program. It
was designed to hold local variables required for a function's operation.

#### The heap

If you need more, shared, or dynamic memory, you need to use the heap. The heap
is managed by your OS, and you can generally access as much as you want (until
you run out of memory), and you can allocate and deallocate in it at will.
That's both the feature, and the problem...

##### Manual management

Classic heap allocation looks like this in C++ (C uses the functions malloc and
dealloc, and you have to specify the exact number of bytes you need, because
it's C):

```cpp
int main() {
    int* x = new int;  // a
    *x = 2;            // b
    delete x;          // c
    return 0;
}
```

This has one stack variable `x`, which a pointer to an int. It's a (probably) 64
bit number pointing to a memory address. We request a new allocation on the heap
on line `a`, and the pointer points at this place in the heap. In line `b`, we
are dereferencing the pointer (`*x`, and yes this feels backwards, since the `*`
in the line above indicated a pointer, while here it's getting the thing the
pointer points at), and then assigning 2 into that memory location. If we were
to use `*x` again, it would be 2. Finally, we have to delete our heap memory
manually in line `c`.

The biggest issue is the `new` / `delete` pattern. We have to have the `delete`
in order to keep from leaking memory (during the program execution, the OS
tracks the program allocations and cleans up everything when it exits). The OS
doesn't now how to call destructors, so C++ objects allocated in the heap will
also never run their destructors if you forget delete. We also shouldn't
deference a pointer after it's been deleted (remember our state discussion?), or
delete it twice, or delete before new, or call new twice before delete, etc. If
an exception is thrown (yes, C++ has those), then we could easily take a path
that misses delete. Really, it's a mess.

Simple rule: never call `new` / `delete` manually. There are better patterns.

##### Pattern 0: Classes

One way to manage heap safely is to tie it to classes. C++ has constructors and
destructors, so why not use them for new / delete?

```cpp
#include <iostream>

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

int main() {
    HeapInt three{3};  // a

    std::cout << three.get_value() << std::endl;
    return 0;  // b
}
```

Here, we create a class that manages allocating and freeing memory in it's
constructor/destructor. Now, to use it, we just create an instance of `HeapInt`

- the act of doing this creates the heap value. When our class goes out of
  scope, it takes the heap out too. We are using the stack to manage the heap!

This doesn't solve all our problems (specifically, we still can't create this
inside one function and then "move" it to another function with a different
stack), but we'll get there. In fact, we completely ignored copying as well.

A _lot_ of the standard library (and C++ classes in general) do this. For
example, `std::string` can hold arbitrary sized strings - it does this by using
the heap (well, mostly - it has a small stack allocation and it will put very
small strings in there if they fit). Copying a `std::string` makes a copy of the
heap allocation. Other common heap structures include most of the containers
like `std::vector`, all the sets and maps. `std::array` is an exception; since
the size is part of the template, it is allocated on the stack. That's why it
requires the size ahead of time and can't be resized.

##### Pattern 1: Smart pointers

The above pattern is useful. So useful, in fact, wouldn't it be nice if there
was nice, templated way to do this for an arbitrary type you want to "hold"? In
order to do that, we have to solve the copy problem we ignored above. What
happens when you copy this "smart pointer" as we'll call it? We have two
choices: We can do the best computer science thing when faced with a hard
problem: just don't allow it!

This is called a unique pointer, `std::unique_ptr` in C++. Here's the above
example:

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

We'll look at moves later; after we cover that, note that this is movable too.

The other way is we can keep a reference count (this is sounding like Python!).
This reference count is a bit expensive because it is thread-safe (which just
means you can copy `std::shared_ptr`'s in multiple threads without worry about
corrupting memory), but it basically gives you a Python-like experience where
you can use it without thinking and it gets cleanup up when the last copy goes
out of scope.

You use it in exactly the same way as `std::unique_ptr` above, with the only
difference being `std::make_shared` was available in C++11, it took three more
years to add `std::make_unique` for some reason.

And there's no garbage collector, so you are responsible for avoiding reference
cycles. You can use `std::weak_ptr` or you can access the raw pointers with
`.get()` (just don't `delete` them!).

##### Pattern 2: Moves

C++11 added a powerful new concept to C++: moves. The idea is this: you can tell
C++ that a variable can no longer be accessed after a usage. Then a special
constructor (the move constructor) will be used instead of the copy constructor.
_The stack does not move_; the move constructor may be supported, but it's no
different than a copy. But the heap can, so the move constructor can simply
reassign ownership of the heap to the new object.

Let's go ahead and expand our little example from above:

```cpp
#include <memory>
#include <iostream>

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
    ~HeapHolder() {  // Destructor
        if(value != nullptr)
            delete value;
    }
    T& operator*() {  // Overload *self (like smart pointers)
        return *value;
    }
};

int main() {
    HeapHolder<int> start{3};
    HeapHolder<int> middle{std::move(start)}; // a
    HeapHolder<int> moved = std::move(middle); // b
    std::cout << *moved << std::endl;
    return 0;
}
```

A few things have changed:

- This is now templated. It works with more that just ints.
- There is now a move constructor that takes over the memory (and nullifies the
  original).
- The destructor now only clears memory if it has active memory.
- We now overload `*item` to access the contained object, like the stdlib.

We play with both the move constructor (`a`) and the move assignment (`b`), and
then print out the result.

If you actually implement classes like the ones above, you should probably hold
`std::unique_ptr`(s) and still avoid writing your own new / delete, even in a
class. Also, it's a bit more common to swap pointers in move constructors than
make the class handle `nullptr`'s, but I thought the above looked simpler.

#### Common needs

There are other reasons to use pointers in C++ that are not related to memory,
but are caused by other things. Let's quickly cover them and the better modern
(C++17, also available earlier in Boost) solution:

##### Optional items

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

Instead of using pointer, you can use `std::optional`, which is stored entirely
on the stack. C++23 is even adding functional methods to `std::optional`.

##### Union

If you have several different types, each possibly with different sizes, the
heap seems to be a natural place to put them. But you don't have to with
`std::variant`!

```cpp
std::variant<int, float> int_or_float;
int_or_float = 12;
int i = std::get<int>(int_or_float);  // i is now 12
```

The variant is sized to the largest item it can hold. There are several ways to
ask it what it holds, or to use generic lambdas (from C++17), overloads, and
more to get the contained value easily.

You can put anything inside, and you can put them inside containers like
`std::vector`.

##### Type erasure

What if you don't know the type you want beforehand? You can't put that on the
stack, obviously, since you don't know the size, but you still don't have to
resort to void pointers (which are very hard to safely use). Instead, you can
use `std::any` to give you type erasure safely:

```cpp
std::any a = 1;
std::cout << a.type().name() << " " << std::any_cast<int>(a) << std::endl;
```

Any also can be "empty", like `std::optional`.

#### A new approach to memory

We now have the ability to completely avoid an entire class of memory errors. If
we carefully use moves and think about ownership, we can avoid ever having
memory at risk of being deleted out from under us or leaking. But the language
allows unsafe access too. What if you built a language that _didn't_ allow
unsafe access at all? Someone did; it's called Rust.

Let's look at a very simple invalid Rust program:

`````{tab-set}
````{tab-item} Broken
```rust
fn main() {
  let s1 = "Hello world".to_string();
  let s2 = s1;
  println!("{} {}", s, s2);
}
```
````
````{tab-item} Reference
```rust
fn main() {
  let s1 = "Hello world".to_string();
  let s2 = &s1;
  println!("{} {}", s, s2);
}
```
````
````{tab-item} Clone
```rust
fn main() {
  let s1 = "Hello world".to_string();
  let s2 = s1.clone();
  println!("{} {}", s, s2);
}
```
````
````{tab-item} Views
```rust
fn main() {
  let s1 = "Hello world";
  let s2 = s1;
  println!("{} {}", s, s2);
}
```
````
`````

A few quick notes on the syntax:

- There's an actual keyword for function definitions `fn`, like Python's `def`.
- There's a keyword for variable definitions (`let`), like JS or Swift.
- Everything is constant by default (C++'s mutable by default is seen as a
  mistake).
- Types are optional if they can be inferred (though they were included here)
  - If included, types follow the value instead of preceding it, like most
    modern languages - including Python (see next week!)
- There's a `&'static str` type for string literals, and a `String` type stored
  on the heap; we explicitly want the `String` one with `to_string()`.
- `println!` is a syntactic macro - ignore that, it's basically just a function.
  It has a format syntax like Python's.

Okay, so why is this function fail to compile? `let s2 = s1` _moves_ `s1` to
`s2`! Since ownership of this heap object is now in `s2`, we can't access `s1`
anymore! You can fix it by using a reference, which means `s2` does not own the
data, ownership stays with `s1`. Or you can use `.clone()` to clone the string
(in Rust terms, `String` implements the `Clone` trait). Or we could just leave
off the `.to_string()`, which gives us a view `&str` (think if it like a slice
or `std::string_view` in C++); this doesn't own memory - it's just a reference,
so is safe to copy.

Feel free to look through the different versions above.

A great read on
[memory safety is here](https://stanford-cs242.github.io/f18/lectures/05-1-rust-memory-safety.html).

## Interfaces

One growing trend in modern programming design is the idea that you can specify
a set of requirements to use a class in a stand-alone form, not just through
inherence. In Java this was called Interfaces, C++ this is called Concepts, in
Rust this is called Traits, and we'll see this in Python as Protocols. Since
we'll be go into it in detail next week, we won't cover it here.

Rust's implementation of this is _partial parametric polymorphism_, which is the
other unique thing about Rust (besides the memory model). This allows you to
extend an existing type to support an Trait (including built-in types!), and it
gives a little more control over what types have what Traits than other
languages that just use name matching. Method lookup uses Traits.

A great read on Traits (after you've mastered the basics of interfaces next
week) is
[here](https://stanford-cs242.github.io/f18/lectures/05-2-rust-traits.html).

## Other patterns

We didn't cover every pattern (and we can't), so here are a few more you can
look up if you are curious:

- Singleton pattern: There can only be one instance of a class. `None`, `True`,
  and `False` are singletons in Python.
- Registries: `logging` uses this design.
- Factory pattern: We've touched on this lightly, classes `__init__` method, for
  example. You can have other factories with `@classmethod`'s that return new
  instances. (or static methods in C++, etc)
