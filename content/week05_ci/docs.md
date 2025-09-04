# Generating documentation

## Documentation in the source

Python (and most other languages) has a convention for inline documentation. For
example:

```python
def f(x):
    """One-line summary of function

    Much longer and more detailed paragraph(s) about the function.  This is in
    the NumPy style.

    Parameters
    ----------
    x : float
        This is a parameter. Notice the type - that predates Python 3!

    Returns
    -------
    float
        A description of what it returns.

    Raises
    ------
    AssertionError
        Explain what you can raise and why.


    References
    ----------
    .. [1] "NumPy", https://numpy.org

    Examples
    --------
    >>> y = f(1.0)
    >>> y = f(2.0)
    """
```

You don't have to style your docs in this way, but if you do, there are several
conventions to choose from.
[NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html), Google
style, or raw Sphinx directives are common. Sections are optional, and there are
other optional sections, like "See Also", "Attributes" (for classes), etc.

If you are writing a lot of functions and don't have as many users as a major
library, you can get away with something simpler. Here's raw Sphinx:

```python
def f(x: float) -> float:
    """Computes f of x.

    :param x: The input value.
    :return: The f(x) value, often called y.

    Usage::

        >>> y = f(1.0)
        >>> y = f(2.0)
    """
```

Depending on your functions, you can actually run your usage examples as part of
your tests! There's even a built-in library for it (doctest), but I'd recommend
xdoctest instead, as it's quite a bit better. There are also pytest integration
plugins. Should you? It _really_ depends on what you are doing. If it's easy to
place inputs and outputs in the examples, then yes; but for many libraries, if
setting up an input is involved, the answer might be no. Just keep that in mind
if you need it!

You should also write high level documentation. Knowing how each unit of a
program works (API documentation) is useful if you understand how it all fits
together and know what you are looking for, but someone just starting with your
package needs to know how it all fits together - that's the "overview"
documentation. Learning to read code efficiently is a substitute for API docs,
but it is not a substitute for overview docs. (Reading a test suite, especially
integration tests, however, can be ;)

## Documentation engines

There are two documentation engines quite popular in Python. The oldest and most
used one is Sphinx - Python's own documentation is built in Sphinx! It has
received a lot of work and good themes lately, like Furo (PyPA) and
sphinx-pydata-theme (SciPy). It is also the basis for JuyterBook, which is what
this material was written in! It has third-party tooling to use markdown instead
of the default RestructredText, include notebooks as pages, and more. Sphinx
uses the aging docutils, which has an intermediate representation that produces
HTML, or other formats too, like ebooks and LaTeX. Example sites: pretty much
everything in Python; pip, build, numpy, scipy, etc.

The other engine is MkDocs. This is a clean fresh start built on top of
markdown. It's much faster than Sphinx, and writing a bit of code to execute
during generation is really easy - adding things like producing rendered output
from custom code is simple. The material theme is great. Many of the advantages
of MkDocs are matched by modern Sphinx with a bit of configuration. Example
sites: cibuildwheel, textual, pipx, and hatch.

The documentation engine for C++ is called Doxygen. If you need to mix it with
Sphinx, use Breathe.

We'll focus on Sphinx - MkDocs is a bit easier, so you can hopefully set that up
easily if you choose that.

## Sphinx

### Getting started

Sphinx provides a way to
[quickstart](https://www.sphinx-doc.org/en/master/tutorial/getting-started.html)
a project:

```console
$ # Install sphinx to get this command
$ sphinx-quickstart docs
```

You can answer the questions, and it will set up a docs folder. A classic
starting docs folder looks like this:

```
- docs
  - make.bat
  - Makefile
  - conf.py
  - index.rst
```

(Newer versions of sphinx place `conf.py` and `index.rst` inside a `source`
subfolder, but you'll see a lot of projects set up like the above.)

The "make" files give you shortcuts for building your project. Though they do
not need to be used; you can do it yourself, cross-platform, with:

```console
$ sphinx-build -M html docs docs/build
```

### Noxfile for docs

Since your environment matters for building docs, and since nox/tox is better
than makefiles for Python, a cleaner solution would be to add a session for docs
into your noxfile:

```python
@nox.session
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "--serve" to serve.
    """

    session.install(".[docs]")
    session.chdir("docs")
    session.run("sphinx-build", "-M", "html", ".", "build")
```

(You can add your docs requirements to your `docs` extra, or install any other
way you like here.)

Want to quickly preview your docs? This will give you a URL to use in a
webbrowser.

```python
@nox.session
def serve(session: nox.Session) -> None:
    docs(session)
    print("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
    session.run("python", "-m", "http.server", "8000", "-d", "_build/html")
```

### Making the docs yours

I would recommend making a few changes. First, you'll want some dependencies:

```toml
[project.optional-dependencies]
docs = [
    "furo",  # Theme
    "myst_parser >=0.13",  # Markdown
    "sphinx >=4.0",
    "sphinx_copybutton",  # Easy code copy button
]
```

You can select any theme you want; `furo` is an ultra modern, well designed,
lightweight theme used by the PyPA.

Next, exit your `conf.py` file. Your extensions should look like this:

```python
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]
```

The two extensions we added to the requirements are here, and there are a few
built-in `sphinx.ext`'s we are using too (those were probably already there).

Make sure you use your theme:

```python
html_theme = "furo"
```

Themes may have custom config in `html_theme_options`, feel free to look this up
for your theme.

### Adding docs

The root of your docs is `index.rst`. Since you have Myst, you can use
`index.md` instead if you want. If you mostly are using this as a table of
contents, it doesn't really matter too much. Here's an example `index.md`:

````md
---
hide-toc: true
---

# My Package

This is a package. It is really interesting.

```{toctree}
:hidden:

installation
user_guide
api/index
```
````

Any valid markdown or Myst additions valid.

````

This starts by hiding this page from the table of contents (options are in YAML
format surrounded by `---`'s at the top, this is a common convention in
markdown).

Then you have some text, then you have a table of contents (this is a Myst addition
to markdown to give you the ability to do a restructured text thing - in fact, you can see
a restructured text option `:hidden:` inside the block). The table of contents
is hidden so it isn't shown inline on the page (since it's already in the side
bar). This assumes you have three files with more content in them, and a folder where you
will put your API documentation.

The other pages can be placed in here in the same way, so let's focus on the api
pages.  You can auto-generate them with
[sphinx-apidoc](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)
(built-in):

```console
$ sphinx-apidoc -o docs/api src/my_package
````

Everything is dynamically imported, so protect code with
`if __name__ == "__main__"`! There are lots of flags to control how it generates
the structure and what it includes. You only need to rerun this if your
structure changes; documentation itself is read on each run.

### CI: ReadTheDocs

If you have a public project, `readthedocs.org` is a service that builds your
docs for you. Most projects use this.

### CI: GitHub Actions and Pages

You can also host your docs on Pages. You can set a up a GitHub Action that
builds your docs and pushes them to Pages. You won't get per-pull request
viewable docs (you can download the output, though).

Remember to set Actions as the source for GitHub Pages in the repo settings.
Here is possible example:

```yaml
on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: build output
        run: pipx run nox -s docs

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/build

  deploy:
    needs:
      - docs
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```
