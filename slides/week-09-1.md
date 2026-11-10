---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Python Bindings

---

## What are bindings?

Bindings let Python call code in a compiled library.

- Reuse existing C, C++, Fortran, or Rust libraries
- Speed up a hot loop
- Give a compiled library a friendly Python interface

Our example for today:

```c
float square(float x) {
    return x*x;
}
```

---

## Options

| Tool        | Languages     | Notes                              |
| ----------- | ------------- | ---------------------------------- |
| ctypes      | C interface   | Built into Python, no compile step |
| CFFI        | C interface   | Reads C declarations               |
| CPython API | C             | What Python itself uses            |
| pybind11    | C++11+        | Header only, very popular          |
| nanobind    | C++17+        | Smaller, faster pybind11 core      |
| PyO3        | Rust          | Uses maturin to build              |
| Cython      | Python-like   | Its own language                   |

---

## Shared objects

Compile to a shared library (`.so`, `.dylib`, or `.dll`):

```bash
gcc -shared -o simple.so simple.c
```

- A shared library holds symbols (names) and machine code
- It does **not** store function signatures
- So the caller must supply the types

---

## ctypes

```python
import ctypes

lib = ctypes.cdll.LoadLibrary("./simple.so")

lib.square.argtypes = (ctypes.c_float,)
lib.square.restype = ctypes.c_float

lib.square(2.5)  # 6.25
```

- No dependencies, part of the standard library
- You can load a library only once per process (like imports)
- Wrap the library in a class to hide these details

---

## C++ and name mangling

C++ mangles symbol names (overloads, templates, namespaces). Use `extern "C"` to export plain C names:

```cpp
template<class T>
T square(T x) { return x*x; }

extern "C" {
    int square_int(int x) { return square<int>(x); }
    double square_double(double x) { return square<double>(x); }
}
```

This is not Python specific. Any language that loads a shared library needs a C interface.

---

## CFFI

```python
from cffi import FFI

ffi = FFI()
ffi.cdef("float square(float);")
C = ffi.dlopen("./simple.so")

C.square(2.0)
```

- You give a C declaration, not ctypes types
- Made for PyPy, works in CPython too
- NumPy has `numpy.ctypeslib` for arrays with ctypes
- Numba can call ctypes and CFFI functions

---

## CPython API: the wrapper

All Python objects are `PyObject*`:

```c
#include <Python.h>

static PyObject* square_wrapper(PyObject* self, PyObject* args) {
    float input;
    if (!PyArg_ParseTuple(args, "f", &input))
        return NULL;
    return PyFloat_FromDouble(square(input));
}
```

`PyArg_ParseTuple` converts the arguments to C types, `PyFloat_FromDouble` converts the result back. Return `NULL` for an error.

---

## CPython API: the module

```c
static PyMethodDef pysimple_methods[] = {
    {"square", square_wrapper, METH_VARARGS, "Square function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pysimple_module = {
    PyModuleDef_HEAD_INIT, "pysimple", NULL, -1, pysimple_methods
};

PyMODINIT_FUNC PyInit_pysimple(void) {
    return PyModule_Create(&pysimple_module);
}
```

The symbol name `PyInit_<name>` must match the module name.

---

## Build with CMake

Do not compile extensions by hand. Use a build system:

```cmake
cmake_minimum_required(VERSION 3.26...4.4)
project(pysimple LANGUAGES C)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
python_add_library(pysimple MODULE pysimple.c WITH_SOABI)
```

- `WITH_SOABI` adds the suffix, like `.cpython-314-darwin.so`
- In a package, a build backend (scikit-build-core) runs CMake

---

## Limited API and stable ABI

Normal extensions work with one Python version. The limited API gives one binary for many versions (abi3).

- Define `Py_LIMITED_API` to the minimum version (like `0x030B0000`)
- CMake: `Development.SABIModule` and `USE_SABI 3.11`
- Only use functions in the limited API
- abi3t (PEP 803): stable ABI for free-threaded and normal Python 3.15+

Support: nanobind, PyO3, Cython 3.1+, SWIG 4.2+; pybind11 in progress.

