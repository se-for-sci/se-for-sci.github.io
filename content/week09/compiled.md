# Intro to compiled languages (Rust)

For the classic approach, please use the jupyter notebook in this directory to
follow the lecture notes. This is a complete rewrite using Rust.

## Intro to compiled languages

So far, we've used interpreted languages. These work by distributing a compiled "interpreter", a program that runs some set of instructions that is given to it "at runtime", that is, well after the program was compiled. These are easy to run, but they tend to have some drawbacks:

- They tend to be (much) slower due to taking general input.
- They require an interpreter on the target machine.
- They generally require a lot of setup (packaging) to ensure all the libraries can be found. (Similar things are true if you use dynamic linking on a compiled language)
- Interpreters take time to start up and load std libraries (40 ms or so for Python).

These drawbacks may often be fine - for example, if you are limited by IO speed, using a compiled language won't be much faster. Use the best tool for the job!

## What language?

There are several good choices for a compiled language. A quick summary:

- **Fortran**: The classic numerics language. Poor support from modern compilers.
- **C**: The classic compiled "systems" language. Simple, but provides very little to make safe designs.
- **C++**: Much more powerful design possibilities compared to C. But all the old unsafe stuff is still there too. Higher level than C.

All three of these are older than modern packaging, so using them is quite tricky. Modern languages take packaging seriously; a few of those are:

- **Go**: Google tool "all the best stuff" from previous languages and made a solid language. Has a garbage collector.
- **Rust**: A "memory-safe" language _without_ a garbage collector. Used in Linux/Windows kernels, but as powerful as (very modern) C++ in many of it's concepts, without the old ways of doing things.

Of these, the most interesting language is currently Rust - it's "systems" design means you can use it everywhere (unlike Go, which is only for applications).

## Step 1: Getting the compiler

Just like downloading the interpreter in an interpreted language, compiled languages require you to download a compiler. Unlike interpreted languages, however, only the developer needs the download. You can probably get the Rust compilers directly; however,
most developers prefer `rustup`, which is a tool that gets Rust compilers for you, allowing you to control the version.

Brew users can `brew install rustup` and then follow the instructions to get the latest version, or just `brew install rust` and accept whatever version was given. The main tool that you get with `rust` besides the compiler (`rustc`) is `cargo`, it's package manager.

## Step 1.5: Try compiling a little file

Let's just make sure we can compile code, and see how a compiler works. Make the following `example.rs` file:

```rust
fn main() {
    println!("Hello world!");
}
```

Now, compile it with `rustc`:

```console
$ rustc example.rs
```

And run it:

```console
$ ./example
Hello world!
```

We skipped one step you often see: linking. You can build library code with making an executable; then you can either statically link (final binary has everything) or dynamically link (the library is still required at runtime) the code. Your build system (CMake for classic languages, Cargo for rust) will generally handle setting this up.

Modern languages like Go and Rust highly prefer static linking by default. Binary size isn't as important as it used to be, and having everything in a single binary makes it much easier to work with and distribute. They also strongly prioritize building all dependencies from source, which is important for cross-compiling and optimizations. Older languages tended to prioritize making source easy to keep from users.

## Step 2: Start a new project

Now that you've seen the compiler, let's try the package-based approach. Use the following command to make a new project with Cargo:

```console
$ cargo new foo
```

This will make a new directory `/foo` with a binary package named `foo`. (You can pass `--lib` if you are making a library.) You can add `--vcs git` if you want it to also set up git for you (due to the way cargo works, you'll have a `.gitignore` regardless).

This makes just three files: `.gitignore` with the `/target` directory ignored, a simple `src/main.rs` hello world application, and creates the `Cargo.toml` configuration file. That's the new one we want to look at; it's contents should look about like this:

```toml
[package]
name = "foo"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
```

This has a `package.name`, `package.version` (which is now optional in Rust 1.75+!), and a `package.edition`, which tells Rust that you are
writing in the 2021 dialect of Rust. Unlike most other languages, you can mix
and match libraries in different editions.

Nothing else is required, and you now have a working package!

## Step 3: Build and run your project

You should interact with your project via `cargo` commands. You can try building and running your project:

```console
$ cargo run
   Compiling foo v0.1.0 (~/tmp/foo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.56s
     Running `target/debug/foo`
Hello, world!
```

This will build in debug mode if it's not already built. A couple of common options are `--bin <name>` if you have more than one binary and `--release` for release mode. As always, use `--help` or `-h` to see what you can run.

The file will end up in `./target/debug/foo` if you want to run the binary directly.

## Step 4: Add tests

Now let's start adding all the things we learned how to do in Python. First, let's tackle unit tests. Try adding the following to the bottom of `src/main.rs`:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_42() {
        assert_eq!(42, 42);
    }
}
```

There are several new Rust features shown here, so let's walk through it:

- `#[...]` is an ["inner attribute"](https://doc.rust-lang.org/reference/attributes.html) - that means it's an attribute on the next item. `cfg(...)` is [an attribute](https://doc.rust-lang.org/reference/conditional-compilation.html#the-cfg-attribute) that enables or disables an item based on what's inside the parens. in this case, `#[cfg(test)]` will only compile `mod tests` if building tests.
- We put the tests in a module. That's really mostly so we can apply an attribute to the module to conditionally compile it. We name it "tests" because that's a good name for tests.
- Unlike some languages, you don't get the outer scope for free in an inner scope, so we explicitly `use super::*` to get all the private goodies in the outer scope. Pretend we had something in the outer scope we wanted to test, of course.
- Then we add a `test` attribute to next item (in this case, a function). Rust will then be able to find and run this tests for us.
- Finally, we have an `assert_eq!` macro. It will pass/fail based on if both items are equal, and it will be able to capture the values for nice printout on failure.

