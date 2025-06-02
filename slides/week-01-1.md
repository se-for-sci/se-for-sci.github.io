---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Intro to the course

---

## The importance of SE in scientific computing

- It's easier to _write_ code than _read_ code
- A goal of good software engineering is to _reuse_ code
- This is the _opposite_ of how we learn to code!

This course aims to fix that by providing a structured introduction to best practices and useful tools.

---

## Some important overarching concepts

- Version control
- Testing and debugging
- Continuous integration
- Packaging and distribution
- Design principles
- Compiled code
- Performance

---

## Notes on language and tooling

We will use Python and Python specific tools (first 2/3 of course).

But concepts are general! You can find similar tools for any language once you know the concepts.

---

## Problem-solution ordering

Other courses have this too, but it hits us hard!

Classic example: Game design

- Make a tutorial teaching about locked doors
  - Give player a key
  - Have them open a locked door
- Make a level with a locked door
  - Player is _supposed to_ go look for key!

But they didn't know that the tutorial key opened the tutorial door!

---

## Problem-solution ordering (2)

- Need to collaborate -> git
- Find a failure introduced in code -> git
- Spend 1+ day hunting bug -> debugger / unit testing
- See compiler catch bug early -> static typing
- Memory leaks / segfaults -> memory safety

These are worth the tradeoff, but you might not see that yet!

---

## New features are restrictions

Each new concept in programming _restricts_ rather than _enables_.

May seem counter-intuitive at first!

We could write any program with a very small set of constructs; even very simple languages are Turing Complete.

However, the most important feature of programming is _organization_ (also called design).

---

## Example: goto (hypothetical)

```text
i = 0
label start
compute(i)
i = i + 1
if i < 10: goto start
```

vs.

```python
for i in range(10):
    compute(i)
```

## Example: match

```python
if isinstance(x, list):
    print(*x)
elif isinstance(x, dict):
    print(*(f"{k}={v}" for k, v in x.items()))
else:
    print(x)
```

vs.

```python
match x:
    case [*_]:
        print(*x)
    case {}:
        print(*(f"{k}={v}" for k, v in x.items()))
    case _:
        print(x)
```

---

## Course structure

The challenges of this course:

- Often introducing solutions before problems
- Large variance in the audience in terms of skill and background
- Good coding basics rarely taught elsewhere

---

## Introductions

I'd like to know who you are and what you are interested in! Let's do a round of introductions. Suggested topics:

- Name
- School
- Preferred programming Language(s)
- A project you are working on or want to work on
