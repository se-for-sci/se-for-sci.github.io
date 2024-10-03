import os
import functools
import re
import nox
import urllib.request
import json
from pathlib import Path
from typing import Any

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


PC_VERS = re.compile(
    r"""\
^( *)- repo: (.*?)
 *  rev: (.*?)$""",
    re.MULTILINE,
)

PC_REPL_LINE = """\
{2}- repo: {0}
{2}  rev: {3}{1}{3}"""


GHA_VERS = re.compile(r"[\s\-]+uses: (.*?)@([^\s]+)")


@nox.session(reuse_venv=True, tags=["bump"])
def pc_bump(session: nox.Session) -> None:
    """
    Bump the pre-commit versions.
    """
    session.install("lastversion>=3.4")
    versions = {}
    pages = Path("content").glob("**/*.md")

    for page in pages:
        txt = page.read_text()
        old_versions = {m[2]: (m[3].strip('"'), m[1]) for m in PC_VERS.finditer(txt)}

        for proj, (old_version, space) in old_versions.items():
            if proj not in versions:
                versions[proj] = session.run(
                    "lastversion",
                    "--at=github",
                    "--format=tag",
                    "--exclude=~alpha|beta|rc",
                    proj,
                    silent=True,
                ).strip()
            new_version = versions[proj]

            after = PC_REPL_LINE.format(proj, new_version, space, '"')

            session.log(f"Bump {proj}: {old_version} -> {new_version} ({page})")
            txt = txt.replace(PC_REPL_LINE.format(proj, old_version, space, '"'), after)
            txt = txt.replace(PC_REPL_LINE.format(proj, old_version, space, ""), after)

            page.write_text(txt)


@functools.lru_cache(maxsize=None)  # noqa: UP033
def get_latest_version_tag(repo: str, old_version: str) -> dict[str, Any] | None:
    auth = os.environ.get("GITHUB_TOKEN", os.environ.get("GITHUB_API_TOKEN", ""))
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/tags?per_page=100"
    )
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if auth:
        request.add_header("Authorization", f"Bearer: {auth}")
    response = urllib.request.urlopen(request)
    results = json.loads(response.read())
    if not results:
        msg = f"No results for {repo}"
        raise RuntimeError(msg)
    tags = [
        x["name"]
        for x in results
        if x["name"].count(".") == old_version.count(".")
        and x["name"].startswith("v") == old_version.startswith("v")
    ]
    if tags:
        return tags[0]
    return None


@nox.session(venv_backend="none", tags=["bump"])
def gha_bump(session: nox.Session) -> None:
    """
    Bump the GitHub Actions.
    """
    pages = list(Path("content").glob("**/*.md"))
    full_txt = "\n".join(page.read_text() for page in pages)

    # This assumes there is a single version per action
    old_versions = {m[1]: m[2] for m in GHA_VERS.finditer(full_txt)}

    for repo, old_version in old_versions.items():
        session.log(f"{repo}: {old_version}")
        new_version = get_latest_version_tag(repo, old_version)
        if not new_version:
            continue
        if new_version != old_version:
            session.log(f"Convert {repo}: {old_version} -> {new_version}")
            for page in pages:
                txt = page.read_text()
                txt = txt.replace(
                    f"uses: {repo}@{old_version}", f"uses: {repo}@{new_version}"
                )
                page.write_text(txt)