Notice that we write the unit tests in the file that contains the code. This will allow the unit tests to test private parts of the code that are not available outside this file.

Now, try running the tests:

```console
$ cargo test
   Compiling foo v0.1.0 (~/tmp/foo)
warning: unused import: `super::*`
 --> src/main.rs:7:9
  |
7 |     use super::*;
  |         ^^^^^^^^
  |
  = note: `#[warn(unused_imports)]` on by default

warning: `foo` (bin "foo" test) generated 1 warning (run `cargo fix --bin "foo" --tests` to apply 1 suggestion)
    Finished test [unoptimized + debuginfo] target(s) in 0.38s
     Running unittests src/main.rs (target/debug/deps/foo-f51fd73e2da0c0ec)

running 1 test
test tests::test_42 ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Notice that we got a warning about our `super` being unused. We even got a recipe to fix it automatically! Let's not worry about that for now. We want to see this again from the linter in the next step!

## Step 5: Format the code

Let's go ahead and format this, similar to `black` or `ruff fmt` from Python:

```console
$ cargo fmt
```

Unless we've been sloppy, it likely won't do much, but now we know how to format our source files!

## Step 6: Static checks

Now let's try adding linting checks. We already get type checking whenever we compile, but let's add helpful optional checks. We can run:

```console
$ ruff clippy --all-targets
    Checking foo v0.1.0 (~/tmp/foo)
warning: unused import: `super::*`
 --> src/main.rs:7:9
  |
7 |     use super::*;
  |         ^^^^^^^^
  |
  = note: `#[warn(unused_imports)]` on by default

warning: `foo` (bin "foo" test) generated 1 warning (run `cargo clippy --fix --bin "foo" --tests` to apply 1 suggestion)
    Finished dev [unoptimized + debuginfo] target(s) in 0.08s
```

> Note: you might not have `cargo-clippy` if you installed Rust minimally. See https://doc.rust-lang.org/stable/clippy/installation.html for info if so.

This will run the checker (clippy) on all targets (including the test target). However, not much is enabled by default. Add the following to your `Cargo.toml`:

```toml
[lints.clippy]
all = "warn"
pedantic = "warn"
nursery = "warn"
```

This will enable "all" lints, "pedantic" lints, and "nursery" lints, which will provide a lot more help for a young (at heart) Rustacean.

Some lints can be fixed automatically with `cargo clippy --fix`.

## Step 7: Adding dependencies

One key feature of Rust is how easy it is to add dependencies. This is usually something that is very challenging for older languages. Because of how easy it is, Rust doesn't encourage a massive standard library; things like regex are relegated to dependencies. Even the Rust AST parser is a dependency. Let's try adding a fun dependency: [`strum`](https://docs.rs/strum/latest/strum/), a string enum package. We want to use it's "derive" feature too, so we'll request that.

You can add it with a command:

```console
$ cargo add strum --features derive
    Updating crates.io index
      Adding strum v0.26.1 to dependencies.
             Features:
             + std
             + derive
             + strum_macros
             - phf
    Updating crates.io index
```

Though, to be fair, all it did is add:

```toml
[dependencies]
strum = {version="0.26.1", features=["derive"]}
```

which you could have done yourself. In fact, I'd recommend loosening the pin; cargo has a lock file (`Cargo.lock`) already. Building or running `cargo update` will update the local files from your `Cargo.toml`/`Cargo.lock`.

> Aside: features
>
> Rust allows dependencies to provide optional components, called "features", with additional dependencies and compiled parts. Unlike Python, features can also be enabled by default. Many packages have a default enabled "std" feature that you can disable to not require Rust's standard library, for use in embedded systems without memory management and other OS-level things.

Now, let's use our new dependency:

```rust
use std::string::ToString;

#[derive(Debug, PartialEq, strum::EnumString, strum::Display)]
enum Card {
    World,
    Planet,
}

fn main() {
    let world = Card::World.to_string();
    println!("Hello, {world}!");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_world() {
        let world: Card = "world".try_into().unwrap();
        assert_eq!(Card::World, world);
    }
}
```

Here, we bring the `ToString` trait into scope so that we can use it (more on traits later). Then, we make a new enum. We add `derive` attributes, which inject code for us. We derive:

- `Debug`, which is like `__repr__` in Python and is used in the `assert_eq!` to print out the enum if the comparison fails
- `PartialEq`, which allows us to compare (in `assert_eq!`)
- `strum::EnumString`, which allows us to convert strings into our enum
- `strum::Display`, which allows us to convert our enum into strings

Then we make our enum, which has two variants, `World` and `Planet`. Strum will use these as the conversions to and from strings, though we could customize this with the `#[strum(...)]` attribute if we wanted to.

Then we use conversion to a string in `main`, and from a string in the tests.

Try `cargo r` (short for `cargo run`) and `cargo t` (short for `cargo test`) and make sure it's working!

Notice that Cargo downloaded and compiled your dependencies for you. Also notice that you now have a `Cargo.lock` with the exact known working versions of everything.
