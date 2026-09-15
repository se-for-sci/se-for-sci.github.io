# New features

While building a new feature, agentic AI can also save you time by generating
the code you want to write. However, some of the time you save will be spent on
carefully constructing your prompt, reviewing the work, and possibly iterating
on it if you are not happy with the result. It is also the place where AI is
most likely to go astray, since there are no tests to constrain the new code and
the guidelines are only as good as your prompt. Still, there are some practices
that can make the process more efficient and less error-prone. As in earlier
chapters, the quoted prompts below are real, with links to the resulting PRs
where public.

## Plan first

It is a good habit to separate planning from implementation. Most
{term}`harnesses <harness>` have a plan mode, where the agent explores the
codebase and proposes an approach without editing anything (editing and most
other tools are disabled in this mode). A good agent will find weak or vague
points in your idea, point out parts of the codebase that will require extra
attention, and ask you questions that you might not have thought about yet.
Answering those questions before any code exists is far better than discovering
the same problems in review.

> I'd like to support optional pre-compilation to speed up usage (header only
> libraries are slow). This is similar to how nanobind works (though I believe
> it's not optional there), and there was an attempt here:
> <https://github.com/pybind/pybind11/pull/2445> tried to start this. It should
> be easy to use from cmake (maybe meson too, if possible), and have a pretty
> simple user-facing mechanism for users not using a supported build system.

- **Edit the plan before it starts.**

  Most harnesses generate a plan file that you can read and modify. Treat it as
  the specification for the work. Removing a step you disagree with, or adding a
  constraint the agent missed, takes a minute and can save you an entire wasted
  implementation. It is also useful to write the plan in the form of a
  checklist, so you can tick off each step as it is completed, and be able to
  resume in another session without the agent having to figure out what has
  already been done. Plans are also durable: you can refine one across sessions,
  and point it at prior art:

  > The code has updated a bit, make sure line numbers are up to date in the
  > plan. Also, check <https://github.com/cliutils/cli11>, which has a good
  > optional precompile and even C++20 module support. Update the plan if there
  > are any improvements from looking at CLI11.

  — [pybind11#6118](https://github.com/pybind/pybind11/pull/6118)

- **Mix model tiers.**

  Planning is where judgment matters the most, and implementation is often
  mechanical once the plan is good. A common and cost-effective pattern is to
  have a strong model produce the plan, then hand it to a cheaper "workhorse"
  model to carry it out. This works because the plan pins down the decisions
  that a weaker model might get wrong.

- **Save the plan where the work lives.**

  Posting the plan as a comment on the issue or pull request gives your
  collaborators a chance to object early, and gives a future agent (or a future
  you) the context behind the change. It also makes the eventual review much
  easier, since the reviewer can check the code against a stated intent instead
  of guessing at one.

  A real example:
  [scikit-build-core#1324](https://github.com/scikit-build/scikit-build-core/issues/1324)
  is a plan for speeding up the test suite, built in plan mode and posted as an
  issue, with the decisions made during planning recorded in it. The PR that
  closed it
  ([#1325](https://github.com/scikit-build/scikit-build-core/pull/1325)) could
  then be reviewed against the stated plan; the profiling side of that change
  appears in [](./profiling.md).

## Implementing from a specification

Agents are very good at working from a written specification. If the feature is
already described somewhere (e.g. a PEP, an issue with a detailed proposal, an
RFC, a design document), you can point the agent directly at it, add whatever
extra details are specific to your codebase, and let it work. The specification
does the same job that a test does in test-driven development (see
[Writing tests](./writing_tests.md)): it constrains the agent to a behavior you
have already agreed on, rather than one it invented.

> Now that we have a new Python discovery system, we should be able to support
> the requires-python option of PEP 723.

— [nox#1142](https://github.com/wntrblm/nox/pull/1142) (the same PR later
revived in [](./common_tasks.md))

This works well in practice for things like implementing a new PEP in a library,
or adding a feature to a build-backend plugin where the interface is already
documented. The more precise the source material, the less supervision the
implementation needs. A reference implementation works as a spec too:

> Let's add support for dynamic-metadata. It is described in
> ../../scikit-build/dynamic-metadata and it is implemented in
> ../../scikit-build/scikit-build-core.

## Prototype to decide

Not every feature is worth building, and it is often hard to tell in advance.
Agentic AI makes it cheap enough to build a rough version and find out. Does the
approach work? Is it fast enough (see [Profiling](./profiling.md))? Once you can
hold it, do you even like the design?

The important part is that the prototype has done its job regardless of what
happens to the code. You might keep the AI version, polish it into something you
are happy to maintain, or throw it away and write it yourself now that you know
what you want. All three are good outcomes, and none of them require you to have
committed to the feature before you had evidence. This scales to comparing whole
alternatives:

> Let's evaluate mkdocs replacements. Launch opus agents in worktrees to try
> zensical, properdocs, and greatdocs as replacements.

— the winner became
[cibuildwheel#2946](https://github.com/pypa/cibuildwheel/pull/2946)

```{note} Model choice matters when building features
This is the place to use the best model you have available. You are asking for
novel code rather than a mechanical transformation, so you want the highest
chance that what comes back is usable. A weak model here produces
plausible-looking code that costs you far more time in review than it saved in
writing.
```

## Validate beyond your own repo

Your own test suite only tells you the feature runs. A few cheap ways to find
out whether the feature is any good:

- **Adapt a downstream project to use the new feature.**

  Have the agent take a real project that would benefit from the feature and
  convert it, then report the pain points. This surfaces interface problems that
  are invisible from inside your own codebase.

  > Let's try out <https://github.com/boostorg/histogram/pull/429>. We need to
  > replace our home-grown implementation in Python with the new feature. I'd
  > like feedback on the new feature, does it work for us?

  That report went straight back into the upstream PR:

  > I tried this downstream in the boost-histogram Python bindings, and got this
  > feedback: **The one real concern is performance at scale.** ... on a
  > 1000×500×50 histogram picking half the bins on two axes, `reduce` takes
  > **320 ms vs 38 ms** for the old vectorized `np.take` path — ~8× slower

  The same works for unreleased dependencies: check out someone else's PR and
  build against it, so your feedback arrives before the API is frozen.

- **Have the agent try to break it.**

  Ask for edge cases, invalid inputs, and unusual combinations of options.
  Agents are good at this (see [Reviewing](./reviewing.md)), and anything it
  finds is worth an issue reproducer in the test suite.

- **Have it follow your own documentation.**

  Point the agent at the tutorial or README you just wrote and have it work
  through the steps as a new user would, reporting anything that is missing,
  wrong, or confusing. Documentation gaps are easy to miss when you already know
  how the feature works.

## The real cost is after generation

Review, not generation, is the bottleneck (see [](./reviewing.md)), and a new
feature is where that bites hardest: the diff is large and there is no existing
behavior to check it against.

The practical way to keep this under control is to iterate instead of trying to
one-shot the feature. Talk to the agent while it works: redirect it when it
heads somewhere you did not intend, ask it to explain a decision you do not
follow, and have it fix the parts you are unhappy with. You do not need to
hand-edit the code yourself, but you do need to keep iterating until it meets
the standards you would apply to your own work. Reviewing in small pieces as
they arrive is much easier than reviewing everything at the end. If you would
not merge it from a human contributor, do not merge it from the agent.

## Exercise

```{exercise}
Take a small written spec, plan it out in plan mode, implement it in
`agentic-ai-example`, and review the result. Ideas: a scatter plot artist, a
log-scale axis, or axis labels/titles.
```
