# Python Setup

The first choice you have to face setting up Python is which distribution you
want: official packaging using PyPA tools (like pip), or the conda Python and
packages. Both options will be outlined below.

## PyPA packaging

To use the standard tools, you can get Python from anywhere (except Conda, see
below). Official Python installers are available for macOS and Windows.

On macOS, you can use homebrew, as well; this is especially useful if you are
already using it to manage everything else on your system.

On Windows, typing `python` will open the Windows store if it's not installed.
You can also use `winget install Python`, Window's official package manager on
recent versions, to get Python from the Windows store.

For Linux, if you use your system Python, make sure it is new enough, and never
modify the base environment except though your package manager (generally true,
but more so here). The system Python is really intended for use in other system
packages, and is not intended for you to modify. Modern pip and modern systems
now work together to provide safegaurds for this.

### Virtual environments

Once you get a Python, how do you install packages safely? Installing or
especially upgrading (which can happen when installing) packages can break your
system Python. There is also a user location for installs, but this is also bad,
as it's not possible to set up more than one, and it can still break things
since it's always included. The proper solution is using virtual environments. A
virtual environment is a complete collection of all your packages and a symlink
to the system Python.

There are several tools that make virtual environments; the slowest one is built
right into Python. You can make a virtual environment like this:

```bash
python3 -m venv .venv
```

This runs your system Python, runs the CLI provided by the `venv` module, which
takes the path to the virtual environment as an argument. Unless you need more
than one, your virtual environment should be at the root of your project with
the name `.venv`. Never check it into git; it should be listed in your
`.gitignore`. If you have the third-party package `virtualenv`, it's just faster
and the pre-installed pip is updated more regularly than the Python standard
library allows - it has the same interface).

