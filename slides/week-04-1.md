---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Packaging

---

## Pip / uv and PyPI

- PyPI hosts packages for pip / uv
- pip: the canonical package manager for Python
- uv: a Rust rewrite of pip, 10-100x faster
  - About 34% of PyPI downloads come from uv (Feb 2026)!
  - Better defaults: uses `.venv`, never installs to system/user without a flag
  - Also has a high-level API

---

## Conda/Mamba/MicroMamba/Pixi and conda-forge

- Conda: multipurpose packager with Python focus
  - Written _in_ Python
  - Now contains the libmamba solver (in C++)
- mamba: a faster conda written in C++
- micromamba: Used to be different, now (2.0) a statically linked mamba
- pixi: a Rust rewrite of conda, with a new high-level API
  - No low-level API to match conda/mamba

---

## Which to use?

- PyPI is the official ecosystem, most packages are there
- Package owners control PyPI, while conda-forge is community driven
- If you develop a package, PyPI is first
- Conda tools can use PyPI packages
- Conda is often preferred in some fields (like ML); use pixi there

So we'll focus on PyPI via uv.

The course website is a pixi project, by the way.

---

## Getting started with uv

There are lots of ways to install uv. It's just a single Rust compiled binary.

<https://docs.astral.sh/uv/getting-started/installation/>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
wget -qO- https://astral.sh/uv/install.sh | sh
pipx install uv
pip install uv
cargo install --git https://github.com/astral-sh/uv uv
brew install uv
# Windows:
winget install --id=astral-sh.uv -e
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Using uv

Low level API:

```bash
uv pip <...>
uv venv <...>
```

High level API:

```bash
uv run <command...>
```

---

## Using packages

You should never just run "pip install <package>"; installing into your global site-packages is a bad idea, and installing into your user site-packages is worse!

Python has a solution for this: virtual environments.

But if you just want to install a command-line tool, you don't have to set them up yourself!

```bash
uv tool install <package>
<package> <args...>
```

---

## Quick run

You can even do it in one line:

```bash
uvx <package> <args...>
```

This will create a temporary virtual environment, install the package, run it. The environment is cached for a time, so reruns are fast.

If the command and package names differ, use `--from`:

```bash
uvx --from <package> <command> <args...>
```

pipx has the same features: `pipx install` and `pipx run` (`--spec` instead of `--from`). pipx is preinstalled on GitHub Actions, and there is an action to set up uv.

(I believe this name was inspired by `npx` from JavaScript, which does the same thing.)

---

## Quick scripts

You can get this functionality for scripts, as well:

```python
# /// script
# dependencies = ["rich"]
# requires-python = ">=3.11"
# ///

import rich

rich.print("[blue]Hello, world!")
```

```bash
uv run myscripts.py <args...>
```

---

## Virtual environments

```bash
uv venv
```

This creates a `.venv` folder with a virtual environment in it. You can then activate it:

```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows
```

Note that `uv` commands will automatically use a `.venv` folder if it exists.

---

## Using venvs

When a venv is "active", commands will run in that venv.

Most common command:

```bash
uv pip install -e. --group dev
```

You can always delete the venv and restart, rerunnning `uv venv` replaces the venv by default.

---

## High level API

uv can help you setup and run a project. The high level API does the things you would normally do manually:

```bash
uv init <...> # start a new project
uv add <package> # add a package to the project
uv run <command...> # run a command in the project environment
```

For an existing project, you just need `uv run`!

---

## What does `uv run` do?

- Creates a `.venv` if not present
- Installs the project's dependencies
- Installs the project in editable mode, if it has a build backend
- Installs the `dev` dependency group, if it exists
- Uses the lockfile if it exists, otherwise creates one

Works with a standard `pyproject.toml`; no uv-specific configuration needed.

---

## Pixi

Pixi only has a high-level interface, and it needs a manifest (`pixi.toml` or `[tool.pixi]` in `pyproject.toml`).

- Installs conda and PyPI packages
- Lists platforms and channels in `[workspace]`
- Has a task system: `pixi run <task>`

```bash
pixi run lab  # starts JupyterLab for this course
```

---

## Other uv features

See `uv --help`

- `uv python` can manage installed Pythons
- `uv build` can build packages
- `uv publish` can publish packages
- `uv tree` can show the dependency tree
- `uv self` can manage uv itself
