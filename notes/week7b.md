Homework 2 notes:

- `__eq__` can be added or all mention of it can be removed (including
  `eq=False`)
- Some strings don't really make sense, but the output still matches.

Projects - go ahead and start.

Environments

- `conda env create` -> makes an environment from your `environment.yml` file

Packaging

- Minimal setup to build a package
- Building an sdist/wheel
- Installing
- Read more at https://packaging.python.org or https://scikit-hep.org/developer

Pre-commit (static checks)

- Intro to pre-commit & usage
- Installed mode (optional)
- Writing your first check
- Black (Jupyter too)
- MyPy at a pre-commit check
- Flake8
- Others include isort, pyupgrade, and codespell

Task Runners

- Comparison
  - Build system generators (like CMake, Meson, autotools)
  - Task Runners (make, invoke, or nox / tox (Python aware)
- Nox: Python environment aware and configured from Python
  - Simple session (tests)
  - Adding dependencies
  - Parametrizations (skipped in class, see online notes)
  - Some common jobs and usages
