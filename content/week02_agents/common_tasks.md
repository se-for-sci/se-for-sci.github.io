# Common tasks

Everyday jobs that an agent does well, such as small edits, docs, and release
chores. AI is good at things you do not want to spend time on. None of these
tasks are hard; they are just friction. An agent turns them into a one-line
request you can fire off while you do something else.

All the example prompts below are real prompts from real sessions; where the
result is public, the prompt links to the PR it produced.

## Small edits

Config tweaks, version bumps, adopting a new tool -- these are perfect
fire-and-forget tasks:

> Let's bump the upper limit on cmake to 4.4

—
[scikit-build-sample-projects#79](https://github.com/scikit-build/scikit-build-sample-projects/pull/79)

> Let's bump the actions to the latest versions in this PR. npx actionsup or
> something like that might help.

Notice the second prompt mentions a tool that might help, without being sure of
the details. That's fine; the agent will figure it out.

## Merge conflicts and rebases

Repetitive conflict resolution does not need a strong model or your hands. Often
one word is enough:

> rebase

With `AGENTS.md` set up (see [](./agents_md.md)), the agent tests the result and
fixes fallout too. It scales up naturally:

> Let's rebase all the PRs made by me now that CI works again.

And it can fold in related work while it is there:

> Rebase and update the changelog (try `nox -s make_changelog`)

> Rebase, cuda's been moved to extras

— [cuda-histogram#69](https://github.com/scikit-hep/cuda-histogram/pull/69)

## Conversion tasks

CI provider migrations, config format changes (`tox.ini` → `tox.toml`), docs
system moves, language ports, citation formats:

> Let's convert the gitbook to mystmd

— [CLI11#1389](https://github.com/CLIUtils/CLI11/pull/1389)

> Let's convert this example to nanobind

> Let's convert this to the new recipe format. There's an automated tool
> somewhere for that, can be run with pixi I think.

—
[histoprint-feedstock#21](https://github.com/conda-forge/histoprint-feedstock/pull/21)

```{tip}
Give it a link to the schema or a description of the target format. If an
existing project already uses the target, point at that instead:

> Let's switch from using prettier to rumdl, see ../se-for-sci.github.io which
> I think uses rumdl. It has a mystmd/jupyterbook mode.
```

## Fixing lints

Enable a lint with no autofix and let the agent iterate over the report. More
lint rules make agent output better overall, so this is a win-win: the agent
cleans up the existing violations, and the rule then keeps future agent (and
human) code honest.

> Can we also lint with prek on PRs?

— [SIMPLE-Py#23](https://github.com/scikit-build/SIMPLE-Py/pull/23)

> Let's update for ruff v0.16.0 - this can now be handled by ruff itself for
> markdown, anyway. The guide might need a few updates for 0.16 too.

— [cookie#833](https://github.com/scientific-python/cookie/pull/833)

## Better docs

Agents are good at converting code into readable text that pairs with the code.
They match existing style, move text inline, and fill missing details. A review
pass is as easy as:

> Review the docs

Good models will generally check for all the things you might want to check,
like consistency, grammar, formatting, broken links, and so on, but if you want
to be sure, you should specifically ask for it.

They are also good at finding drift between code and docs, and at making sure it
does not come back:

> In the docs, cp314-pyodide_wasm32 is missing. Are there any others missing? Is
> there a way to keep this from happening again?

— [cibuildwheel#2947](https://github.com/pypa/cibuildwheel/pull/2947)

> Docs still refer to `dynamic_metadata.plugins.<plugin>`, we removed the
> `.plugins` part.

—
[dynamic-metadata#88](https://github.com/scikit-build/dynamic-metadata/pull/88)

## One-off scripts

Plots, data analysis, Dockerfiles from shell history, quick tooling -- output
you use once and do not need to review as production code:

> Let's make a script that makes a plot of the minimum scikit-build-core
> versions set in these pyproject.toml's. The script can use PEP 723 for
> dependencies (packaging, plotting tools), and run with `uv run`.

Small web work fits here too: pages, JavaScript/TypeScript when you are rusty.
You can describe visuals in plain words:

> The github and documentation buttons don't have the frosted glass effect on
> the main page, they should have it too (tiles do already)

—
[scikit-build.github.io#10](https://github.com/scikit-build/scikit-build.github.io/pull/10)

## Release chores

Draft release notes or a changelog from the git log between two tags; the agent
mimics your existing style:

> What's new since last release?

> Fill out the changelog since last release

> Let's prepare the changelog and version number for a new patch release.

— [CLI11#1410](https://github.com/CLIUtils/CLI11/pull/1410)

> Merged. Let's make the gh release. Use the changelog to fill the description
> (as markdown).

— [plumbum v2.0.2](https://github.com/tomerfiliba/plumbum/releases/tag/v2.0.2)

## Reviving old work

Ask it to bring an outdated PR up to date with the current codebase, even one
that has been dead for years:

> Let's rebase #4272 and see if we can make it work.

— [pybind11#4272](https://github.com/pybind/pybind11/pull/4272), opened in 2022
and merged in 2026

> I want to reopen #1142 and rebase it on main (it was pointing at a branch that
> got merged).

— [nox#1142](https://github.com/wntrblm/nox/pull/1142), reopened and merged

## Tasks you never had time for

Small cleanups, dependency swaps, restructuring; the backlog items that were
hard to justify time for are now just a sentence and a little time in the
background:

> Let's remove the "needs-changelog" label infrastructure, it's not really
> needed anymore, and not kept up to date.

—
[boost-histogram#1164](https://github.com/scikit-hep/boost-histogram/pull/1164)

Also things you _wouldn't_ have done, because they were too much work, like
testing downstream projects before and after a change:

> What downstream projects need updates for this, from the ones I work on:
> packaging, cibuildwheel, cmake, scikit-build-core, ...

## Low-friction mixing

You can mix your own writing with agent work at any granularity. Leave `TODO`
comments while writing, then ask the AI to find and fix them. This works for
prose too:

> Here's a draft message, help me fill in the TODOs: ...

— the filled-in message became the description of
[boostorg/histogram#429](https://github.com/boostorg/histogram/pull/429)

You keep the structure and the voice; the agent fills in the mechanical parts.

## Exercise

```{exercise}
Try running a linter in `agentic-ai-example`, try adding a new rule.
```
