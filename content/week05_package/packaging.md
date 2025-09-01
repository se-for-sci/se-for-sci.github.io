# Packaging and quality control

[Slides](https://se-for-sci.github.io/slides/week-05-1)

Now you have your Git Repo, it's time to talk about how you structure it to make
it distributable and usable by others. We'll focus on building a Python package,
though most of the ideas here are available in other ecosystems for modern
languages. C, C++, and Fortran stick out a bit for not having things like
standard package managers; you can substitute a build system for these.

## Pip / uv and PyPI

Most languages have at least one package manager; "pip" is the canonical package
manager for Python. To distribute packages for pip to install, either SDists or
wheels are distributed on PyPI, a service with free hosting.

An SDist is a source distribution; there is one for all platforms, and it has to
be "built" (assembled from files, including compilation if there are C/C++ or
other compiled extensions in it).

A Wheel is a "built" distribution - it is simply unpacked into the correct
locations (generally "site-packages"), and you are ready to go. These are either
pure-python (in which case they work everywhere), or more specific wheels that
work on a certain platform and/or for specific Python versions.

When you type:

```console
$ pip install numpy
```

Then pip looks on PyPI for a package named numpy. Once it finds it, it selects
the newest version and checks to see if there is a matching wheel for your
platform. If it finds multiple matching wheels, it selects the most specific one
(this is fairly rare). If there are no matching wheels, pip reverts to the
source and builds that.

It unpacks it or installs it to your global site-packages if you have
permission, or to your user's site-packages if you don't, or if you are in a
virtual environment (more on those later), then it installs into that
environment's site-packages.

There is also a Rust rewrite of pip (and several other tools) called "uv" that
is faster (think 10-100x faster) and has an alternate high-level API. It's only
about a year old, but already 20% of the PyPI downloads are now via uv.

## Conda/Mamba/MicroMamba/Pixi and conda-forge

Wheels have been a huge success in binary packaging, but before wheels solved
many of the problems with binary packaging, conda was developed with different
solutions. Conda is a multipurpose packager with an ecosystem that has a strong
Python focus, though it can distribute any sort of package, and includes at
least 1-2 other ecosystems like R.

Building conda packages is either done by the company Anaconda (with
restrictions on commercial use), or by the OSS community in the "conda-forge"
channel, a massive (10K+) collection of community maintained recipes building
packages via centrally managed mechanisms. There are also a few other channels
for specific ecosystems, like bioconda.

Conda packages tend to be a lot larger, because they bundle in more
dependencies. Binary wheels generally target a minimal subset of the host system
that works everywhere, while conda packages bundle everything and are build with
custom toolchains. Conda distributes Python itself - it's just another
dependency to Conda, while Pip can only install to an existing Python.

There are several packages, so here's a quick summary:

- **Conda**: The original, written in Python. The resolver is now from Mamba, so
  it's much closer to speed in mamba that is used to be. a large ecosystem.
- **Mamba**: A faster, drop-in replacement for conda that uses a different
  dependency resolver and is written in C++.
- **MicroMamba**: Used to be different from Mamba, but now is simply a
  statically linked version of Mamba.
- **Pixi**: A Rust rewrite of conda, designed around a new high-level API.
  Unlike uv, it does not have a low-level API to match conda/mamba.

It turns out, writing a tool that can get Python, in Python, has bad
chicken-and-egg problem. That's why it's been rewritten not once, but twice, in
compiled languages.

Which do you pick? I'll focus on PyPI; it's the "official" ecosystem, and most
conda packages just build PyPI packages. But there are often places (like ML)
where conda is preferred. Unless you are making your own package (in which case
nearly always start with PyPI). Both systems have great ways to manage
environments and can do some form of locking, which is all you need for an
"application" style project.
