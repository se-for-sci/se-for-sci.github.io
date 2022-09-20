# WebAssembly

- [Pyodide](https://pyodide.org)
- [JupyterLite](https://jupyterlite.readthedocs.io/en/latest/)
- [PyScript](https://pyscript.net)

## Limitations

There is no terminal in WASM. You _do_ have a filesystem, though it is a
sandboxed one - you can't access arbitrary files on a users computer. There is
an opt-in experiment for chrome that loads a a directory with user permissions.
JuptyerLite keeps it's directory in your browser's cache, so it is persistent.

Sync IO does not work in WASM. This includes `time.sleep`, which just returns
instantly. Use `await ascyncio.sleep` instead.

Threading is not available (yet?), including `multiprocessing`, `threading`, and
`sockets`. Use async programming instead.

Libraries that draw to the screen (`tkinter`, `turtle`, the `idle` app) or are
highly integrated with the console (`curses`) are not available. Use HTML or
javascript instead. `venv` and `ensurepip` are not available, use `micropip`
instead.

Furthermore, I've found debugging in JupyterLite to not work very well (or at
all?), and importing files from the local filesystem may require a little more
setup than you are used to.

## Installing packages

Since there's no terminal, you need to use the micropip library to install
packages. Use it like this, for example to install `rich`:

```python
import micropip

await micropip.install("rich")
```

You can install anything that has a pure Python wheel, and has either pure
Python wheel dependencies or dependencies already compiled into the Pyodide
distribution. Binary packages have to be compiled into Pyodide or compiled
separately into WASM and provided by URL - binaries are not get backward
compatible enough to be proposed and added to PyPI.

Pyodide compiles many of the most popular data science libraries, like NumPy,
Pandas, and more. It even has a patched version of matplotlib.
