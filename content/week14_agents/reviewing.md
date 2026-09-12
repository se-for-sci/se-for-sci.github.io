# Reviewing

How to review text, code, and pull requests with an agent.

You can review almost anything. You might already know that you can copy
non-confidential documents into a chatbot and ask for a review; your agent can
do a lot more too. You can also use local models to help (a little) with private
material.

```{tip}
While reviewing, it is important to remember to manage your context. Unless you
are reviewing the codebase or project as a whole, it works best to clear the
context every time you switch to reviewing a new file, PR, feature, or document.
```

## Reviewing text

You can ask for reviews of documentation, plans, and just about any text in a
repository. You can ask for a general review, which will catch a variety of
things like grammar, and you can also ask for reviews into specific things. Some
examples:

> Check all the code snippets and make sure they are valid, run correctly, and
> follow the project guidelines.

> Look for things that could use links.

> Is anything outdated?

> Scan the repo and collect all the public API, check the documentation and look
> for gaps. Is everything covered?

> You are an NSF reviewer for call <call name> described in detail at <RFP URL>.
> Critically evaluate this proposal.

Don't mix tasks in a single context; if you have a specific ask, that will
affect a general one. "Review this and also check for links" will likely focus
nearly entirely on links, for example.

## Reviewing PRs

AI has gotten really good at reviewing PRs / changesets. There are several
options:

### Review tool

Most {term}`harnesses <harness>` have a built-in option, usually `/review` or
similar. You might need to give it further information, like a PR number,
branch, etc.

This is a great place to start. Try it out on a PR.

### Adversarial review

Another thing you can try is an adversarial review. Try something like this:

> You are an adversarial reviewer for the new feature in this branch. Do you see
> any problems? Anything that could be done or written more cleanly? Can you
> break it?

This is a real prompt too; it was used (more than once) while developing
[nox#1131](https://github.com/wntrblm/nox/pull/1131), parallel session support.

### Simplifying review

Claude Code has this as `/simplify`, but you can prompt it yourself. The key
idea is to use four {term}`subagents <subagent>`[^1], each looking for a
specific type of simplification. These are:

[^1]:
    Subagents are agents that have a fresh context, they don't have to run in
    parallel (though they might).

- Altitude
- Reuse
- Simplification
- Efficiency

They report back, and any findings that check out as correct are applied.

## Reviewing AI with AI (Rubber Duck)

AI review is a powerful tool for AI-generated code. To be most effective, you
should have two models of similar level from different model families. By using
one as the implementer, and the other as the reviewer, you can get better
results than a single model alone, much of the way to the next model class
above. This is called Rubber Duck, and it is built into GitHub Copilot CLI;
GitHub reports that Claude Sonnet 4.6 reviewed by GPT-5.4 closed 74.7% of the
gap to Claude Opus 4.6 running alone.[^rubber-duck]

[^rubber-duck]:
    [GitHub Copilot CLI combines model families for a second opinion](https://github.blog/ai-and-ml/github-copilot/github-copilot-cli-combines-model-families-for-a-second-opinion/),
    Nick McKenna and Bartek Perz, 2026-04-06.

If you try this with matching models, they will generally just praise the work.
If the reviewer is a model class above the implementer, it does work (but then
you could have just used the better model to do the implementation).

This is also why it's nice to let reviewers know what model(s) you used in PRs.

## Human in the loop

AI writes code really fast, often code that looks really well thought out (and
sometimes is, depending on lots of factors). Review is more of a bottleneck. AI
is also good at helping review; you can review code much faster with an AI
helping you.

An important, rather new bottleneck is actually _design_; is some new feature
you've thought about for 10 minutes a good fit? Are you willing to support this
API forever? Is the extra code worth it? This was less noticeable when a new
feature took much longer and more effort.

One thing you can do is to use AI to simulate downstream. You can ask it to
adopt your new feature in a library that uses yours and report on how well it
works.
