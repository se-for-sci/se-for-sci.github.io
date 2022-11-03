# Generating documentation

## Documentation in the source

Python (and most other languages) has a convention for inline documentation. For
example:

```python
def f(x):
    """
    ...
    """
```

You don't have to style your docs in this way, but if you do, there are several
conventions to choose from. Google style, NumPy style, or raw Sphinx directives
are common.

You should also write high level documentation.

## Documentation engines

There are two documentation engines quite popular in Python. The oldest and most
used one is Sphinx - Python's own documentation is built in Sphinx! It has
received a lot of work and good themes lately, like Furo (PyPA) and
sphinx-pydata-theme (SciPy). It is also the basis for JuyterBook, which is what
this material was written in! It has third-party tooling to use markdown instead
of the default RestructredText, include notebooks as pages, and more. Sphinx
uses the aging docutils, which has an intermediate representation that produces
HTML, or other formats too, like ebooks and LaTeX. Example sites: pretty much
everything in Python.

The other engine is MkDocs. This is a clean fresh start built on top of
markdown. It's much faster than Sphinx, and writing a bit of code to execute
during generation is really easy - adding things like producing rendered output
from custom code is simple. The material theme is great. Many of the advantages
of MkDocs are matched by modern Sphinx with a bit of configuration. Example
sites: cibuildwheel & textual.

The documentation engine for C++ is called Doxygen. If you need to mix it with
Sphinx, use Breathe.
