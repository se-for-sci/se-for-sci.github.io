# Continuous Integration

There are a lot of services that can run code for you and integrate with git.
These CI services may be hosted for you, or sometimes you can host them
yourself.

What is CI for?

- Running tests (dynamic and static)
- Building documentation
- Building static websites
- Building packages and/or binaries and making releases
- Generating pull requests for updates and other maintenance

What are the benefits?

- Consistent, controlled environment between runs
- Runs every (PR / commit / tag / whatever you choose)
- Can't be skipped / forgotten, no contributor setup
- Can run lots of OS's, Python versions, compilers, etc.

Here are a few of the major CI services, with biased opinions:

- **Travis CI**: The original Linux CI service to provide free time for public
  projects. Many, many projects used this for years. It was bogged down by
  design that didn't allow easy upgrades and was hard to configure for anything
  other than pre-programmed defaults. The service slowly expanded to other
  platforms. The service still exists, but was sold off, has killed off most
  free support, requires a credit card to sign up, etc. It was/is one of the
  best places to get special architectures, due to Intel and other manufacturers
  supporting it. But that seems to also be dying.
- **Jenkins**: A self-host only OSS solution.
- **Appveyor**: The original Windows CI service. Has held up much better than
  Travis.
- **Circle CI**: The first more "modern" design. Limits free time for public
  projects, though.
- **GitLab CI**: For years, this was one of the best services, and one of the
  first to support running either self-hosted or centrally hosted (like GitLab
  itself). Works with other services too, but best with GitLab. Not as modular
  as the next two items on this list, but still very good.
- **Azure Pipelines** (Also called Azure DevOps): Microsoft's first try at a CI
  service. It shocked the industry when it was introduced due to the number of
  parallel jobs provided (10-20), as well as fantastic multiple OS support,
  including great Windows support. Extremely modular design is easy to upgrade
  and maintain. This service really focuses on all aspects of CI/CD, not just
  testing.
- **GitHub Actions** (GHA): Microsoft's second try took everything good from
  Azure and cleaned it up, simplified, and fixed non-backward compatible
  defaults. Microsoft still uses Azure as a bit of testing ground, bringing
  simpler redesigned versions of things to GHA. Extremely simple and close
  integration with GitHub. Modular Actions are easy to write and share.

## Introduction to GitHub Actions

GHA will be used in this class due to the flexible, extensible design and the
tight integration with the GitHub permissions model (and UI).

GHA is made up of workflows which consist of actions. Any file named
`.github/workflows/*.yml` is a workflow. In general, workflows are based on
events; you might have a `ci.yml` workflow for tests, and a `cd.yml` workflow
that publishes packages when you make a release.

### Simple workflow

Let's look at a simple workflow:

```yaml
on:
  pull_request:
  push:
    branches:
      - main

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install package
        run: python -m pip install .[test]

      - name: Test package
        run: python -m pytest
```

The most important key in this file is `on:`. This defines _when_ the workflow
runs. In this case, it runs on every pull request (`pull_request:` is present,
empty means all), and every time you push to the `main` branch. There are a lot
of events you can choose from, and a lot of controls inside each (like only
running when certain files change).

The `jobs:` dict is the other required key, and it has holds a dict with
arbitrary keys; we used the name `tests:`, but it could have been `hefalump:`
instead, it's the unique "id" of the job. Inside each job, you'll at least have
a `runs-on:` setting that tells GHA which operating system image to run on (like
`ubuntu-latests`, `ubunutu-22.04`, `macos-latest`, `windows-latest`, etc.) There
is also are required `steps:`, containing a list of steps.

GitHub Actions runs each step. Steps have an optional (but nice) `name:`. Then
they can either have a `uses:` key, which will load a GitHub "Action", or a
`runs:` key, which will run a shell command. There are a bunch of optional keys.
For example, you can specify the shell used on `run:` with `shell:`. Actions
also have a special `with:` key which takes a dict of configuration that the
action can see and act on. You can see the `setup-python` action above has a
(required) setting for the Python version called `python-version:`.

