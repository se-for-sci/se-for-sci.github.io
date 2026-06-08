# Setting up Agentic AI

{button}`Slides <https://se-for-sci.github.io/slides/week-14-1>`

Agentic AI is the most significant change to software engineering ever. It is
also still a fast-changing field; we'll try to balance general advice and
specific examples that might change.

## LLM details

The core of agentic programming is an LLM, large language model. These are
simply completion engines trained on lots of data with a limited enough number
of parameters so that they learn concepts from the dataset.

Models don't take letters in, they take tokens. That's why you can't ask a model
to count the "r"'s in "strawberry" - it doesn't actually see the word that way.
Tokenization is model specific; Claude Opus 4.7 has a finer tokenization than
Opus 4.6. (Different tokenizations are usually associated with a newly trained
model, rather than just updated weights, but model numbering has social
implications.)

## Selecting a harness

The first thing you'll interact with is the harness. These tend to come in three
flavors:

- **TUI**, short for Terminal User Interface. These run in your terminal. Works
  anywhere, including on clusters.
- **GUI**, short for Graphical User Interface. These are stand-alone application
  with custom graphics. These can often do a little more than TUI's, like render
  webpage previews.
- **Editor plugins**: These run in your editor, usually looking like a chat
  window alongside the normal editor.

Most harnesses come in all three flavors, you just pick the one you like
interacting with best. Some harnesses are more feature rich in one flavor. For
example, Copilot usually adds features to the editor plugin first. Claude Code
and OpenCode favor the TUI.

There's a second component to harnesses, and it's really important: the **system
prompt**. The reason most model providers have a harness is to provide a system
prompt that is customized to that model. Model specific customizations are
likely not really needed, especially for larger models, so feel free to explore
if you can. But note that's likely the biggest difference between the same model
using different harnesses.

Some providers (like Anthropic) require you use their harness to use
subscription coding, so you don't get a choice. (Providers can cache the prompt
tokens, reducing the cost and latency of the 10k-30k tokens of system prompt).

Harnesses provide **tools**, which are things the model can call to perform
operations. Models are mostly smart enough to figure out how to use tools, and
most harnesses provide a small set of useful tools, so this isn't usually an
issue except maybe for small local models.

This is what makes Agentic AI special, and more useful than a simple chat; the
model can call tools, read output, and loop, fixing mistakes, just like a human
would. Many other things in this course - tests, formatters, linters, type
checking, and CI all feed into the agentic loop, letting the agent correct
mistakes and produce high quality output.

Most harnesses have these features:

- `/` commands - these control the harness. Common examples:
  - `/init`: Set up or update the `AGENTS.md` file (equivalent)
  - `/restore` (or `/sessions`): open up a previous session
  - `/review`: Review a PR and/or other diff (depends on the harness)
- `@` to load files into context (just mentioning them works too, but it's up to
  the model to load all or parts)

## Selecting a model

There are different levels of models, with different costs / subscription usages
associated with them. Small open source models can even run locally. Some models
are faster than others, too. In general, if you are just learning about agentic
AI, you should use a fairly powerful model, so you don't hit model limitations.
Once you've used it for a bit, then you can start matching model strength to the
problem description. You often have an "effort level" toggle as well. Using a
strong model with a high effort level on a simple task can actually overengineer
sometimes.

Here's a current breakdown of some current models:

- Frontier models: Claude Opus, GPT 5.5
- Workhorse models: Claude Sonnet, GPT 5.4, Kimi K2.6, Composer 2.5
- Simple models: Claude Haiku, GPT 5.4 mini
- Local models: Gemma 4, Qwen 3.6

(GLM 5.1 sits right in between Simple and Workhorse, and is a personal
favorite).

Here are some suggested task breakdowns. You can always use a stronger model,
this is just a recommended minimum:

- Local models
  - Asking questions about a codebase
  - Very, very simple edits
  - Throw-away scripts (like plotting code)
  - Writing config for AI
  - Summaries
- Simple models
  - Repetitive edits
  - Categorization/triage of open issues
  - Simple merge conflicts (rebase)
  - Simple tests
  - Fixing lints
  - Quick chores
  - Setting up, compiling, running code
  - Working on webpages / theming
- Workhorse models
  - Complex merge conflicts (rebase)
  - Complex tests
  - PR/diff review
  - Assistance with docs
  - Bug fixes
  - Fixing CI
  - Conversion (languages, CI providers, documentation generators, etc)
  - Adding static types
  - Recovering old PRs or changes
  - Applying a design document / standard
- Frontier models
  - Large refactors
  - Profiling and optimizations
  - Difficult bug fixes
  - Prototyping new features
  - New features
  - Any of the smaller model items if they fail to do it first

## Setting up the harness

Once you've picked a harness and model provider, then you'll need to download
and install it, and get signed in or your API key set somewhere.

Your harness has a central location for config and a user-level
`AGENTS.md`-equivalent file. You can add a little bit of text here that will
always be loaded right after the system prompt. Here's a template:

