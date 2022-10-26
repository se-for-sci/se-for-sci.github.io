Updates

- Projects proposal feedback planned for tomorrow
  - May have to combine a couple of projects due to drops
  - Next project assignment coming soon

Git & GitHub

- Making a PR (MR on gitlab) the long way (example of Hist Python 3.11 PR with
  the `gh` CLI and `git grep`)
  - Clone a repo
  - Make a branch
  - 1 or more commits
  - Make the pr (via gh or web + fork)
  - Review
  - Merge via squash or rebase
- Advanced example: doing a git bisect
  - Example locating error
- Other useful commands: log, diff, grep, ls-files, status, config (.git/config
  & ~/.gitconfig), gui, gitk (bundled program), stash, blame, submodule (mostly
  just use `--recurse-submodules` when cloning unless you are setting them up)
- Git hooks: only manually activated (can't be "declared" by the repo), usually
  use a tool to manage

Packaging

- Python focused, but many ideas general
- Packaging is not confusing!
  - "library": something you import (numpy, pandas)
  - "application": something you run (pip, black, pipx)
  - "application": something that you setup to do something (webpage, analysis,
    etc), usually with a dedicated, reproducible environment.
- `pip install`, `pip install --user` are wrong! You can make a mess of your
  global environment. The solution depends on what you are doing.
- Safe libraries: try to keep global installs down to a bare minimum. Maybe just
  one: `pipx`!
  - Fully isolated environments created for every install. Apps do not touch
    your "import"s!
  - Easy upgrades
  - `pipx run` can even install and run in one command! Cached for a week.
  - Using brew also creates isolated environments
- Environments
  - `python -m venv` and `virtualenv` (`pipx install virtualenv`, perhaps? :) )
    are similar - the first is built-in, the second is better updated and
    faster. Same API.
  - Name your main environment for a project `.venv`, a few tools pick it up
    automatically
  - Lock your environments with `pip freeze` or pip-tools's `pip-compile`.
    Optionally include hashes for security.
- Tools can manage these for you, like `pdm`, `hatch`, or `poetry`
- Environment aware task runners
  - Examples include `nox`, `tox`, and `hatch`
  - Small nox example

We did a example of a textual app with an environment file and a noxfile, from
the class notes repo. Pushed after class (oops).
