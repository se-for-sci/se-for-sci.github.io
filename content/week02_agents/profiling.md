# Profiling

Profiling and optimizing code is generally a time-consuming process, due to
repeated iterations that often involve trial-and-error. Agentic AI can help
speed this up by writing profiling scripts, finding hotspots, trying
alternatives, and measuring the results, all with little human intervention
required. AI does well here because the goal is clear (make it faster, use less
memory, or make it more efficient in some particular way) while sticking with
the design and requirements that the test suite enforces (see
[Writing tests](./writing_tests.md)). As in earlier chapters, the quoted prompts
below are real, with links to the resulting PRs where public.

## Start profiling

All it takes is a single prompt to get started. For example, you can ask the
agent to profile a function in your codebase, and it will come up with a plan
for how to do it. It starts by identifying the right tool for the job (e.g.
`cProfile` for Python or `perf` for compiled binaries). It handles the verbose
raw output from these lower-level tools well - the kind of thing people usually
skim or need a separate viewer to interpret. If a profiler is not available, or
the profiler requires permissions that you don't have, it will find alternative
approaches like temporarily modifying the code to identify time-consuming
pieces. It can also set up a script to run through common workflows and collect
the results to make them easier to analyze.

> Let's fix the fill_n performance issue. How much faster might that make
> something like boost_histogram (the Python bindings)?

— [boostorg/histogram#439](https://github.com/boostorg/histogram/pull/439)

Runtime is not the only thing worth measuring. Compile time, memory usage, and
binary size are all fair targets, and the workflow is the same:

> I'd like to make this compile a bit faster with less memory usage, especially
> at the linking stage. See if there's some way to improve compiling. One idea
> is explicit instantiation on templates, perhaps?

—
[boost-histogram#1160](https://github.com/scikit-hep/boost-histogram/pull/1160)

The test suite itself is a good target too.
[scikit-build-core#1325](https://github.com/scikit-build/scikit-build-core/pull/1325)
started from real `--durations=20` data on the slowest (13-17 minute) Windows CI
jobs, then roughly halved them by consolidating 32 identical test installs into
4, swapping C++ sample packages for plain C where bindings were not under test,
and removing a network fetch. The plan behind it was posted as an issue first
(see [](./new_features.md)).

```{caution} Verify the measurement
Check what the script actually times before trusting conclusions.
```

## Iterate on performance

Trying out different ideas is easy with agentic AI. You can try many more
options, and attempt riskier or more complex ideas than you would normally do by
hand, since wasteful iterations are much less costly. The agent can also suggest
new approaches to improve performance, and help you avoid common pitfalls (e.g.
benchmark noise, cache effects, thermal throttling). However, you have a better
understanding of the bigger picture, so it works best when you provide guidance
and constraints.

A real iteration looks like a conversation, each message a new idea to measure
(these three are consecutive prompts from one session on a pull request review):

> Does this PR have a performance impact?

> Is there any other way to do the re.search's job that might be better?

> What about fusing it into tokenization, would that be faster?

Insist on controls, too -- an agent will happily report a speedup without a
baseline unless you ask:

> I did a run with the current change. Could you also do a run with the change
> reverted?

— [boostorg/histogram#439](https://github.com/boostorg/histogram/pull/439)

## When to profile

This will depend on your specific situation and will be up to your discretion.
AI makes it easy enough that you could profile after each change, or just when
the change is big enough or complex enough that you feel the need to do so.

Another common case is when you notice that something is running slower than it
used to be. You can ask the agent to check older versions and compare the
performance. It can then help you identify the change that caused the slowdown,
and suggest ways to fix it.

> Let's run the benchmarking suite (asv) for 3.14 for all tagged versions and
> current main.

You can also measure a change before it is merged, including someone else's.
This prompt was run in three different downstream projects to evaluate the same
upstream PR:

> Let's try pybind11's #6138 PR here. Enable the optional precompile mode, and
> see if it compiles faster and/or with less memory, and if the binaries change
> size.

— evaluating [pybind11#6138](https://github.com/pybind/pybind11/pull/6138), the
feature planned in [](./new_features.md)

## One-off vs. lasting

The one-off profiling scripts that we have mentioned are a uniquely AI-shaped
task, since most people won't spend the time to write them just to profile a
specific thing. But throwaway scripts get thrown away, sometimes before you are
done with them:

> What's the exact command to rerun that profile (it got removed)?

If you find yourself profiling the same thing repeatedly, it is worth investing
in a more permanent solution. For example, you could have the agent help you
build a benchmark suite (e.g. [ASV](https://asv.readthedocs.io/en/stable/)) that
can be run automatically to track performance over time, or fold the one-off
measurements into a suite you already have:

> We have a benchmarking system in the repo, integrate those benchmarks in there

— [boostorg/histogram#439](https://github.com/boostorg/histogram/pull/439)

## Exercise

```{exercise}
Profile a slow function in `agentic-ai-example`, test two optimization ideas,
and report the numbers.
```