```md
You are on macOS. The github user is `<username>`. `python3` can be used if
python without dependencies is needed. Use `uv run` if in a python package.

Use `prek -a --quiet` instead of `pre-commit run -a` for linting.

If you make a commit, follow conventional commits and add a trailer:
`Assisted-by: <harness>:<model>`, where `<harness>` is the current agent harness
(like ClaudeCode), and `<model>` is the AI model (Like claude-opus-4.8).

Prefix PR descriptions and comments on PRs with the line ":robot: _AI text
below_ :robot:" to indicate you are an agent speaking on a user's behalf.
```

(You would insert your GitHub username above). This does several things:

- Some basic system setup, so the agents don't have to keep asking the same
  questions
- Guide for running prek, since I use that everywhere
- Enforce conventional commits and Linux kernel style trailer. If using claude,
  `You don't need to add a coauthored-by claude when you have this.` can be
  added.
- Not needed for a large model, but if using local models, add
  `Use relative paths when possible.`, this reduces the errors in making paths.
- Makes sure AI text is clearly marked (Claude also seems to comment on PRs
  sometimes without asking, so this helps there too).

Some example locations for this file:

- Claude Code: `~/.claude/CLAUDE.md`
- OpenCode: `~/.config/opencode/AGENTS.md`
- Pi: `~/.pi/agent/APPEND_SYSTEM.md`

There are also useful settings in these folders, too, like auto approve for
certain tools.

## Setting up the project

When you start up a harness, you are starting fresh, there's no knowledge about
the high level project features or low level details, everything must be
investigated by the agent. To speed this up, reduce token usage, and give the
agent a better "big-picture" view, you should create a project-level `AGENTS.md`
file. You can type `/init` into your harness, and that should generate one. Some
tools have custom file names; if yours does, move it to `AGENTS.md` after it is
generated. The only tool that does not support the `AGENTS.md` standard is
Claude Code; if you are using that then you'll also need to run
`ln -s AGENTS.md CLAUDE.md` and add `CLAUDE.md` to your gitignore (also
`.claude` while you are at it). Feel free to review and edit if it got anything
wrong (like best way to run the tests, etc).

If it's a new project, you can write one shortly after getting started. You can
update it with AI as well, so feel free to include specifics that might change.
You can even instruct the AI to update `AGENTS.md` when things change in the
`AGENTS.md`!

## Things to try first

You can do nearly anything, but some ideas to get started.

Try investigating the codebase. Some example prompts:

- `How do I run the tests?`
- `Write an ARCHITECTURE.md describing how this project works.`
- `Who wrote the majority of the CI?`

Your agent can look up git history, webpages, and much more, as it needs,
without being explicitly told.

Try reviewing code:

- `/review` (some harnesses require a PR number or description of what to
  review)
- `Review this repository and look for things that can be modernized or simplified`

And try this on issues or PRs if you have any:

- `Categorize the open issues and tell me which ones are easiest to close`
- `Fix #123`
- `Is #234 still broken?`
- `Fix the CI` (on a failing PR)

## Important notes

If you generate text on an issue or PR, it should be clearly marked as AI
generated (handled by example user file above). Respond and talk to reviewers in
person. You can ask your AI to address reviews, but don't let it comment, and
understand what it's doing and why.

Add a trailer to AI generated contributions with the model used (handled by
example user file above). Note that a reviewer should use a different model
family to help review AI generated contributions! If you review a Claude model
with a Claude model, it will just praise itself. While Claude vs. GPT (for
example) will go back and forth and could make the result 70% better. Letting
them know what you use can help avoid the self praise loop.

Using AI to prototype a few features is really great. Use plan mode to get it to
ask you questions and build a plan you can edit. (Most harnesses will generate a
file you can edit in plan mode). AI is _really_ good at making things work (this
is why it's so good at solving broken tests, failing lints, and CI failures). It
will very likely succeed at the feature you are working on. But the code it
produces might either need iteration, or you might need to rewrite it. That's
okay, that doesn't mean it's bad!

On that note: always iterate. Find things it can clean up. _You don't need to
hand edit_, you can use the AI to iterate, but iterate. Make sure code is up to
your standards before making a PR. Be prepared to defend it and/or explain it.

Have extra time on a subscription? Have AI hunt for things to clean up,
simplify, have it look for bugs. Have it compare documentation and
implementation. Try a couple of refactors if you have ideas on how code could be
improved. Have it rewrite your cupy code as raw kernels.

AI will hallucinate occasionally. Just be aware that it does that. If it invents
a reason for a failure, check it. Good models/harnesses will often verify things
they can verify by writing little tests, but when that can't be done, the
hallucinations can leak through. It's okay, verify yourself (including by asking
the AI to look stuff up or write little tests).

If you have the option, don't tie yourself to a single model family. Even a
little access to a secondary family can go a long way - "rubber duck" (an actual
mode in Copilot) is the process of using one family (like Claude) as the
implementer, and another family (like GPT) as the reviewer, and you can get ~70%
better results that way. (Not really something very measurable, but I'd say it's
a good approximate figure).
