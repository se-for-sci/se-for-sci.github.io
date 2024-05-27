# Pre-commit

## Intro to pre-commit

You can install pre-commit from `brew` (macOS), or via `pipx`/`pip` for anything
with Python.

You can then run it like this:

```bash
pre-commit run -a
```

That will check everything. You don't need to know anything about how to run the
checkers or linters, it's a single standard interface for all projects. Each
hook gets a unique, cached environment, so the next time you run it, it's
lightning fast. If you leave off the `-a`, it _only checks the changed files in
your staging area, even partially staged ones!_

If you want to update to the latest versions of all your hooks, run:

```bash
pre-commit autoupdate
```

If you want to use it in the namesake "pre-commit" mode, then run:

```bash
pre-commit install
```

Now it runs before every commit, and you'll never check in "bad" code again! Use
`-n` to skip the pre-commit check when committing for emergencies.

PS: This is generally not used for pytest (though it could be), since tests are
generally slower and take more setup, including being installed properly.

Here is a minimal `.pre-commit-config.yaml` file with some handy options:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: "v4.4.0"
    hooks:
      - id: check-added-large-files
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: check-symlinks
      - id: check-yaml
      - id: debug-statements
      - id: end-of-file-fixer
      - id: mixed-line-ending
      - id: requirements-txt-fixer
      - id: trailing-whitespace
```

**Helpful tip**: Pre-commit runs top-to-bottom, so put checks that modify
content (like the several of the pre-commit-hooks above, or Black) above checks
that might be more likely to pass after the modification (like flake8).

**Keeping pinned versions fresh**: You can use `pre-commit autoupdate` to move
your tagged versions forward to the latest tags! Due to the design of
pre-commit's caching system, these _must_ point at fixed tags, never put a
branch here.

## A selection of pre-commit checks

### Black

[Black](https://black.readthedocs.io/en/latest/) is a popular auto-formatter
from the Python Software Foundation. One of the main features of Black is that
it is "opinionated"; that is, it is almost completely unconfigurable. Instead of
allowing you to come up with your own format, it enforces one on you. While I am
quite sure you can come up with a better format, having a single standard makes
it possible to learn to read code very fast - you can immediately see nested
lists, matching brackets, etc. There also is a faction of developers that
dislikes all auto-formatting tools, but inside a system like pre-commit,
auto-formatters are ideal. They also speed up the writing of code because you
can ignore formatting your code when you write it. By imposing a standard, all
developers can quickly read any package's code.

Also, properly formatted code has other benefits, such as if two developers make
the same change, they get the same formatting, and merge requests are easier.
The style choices in Black were explicitly made to optimize git diffs!

There are a _few_ options, mostly to enable/disable certain files, remove string
normalization, and to change the line length, and those go in your
`pyproject.toml` file.

Here is the snippet to add Black to your `.pre-commit-config.yml`:

```yaml
- repo: https://github.com/psf/black-pre-commit-mirror
  rev: "23.9.1"
  hooks:
    - id: black
```

In _very_ specific situations, you may want to retain special formatting. After
carefully deciding that it is a special use case, you can use `# fmt: on` and
`# fmt: off` around a code block to have it keep custom formatting. _Always_
consider refactoring before you try this option! Most of the time, you can find
a way to make the Blacked code look better by rewriting your code; factor out
long unreadable portions into a variable, avoid writing matrices as 1D lists,
etc.

#### Jupyter notebook support

If you want Black for Jupyter notebooks _too_, replace `id: black` with
`id:black-jupyter` above. You also might like the following hook, which cleans
Jupyter outputs:

```yaml
- repo: https://github.com/kynan/nbstripout
  rev: "0.6.1"
  hooks:
    - id: nbstripout
```

### Type checking

We saw how to use mypy before; now let's integrate it into our pre-commit
runner!

The MyPy addition for pre-commit:

```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: "v1.5.1"
  hooks:
    - id: mypy
      files: src
      args: []
```

You should always specify args, as the hook's default hides issues - it's
designed to avoid configuration, but you should add configuration. You can also
add items to the virtual environment setup for MyPy by pre-commit, for example:

```yaml
additional_dependencies: [attrs==21.2.0]
```

MyPy has a config section in `pyproject.toml` that looks like this:

```ini
[tool.mypy]
files = "src"
python_version = "3.9"
strict = true
show_error_codes = true
enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
warn_unreachable = true


# You can disable imports or control per-module/file settings here
[[tool.mypy.overrides]]
module = [ "numpy.*", ]
ignore_missing_imports = true
```

There are a lot of options, and you can start with only typing global code and
functions with at least one type annotation (the default) and enable more checks
as you go (possibly by slowly uncommenting items in the list above). You can
ignore missing imports on libraries as shown above, one section each. And you
can disable MyPy on a line with `# type: ignore`. One strategy would be to
enable `check_untyped_defs` first, followed by `disallow_untyped_defs` then
`disallow_incomplete_defs`. You can add these _per file_ by adding a
`# mypy: <option>` at the top of a file. You can also pass `--strict` on the
command line. `strict = true` is now allowed in config files, too.

The extra strict options shown above (`warn_unreachable`, `redundant-expr`, and
`truthy-bool`) can trigger too often (like on `sys.platform` checks) and have to
be ignored occasionally, but can find some significant logic errors in your
typing.

### Ruff

[Ruff][] [(docs)][ruff docs] is a Python code linter and autofixer that replaces
many other tools in the ecosystem with a ultra-fast (written in Rust), single
zero-dependency package. All plugins are compiled in, so you can't get new
failures from plugins updating without updating your pre-commit hook.

