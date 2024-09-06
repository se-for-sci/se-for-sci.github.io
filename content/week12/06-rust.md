# Extensions with Rust

Rust has enjoyed fantastic synergy with Python; it's one of the reasons Rust has
been doing so well in the Python extension module landscape. There are two key
projects: PyO3, which functions as a powerful pure Rust library for creating
extensions (very much like pybind11 for C++), and Maturin, a very simple modern
build system tied to Cargo (much like Scikit-build-core and CMake for
C/C++/Fortran languages).

## Getting started

Creating a new project is easy. Install maturin (`cargo install maturin`,
`brew install maturin`, `pipx install maturin`, etc). Then you can use the
maturin command line tool to quickly make a new project:

```console
$ maturin new rust_example
```

If you don't provide a binding mechanism to use, it will ask you. It will
default to a pure-Rust project; you can add flags to get a mixed Python and Rust
project instead (most more advanced projects will have at least some Python
parts). Check the flags with `--help/-h`.

Now, you should have a project like this:

```
rust_example
├── Cargo.toml
├── pyproject.toml
└── src
    └── lib.rs
```

Your `Cargo.toml` should look something like this:

```toml
[package]
name = "rust_example"
version = "0.1.0"
edition = "2021"

[lib]
name = "rust_example"
crate-type = ["cdylib"]

[dependencies]
pyo3 = {version = "0.21.1", features = ["abi3-py38"]}
```

The standard rust package stuff is at the top. The `lib` table has the library
name (this must match the module name), and the crate-type, which must include
`cdylib` to be importable in Python. If you want to access it from Rust too, you
can add to this list.

The line that might look a little different vs. the template is the
`dependencies`; we've ensured that we have a version of pyo3 new enough to use
the new `Bound`, and we are compiling for the Limited ABI - which will make our
compiles without needing Python (at least on Unix) and allow us to support all
versions of Python newer than some minimum with a single binary. The cost is a
few features will be disabled (less if the version is higher), and some
optimizations will be disabled.

The `pyproject.toml` file should look pretty normal:

```toml
[build-system]
requires = ["maturin>=1.5,<2.0"]
build-backend = "maturin"

[project]
name = "rust_example"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]
dynamic = ["version"]

[tool.maturin]
features = ["pyo3/extension-module"]
```

The main thing of note here is the `tool.maturin.features` field, which tells it
you have a PyO3 module. Otherwise, this is pretty similar to other build
backends. It it able to pull the version from the `Cargo.toml` file if you
include `"version"` in the `dynamic` list.

Finally, we have the library itself. Here's the simple template example,
`src/lib.rs`:

```rs
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_example(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
```

It starts with a `use` statement that pulls in the basics for using PyO3.

Then there's a docstring on a function (notice the triple slashes) - PyO3 will
actually be able to capture this for the Python docstring! You can't natively do
this in C++; you can write scripts that try to collect these, but Rust supports
it natively.

The function is annotated with `#[pyfunction]`, which will make it a function
you can add to Python. You return a `PyResult<...>` if a function could "throw"
an error in Python. Functions that don't ever throw errors can just return
normal Rust values that have known conversions. Otherwise, it's pretty normal.
(Actually, we don't ever return a non-OK value in this example, so feel free to
simplify this to just return `String`).

Now, we have a module. This is a function that sets up a module by taking a
Bound PyModule and running `.add_*` functions on it to add (much like pybind11).
Functions need to be given in the `wrap_pyfunction!` macro.

This is the classic interface; there's a new interface based on Rust inline
modules that is much nicer, as well. Here's the new interface, currently (0.21)
requires the `experimental-declarative-modules` (PyO3) feature:

```rs
/// A Python module implemented in Rust.
#[pymodule]
mod rust_example {
  use super::*;

  /// Formats the sum of two numbers as string.
  #[pyfunction]
  fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
      Ok((a + b).to_string())
  }
}
```

Our square example would look like this:

```rs
use pyo3::prelude::*;

#[pymodule]
mod rust_example {
  use super::*;

  #[pyfunction]
  fn square(a: usize, b: usize) -> usize {
      a + b
  }
}
```

## Building and running

You can use all the usual Python tools (like pip, build, etc), but you can also
build directly with maturin. In many cases, this will skip many of the Python
calls altogether. The `maturin build` command will build a wheel. The
`maturin develop` command will do an editable install (requires `pip` in the
venv you are building in).
