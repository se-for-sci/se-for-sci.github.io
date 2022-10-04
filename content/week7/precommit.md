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
your staging area, even partially staged ones!_.

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
      - id: name-tests-test
        args: ["--pytest-test-first"]
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

[pre-commit]: https://pre-commit.com
