# CI and bugfixes

How to find the cause of a failed CI run and fix the bug behind it.

## Pass / fail

Agentic AI is very good at making something pass a check. It can iterate
tirelessly with a stubborn CI job to find some way to make it pass. It can add
debug statements and trace down failures. It is happy to search and read long
obscure logs. It also has a deep knowledge of facts, which helps it work out
obscure bugs; but facts are not pass/fail checks, so sometimes it hallucinates
them.

If CI is failing, just ask:

> Fix the failing CI on this PR

(You can even go shorter usually, like "check CI").

You can pass it the URL of a specific flaky run if you want. This is useful from
the main branch if you are fixing a flake that was not related to the PR it
occurred in. The agent may read runs with `gh run view`, so make sure `gh` is
authenticated for the repository first.

```{warning}
The cheapest way to make a check pass is to weaken the check. Watch for skips,
loosened tolerances, deleted assertions, and tests that now assert the buggy
behavior. Read the diff, not just the green mark.
```

## Bisect

You can use AI to do a `git bisect`. It can do the setup, preparing something to
pass/fail, and interact with the process. In fact, you don't really need to
describe in detail, just ask for the commit when something started failing:

> Find the commit where `test_foo` started failing

Give it a reliable reproducer first. A bisect on a flaky test wastes many runs
and can point at the wrong commit.

## Issues to fixes

Using AI to turn a list of issues into a list of fix PRs can be really useful;
you can review the fix instead of the problem. See [](./issue_triage.md) for how
to get to that list of issues. These fix PRs are often easier to review than
contributor PRs; you know the model and what it was trying to fix, rather than
having to also judge the quality of the PR and validity of every change. But
keep in mind that just because something passes (which AI is good at!), doesn't
mean it's correct or the best fix. Great tests and lints become more important
with AI; the harder it is to produce an incorrect fix, the better.

```{tip}
Add regression tests first, then fix. High end models and {term}`harnesses <harness>` might do
this for you; you can always request this in your user AGENTS.md or project
AGENTS.md files, see [](./agents_md.md) and [](./writing_tests.md).
```

## Exercise

```{exercise}
Break something in `agentic-ai-example`, push it, and ask an agent to fix the
failing CI. Check the diff: did it fix the bug, or the check?
```
