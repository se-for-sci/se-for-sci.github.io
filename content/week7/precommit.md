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
    rev: "v4.3.0"
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
Scikit-HEP developers can quickly read any package's code.

Also, properly formatted code has other benefits, such as if two developers make
the same change, they get the same formatting, and merge requests are easier.
The style choices in Black were explicitly made to optimize git diffs!

There are a _few_ options, mostly to enable/disable certain files, remove string
normalization, and to change the line length, and those go in your
`pyproject.toml` file.

Here is the snippet to add Black to your `.pre-commit-config.yml`:

```yaml
- repo: https://github.com/psf/black
  rev: "22.10.0"
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
  rev: "v0.982"
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
python_version = "3.7"
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
be ignored occasionally, but can find some signifiant logic errors in your
typing.

### Flake8

[Flake8][] can check a collection of good practices for you, ranging from simple
style to things that might confuse or detract users, such as unused imports,
named values that are never used, mutable default arguments, and more. Unlike
black and some other tools, flake8 does not correct problems, it just reports
them. Some of the checks could have had automated fixes, sadly (which is why
Black is nice). Here is a suggested `.flake8` or `setup.cfg` to enable
compatibility with Black (flake8 does not support pyproject.toml configuration,
sadly):

```ini
[flake8]
extend-ignore = E203, E501
```

One recommended plugin for flake8 is `flake8-bugbear`, which catches many common
bugs. It is highly opinionated and can be made more so with the `B9` setting.
You can also set a max complexity, which bugs you when you have complex
functions that should be broken up. Here is an opinionated config:

```ini
[flake8]
max-complexity = 12
extend-select = B9
extend-ignore = E203, E501, E722, B950
```

(Error E722 is important, but it is identical to the activated B001.) Here is
the flake8 addition for pre-commit, with the `bugbear` plugin:

```yaml
- repo: https://github.com/pycqa/flake8
  rev: "5.0.4"
  hooks:
    - id: flake8
      additional_dependencies: [flake8-bugbear]
```

This _will_ be too much at first, so you can disable or enable any test by it's
label. You can also disable a check or a list of checks inline with
`# noqa: X###` (where you list the check label(s)). Over time, you can fix and
enable more checks. A few interesting plugins:

- [`flake8-bugbear`](https://pypi.org/project/flake8-bugbear/): Fantastic
  checker that catches common situations that tend to create bugs. Codes: `B`,
  `B9`
- [`flake8-docstrings`](https://pypi.org/project/flake8-docstrings/): Docstring
  checker. `--docstring-convention=pep257` is default, `numpy` and `google` also
  allowed.
- [`flake8-spellcheck`](https://pypi.org/project/flake8-spellcheck/): Spelling
  checker. Code: `SC`
- [`flake8-import-order`](https://pypi.org/project/flake8-import-order/):
  Enforces PEP8 grouped imports (you may prefer isort). Code: `I`
- [`pep8-naming`](https://pypi.org/project/pep8-naming/): Enforces PEP8 naming
  rules. Code: `N`
- [`flake8-print`](https://pypi.org/project/pep8-naming/): Makes sure you don't
  have print statements that sneak in. Code: `T`

### isort

You can have your imports sorted automatically by [isort][]. This will sort your
imports, and is black compatible. One reason to have sorted imports is to reduce
merge conflicts. Another is to clarify where imports come from - standard
library imports are in a group above third party imports, which are above local
imports. All this is configurable, as well. To use isort, the following
pre-commit config will work:

```yaml
- repo: https://github.com/PyCQA/isort
  rev: "5.10.1"
  hooks:
    - id: isort
```

In order to use it, you need to add some configuration. You can add it to
`pyproject.toml` or classic config files:

```ini
[tool.isort]
profile = "black"
```

### PyUpgrade

Another useful tool is [PyUpgrade][], which monitors your codebase for "old"
style syntax. Most useful to keep Python 2 outdated constructs out, it can even
do some code updates for different versions of Python 3, like adding f-strings
when clearly better (please always use them, they are faster) if you set
`--py36-plus` (for example). This is a recommended addition for any project.

```yaml
- repo: https://github.com/asottile/pyupgrade
  rev: "v3.1.0"
  hooks:
    - id: pyupgrade
      args: ["--py37-plus"]
```

[pyupgrade]: https://github.com/asottile/pyupgrade:

> #### Note:
>
> If you set this to `--py37-plus`, you can add the annotations import by adding
> the following line to your isort pre-commit hook configuration:
>
> ```yaml
> args: ["-a", "from __future__ import annotations"]
> ```
>
> Also make sure isort comes before pyupgrade. Now when you run pre-commit, it
> will clean up your annotations to 3.7+ style, too!

### Spelling

You can and should check for spelling errors in your code too. If you want to
add this, you can use [codespell][] for common spelling mistakes. Unlike most
spell checkers, this has a list of mistakes it looks for, rather than a list of
"valid" words. To use:

```yaml
- repo: https://github.com/codespell-project/codespell
  rev: "v2.2.2"
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