---

## pybind11

```cpp
#include <pybind11/pybind11.h>

namespace py = pybind11;

float square(float x) { return x*x; }

PYBIND11_MODULE(pysimple, m) {
    m.def("square", &square);
}
```

- Header only C++11, no new language, no code generation
- Types are found from the C++ signature
- Used by SciPy, PyTorch, boost-histogram, and many more

---

## Overloads and classes

```cpp
PYBIND11_MODULE(pytempl, m) {
    m.def("square", [](int value){ return square(value); });
    m.def("square", [](double value){ return square(value); });
}
```

```cpp
PYBIND11_MODULE(pybindclass, m) {
    py::class_<Simple>(m, "Simple")
        .def(py::init<int>())
        .def("get", &Simple::get);
}
```

pybind11 tries each overload in order until one matches.

---

## More pybind11 features

```cpp
py::class_<Vector2D>(m, "Vector2D")
    .def(py::init<double, double>(), "x"_a, "y"_a)
    .def_property("x", &Vector2D::get_x, &Vector2D::set_x)
    .def(py::self + py::self)
    .def("__repr__", [](py::object self){
        return py::str("{0.__class__.__name__}({0.x})").format(self);
    });
```

- `"x"_a` gives argument names (and defaults with `= value`)
- `def_property` makes a Python property
- `py::self` binds operators
- `py::str`, `py::object`, and more wrap Python types

---

## Example: Minuit2

Bind a real C++ library in steps:

1. Get the source (CMake `FetchContent`)
2. Plan the interface: what does the C++ look like? What should the Python look like?
3. Bind only the parts you need
4. Build a wheel with scikit-build-core

---

## Trampoline classes

To subclass a C++ class in Python, give a "trampoline":

```cpp
class PyFCNBase : public FCNBase {
  public:
    using FCNBase::FCNBase;

    double Up() const override {
        PYBIND11_OVERRIDE_PURE(double, FCNBase, Up, );
    }
};

py::class_<FCNBase, PyFCNBase>(m, "FCNBase")
    .def(py::init<>())
    .def("Up", &FCNBase::Up);
```

---

## Overloaded methods

Select one overload with `py::overload_cast` (C++14):

```cpp
py::class_<MnUserParameters>(m, "MnUserParameters")
    .def(py::init<>())
    .def("Add", py::overload_cast<const std::string &, double>(
                    &MnUserParameters::Add))
    .def("Add", py::overload_cast<const std::string &, double, double>(
                    &MnUserParameters::Add));
```

Put each part of a large module in its own file, with an `init_*` function called from the module file. This keeps compile times low.

---

## Packaging

```cmake
find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module(minuit2 ${SOURCES})
target_link_libraries(minuit2 PUBLIC Minuit2::Minuit2)
install(TARGETS minuit2 DESTINATION .)
```

```toml
[build-system]
requires = ["scikit-build-core>=0.11", "pybind11>=3"]
build-backend = "scikit_build_core.build"
```

Now `pip wheel .` or `uv build` makes a wheel.

---

## Rust: PyO3 and maturin

```rs
use pyo3::prelude::*;

#[pymodule]
mod rust_example {
    use pyo3::prelude::*;

    /// Square a number
    #[pyfunction]
    fn square(a: usize) -> usize { a * a }
}
```

PyO3 is the binding library (like pybind11). `///` doc comments become Python docstrings.

---

## Rust: project files

```toml
# Cargo.toml
[lib]
name = "rust_example"
crate-type = ["cdylib"]

[dependencies]
pyo3 = {version = "0.30.1", features = ["abi3-py311"]}
```

```toml
# pyproject.toml
[build-system]
requires = ["maturin>=1.16,<2.0"]
build-backend = "maturin"
```

Start with `maturin new`; use `maturin develop` for an editable install.

---

## Summary

- ctypes / CFFI: call a C interface, no compile step for bindings
- CPython API: shows how extensions work; verbose
- pybind11 / nanobind: the natural choice for C++
- PyO3 + maturin: the natural choice for Rust
- Always use a build backend (scikit-build-core, meson-python, maturin)
