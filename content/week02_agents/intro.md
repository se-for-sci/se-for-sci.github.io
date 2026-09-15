# Intro to Agentic AI

What an agent is, how it differs from a chat model, and what it can do in a
repository.

## It's useful now?

In November of 2025, AI in coding work suddenly changed. Agentic
{term}`harnesses <harness>` like Claude Code and models like Opus 4.5 changed
coding work from occasionally helping to being a valuable tool in any
programmer's toolbox.

There are two different forms of agentic AI that often get lumped together:

- A developer driving an interactive harness (Claude Code, OpenCode, Codex, Pi,
  etc).
- An autonomous agent (OpenClaw, Hermes) that runs unattended, often on a
  low-cost or local model to keep it cheap to run continuously.

We will be exclusively talking about interactive harnesses running agents here,
but let's briefly explain the autonomous agents and why they annoy open source
developers.

- A person sets up a personal autonomous agent with instructions like "build up
  a developer profile, look for easy PRs to make with a high chance of getting
  merged".
- The agent runs unattended, often on a cheap or local model (a frontier model
  would be expensive to run continuously).
- It opens simple, low-effort PRs, since that is all a weak model without
  supervision can do.
- The submitters often do not (or cannot) follow up on review feedback; opening
  the next PR is cheaper than engaging with the last one.

