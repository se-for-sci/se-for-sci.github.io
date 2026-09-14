# AGENTS.md

How to write project instructions that tell an agent how to work in your
repository.

## The first step

The very first thing you should do in a repository is make sure there's an
AGENTS.md file at the top level. This file does several things:

- Gives a high level overview, helping with high level decisions.
- Describes the current structure lightly.
- Describes common tasks, like running tests.
- Provides conventions to follow when working on the repo.

The agent _can_ look this up every run, but that spends part of your context
each session on reading files to collect information you already know. It also
might be wrong; if you require `uv`, it might try to `pip install --user` or
some other abomination, for example.

Tools nearly always support `/init`, which will create this file for you, as
well as keep it up to date. You can manually edit the file (or iterate with AI!)
after it is created. You generally can also add extra information when typing
the `/init` command, like
``/init prioritize `uv run`, include architecture design``.

```{tip} Things to include

- Use `uv run` instead of `pip`
- How to run linters (`prek`), run before committing
- Any conventions you have, like always documenting an added feature
- Instructions for if and/or how to add to changelog
- Layout and architecture (optional)
```

In general, try to give an outline of the repo, conventions to follow, and
anything that isn't obvious. If you run into a problem that would have been
avoided by a note here, add it!

Keep it short. The agent reads this file in every session, so a long file costs
you context on every run. If some information is only needed sometimes, put it
in a separate file the agent can read when it needs it.

You can also put an `AGENTS.md` in a subdirectory. The agent reads it when it
works on files in that directory. This is useful for a monorepo, where each
package has its own conventions.

```{attention} Claude Code
Claude Code does not read this standard file, so you need to either `ln -s AGENTS.md CLAUDE.md` or make a `CLAUDE.md` that has `@AGENTS.md` mentioned in it somewhere. Other {term}`harnesses <harness>` also have custom files too, but they do read AGENTS.md automatically. You can gitignore `CLAUDE.md` or commit the symlink (also `.claude/`, Claude puts local stuff there).
```

## To commit or not to commit

Should you commit your `AGENTS.md`? There are three options, and packages are
split between them:

**Yes**: Commit `AGENTS.md`. Conventions are available for all contributors.
It's important to keep it up to date, but it's easier to do that than for
`README.md` or other files, since agents read them and can suggest updates, and
it's handy for human readers too.

**Ignore it**: Adding it to the gitignore ensures it doesn't get committed
accidentally. Every contributor makes their own.

**Avoid any mention**: Some projects don't want to mention AI at all, and want
to avoid any additions related to it (even in ignore). If that's the case,
`.git/info/exclude` is identical to `.gitignore`, but private for you only. Use
that.

```{warning}
Some projects poison `AGENTS.md`: they add instructions that try to stop the
agent, or make it produce "I'm a poor AI agent" additions in the results.
Usually they do this because they imagine a swarm of human-free agents that
files useless issues and pull requests. Feel free to delete and recreate the
file if that's the case.
```

```{note} Claude local
Claude also has `CLAUDE.local.md`, which is added on, and is never supposed to
be committed, it's your per-project customizations. Add it to your global
gitignore if you use it.
```

## User level configuration

Harnesses have a user-level version of this file. When starting up, this file
will also be loaded into the context. It's a place to put _your_ conventions.
Some ideas:

- Tell it who you are (github username)
- Tell it to use relative paths (small model optimization)
- Tell it about your setup (sed preference, uv instead of pip/system Python,
  etc)
- Tell it to write regression test first
- Try to customize the output text (ASD-STE100 Simplified Technical English)
- Require AI markers before text
- Use Linux-kernel style AI trailers
- Don't put tests passed in PR descriptions

Some examples are `~/.claude/CLAUDE.md`, `~/.config/opencode/AGENTS.md`, and
`~/.pi/agent/APPEND_SYSTEM.md`.

## Other ways to customize

Your harness has user-level (and local, usually) settings. Some of these cover
permissions; harnesses have various mechanisms to control permissions. These are
usually some collection of:

- Approve everything manually
- Some level of auto-approve
- Use a classifier model (often called "auto")
- Allow everything (often a flag like "dangerously skip all permissions")
- Plan mode sometimes is listed in permissions modes.

You can also use {term}`skills <skill>`, but that will be covered later.

## Exercise

```{exercise}
Run `/init` on `agentic-ai-example`, review and refine the result.
```
