# Refactors

How to make large structural changes safely. As in earlier chapters, the quoted
prompts are real, with links to the resulting PRs where public.

## Write the plan, let the agent implement it

Refactors that stalled for years because they were too tedious are now a plan
file away. Write (or dictate) the plan, let the agent implement it; it will
likely work and pass the tests. Then it is your call: is the new structure
better, and worth the churn? A passing refactor you discard still taught you
something cheap.

## Example refactors

Restructuring files and breaking up modules:

> This still looks complex, I think because the machinery and options sit in the
> same file. Reevaluate the locations of items in _options.py and
> \_options_set.py - and maybe we even need a new \_options_?.py?

— [nox#1144](https://github.com/wntrblm/nox/pull/1144)

Removing a dependency or a long-dead workaround:

> Launch an opus agent to make a PR to move off of
> build.util.project_wheel_metadata in a worktree.

—
[scikit-build-core#1494](https://github.com/scikit-build/scikit-build-core/pull/1494)

> Launch a agent to remove WORKAROUND_ENABLING_ROLLBACK_OF_PR3068 in a worktree,
> making a PR

— [pybind11#6109](https://github.com/pybind/pybind11/pull/6109)

Other classics: swapping click for argparse, converting decorators to fixtures,
language migrations (JavaScript → TypeScript, see [](./repetitive_work.md)), and
packaging a webapp properly.

## Safety nets make refactoring possible

A solid test suite, linters, and a type checker are what let the agent (and you)
trust a large change; the refactor is only as safe as the checks it must pass.
This pays forward, too: simpler, better-structured code is easier for the AI to
work on next time, just as it is for humans.

For changes too large for one PR, stage them. Multi-phase changes that failed by
hand, like a two-phase framework upgrade, can succeed with an agent because each
phase gets verified and fixed before the next, instead of one giant leap.
Splitting also makes review humane:

> Let's break out into 5 other PRs, and reduce this PR to just the remaining
> item. Feel free to use subagents in worktrees. Edit the description of this
> one when done.

— [iminuit#1145](https://github.com/scikit-hep/iminuit/pull/1145) through
[#1149](https://github.com/scikit-hep/iminuit/pull/1149)

## Working in parallel

Nothing stops you from running several refactors at once, in separate clones or
`git worktree` checkouts; the prompts above do exactly that.
{term}`Harnesses <harness>` can manage worktrees for their
{term}`subagents <subagent>`; you review the resulting PRs one at a time. Larger
models reach for worktrees on their own; with a smaller model, ask for them.

## Know your git

Big refactors mean rebases, force-pushes, history rewriting, and the occasional
reflog rescue. You must know these well enough to direct the agent or do them
yourself. Harnesses are (sensibly) shy about history manipulation, but will do
it when asked clearly:

> Let's commit, rebase, then force-push

> Let's gitignore .venv folders, and rewrite history to remove them (oops!)

History is part of the deliverable, too:

> Can we restructure the history to tell a story?

## Spare subscription time? Point it at cleanups

If you have agent capacity left at the end of a billing cycle, aim it at the
backlog: hunt for simplifications and bugs, or compare the documentation against
the implementation.

> Sure, let's do safe stuff and cleanup. Break into PRs as needed, use opus
> agents.

## Exercise

```{exercise}
Run a prepared refactor plan on `agentic-ai-example` (for example, split
`artists.py` into one module per artist, or extract the ANSI handling from
`canvas.py`) and validate it with the test suite.
```
