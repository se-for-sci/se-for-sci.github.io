# Making a Package

Now, let's change gears and look at creating our own packages. If you want to
make your code accessible to someone else to use via `pip` install, you need to
make it a package. In fact, as you'll see at the end of this section, even if
you just want to develop an application, it's much better to be working in a
package. I won't show you the internals of setting up a setuptools package, but
we'll just go over how you work with it and how it is distributed.

To install a local package, use:

```bash
pip install .
```

This will _copy_ the files into site-packages. If you want to actively develop a
module, use this instead (setuptools only, command varies on other tools):

```bash
pip install -e .
```

This uses symlink(s) so that you can edit the local files and immediately see
the changes (after restarting Python, as usual). If you want to produce an SDist
for distributing the source, use

```bash
pip install build
python -m build --sdist
```

If you want to produce a wheel for distributing, use

```bash
python -m build --wheel
```

You'll see old tutorials directly call `python setup.py ...`; if you can
possibly avoid doing that, please do! The `setup.py` file is still a good idea
for setuptools, but it's not even required there (and doesn't exist for any
other packaging software). (It's also quite valid to use pipx to install build,
but remember the command is `pyproject-build` if you do that).

## Distributions

### Wheel: fast and simple

A wheel is just a normal zipped file with the extension `.whl`. It contains
folders that get copied to specific locations, and a metadata folder.

It _does not_ contain `setup.py`/`setup.cfg`/`pyproject.toml`.

Why use wheels?

- Secure installs - arbitrary code does not run
- Fast installs - files are just copied inplace
- Reliable - does not depend on pretty much anything being on user's machine,
  including setuptools!
- Faster first imports - pip makes .pyc files when it installs
- Can be tagged for Python version, OS, and/or architecture (supports
  binaries!).

See <https://pythonwheels.com>

### SDist: Source distribution

This is a `.tar.gz` file holding the files needed to make a wheel. It is often a
subset of the files in the GitHub repo, though sometimes it contains generated
files, like `version.py` or maybe Cython/SWIG generated source files. If there
is no matching wheel (only for projects with binary components, in general),
then pip gets the SDist and builds/installs manually.
