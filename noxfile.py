import nox
from pathlib import Path

DIR = Path(__file__).parent.resolve()

nox.needs_version = ">=2024.4.15"
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session(reuse_venv=True)
def pyodide(session: nox.Session) -> None:
    session.install(
        "jupyterlite-core==0.4.1",
        "jupyterlab~=4.2.5",
        "notebook~=7.2.2",
        "jupyterlite-pyodide-kernel==0.4.2",
    )
    session.run("jupyter", "lite", "init")
    session.run("jupyter", "lite", "build", "--contents=content")

    if session.interactive:
        session.run("jupyter", "lite", "serve")


@nox.session(reuse_venv=True)
def book(session: nox.Session) -> None:
    session.install(
        "black",
        "cattrs",
        "cffi",
        "ipykernel",
        "ipython",
        "ipywidgets",
        "jupyter-book",
        "matplotlib",
        "numba",
        "numpy",
        "pandas",
        "pybind11",
        "pytest",
        "rich",
        "scikit-build-core",
        "sphinxcontrib-mermaid",
    )
    env = {"PYDEVD_DISABLE_FILE_VALIDATION": "1"}
    session.run(
        "python",
        "-m",
        "ipykernel",
        "install",
        "--user",
        "--name",
        "conda-env-se-for-sci-py",
        env=env,
    )
    session.run("jupyter-book", "build", ".", env=env)
