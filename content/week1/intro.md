# Introductions and motivation

- Course by Henry Schreiner & Romain Teyssier. Some material written by Gabriel
  Perez-Giz for previous iterations of this course.

## The importance of software engineering in scientific computing

It's really easy to learn to code. In fact, it's easier to _write_ code than
_read_ code. Often this leads to the desire to rewrite legacy codebases instead
of deciphering what the original author intended. Since a main goal of good
software engineering is to reuse code, this is clearly wasteful! Good code is
easy to read, always strive for readability.

What does someone working on code spend time on? Rewriting code that others have
already written. The action of rewriting code to improve its readability or
performance without changing how it operates is commonly called refactoring.
Other reasons to rewrite code is because it didn't scale or was not flexible
enough. It also can feel like you spend a lot of time debugging. Lots of painful
debugging. Having strong unit tests and using version control can simplify or
eliminate some debugging problems.

There are a lot of tools, practices, and techniques available to help you read
other people's code, write code that others can read (including yourself in six
months), manage scale and flexibility, and make debugging easier.

But deadlines get in the way. Your PI cares about results, not how maintainable
your codebase is. Learning new tools to accelerate your development doesn't fit
into tight schedules or isn't seen as necessary at the beginning of a project.
Frequently, a small script will morph and evolve into a full codebase without
much planning or design. It's much easier just to get something working than
study design principles. You pay the price in the end, when trying to publish,
distribute, or replicate your results.

This course aims to fix that by providing a structured introduction to common,
useful tools and practices.

## Some important overarching concepts

- Version control
- Testing and debugging
- Design principles

## Problem-solution ordering

[Problem-solution ordering](https://mkremins.github.io/blog/doors-headaches-intellectual-need/)
is a problem for many courses, but is especially true for Software Engineering.

The classic example of problem-solution ordering is in game design. Let's say
you design a tutorial level that teaches players about locked doors. You give
them a key, then they open a door that is unlocked by that key. Assuming players
now know how to open locked doors, you put a locked door in a real level - and
players have no idea how to open it; they don't know to go look for a key. Why?
Because they didn't encounter the locked door before they picked up the key, so
they don't know that it was the key that made the door open. (The "key" and the
"door" could be any cause and effect relationship.)

This occurs in a lot of fields, like math. How do you convince someone who
hasn't needed math yet that it's a useful skill to learn?

This is what we face in Software Engineering. If you've never had to collaborate
with others or manage a large software project, you might not see why "git" is
worth learning. If you haven't spent days or weeks trying to track down a
hard-to-find bug, you might not get why you should spend time learning a
debugger or unit testing your code. If you've never had a compiler catch a bug
that would have been disastrous at runtime, you might not recognize the
usefulness of static typing. If you've never had a memory leak or segfault, you
might not see why it's worth effort to design with memory safety in mind. And so
on.

We'll try to motivate what we do, but the best motivator is experience and
exposure to the "simple" way to do things and its shortcomings; then you will
understand why the more advanced method was created.

### New features are restrictions

Each new concept in programming _restricts_ rather than _enables_. When we go
further into topics like functional programming, this will continue to be the
case. This is odd but true: we could write any program with a very small set of
constructs; very simple languages are Turing Complete. However, the most
important feature of programming is _organization_ (also called design).

Compare this hypothetical pseudo-code:

```text
i = 0
label start
compute(i)
i = i + 1
if i < 10: goto start
```

Versus real code:

```python
for i in range(10):
    compute(i)
```

Now imagine a complex program with thousands of `goto` statements; you would
have to work through every line of code to understand it. But if you restrict
yourself to common structures, like loops, objects, functions, etc., you no
longer have to look at the whole program, but just smaller, digestible parts.

Everyone learning a language will know what these common constructs are. No one
will know what your special constructs are.

## Course structure

The challenges of APC 524:

- Often introducing solutions before problems
- Large variance in the audience in terms of skill and background
- Good coding basics rarely taught elsewhere

## Introductions

I'd like to know who you are and what you are interested in! Let's do a round of
introductions. Suggested topics:

- Name
- Field of study
- Preferred programming Language(s)
- A project you are working on or want to work on