(Notice I didn't mention `python3 -m ensurepip`? That's because you don't need
it with a virtualenv, the virtualenv will come with pip installed, even if it's
not on your system. In fact, it's not a bad idea to not have a system pip at
all, so you can't accidentally modify the system environment)

(Feel free to look at the virtual environment directory! It has a `pyvenv.cfg`,
which is the key part that tells Python you are in an isolated virtual
environment, and otherwise looks a bit like a mini unix system layout, with
`/bin` (`\scripts` on Windows), `lib/python3.x/site-packages`, etc.)

To use the virtual environment, either use the full path (like
`.venv/bin/python`), or "activate" it, using the appropriate script for your
shell inside `.venv/bin`. If you activate it, it will add a function
`deactivate` that you can run to undo everything activation does.

### Locking environments

When making a virtual env, it's a good idea to record the packages you want to
install so that you can recreate the environment easily. This list is often
called `requirements.txt` (not needed for creating a package, though, which we
will cover later).

A very powerful technique is to call this generic list `requirements.in`
instead, and use something like `pip-compile` from `pip-tools` to generate a
`requirements.txt` from this file with all the versions pinned. This way, you
can easily create exactly the same environment on another machine or later, and
you can also easily update by recreating the `requirements.txt` file.

### Pipx

Virtual environments work great for projects, but what about applications that
you find on PyPI that you want to use? There's a simple solution for this: pipx,
which is pip's counterpart for "executables". When you run
`pipx install <package>`, pipx will create a managed virtual environment for
just that application, and only expose it's applications on the command line. So
`pipx install twine` will allow you to run `twine` anywhere, but you will not be
able to `import twine`, since it really lives in it's own virtual environment.

Even better, `pip run <app>` will combine the two steps of installing and
running an application into one command; pipx will install the app into a
temporary virtual environment (reused if you rerun the same command less than a
week later), and then run it. With `pipx run`, you never have to think about
what is installed on the machine you are on, or updating anything. All of PyPI
is at your fingertips.

### Self-contained scripts

A related concern is making self-contained scripts that declare their own
dependencies. This looks like this:

```python
# /// script
# dependencies = ["requests", "numpy"]
# ///
```

Tools like pipx can read this and install the dependencies in a temporary
virtual environment before running the script. When running this with
`pipx run`, make sure to pass it a path, like `pipx run ./script.py`; if you
pass a raw filename like `script.py`, it will look for a package on PyPI with
that name.

### Task runners

The last common need is to run a series of commands in a specific environment.
This can be your tests, your documentation, or various other tasks. The original
tool for this is `tox`, but due to it's custom configuration format, the
Python-based tool `nox` is recommended instead for newcomers as well as
experienced users.

You write a `noxfile.py` with functions that represent the tasks you want to to
run. It looks something like this:

```python
import nox


@nox.session
def tests(session):
    session.install("pytest")
    session.run("pytest", *session.posargs)
```

Now you can run `nox -s tests` to run your tests in a clean environment. You can
install nox with pipx! (Or brew, etc.)

### Pre-commit

For static checks, like linting, formatting, and spell-checkers, you can use
`pre-commit`. We will cover this in detail later in the course. For now, just
know `pre-commit run -a` will run all your pre-commit checks in globally cached
isolated environments, and the check list is stored in
`.pre-commit-config.yaml`. This is intended for fast checks, not running pytest
(for example).

If you want to use it in it's namesake mode, then you can use
`pre-commit install`, which will add git hooks that run on every commit, only
for changed files (skip with `-n`).

### Other tools

There are many other tools that build on these concepts and make various aspects
easier or faster. Here are some popular ones:

- `poetry` - The first major attempt to make a modern package manager. It's
  become a bit too opinionated in some areas, like it is the only one to force
  you to use it's build-backend, and is behind on following standards.
- `pdm`: A mostly drop-in replacement for poetry that is more flexible and
  follows standards better. It can also do things like install Python for you.
- `hatch`: The only tool in this list that can do multiple environments properly
  (uv might later), but also the only one to not have built-in locking yet.
- `uv` - The most interesting new tool, it will be covered in depth below.

Each tool has strengths and drawbacks. Before uv, the best tool for projects
that needed locking was pdm, and tasks could be handled with nox (so that's a
two-tool solution, which isn't bad). However, uv is a very new and very
interesting entry, so let's cover that below.

#### uv

The team at astral-sh has been developing Rust-based tooling for Python. They
recently introduced `uv`, which started out as a drop-in replacement for venv,
pip, and pip-tools that was 10-100x faster. They also have a more modern design
since they don't have to worry about backwards-compatibly (so technically not
quite drop-in), and had many long-requested features added (to be fair, uv has
likely had more dedicated developer time than these other tools, probably
combined). Since launching, they've also replaced pipx, build, Python
installers, and are starting to replace poetry/pdm. By targeting the stand alone
tools first, it's easy to just use uv for whatever you want faster without fully
committing to it like, for example, Poetry forces you to do.

If you use `uv venv`, this creates virtual environments faster than Python can
start up. They do not, by default, contain _anything_, since uv was designed to
be able to target a virtual environment from the outside (modern pip can too,
but for legacy reasons, we are used to running it from inside the virtual
environment).

If you use `uv pip install`, you will get an ultra-fast package installer. A few
key differences: It will look for a virtual environment named `./.venv` if one
is not active by default, it will not install to the system Python unless you
add `--system` or pass an path to `--python`, and it will never install to the
user location. It also has some amazing features, like limiting the date of the
searched packages, and a minimum-versions resolver so you can make sure your
stated minimums are valid.

If you use `uv pip compile`, you'll get an ultra-fast lock file generator that
can target versions of Python and platforms you don't even have.

If you use `uv tool run` (or `uvx`), you'll get a tool runner that can run any
Python tool in a temporary virtual environment. You can also use
`uv tool install` to manage tools. And you can use `uv run` to run a script with
dependencies.

If you need to build packages, `uv build` is a drop-in replacement for the
standard pypa/build.

If you want to install and manage Python, `uv python install` and related
commands will install Python on your system for you in a uv managed location.
After installing, uv commands will prefer these managed versions. These are
binary installs, so they are faster than most of the classic tools like pyenv.

The most recent addition is a series of poetry/pdm-like project commands, such
as `uv init`, `uv add`, and `uv sync`. These let you set up a managed
environment with an integrated lockfile. There is also now uv configuration in
`pyproject.toml` or `uv.toml`.

Task support and hopefully multiple environments are coming soon, which would
basically allow uv to be a true all-in-one tool for Python development.

Many of the above tools also support using uv, such as `nox`, `build`, `hatch`,
and `pdm`, usually with flags or configuration settings. There is also a plugin
for `tox` and a hack for `pre-commit`.

## Conda

Conda is a package manager that is not Python-specific, but is very popular in
the Python scientific community. The format predates wheels (the current PyPI
binary format), and still has some advantages over wheels. Besides the obvious
advantage of being able to install Python itself, and having lots of
non-Python-related packages, it also doesn't require that packages be
stand-alone and supports shared libraries.

It was written in Python (which is a strange idea for a tool that is supposed to
install Python...) and had a very slow solver, which as the number of packages
and versions of packages grew, made it ridiculously slow, especially when adding
a package to an existing environment, or updating an environment. This has
caused the tool to be written multiple times: mamba has a faster, C++ solver,
micromamba was a complete C++ package that didn't require bootstrapping Python,
and pixi, which is a complete rethinking of the tool in Rust. The mamba solver
was finally added to the original conda as libmamba, and is now the default.

The packages for these tools were originally distributed by Anaconda, under the
Anaconda ToS, which was not open source. They shipped "anaconda", which was
conda with a pre-installed set of "common" packages. Using packages from the
defaults channel is allowed for some purposes, like education at a university. A
community project, conda-forge, was created to provide a free, open-source
channel with regular updates built using free CI offerings. This has grown to be
the largest channel, with thousands of packages. Just to complicate matters,
there are several installers like "miniforge" and "mambaforge" that are just
conda or mamba with conda-forge set as the default channel; you can do this
yourself with the base tools, and pixi already defaults to conda-forge.

Note that conda-forge has it's own compiler toolchain. You generally should not
be compiling code with conda-forge packages; if you have to, make sure you get
the compiler toolchain from conda-forge as well. Wheels mostly work, but you
lose the advantages of conda's shared libraries. If you are just using conda to
get Python, then using pip, this is a very bad way to use conda, use something
like uv, pdm, or hatch's python installation features instead.

### Pixi

Pixi is a new tool with a modern, package manager-like interface. It is really,
really fast, has automatic locking, a task system, great integration with PyPI
too (via uv), and much more. This website is built with pixi. If you are using
conda for project-based development, it's a great choice. Like most Rust
software, it's just a single binary, so it's easy to install and use. You can
also get it from places like homebrew. Like uv, it has great GitHub Actions
integration, as well (CI).

You can start a project with `pixi init` or `pixi init --pyproject` (the former
is for standalone projects like websites, the latter is better if you plan to
let other people import your project; we'll talk about packaging later). This
just sets up a few files. Here's an example of a simple pixi configuration in
`pixi.toml`:

```toml
[project]
name = "se-for-sci"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "osx-64"]

[dependencies]
ipykernel = "*"
jupyterlab = ">=3"

[tasks]
lab = "jupyter lab"
```

Notice the platform list: this locks for all platforms listed. Now, you can run
`pixi run lab` to start up jupyter lab. You don't need to call `pixi sync`, run
will do it for you if it's out of date. There won't be a solve here unless you
don't have a `pixi.lock` yet. You can use `pixi add` to add packages,
`pixi update` to update all packages. You can also use `pixi global install` as
a conda-forge version of `pipx install`.
