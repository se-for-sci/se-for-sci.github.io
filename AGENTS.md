# AGENTS.md

MyST MD course site for _Software Engineering for Scientific Computing_.

## Build & run

| Target                 | Command                                                              |
| ---------------------- | -------------------------------------------------------------------- |
| Book (with pixi)       | `pixi run book`                                                      |
| Pyodide / JupyterLite  | `nox -s pyodide`                                                     |
| Slides                 | `npx @marp-team/marp-cli@latest --input-dir slides --output _output` |
| Live dev server (MyST) | `pixi run serve`                                                     |
| JupyterLab             | `pixi run lab`                                                       |

- `pixi run book` depends on the `install-kernel` task, which installs the
  project's Python kernel into the pixi environment (`--sys-prefix`), then
  builds the site using `myst build --execute --html`. It sets
  `PYDEVD_DISABLE_FILE_VALIDATION=1`.
- `mystmd` is configured to **execute all notebooks** on every build
  (`--execute` flag), so broken code in a notebook breaks CI.
- Only files listed in the `toc` section of `myst.yml` are included in the
  build. Adding a new chapter file means adding it to `myst.yml`. The `notes/`
  directory is explicitly excluded and contains instructor notes—do not
  reference it as book content.

## Environment

- **Pixi** (`pixi.toml`) is the primary package manager. `environment.yml`
  duplicates the same Conda dependencies and should be kept in sync.
- `pixi.lock` is checked in.
- Nox sessions use `uv|virtualenv` by default
  (`nox.options.default_venv_backend`).

## Content structure

- `content/` — Book chapters (mix of `.md` and `.ipynb`).
- `slides/` — Marp slide decks. These are rendered by CI and deployed to
  `public/slides`. Files are named `week-NN-N.md` (e.g. `week-14-1.md`) and use
  the Marp `gaia` theme; copy the front matter from an existing deck. Slides
  parallel a content chapter: the chapter links to its deck near the top with
  `` {button}`Slides <https://se-for-sci.github.io/slides/week-NN-N>` ``, and
  the deck opens with a `# SE4Sci` / `## <Title>` lead slide, with `---`
  separating slides.
- `notes/` — Instructor notes; not built into the book.
- `myst.yml` drives the project configuration and table of contents.

## Lint / format / pre-commit

- Always use `prek -a --quiet` instead of `pre-commit run -a`.
- Hooks include: ruff-format, blacken-docs, nbstripout, prettier, codespell,
  blocklint, plus a **custom `disallow-caps` hook** that rejects
  miscapitalizations of names like pybind11, NumPy, CMake, ccache, GitHub, and
  pytest — always use the canonical spelling (the hook also applies to this
  file).
- Prettier config (`.prettierrc.toml`): prose wraps at 80 chars by default,
  **but never for `slides/*.md`**.

## CI / deploy

`.github/workflows/cd.yml` builds three artifacts and deploys to GitHub Pages on
push to `main`:

1. Book via `pixi run book` (mystmd).
2. Pyodide via `uvx nox -s pyodide`.
3. Slides via `npx @marp-team/marp-cli@latest ...`.

## Generated / ignored artifacts

- Many `content/week*/` subdirs contain compiled examples (C++, Rust, Fortran).
  Build artifacts (`.so`, `.o`, `CMakeLists.txt`, `pyproject.toml`, etc.) inside
  those dirs are gitignored.
- `_build/`, `_output/`, `.nox/`, `.pixi/`, `.ipynb_checkpoints` are ignored.

## Nox bump helpers

- `nox -s pc_bump` — bumps pre-commit versions embedded in course markdown
  (searches `content/**/*.md`).
- `nox -s gha_bump` — bumps GitHub Actions versions embedded in course markdown.
