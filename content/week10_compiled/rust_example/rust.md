# Intro to Rust

This is an introduction to some of the unique design of Rust. This is not
comprehensive - the fantastic [Rust Book][] is much better if you want to fully
learn Rust. Instead, we'll look at how it's different from what we've seen so
far in Python, and discuss some of the aspects that make special, like how it is
memory safe without resorting to a garbage collector, the trait system, and
syntactic macros.

## Basic syntax

| Feature                     | Python                      | Rust                               |
| --------------------------- | --------------------------- | ---------------------------------- |
| Assignment                  | `x = 2`                     | `let x = 2;`                       |
| Reassignment (non-mutating) | `x = 3`                     | `let x = 3;`                       |
| Integers                    | `x: int = 2`                | `x: i32 = 2;` (`u32` for unsigned) |
| Else if                     | `elif`                      | `else if`                          |
| Range loop                  | `for i in range(4): pass`   | `for i in (0..4) {}`               |
| Function definition         | `def f(): pass`             | `fn f() {}`                        |
| Return value                | `return x`                  | Final statement                    |
| Return type                 | `def f() -> int: return 42` | `fn f() -> i32 {42}`               |
| Ternary                     | `x if b else y`             | `if b {x} else {y}`                |
| Lambda                      | `lambda x: x+1`             | `\|x\| x+1` (`{}` can be used)     |
| Tuple (heterogeneous)       | `(x, y)`                    | `(x, y)`                           |
| List (homogeneous)          | `[x, y]`                    | `[x, y]`                           |
| Vector (homogeneous)        | `[x, y]`                    | `vec![x, y]` (stdlib)              |
| Interpolated print          | `print(f"Hi {var})`         | `println!("Hi {var}");`            |
| Repr (debug) print          | `print(f"Hi {var!r})`       | `println!("Hi {var:?}");`          |
| Interpolated string         | `f"Hi {var}`                | `format!("Hi {var}");`             |

Lambda functions can be multiple lines in Rust. All blocks in Rust return the
last statement's return value (including functions, but also things like `if`
statements), and you can assign it.

