# Using packages

Packaging is absolutely critical as soon as you:

- Work on more than one thing
- Share your work with anyone (even if not as a package)
- Work in more than one place
- Upgrade or change anything on your computer

Unfortunately, packing has a _lot_ of historical cruft, bad practices that have
easy solutions today but are still propagated.

We will split our focus into two situations, then pull both ideas together.

## Installing a package

You will see two _very_ common recommendations:

```bash
pip install <package>         # Use only in virtual environment!
pip install --user <package>  # Almost never use
```

Don't use them unless you know exactly what you are doing! The first one will
try to install globally, and if you don't have permission, will install to your
user site packages (as of a recent pip update). In global site packages, you can
get conflicting versions of libraries, you can't tell what you've installed for
what, it's a mess. And user site packages are worse, because all installs of
Python on your computer share it, so you might override and break things you
didn't intend to.

The solution depends on what you are doing:

### Safe libraries

There are likely a _few_ libraries (possibly one) that you just have to install
globally. Go ahead, but be careful (and always use your system package manager
instead if you can, like [`brew` on macOS](https://brew.sh) or the Windows
ones - Linux package managers tend to be too old to use for Python libraries).

Ideas for safe libraries: the other libraries you see listed in this lesson!
It's likely better than bootstrapping them. In fact, you can get away with just
one:

### pipx: pip for executables!

If you are installing an "application", that is, it has a script end-point and
you don't expect to import it, _do not use pip_; use
[pipx](https://pypa.github.io/pipx/). It will isolate it in a virtual
environment, but hide all that for you, and then you'll just have an application
you can use with no global/user side effects!

```bash
pip install pipx  # Easier to install like this

pipx install black
black myfile.py
```

Now you have "black", but nothing has changed in your global site packages! You
cannot import black or any of it's dependencies! There are no conflicting
requirements (more common in pip 20.3+, which now will refuse to install two
packages that have incompatible requirements).

#### Directly running applications

Pipx also has a very powerful feature: you can install and run an application in
a temporary environment!

For example, this works just as well as the second two lines above:

```bash
pipx run black myfile.py
```

The first time you do this, pipx create a venv and puts black in it, then runs
it. If you run it again, it will reuse the cached environment if it hasn't been
cleaned up yet, so it's fast.

Another example:

```bash
pipx run build
```

> This is great for CI! Pipx is installed by default in GitHub Actions (GHA);
> you do not need `actions/setup-python` to run it.

If the command and the package have different names, then you may have to write
this with a `--spec`, though pipx has a way to customize this, and it will try
to guess if there's only one command in the package. You can also pin exactly,
specify extras, etc:

```bash
pipx run --spec cibuildwheel==2.9.0 cibuildwheel --platform linux
```

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

```
requests
rich >=9.8
```

This is technically a valid `requirements.txt` file. If you wanted to use it,
you would do:

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

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

```
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

### Conda environments

If you use Conda, the environment file is called `environment.yaml`. The one we
are using can be seen here:

```{literalinclude} ../../environment.yml
:language: yaml
```

You can specify pip dependencies, too:

```yaml
- pip:
    - i_couldnt_think_of_a_library_missing_from_conda
```