There are several "official" actions, stored in the `github.com/actions` org.
These have moving tags like "v3" that make it easy to pin this to something that
shouldn't intentionally break you, won't require you keep changing the tag
number, but will get reasonable security updates. The format for Actions is
`uses: <org>/<repo>@<tag>`, where the tag can be anything valid in git,
including a branch name or a SHA. (Advanced: This can also be a local git path,
and you can write your own local action)

Almost all jobs will use `actions/checkout`, which checks out the current
repository. There are actions for caching, for uploading "artifacts" (which are
simply things that you can download later, either in another job or onto your
computer), pushing websites to GitHub Pages, and more.

There are lots of third party actions available, as well. They were originally
written in Docker (linux only) or JavaScript, but now they can also be written
as a composite of other actions (including shell invocations), which makes
writing an Action just about as easy as writing a workflow job.

### Adding a matrix

One of the most common needs is to be able to run on multiple operating systems,
or with multiple versions of something like Python. GitHub Actions makes this
easy with a "matrix". This lets you set a matrix of options, and then you can
use them anywhere in the job.

First, let's look at a simple matrix:

```yaml
strategy:
  matrix:
    runs-on:
      - ubuntu-latest
      - windows-latest
```

The `matrix:` key (which is inside the `strategy:` key, which itself is inside
the specific job that's being parametrized) defines the matrix. You can specify
any key(s) you want, each containing a list. The job will run once for every
possible combination of these keys (hence the "matrix" name). In this example,
there will be two instances of the job: one with `matrix.runs-on` set to
`"ubuntu-latest"`, and the other with `matrix.runs-on` set to
`"windows-latest"`. This does _not_ do anything special to the runs-on key; you
still have to use the values when making the job. In this case, you'd use:

```yaml
runs-on: ${{ matrix.runs-on }}
```

These substitutions are available throughout the job, including in the `name:`
field - you should try to provide nice helpful names.

There are two special keys inside `matrix:`. One is `include:`, and the other is
`exclude:`. You can use these keys to add or remove items from the matrix. For
example:

```yaml
strategy:
  matrix:
    runs-on: [ubuntu-latest, windows-latest]
    python-version: ["3.9", "3.11"]
    include:
      - runs-on: macos-latest
        python-version: "3.10"
```

Will generate 5 jobs - ubuntu + 3.9, ubuntu + 3.11, windows + 3.9, windows +
3.11, and macos + 3.10.

(Advanced) You can also use this to add a new key to an existing run if all
pre-defined keys match an existing run.

There is also one more very useful setting inside `strategy:`, and that is
`fail-fast: false`. That will allow all items in the matrix to run even if one
fails - by default, GHA will stop the run as soon as one matrix item fails.

### Useful variables

There are a lot of useful variables available to you. One to highlight is
`runner.os`, which will tell you what OS you are on. It is usually better to
write `if: runner.os == "Linux"` over `if: matrix.runs-on == "ubuntu-latest"`,
since it is less fragile, especially if you use versioned image runners like
`ubuntu-22.04`; it also doesn't depend on whatever you named `runs-on` in your
matrix.

### Useful things to know

GitHub Actions (and Azure Pipelines, they use the same images) supplies pipx as
a supported ecosystem. So you can `pipx install` or even `pipx run` anything
from Python!

Nox (or other task runners) are very useful when combined with CI. You can set
up the complex bits of your workflow in nox, and verify it works locally. Then
your CI job can just run your nox file. This also means you could switch CI
providers easily if needed if you have very simple CI files.

You can run GitHub Actions locally! There's a tool called `act` that sets up and
runs your actions on your own machine (linux only, in docker, with small, large,
and accurate (huge) image options).

### Dependabot

It's a good idea to pin your actions, but also to keep them up to date. GitHub
provided a way to do this with dependabot. Just add the following file as
`.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Maintain dependencies for GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

This will check to see if there are updates to the action weekly, and will make
a PR if there are updates, including the changelog and commit summary in the PR.
If you select a name like `v1`, this should only look for updates of the same
form (since April 2022) - there is no need to restrict updates for "moving tag"
updates anymore. You can also use SHA's and dependabot will respect that too.

You can use this for other ecosystems too, including Python.

## Specific tasks

### Pre-commit

If you use [pre-commit](https://pre-commit.com) (and you should), and you don't
want to / can't use [pre-commit.ci](https://pre-commit.ci) yet, then this is a
job that will check pre-commit for you:

```yaml
lint:
  name: Lint
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.x"
    - uses: pre-commit/action@v3.0.1
```

If you do use [pre-commit.ci](https://pre-commit.ci), but you need this job to
run a manual check, like check-manifest, then you can keep it but just use
`with: extra_args: --all-files --hook-stage manual check-manifest` to run just
this one check. You can also use `needs: lint` in your other jobs to keep them
from running if the lint check does not pass.

### Unit tests

Implementing unit tests is also easy. Since you should be following best
practices listed in the previous sections, this becomes an almost directly
copy-and-paste formula, regardless of the package details. You might need to
adjust the Python versions to suit your taste; you can also test on different
OS's if you'd like by adding them to the matrix and inputting them into
`runs-on`.

```yaml
tests:
  runs-on: ubuntu-latest
  strategy:
    fail-fast: false
    matrix:
      python-version:
        - "3.9"
        - "3.12"
  name: Check Python ${{ matrix.python-version }}
  steps:
    - uses: actions/checkout@v4

    - name: Setup Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install package
      run: python -m pip install -e .[test]

    - name: Test package
      run: python -m pytest
```

A few things to note from above:

The matrix should contain the versions you are interested in. You can also test
on other OS's if you are building any extensions or are worried about your
package on macOS or Windows. Fail-fast is optional.

The formula here for installing should be identical for all users; and using
[PEP 517](https://www.python.org/dev/peps/pep-0517/)/[518](https://www.python.org/dev/peps/pep-0518/)
builds, you are even guaranteed a consistent wheel will be produced just as if
you were building a final package.

## Common needs

### Single OS steps

If you need to have a step run only on a specific OS, use an if on that step
with `runner.os`:

```yaml
if: runner.os != 'Windows' # also 'macOS' and 'Linux'
```

Using `runner.os` is better than `matrix.<something>`. You also have an
environment variable `$RUNNER_OS` as well. Single quotes are required here.

### Changing the environment in a step

If you need to change environment variables for later steps, such combining with
an if condition for only for one OS, then you add it to a special file:

```yaml
run: echo "MY_VAR=1" >> $GITHUB_ENV
```

Later steps will see this environment variable.

### Common useful actions

There are a variety of useful actions. There are GitHub supplied ones:

- [actions/checkout](https://github.com/actions/checkout): Almost always the
  first action. v2+ does not keep Git history unless `with: fetch-depth: 0` is
  included (important for SCM versioning). v1 works on very old docker images.
- [actions/setup-python](https://github.com/actions/setup-python): Do not use
  v1; v2+ can setup any Python, including uninstalled ones and pre-releases. v4
  requires a Python version to be selected.
- [actions/cache](https://github.com/actions/cache): Can store files and restore
  them on future runs, with a settable key.
- [actions/upload-artifact](https://github.com/actions/upload-artifact): Upload
  a file to be accessed from the UI or from a later job.
- [actions/download-artifact](https://github.com/actions/download-artifact):
  Download a file that was previously uploaded, often for releasing. Match
  upload-artifact version.

And many other useful ones:

- [ilammy/msvc-dev-cmd](https://github.com/ilammy/msvc-dev-cmd): Setup MSVC
  compilers.
- [jwlawson/actions-setup-cmake](https://github.com/jwlawson/actions-setup-cmake):
  Setup any version of CMake on almost any image.
- [wntrblm/nox](https://github.com/wntrblm/nox): Setup all versions of Python
  and provide nox.
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish):
  Publish Python packages to PyPI.
- [pre-commit/action](https://github.com/pre-commit/action): Run pre-commit with
  built-in caching.
- [conda-incubator/setup-miniconda](https://github.com/conda-incubator/setup-miniconda):
  Setup conda or mamba on GitHub Actions.
- [ruby/setup-ruby](https://github.com/ruby/setup-ruby) Setup Ruby if you need
  it for something.

There are also a few useful tools installed which can really simplify your
workflow or adding custom actions. This includes system package managers (like
brew, chocolaty, NuGet, Vcpkg, etc), as well as a fantastic cross platform one:

- [pipx](https://github.com/pypy/pipx): This is pre-installed on all runners
  (GitHub uses to set up other things), and is kept up to date. It enables you
  to use any PyPI application in a single line with `pipx run <app>`.

You can also run GitHub Actions locally:

- [act](https://github.com/nektos/act): Run GitHub Actions in a docker image
  locally.

### Custom actions

You can
[write your own actions](https://docs.github.com/en/actions/creating-actions)
locally or in a shared GitHub repo in either GitHub actions syntax itself
(called "composite"), JavaScript, or Docker. Combined with pipx, composite
actions are very easy to write!

You can also make reusable workflows.

### GitHub pages

GitHub has finished moving their pages build infrastructure to Actions, and they
[now provide](https://github.blog/changelog/2022-07-27-github-pages-custom-github-actions-workflows-beta/)
the ability to directly push to Pages from Actions. This replaced the old
workarounds of (force) pushing output to a branch or to separate repository.

<details markdown="1"><summary>Setting up GitHub Pages custom builds</summary>

Before starting, make sure in the Pages settings the source is set to "Actions".

You'll probably want this job to run on both your main branch, as well as
`workflow_dispatch`, just in case you want to manually trigger a rebuild. You
should set the permission so that the built-in `GITHUB_TOKEN` can write to
pages:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

You probably only want one deployment at a time, so you can use:

```yaml
concurrency:
  group: "pages"
  cancel-in-progress: true
```

Now you'll want three custom actions in your `steps:`. First, you need to
configure Pages.

```yaml
- name: Setup Pages
  id: pages
  uses: actions/configure-pages@v2
```

Notice this action sets an `id:`; this will allow you to use the outputs from
this action later; specifically, may want to use
`${{ steps.pages.outputs.base_path }}` when building (you can also get `origin`,
`base_url`, or `host` - see the action
[config](https://github.com/actions/configure-pages/blob/main/action.yml)).

```yaml
- name: Upload artifact
  uses: actions/upload-pages-artifact@v1
```

This actions defaults to uploading `_site`, but you can give any `with: path:`
if you want, including `"."` which is the whole repository.

Finally, you'll need to deploy the artifact (named `github-pages`) to Pages. You
can make this a custom job with `needs:` pointing at your previous job (in this
example, the previous job is called `build`):

```yaml
deploy:
  environment:
    name: github-pages
    url: ${{ steps.deployment.outputs.page_url }}
  runs-on: ubuntu-latest
  needs: [build]
  steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v1
```

The deploy-pages job gives a `page_url`, which is the same as `base_url` on the
configure step, and can be set in the `environment`. If you want to do
everything in one job, you only need one of these.

See the
[official starter workflows](https://github.com/actions/starter-workflows/tree/main/pages)
for examples.

</details>

## Advanced usage

These are some things you might need.

### Cancel existing runs

If you add the following, you can ensure only one run per PR/branch happens at a
time, cancelling the old run when a new one starts:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Anything with a matching group name will count in the same group - the ref is
the "from" name for the PR. If you want, you can replace `github.ref` with
`github.event.pull_request.number || github.sha`; this will still cancel on PR
pushes but will build each commit on `main`.

## Setting up pre-commit.ci

To set up pre-commit.ci, visit <https://pre-commit.ci>.

This has two benefits: it can update your hooks weekly/monthly/quarterly, and it
can automatically push fixes to pull requests.