This likely comes from thousands of individuals each running one agent, often
converging on the same repos and even identical features. The OpenClaw
repository itself became the most famous victim: it went from about 2 PRs per
week in December 2025 to about 3,400 per week by February 2026, and the merge
rate fell from roughly 48% to under 10%. One contributor opened 106 PRs in a
single day, with a median gap of *three seconds* between submissions
([Greptile's statistical study](https://www.greptile.com/blog/prs-on-openclaw)).
Security maintainers report the same pattern with AI-generated vulnerability
reports whose submitters cannot answer follow-up questions
([Axios](https://axios.com/2026/03/10/ai-agents-spam-the-volunteers-securing-open-source-software)).

You (probably) can use autonomous agents for some impressive things, but working
on public projects you don't own is not one of them. It's the same
"credit-building" people have always tried to do on GitHub, just scaled up. In
fact, that's a recurring theme: AI can scale up impact, either for good or bad.

Throughout this course, there will be examples of prompts, often real ones with
links to where they were used. Above, this prompt was used with Claude Fable in
Claude Code:

> Quick check: is my description of agent swarms (which I've never used) in
> `@content/01_intro.md` accurate?

Claude came up with the paragraph with links, and reworded "swarms" to
"autonomous".

## Chat model vs. agent

{term}`LLMs <LLM>` start out as completion engines; they are fed basically
everything anyone has ever written, and the model tries to predict the next
{term}`token`. By making the model much smaller than the dataset, and reserving
text for validation only, the model is forced to learn concepts instead of just
memorizing the dataset. If a model starts replicating the dataset exactly,
that's called overfitting and the model will not perform as well, and the
verification holdout detects it.

While this is useful for autocomplete, it's not how we use these today. Since
ChatGPT in 2022, models are post-trained on "chatbot" style interactions: first
supervised fine-tuning on example conversations, then Reinforcement Learning
from Human Feedback, RLHF, which trains models on human preferences; this is why
older models often feel "likable". Agentic models, popularized by Claude 3.5
Sonnet in 2024, are also trained on tool use, thinking phases, and other
structure that is used today. To get the agentic training, models are given huge
numbers of problems with checkable answers, generate many candidate solutions
for each, and are rewarded when a solution passes a verifiable check like a test
suite (Reinforcement Learning from Verifiable Rewards, RLVR). Because no human
judgment is needed, this mechanism scales, but it also makes "less likable"
models.

The agentic models operate on a loop; they can affect the problem via
{term}`tool` calls (an example of a tool call is an edit tool, like
`Edit(file, old, new)`), run diagnostics like compiling or linting, then inspect
the output and try again.

## Core concepts

These terms come up throughout the workshop.

```{glossary}
LLM
: Large Language Model. A neural network trained to predict the next token of
  text. All the tools in this workshop are built around one.

token
: The unit an {term}`LLM` reads and writes. A token is roughly three-quarters
  of an English word; code often uses more tokens per character. Try the
  [OpenAI tokenizer](https://platform.openai.com/tokenizer) to see how text
  splits.

context window
: The maximum number of {term}`tokens <token>` a model can see at once: the
  system prompt, the conversation, file contents, and tool output all share
  it. When it fills up, the model forgets or the session must be compacted.

/compact
: A {term}`harness` command that summarizes the conversation so far and replaces the
  full history with the summary, freeing space in the {term}`context window`.

cache
: AKA prompt caching. The provider stores the processed prefix of a
  conversation so repeated turns do not pay to reprocess it. This is why long
  agentic sessions are affordable, and why editing early context is expensive.
  Different providers keep it for different lengths of time, check your provider.

training cutoff
: The date after which the model has seen no data. Anything newer (a library
  release, an API change) must be put into context, or the model will guess
  from stale knowledge.

harness
: The program around the model: the system prompt, the tools, MCP servers,
  subagents, and skills. Claude Code, OpenCode, and Codex are harnesses; the
  same model behaves differently in different harnesses.

system prompt
: Instructions the {term}`harness` sends before the conversation. It defines
  the agent's behavior, available tools, and rules.

tool
: A function the model can call, such as reading a file, editing it, or
  running a shell command. Tool calls and their results are what turn a chat
  model into an agent.

MCP
: Model Context Protocol. An open standard for plugging external tool servers
  (browsers, databases, issue trackers) into a {term}`harness`.

subagent
: A separate agent the main agent can launch. It gets its own
  {term}`context window`, does a task, and reports back only a summary, which
  keeps the parent context small. A *fork*, by contrast, shares the parent's
  context.

skill
: A packaged instruction set the harness can load for a specific task, often
  invoked as a slash command.

open-weight model
: A model whose weights are published so you can run it yourself. Local use
  usually needs *quantization* (storing weights at lower precision to fit in
  memory), and many large models use MoE (Mixture of Experts), where only a
  fraction of the weights are active per {term}`token`.
```

## What agents are good at

What can you use agents for? See the other chapters! Things like inspection,
review, triage, bugfixes, common tasks, repetitive work, tests, features,
profiling, and refactors are covered.

In general, anything with a clear pass/fail condition: tests, linters, type
checkers, and CI feed the agentic loop and directly improve output quality.
Things humans do not like to spend time on are good candidates; long or annoying
tasks (slow CI, Docker, builds).

## What agents are not good at

Be more careful if you use agents for decision making and judging what is
"best". This is much weaker than pass/fail checking, and is limited by what is
in the {term}`context window`. If you have a good model and fill the context
window with the information that is needed to make the best decision, it might
do fine, but that's tricky.

If you want to follow best practices, it needs them in the context window or via
tooling; it might struggle if you just say "follow best practices" without
context. (Due to RLVR, it will do better than average code quality by default,
at least). Also note that it doesn't know anything past the
{term}`training cutoff` window (usually a few months before the model was
released), so you need to load newer information into context.

Writing code from scratch is one of the hardest tasks; if it has existing code,
it will mimic your style and preferences.

Communicating with humans is another one (see the working norms and disclosure
section). Text from an LLM is very detailed and usually verbose. There are some
methods to reduce it a bit, and some models are better than others. Regardless,
in general, humans should not be expected to read LLM text thinking it's from a
human. If you know it's LLM text, you can collect the information you need from
it without treating it as human communication.

## The core skill: context management

The most important thing when using harnesses is controlling the context. If you
don't put enough in, the LLM will tend to make bad decisions. Load design
documents, relevant issues, discussions, and related files to improve the LLM's
ability to work. Modern LLMs have incredible context windows, from 200K to 1M
tokens. The LLM will take it into account when generating commands, text, code,
etc.

The other side is also a problem; once the context window starts getting too
full, the LLM will start getting forgetful and the impact of the context will
decrease. The advertised limit of models is too large; if you have a 1M token
context window, you should probably not usually let it get over 300K-400K unless
you are in the middle of an active task.

You will get the best results if the context is balanced and focused: load
supporting documents and conversations, try to avoid unrelated stuff. As your
conversation grows, things like logging will tend to fill up the context, along
with thinking traces from the LLM.

You can run {term}`/compact` to compact the context. This is safe to do most of
the time; most of the context you don't need in the next step. It's good
practice to do this whenever returning to a previous conversation, and when
there's a clear break in what you are doing. Some harnesses have other commands
to view and trim the context.

## Working norms and disclosure

This is a fast moving field, so I'll give you my recommendations. I will also
note that I am not a lawyer. Always match a project's expectations if they have
an `AI_POLICY.md` or other guidelines in place.

Any AI written descriptions, issues, or comments on PRs/Issues should be clearly
marked. I use `:robot: _AI text below_ :robot:`, and sometimes I even put it
inside a `details` block so it has to be expanded to be read. By using that
mark, I can put human text above, while still having the AI text as a reference.
I instruct all my AI harnesses to always add this marker, and they do.

Credit AI in commits with the Linux kernel trailer
`Assisted-by: <harness>:<model>`; never `Co-authored-by` or especially
`Signed-off-by` (DCO is a human legal act). Your model is not a co-author,
that's a human thing; it's an assistant. Some projects prefer no disclosure at
all in the commits and only in the PR description (Kubernetes, for example), so
it cannot be traced back to an AI company at all, but most are happy with the
Linux kernel trailer. Knowing the model helps when reviewing.

```{tip} Claude Code
Claude Code adds itself as a coauthor by default. You can turn it off in
settings, then you are free to add the Linux style trailer in via
`~/.claude/CLAUDE.md` (below).
```

````{tip} User configuration

Something like this in your harness's user agents file:

```text
If you make a commit, follow conventional commits and add a trailer:
`Assisted-by: <harness>:<model>`, where `<harness>` is the current agent
harness (like ClaudeCode), and `<model>` is the AI model (Like claude-opus-5).
```

Customize based on the most likely harness and model. Note that the Pi harness doesn't
include the model name in the default context, the others do.
````

Disclose in the PR description. There's not a convention here; I either copy the
Linux kernel trailer or have the AI text below marker somewhere in the
description.

```{tip} User configuration
Prefix PR descriptions and comments on PRs with the line ":robot:
*AI text below* :robot:" to indicate you are an agent speaking on a user's
behalf.
```

Follow the golden rule (LLVM/curl): a contribution should be worth more than the
time it takes to review. With AI able to produce code faster than humans can
read it, review time is the new bottleneck; human review time is the most
valuable resource. Never use AI on "good first issues", those are simple issues
meant to help onboard new contributors (and due to AI, are rapidly being phased
out in many projects).