[ruff docs]: https://beta.ruff.rs
[ruff]: https://github.com/astral-sh/ruff

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: "v0.0.292"
  hooks:
    - id: ruff
      args: ["--fix", "--show-fixes"]
```

The `--fix` argument is optional, but recommended, since you can inspect and
undo changes in git.

Ruff is configured in your `pyproject.toml`. Here's an example:

```toml
[tool.ruff]
select = [
  "E", "F", "W", # flake8
  "B",           # flake8-bugbear
  "I",           # isort
  "ARG",         # flake8-unused-arguments
  "C4",          # flake8-comprehensions
  "EM",          # flake8-errmsg
  "ICN",         # flake8-import-conventions
  "ISC",         # flake8-implicit-str-concat
  "G",           # flake8-logging-format
  "PGH",         # pygrep-hooks
  "PIE",         # flake8-pie
  "PL",          # pylint
  "PT",          # flake8-pytest-style
  "PTH",         # flake8-use-pathlib
  "RET",         # flake8-return
  "RUF",         # Ruff-specific
  "SIM",         # flake8-simplify
  "T20",         # flake8-print
  "UP",          # pyupgrade
  "YTT",         # flake8-2020
  "EXE",         # flake8-executable
  "NPY",         # NumPy specific rules
  "PD",          # pandas-vet
]
extend-ignore = [
  "PLR",    # Design related pylint codes
  "E501",   # Line too long
  "PT004",  # Use underscore for non-returning fixture (use usefixture instead)
]
typing-modules = ["mypackage._compat.typing"]
src = ["src"]
unfixable = [
  "T20",  # Removes print statements
  "F841", # Removes unused variables
]
exclude = []
flake8-unused-arguments.ignore-variadic-names = true
isort.required-imports = ["from __future__ import annotations"]

[tool.ruff.per-file-ignores]
"tests/**" = ["T20"]
```

Ruff [provides dozens of rule sets](https://beta.ruff.rs/docs/rules/); you can
select what you want from these. Like Flake8, plugins match by whole letter
sequences (with the special exception of pylint's "PL" shortcut), then you can
also include leading or whole error codes. Codes starting with 9 must be
selected explicitly, with at least the letters followed by a 9. You can also
ignore certain error codes via `extend-ignore`. You can also set codes per paths
to ignore in `per-file-ignores`. If you don't like certain auto-fixes, you can
disable auto-fixing for specific error codes via `unfixable`.

There are other configuration options, such as the `src` list which tells it
where to look for top level packages (mostly for "I" codes, which also have a
lot of custom configuration options) {% rr RF003 %}, `typing-modules`, which
helps apply typing-specific rules to a re-exported typing module (a common
practice for unifying typing and `typing_extensions` based on Python version).
There's also a file `exclude` set, which you can override if you are running
this entirely from pre-commit (default excludes include "build", so if you have
a `build` module or file named `build.py`, it would get skipped by default
without this).

Here are some good error codes to enable on most (but not all!) projects:

- `E`, `F`, `W`: These are the standard flake8 checks, classic checks that have
  stood the test of time.
- `B`: This finds patterns that are very bug-prone.
- `I`: This sorts your includes. There are multiple benefits, such as smaller
  diffs, fewer conflicts, a way to auto-inject `__future__` imports, and easier
  for readers to tell what's built-in, third-party, and local. It has a lot of
  configuration options, but defaults to a Black-compatible style.
- `ARG`: This looks for unused arguments. You might need to `# noqa: ARG001`
  occasionally, but it's overall pretty useful.
- `C4`: This looks for places that could use comprehensions, and can autofix
  them.
- `EM`: Very opinionated trick for error messages: it stops you from putting the
  error string directly in the exception you are throwing, producing a cleaner
  traceback without duplicating the error string.
- `ISC`: Checks for implicit string concatenation, which can help catch mistakes
  with missing commas.
- `PGH`: Checks for patterns, such as type ignores or noqa's without a specific
  error code.
- `PL`: A set of four code groups that cover some (200 or so out of 600 rules)
  of PyLint.
- `PT`: Helps tests follow best pytest practices. A few codes are not ideal, but
  many are helpful.
- `PTH`: Want to move to using modern pathlib? This will help. There are some
  cases where performance matters, but otherwise, pathlib is easier to read and
  use.
- `RUF`: Codes specific to Ruff, including removing noqa's that aren't used.
- `T20`: Disallow `print` in your code (built on the assumption that it's a
  common debugging tool).
- `UP`: Upgrade old Python syntax to your `target-version`.

A few others small ones are included above, and there are even more available in
Ruff.

### Spelling

You can and should check for spelling errors in your code too. If you want to
add this, you can use [codespell][] for common spelling mistakes. Unlike most
spell checkers, this has a list of mistakes it looks for, rather than a list of
"valid" words. To use:

```yaml
- repo: https://github.com/codespell-project/codespell
  rev: "v2.2.5"
  hooks:
    - id: codespell
      args: ["-L", "sur,nd"]
```

You can list allowed spellings in a comma separated string passed to `-L` (or
`--ignore-words-list` - usually it is better to use long options when you are
not typing things live). The example above will allow "Big Sur" and "ND". You
can instead use a comma separated list in `setup.cfg` or `.codespellrc`:

```ini
[codespell]
ignore-words-list = sur,nd
```

You can also use a local pygrep check to eliminate common capitalization errors,
such as the one below:

```yaml
- repo: local
  hooks:
    - id: disallow-caps
      name: Disallow improper capitalization
      language: pygrep
      entry: PyBind|Numpy|Cmake|CCache|Github|PyTest
      exclude: .pre-commit-config.yaml
```

[codespell]: https://github.com/codespell-project/codespell
[pre-commit]: https://pre-commit.com
[isort]: https://pycqa.github.io/isort/
