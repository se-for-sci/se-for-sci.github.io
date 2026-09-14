# Inspection

How to use an agent to explore and explain an unfamiliar codebase.

## Ask questions

You can ask questions of a codebase in the {term}`harness`. Some examples:

> How do I run the tests?

This will find the documentation for it, look at CI setup, and general setup to
find the expected way for a contributor to run the tests.

> Where is X defined?

This even works across languages; try it in CPython for something defined in C!

> Can this return value be `None`?

This will trace through the logic. It's also possible it will set up and run
code to check.

> Who wrote this function?

You can refer to anything in the context, like a chatbot. And it can check git
history and trace through to find answers.

> Write an `ARCHITECTURE.md` describing how this project works

You can ask it to record artifacts instead of just answering.

```{tip}
Harnesses have a way to copy the last response in markdown. Usually `/copy` or a similar shortcut.
```

## Watch it work

Most harnesses let you see the thinking phase. Open models show the raw text;
commercial models usually show a summary, and some redact it. Either way, you
can still see the operations it performs. It will grep, read, and search around
much like you would when looking for answers.

## Beyond code

You can ask about anything, not just code. For example, you can ask about the
difference between a passing log and a failing one, or between two archives. You
can tell it to load a webpage and summarize it, or if your code fulfils the
description on the page.

## Exercise

```{exercise}
Investigate `agentic-ai-example`, how does it work?
```
