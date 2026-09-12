# Issue triage

How to sort, label, and reproduce reported issues with an agent.

## Ask the agent to survey open issues

You can ask the agent to look over issues, it will figure out how to use `gh` or
whatever it needs:

> Categorize all open issues. Highlight ones that are easy to close, and bugs
> that you can reproduce

Then close the closable issues by hand (such as with the `gh` tool), respond,
etc. The agent can help with any of this if you wish, but keep a human touch on
interactions.

Ask for a report with the categorized issues to guide your next steps.

To scale up, have it launch {term}`subagents <subagent>` to fix the bugs it was
able to reproduce, opening a draft PR for each. Ask for git worktrees so the
subagents do not step on each other, see [](./refactors.md).

A specific issue works too:

> Is #123 still broken?

## MWEs and tests

Agents are great at producing a minimal working example (MWE) of some bug you
are seeing. They can also adapt an MWE, or other things in an issue, into your
test suite as a regression test. See [](./writing_tests.md) for more on this.

## Fully automated?

It might seem attractive to have a fully automated system, but it's a bit early
for that. Attempts have been hacked by malicious issue titles with prompt
injection (instructions to an agent in the issue title). Comments can hide
prompt injection too. Do not run reporter-supplied text through an agent that
can act without human review.

```{note}
Remember, users should know if an AI is writing things for them to read. AI text
should be clearly marked.
```

## Exercise

```{exercise}
Triage the open issues of `agentic-ai-example`, and produce a ranked list with
reasons.
```
