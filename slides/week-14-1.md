---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Setting up Agentic AI

---

## Agentic AI

- The most significant change to software engineering ever
- Still a fast-changing field
- We'll balance general advice with specific (and changing) examples

---

## LLM details

- The core of agentic programming is an LLM (large language model)
- Simply completion engines trained on lots of data
- Limited number of parameters, so they learn _concepts_ from the data

---

## Tokenization

- Models don't take in letters, they take in **tokens**
- That's why a model can't count the "r"'s in "strawberry"
- Tokenization is model specific
  - Claude Opus 4.7 has finer tokenization than Opus 4.6
  - Usually tied to a newly trained model, not just updated weights

---

## Selecting a harness

The first thing you interact with. Three flavors:

- **TUI** (Terminal User Interface) — runs in your terminal, works anywhere, even on clusters
- **GUI** (Graphical User Interface) — stand-alone app, can render extras like webpage previews
- **Editor plugins** — chat window alongside your editor

Most harnesses come in all three; pick the one you like best.

---

## The system prompt

- The biggest reason providers ship a harness
- A system prompt customized to that model (10k–30k tokens, cached)
- Model-specific tuning often isn't really needed for larger models
- Likely the **biggest difference** between the same model in different harnesses
- Some providers (e.g. Anthropic) require their harness for subscription coding

---

## Tools and the agentic loop

- Harnesses provide **tools** — things the model can call to do work
- Models are mostly smart enough to figure out how to use them
- The model can call tools, read output, and **loop**, fixing mistakes — like a human
- Tests, formatters, linters, type checking, and CI all feed the loop, producing high quality output

---

## Common harness features

- `/` commands control the harness:
  - `/init`: set up or update the `AGENTS.md` file
  - `/restore` (or `/sessions`): open a previous session
  - `/review`: review a PR and/or other diff
- `@` to load files into context (mentioning them often works too)

---

## Selecting a model

- Different levels, with different costs / subscription usage
- Some models are faster; small open source models can run locally
- Learning agentic AI? Use a fairly powerful model so you don't hit limits
- Later, match model strength to the problem
- An "effort level" toggle exists too — strong model + high effort on a simple task can **overengineer**

---

## A current breakdown

- **Frontier**: Claude Opus, GPT 5.5
- **Workhorse**: Claude Sonnet, GPT 5.4, Kimi K2.6, Composer 2.5
- **Simple**: Claude Haiku, GPT 5.4 mini
- **Local**: Gemma 4, Qwen 3.6

(GLM 5.1 sits between Simple and Workhorse, and is a personal favorite.)

---

## Suggested tasks (minimums)

- **Local**: codebase questions, very simple edits, throw-away scripts, AI config, summaries
- **Simple**: repetitive edits, issue triage, simple merge conflicts/tests, fixing lints, building & running code, theming
- **Workhorse**: complex merge conflicts/tests, PR review, docs, bug fixes, fixing CI, conversions, static types
- **Frontier**: large refactors, profiling/optimization, hard bugs, prototyping and new features

---

## Setting up the harness

- Download, install, sign in or set your API key
- Each harness has a user-level `AGENTS.md`-equivalent, loaded right after the system prompt

Some locations:

- Claude Code: `~/.claude/CLAUDE.md`
- OpenCode: `~/.config/opencode/AGENTS.md`
- Pi: `~/.pi/agent/APPEND_SYSTEM.md`

---

## A user config template

```md
You are on macOS. The github user is `<username>`. `python3` can be used if python without dependencies is needed. Use `uv run` if in a python package.

Use `prek -a --quiet` instead of `pre-commit run -a` for linting.

If you make a commit, follow conventional commits and add a trailer: `Assisted-by: <harness>:<model>`.

Prefix PR descriptions and comments with ":robot: _AI text below_ :robot:".
```

For local models, add `Use relative paths when possible.`

---

## Setting up the project

- A fresh harness knows nothing — everything must be investigated
- A project-level `AGENTS.md` speeds this up, cuts tokens, gives a big-picture view
- Type `/init` to generate one; rename to `AGENTS.md` if needed
- Claude Code is the only tool not supporting `AGENTS.md`:
  - `ln -s AGENTS.md CLAUDE.md` and gitignore `CLAUDE.md` (and `.claude`)
- Review and edit anything it got wrong

---

## Things to try first

Investigate the codebase:

- `How do I run the tests?`
- `Write an ARCHITECTURE.md describing how this project works.`
- `Who wrote the majority of the CI?`

Review code:

- `/review`
- `Review this repository and look for things that can be modernized or simplified`

---

## Things to try first (2)

On issues or PRs:

- `Categorize the open issues and tell me which ones are easiest to close`
- `Fix #123`
- `Is #234 still broken?`
- `Fix the CI` (on a failing PR)

The agent can look up git history, webpages, and more — without being told.
