import nox
from pathlib import Path

nox.needs_version = ">=2022.1.7"
DIR = Path(__file__).parent.resolve()


@nox.session(reuse_venv=True)
def pyodide(session: nox.Session) -> None:
    session.install("jupyterlite[lab]")
    session.run("jupyter", "lite", "init")
    session.run("jupyter", "lite", "build", "--contents=content")

    if "--serve" in session.posargs:
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