See also a
[Python Rust cheat sheet](https://programming-idioms.org/cheatsheet/Python/Rust).

Rust makes everything const by default; you have to add `mut` to make something
mutable. It also makes everything private by default; you have to add `pub` if
you want to access it elsewhere.

### Syntactic macros

You might notice some functions in Rust have a `!` in them, such as:

```rust
println!("Hello world");
```

This are not normal functions, but syntactic macros. Functions in Rust cannot
take a variable number of arguments or optional arguments, but you can work
around this using macro functions. These are incredibly powerful - you can
process the tokens yourself and return the new code, and you can write them in
Rust! (There's also a simple inline syntax you can use for small macros.) You
can always tell them apart from normal functions by the `!` after the name.

These are not just function syntax, you also might notice them when making a
vector, which is a resizable homogeneous container:

```rust
let array = vec![1,2,3];
```

### Pattern matching

Both Python (3.10+) and Rust have pattern matching, though Rust has it deeply
baked in from a much earlier point in it's design. It's an integral part of how
error propagation works, how optional values are processed, how enums
(Union+enum in Python) are used, and more.

Pattern matching is broken into two categories; fallible and infallible
patterns. Infallible patterns have been around in Python for many years[^1], and
in many other languages, including C++. It looks like this:

[^1]:
    They actually can fail (throw an error) in Python, so the terminology is
    specific to statically typed languages.

```rust
let point = (1, 2);
let (x, y) = point;
```

The famous one line variable swap in Python is an infallible pattern match, and
works here too:

```rust
let (x, y) = (y, x);
```

For fallible pattern matching, you use a `match` statement, and if the pattern
match "fails", then the next match is attempted. In Rust, the patterns must
cover all cases.

For example, if you had a Coin enum, you could do:

```rust
let cost = match coin {
    Coin::Penny => 1,
    Coin::Nickel => 5,
    Coin::Dime => 10,
    Coin::Quarter => 25,
};
```

You can put `{}` blocks here if you want. This is is so common, there's even a
shortcut for a 1-2 branch match, called `if let`:

```rust
if let [x, y] = variable {
    println!("The values are {x}, {y}")
};
```

This will only define `x, y` and run the block if the pattern matches - that is,
if the variable is a two-item array. This is very common with the `Option` enum:

```rust
if let Some(val) = opt_val {
    println!("Got {val}");
} else {
    println!("Got nothing");
}
```

Also error handling, etc.

### Structs

Rust is careful to call it's data collection type a "struct", though it has many
similarities with classes from other libraries. The main reason they avoid the
object-oriented term is due to the fact that Rust's struct doesn't support
inheritance - the Trait system (later) replaces it. Defining a `struct` looks
like this:

```rust
struct Vector {
    x: f64,
    y: f64,
}
```

If you want to add methods, you do that in a `impl` block:

```rust
impl Vector {
    fn mag2(&self) -> f64 {
        self.x*self.x + self.y*self.y
    }
}
```

The special type `Self` is used for the first argument for normal methods, and
`&self` is short for `self: &Self`. We'll cover the `&` meaning later.

Often, however, you'll want traits instead of methods. We'll cover that in a
bit.

### Enums

Rust's enum is more than meets the eye - it's a combination of a classic Enum
and a Union (Python or C) / Variant (C++). The `Coin` enum above looks like
this:

```rust
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}
```

And the Optional enum (which is in the stdlib, don't write this yourself!) might
look like this:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

If we store a `Some`, we have a value too, not just the enum `Some`. We can
access it via fallable pattern matching as `Some(val)`. If you need to make a
vector that could hold a pre-known collection of types, you can use an Enum to
do that.

Enums can have methods and traits, just like a struct.

### Errors with Result

Another built-in enum is `Result`, which looks something like this:

```rust
enum Result<T,E> {
    Ok(T),
    Err(E),
}
```

This is how Rust does error handling; functions return `Result` or `Option`, and
the programmer must handle every error every time. The simplest way to handle
them, especially as a new programmer in Rust, is to call `.unwrap()`, which will
convert the Option or the Result into the `Some`/`Ok` value, or the program will
immediately quit. In "real" code, you should only do this is you know for a fact
it can't be `None`/`Err`.

### Iterators

Rust has functional style lazy iterators; this allows you to write some nice
high level code and should give you low level performance. Here's an example
that converts a sequence of letters into numbers:

```rust
let line = "pqr3stu8vwx";
let chars = line.chars().filter_map(|c| c.to_digit(10));
for c in chars {
    println!("Got {c}!");
}
```

This will convert the unicode string into a chars iterator, the apply the lambda
function to each char. The `.to_digit` call returns `Option`, which is `None` if
it's not a valid digit, which gets filtered out, so only `3` and `8` remain.
Here, `chars` is a lazy iterator; it hasn't computed anything yet. It only gets
processed when you iterator over it.

### Traits

One of the best things about Rust is the Traits system. They are similar to
Python Protocols, but explicitly opted in. They look quite a bit like methods,
and work like methods, too.

For example, we could define a `Magnitude` trait:

```rust
trait Magnitude {
    fn mag(&self) -> f64;
}
```

Then, we could implement our trait for `Vector`, defined previously:

```rust
impl Magnitude for Vector {
    fn mag(&self) -> f64 {
        self.mag2().sqrt()
    }
}
```

Now, we can call `.mag()` on a Vector, just as if we had a normal method. `.`
access looks up methods first, then it looks through all Traits defined for that
object's type (structs and enums work identically).

This should look like Python's Protocols; the main difference is that instead of
just treating any `mag` method specially, we only call ones that explicitly say
they were intended for `Magnitude`. You also will only look this up if
`Magnitude` is in scope; if you put it in a different scope, you can have
"opt-in" behaviors.

There are a lot of built-in traits. Here are a few with Python equivalents:

| Feature                   | Python method | Rust trait           |
| ------------------------- | ------------- | -------------------- |
| Stringification           | `__str__`     | `Display`/`ToString` |
| Programmer Representation | `__repr__`    | `Debug`              |
| Copy                      | `__copy__`    | `Clone` or `Copy`    |

More complex Protocols, like the ones in `collections.abc`, are there as well.
There are traits for mathematical operations, and much more.

Rust has an interesting rule for traits: Traits can only be implemented if you
"own" either the trait or the type. So you can add `Display` to your own types,
but you can't get a third-party library and add a `Display` to one of there
types, since you don't own the stdlib trait or the third party type. This means
you can't ever collide with multiple trait definitions by mistake when loading
two libraries.

Traits also have an interesting interaction with templating (generics in
Python).

### Templates

Templating looks like C++, but it actually also _enforces_ "concepts" from
C++20, which makes error messages fantastic in comparison. It's also tied to
traits. Here's an example. Let's try to write a templated function that takes
the magnitude of a vector as part of what it does.

```rust
fn double_mag<T>(vec: &T) -> f64 {
    vec.mag() * 2.0
}
```

This will _fail to compile_! You tried to call `.mag` on some arbitrary type,
and that's not supported. What you have to do is constrain T to only take types
that have implemented the `Magnitude` trait.

```rust
fn double_mag<T: Magnitude>(vec: &T) -> f64 {
    vec.mag() * 2.0
}
```

Now this works. Unlike C++ (unless you use concepts), the error message will be
simple and clear if you pass something that doesn't implement the `Magnitude`
trait. Note there are a couple of ways to write this, I've chosen the shortest
syntax, `T: Trait1 + Trait2 + ...`.

## Memory safety

### References

You might have been noticing the `&` popping up above. It's the const reference
operator, and is an important part of Rust's memory safety system. In Rust, this
is usually an error:

```rust
let x = SomeType{};
let y = x;
f(x);
```

Rust has the concept of ownership. In the first line, the object is owned by
`x`. In the second line, `y` receives ownership of the object, `x` is now
unusable. Then you try too use it in the function call, which causes the
compiler to stop. If you reversed the order of the last two lines, it would
still fail, as `x` has been consumed by the function `f`.

There is one exception: if `SomeType` implements the `Copy` trait, then it can
be copied instead of moved automatically. Only very small, simple types should
implement this. Integers, floats, and bools implement this, for example, which
helps keep those simple to use. But most types do not.

Most types do implement the `Clone` trait, which allows you to fix this by
explicitly making a copy, then consuming/moving that copy. For example, this is
fine:

```rust
let x = SomeType{};
let y = x.clone();
f(x);
```

However, often you don't want a copy, but you also don't want to take ownership.
You can do this with a const reference. This is like a pointer in C, or a
reference in C++; it can't be "null" (which is considered
[a billion dollar mistake](https://www.infoq.com/presentations/Null-References-The-Billion-Dollar-Mistake-Tony-Hoare/)),
and it must have a lifespan that outlives the reference (more on lifetimes
later). This is perfect for a function parameter that doesn't get stored
somewhere else.

Now our little example above can be written:

```rust
let x = SomeType{};
f(&x);
let y = &x;
```

(I've explicitly reversed the order for illustrative purposes, but both work).
Above, `x` must be destroyed after `y`, but it will be since they are in the
same scope. In fact, Rust's powerful tooling will ensure even references to
temporaries will live the correct amount of time, so `&(x+1)` is a valid
function argument.

The final reference type to cover here (we won't cover the various std library
structs to help with things like reference counting, but there are several) is a
mutable reference, `&mut`. Rust has a really interesting rule for mutable
references: You can have as many const references as you want, but only one
mutable reference, _and they can't overlap_. So you can take one `&mut`, or as
many `&` as you want, but not both.

You don't have to worry about cleaning up variables. Since Rust is a compiled
language, the compiler can check to see if a variable is used again, and the
last place it's used is it's lifespan. For example, this is valid:

```rust
let mut x = SomeType{};
change_value(&mut x);
change_value(&mut x);
f(&x);
```

The mutable reference on the second line only lives for that line, so it's okay
to take a mutable reference again. And since it doesn't live on, it's okay to
take a const reference in the last line.

Why have such a strict rule? It saves you from an entire class of really, really
hard to catch errors. For example, this famously horrible bug that's common in
C++ is invalid at compile time in Rust:

```rust
let mut vec = vec![1,2,3];
let slice = &vec[0..2];
vec.push(4);
println!("Hello, {slice:?}!");
```

This will fail to compile. Why? Because the method `.push` takes a mutable
reference to `self`. But `slice` is still alive, since it will be used in the
final line. This has just saved us from a whole class of really terrible, hard
to debug errors that occur in other languages, like C++! The reason this is bad
is because vectors store memory contiguously, and they reserve more than you
initially ask for. When you add a value, most of the time, they can just add it
to the pre-allocated memory, and everything is fine. But when you hit the end of
the pre-reserved size, they allocate new memory, and copy everything over to the
new place, deleting the old memory. So that static reference now points to
returned memory! This doesn't happen every time, so it's a really terrible bug
to track down. Rust simply doesn't allow you to write the bug in the first
place.

## Lifetimes

To help with ownership, Rust has lifetime tracking built in. For simple cases,
and for pre-existing functions, it is mostly transparent, but when you are
writing your own functions, you occasionally need to help it. Like most things,
the compiler can usually give you a helping hand, but knowing a bit about them
can help.

First, lifetimes can be given explicit names. `'a` is a lifetime named `a`, and
it is specified right after the `&` but before `mut` if present. One special
lifetime is `&'static`, which lasts for the duration of the program (useful for
things like strings). You can (and often do) use them in templates. For example:

```rust
fn first<'a>(x: &'a str, _: &str) -> &'a str {
    x
}
```

Here, the lifetime of the returned string is the lifetime of the first string
passed in (the second one doesn't matter, as it's not used). You wouldn't need
to name the lifetimes if you didn't have the second argument, since Rust has
lifetime elision rules for one lifetime in and one needed out.

Lifetimes are often used for structs, as well, to tie the input to the members.

## Slices

Rust has the concept of slices (seen earlier briefly), but there are a couple of
interesting features about them. First, the syntax is similar to Python, but
with `..` instead of `:`. Rust also has `..=` to indicate a slice where the
final item is also included. A fairly common idiom is `&x[..]`, which is a slice
covering the entire original object. You always take references to slices, they
aren't usable on their own.

A string slice is so important it has its own name: `str`. This is distinct from
the `String` type, which is a heap-storage string. And if you embed a string
into your program's source, you get a `&'static str` reference to it. Most
string functions take `&str`, rather than `&String` (for example), as it's much
more versatile and doesn't require a heap-stored string. While you could use
`&[..]` to convert a `String` into a `&str`, this is such a common occurrence
that Rust will perform an _implicit_ conversion for you - one of the few places
in the entire language where implicit conversions happen - even basic numbers
don't implicitly convert!

Vectors and arrays also have a slice type, such as `&[u32]` for a slice of a
unsigned integer array or vector. Again, this allows code to operate on a
sequence of values without worrying about the way it is stored.

Slices are one of the reasons Rust's string processing is so good. This was only
added to C++17 with `std::string_view` and C++20 with `std::span`, and it's
still much more likely to see `std::string` or vectors respectively as
parameters. (Rust also stores strings as a sequence of bytes with a length,
which is better than C's null terminated strings. Rust also carefully refuses to
do a lot of things that would be invalid for arbitrary unicode).

[rust book]: https://doc.rust-lang.org/book
