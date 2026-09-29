# Using packages

Packaging is absolutely critical as soon as you:

- Work on more than one thing
- Share your work with anyone (even if not as a package)
- Work in more than one place
- Upgrade or change anything on your computer

Unfortunately, packaging has a _lot_ of historical cruft, bad practices that
have easy solutions today but are still propagated.

We will split our focus into two situations, then pull both ideas together.

## Installing a package

You will see two _very_ common recommendations:

```bash
pip install <package>         # Use only in virtual environment!
pip install --user <package>  # Almost never use
```

Don't use them unless you know exactly what you are doing! The first one will
try to install globally, and if you don't have permission, will install to your
user site packages. In global site packages, you can get conflicting versions
of libraries, you can't tell what you've installed for what, it's a mess. And
user site packages are worse, because all installs of Python on your computer
share it, so you might override and break things you didn't intend to.

The solution depends on what you are doing:

### Safe libraries

There are likely a _few_ libraries (possibly one) that you just have to install
globally. Go ahead, but be careful (and always use your system package manager
instead if you can, like [`brew` on macOS](https://brew.sh) or the Windows
ones - Linux package managers tend to be too old to use for Python libraries).

Ideas for safe libraries: the other libraries you see listed in this lesson!
It's likely better than bootstrapping them. In fact, you can get away with just
one: uv.

### uv tool / pipx: pip for executables!

If you are installing an "application", that is, it has a script end-point and
you don't expect to import it, _do not use pip/`uv pip`_; use `uv tool` or
[pipx](https://pypa.github.io/pipx/). It will isolate it in a virtual
environment, but hide all that for you, and then you'll just have an application
you can use with no global/user side effects!

`````{tab-set}
````{tab-item} uv
```bash
uv tool install black
black myfile.py
```
````
````{tab-item} pipx
```bash
pipx install black
black myfile.py
```
````
`````

Now you have "black", but nothing has changed in your global site packages! You
cannot import black or any of its dependencies! There are no conflicting
requirements (pip 20.3+ refuses to install two packages that have incompatible
requirements).

#### Directly running applications

uv and pipx also have a very powerful feature: you can install and run an
application in a temporary environment!

For example, this works just as well as the lines above:

`````{tab-set}
````{tab-item} uv
```bash
uvx black myfile.py
```
````
````{tab-item} pipx
```bash
pipx run black myfile.py
```
````
`````

The first time you do this, pipx creates a venv and puts black in it, then runs
it. If you run it again, it will reuse the cached environment if it hasn't been
cleaned up yet, so it's fast.

Another example (`uv build` is a built-in command, `pipx run` is using the
package named `build`):

`````{tab-set}
````{tab-item} uv
```bash
uv build
```
````
````{tab-item} pipx
```bash
pipx run build
```
````
`````

> This is great for CI! Pipx is installed by default in GitHub Actions (GHA);
> you do not need `actions/setup-python` to run it. There's an easy action to
> set up uv, as well.

If the command and the package have different names, then you may have to write
this with a `--from` (`--spec` with pipx), though pipx (only) has a way to
customize this, and it will try to guess if there's only one command in the
package. You can also pin exactly, specify extras, etc:

`````{tab-set}
````{tab-item} uv
```bash
uvx --from cibuildwheel==2.9.0 cibuildwheel --platform linux
```
````
````{tab-item} pipx
```bash
pipx run --spec cibuildwheel==2.9.0 cibuildwheel --platform linux
```
````
`````

#### Self-contained scripts

You can now make a self-contained script; that is, one that describes its own
requirements. You could make a `print_blue.py` file that looks like this:

```python
# /// script
# dependencies = ["rich"]
# requires-python = ">=3.11"
# ///

import rich

rich.print("[blue]This worked!")
```

Then run it with almost any tool that understands this:

```bash
pipx run ./print_blue.py
uv run ./print_blue.py
hatch run ./print_blue.py
```

These will make an environment with the specifications you give and run it for
you.

### Environment tools

There are other tools we are about to talk about, like `virtualenv`, `poetry`,
`pipenv`, `nox`, `tox`, etc. that you could also install with `pip` (or better
yet, with `pipx`), and are _not too_ likely to interfere or break down if you
use `pip`. But keep it to a minimum or use `pipx`.

### Nox and Tox

You can also use a task runner tool like `nox` or `tox`. These create and manage
virtual environment for each task (called sessions in `nox`). This is a very
simple way to avoid making and entering an environment, and is great for less
common tasks, like scripts and docs.

### Python launcher

The Python launcher for Unix (a Rust port of the one bundled with Python on
Windows by a Python core developer) supports virtual environments in a `.venv`
folder. So if you make a virtual environment with `python -m venv .venv` or
`virtualenv .venv`, then you can just run `py <stuff>` instead of
`python <stuff>` and it uses the virtual environment for you. This feature has
not been back-ported to the Windows version yet.

## Environments

There are several environment systems available for Python, and they generally
come in two categories. The Python Packaging Authority supports PyPI (Python
Package Index), and all the systems except one build on this (usually by pip
somewhere). The lone exception is Conda, which has a completely separate set of
packages (often but not always with matching names).

### Environment specification

All systems have an environment specification, something like this:

```text
requests
rich >=9.8
```

This is technically a valid `requirements.txt` file. If you wanted to use it,
you would do:

`````{tab-set}
````{tab-item} uv
```bash
uv venv
. .venv/bin/activate
uv pip install -r requirements.txt
```
````
````{tab-item} pip
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
````
`````

Use `deactivate` to "leave" the virtual environment.

These two tools (venv to isolate a virtual environment) and the requirements
file let you set up non-interacting places to work for each project, and you can
set up again anywhere.

### Locking an environment

But now you want to share your environment with someone else. But let's say
`rich` updated and now something doesn't work. You have a working environment
(until you update), but your friend does not, theirs installed broken (this just
happened to me with `IPython` and `jedi`, by the way). How do you recover a
working version without going back to your computer? With a lock file! This
would look something like this:

```text
requests ==2.25.1
rich ==9.8.0
typing-extensions ==3.7.4
...
```

This file lists all installed packages with exact versions, so now you can
restore your environment if you need to. However, managing these by hand is not
ideal and easy to forget. If you like this, `pipenv`, which was taken over by
`PyPA` has a `Pipfile` and a `Pipfile.lock` which do exactly this, and combines
the features of a virtual environment and pip. You can look into it off-line,
but we are moving on. We'll encounter this idea again.

### Dev environments or Extras

Some environment tools have the idea of a "dev" environment, or optional
components to the environment that you can ask for. Look for them wherever fine
environments are made.

When you install a package via pip or any of the (non-locked) methods, you can
also ask for "extras", though you have to know about them beforehand. For
example, `pip install rich[jupyter]` will add some extra requirements for
interacting with notebooks. _These add requirements only_, you can't change the
package with an extra.

### Dependency-groups

You can also use dependency groups, which are a way to specify optional
dependencies in `pyproject.toml`. This is a new feature, but most recent
versions of most tools support it. It looks like this:

```toml
[dependency-groups]
dev = ["pytest"]
```

You can install it with `--group dev`. The high-level interface to uv
automatically installs the `dev` group, so using this makes `uv run` work out of
the box.

### Conda environments

If you use Conda, the environment file is called `environment.yml`. The one we
are using can be seen here:

```{literalinclude} ../../environment.yml
:language: yaml
```

You can specify pip dependencies, too:

```yaml
- pip:
    - i_couldnt_think_of_a_library_missing_from_conda
```

## High level interface

In practice, you don't need to do manual environment manipulation if you have a
tool supporting a high level interface (uv or pixi, also hatch, poetry, and
pdm).

### uv

In order to use uv's high level interface, run:

```console
uv run <command>
```

That will:

- Create a `.venv` folder with a virtual environment if not present already
- Install the project's dependencies
- Install the project itself in editable mode, if it has a build backend
- Install the `dev` dependency group if it exists
- Everything installed will come from the locked versions in the lockfile if it
  exists, otherwise one will be created.

The `<command>` can be anything; `uv run python`, `uv run pytest`, etc.

While there are some custom configuration options for uv, it works out of the
box with a standard `pyproject.toml`, so you don't need uv specific
configuration to support uv's high level mode.

### pixi

Pixi only has a high level interface, and it needs a manifest (`pixi.toml` or
`[tool.pixi]` in `pyproject.toml`). It can install both conda and PyPI packages.
There is also a task system in pixi.

For an example, you can see the one in this repo:

```{literalinclude} ../../pixi.toml
:language: toml
```

The platforms you want to lock for and conda channels you want to use are listed
in `workspace`. You have a set of dependencies (the `environment.yml` file above
lists the same dependencies, by the way). Then you can also make a list of
tasks. When you do `pixi run <command>`, if the command is listed in the tasks,
that will get run instead. So `pixi run lab` starts up JupyterLab, for example.
