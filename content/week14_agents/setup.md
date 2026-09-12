# Setting up Agentic AI

{button}`Slides <https://se-for-sci.github.io/slides/week-14-1>`

Agentic AI is the most significant change to software engineering ever. It is
also still a fast-changing field; we'll try to balance general advice and
specific examples that might change.

## Selecting a harness

The first thing you'll interact with is the harness. These tend to come in three
flavors:

- **TUI**, short for Terminal User Interface. These run in your terminal. Works
  anywhere, including on clusters.
- **GUI**, short for Graphical User Interface. These are stand-alone
  applications with custom graphics. These can often do a little more than TUIs,
  like render webpage previews.
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
  - `/diff`: See what changed (or just open a new terminal tab and use
    `git diff`)
  - `/plan` (or sometimes this is a key to toggle on/off): Prepare a plan before
    editing
  - Direct access to skills, including `/skills`
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

## Next steps

Once you have a harness installed and signed in, the rest of this week covers
what to do with it:

- [](./intro.md) — what an agent is, the core vocabulary, context management,
  and the norms for disclosing AI work.
- [](./agents_md.md) — the project and user configuration files, and where to
  put your own conventions.
- The remaining chapters are task-shaped: inspection, review, triage, CI and
  bugfixes, common tasks, repetitive work, tests, profiling, features, and
  refactors.
