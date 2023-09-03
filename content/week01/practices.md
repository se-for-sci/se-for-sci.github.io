# Programming/style general practices

## Legibility

### Comments

Use _helpful_ comments. Examples of bad comments:

```python
# Multiply x by two and store it in y
y = 2 * x

# Then we do this
z = 3 * x
```

A comment should help the reader understand something in the code that they
can't easily get from reading the code. If you are just describing _what_ the
code does, that's probably bad unless it's a tricky expression. If you are
describing _why_ the code does it, that's much better. Always strive for self
documenting code by using small, well named functions with any implementation
details in the function description or docstring.

Beware that comments can lie. Code may be modified without updating a comment or
do something completely different. Comments are what the developer wants to
happen (or wanted to at some point), code is the truth.

Another bad comment: commented out code. Commented out code will quickly become
outdated, and is not helpful to the reader. If you are using VCS, old versions
of code are saved in your git history. Make every line count!

Examples of good comments:

```python
# The following workaround is required because ...

# Here we are going to compute ... (followed by a block of complex code)
```

### Variable names

If you select reasonable names, you can often make the code itself read like
comments. Compare:

```python
# Compute the volume using width x depth x height
v = w * d * h
```

and

```python
volume = width * depth * height
```

One letter variables / short variables are fine as long as they are used close
to the definition. If it's more than a line or two, try to be (reasonably)
descriptive.

Some strict style guides recommend one-letter variables only as loop indices.
While short variable or function names may seem efficient, you will typically
read a name about 10-100x more than you write it. The additional mental strain
of decoding variables can limit overall code readability.

### Follow conventions

A programming language has conventions for naming and various idioms; try to
follow them whenever possible. For example, naming in Python & C++:

- Variable: `snake_case`
- Global constant: `ALL_CAPS`
- Function: `snake_case`
- Class: `CamelCase`

For C and C++, you should loop from 0 to 1-len:

```cpp
// Good
for (i=0; i < 10; i++) {
    /* do some stuff */
}

// Bad
for (i=1; i <= 10; i++) {
    /* do some stuff */
}
```

Why? Because it's conventional, and a C++ programmer will have to think less
about the loop if they see the form they are used to. This is the same in
Python:

```python
for i in range(10):
    ...  # i goes from 0 to 9
```

In a different language, like Matlab, the conventions may be different; follow
the conventions of the language you are using.

### Be consistent

Clean &emsp; formatting helps &emsp;you process &emsp;&emsp;&emsp; things
quickly. We &emsp; use &emsp; &emsp; consistent style &emsp; so that readers
&emsp; &emsp; can &emsp; focus on &emsp; content, rather than &emsp;&emsp;&emsp;
on how things are &emsp;&emsp; written. The human brain interprets style
differences as meaningful, adding cognitive load to future readers (including
you). Avoid it!

For Python, style is described in PEP 8, and the most popular autoformatter is
Black. I'd highly recommend sticking to that style if you don't have strong
preferences otherwise. For C++, there are more to choose from - pick one and be
consistent. LLVM's styling is good. Again, styling can be enforced by tools like
clang-format. We'll cover those sorts of things later.

```python
def f(x, y):
    return x**2 + y
```

Notice the style:

- One space between constructs
- Four space indent
- Power operator `**` doesn't need spaces for simple expressions

### Avoid a bajillion parameters/function arguments

What do you think of this code?

```python
def simulate_plasma(x_i, v_i, t_i, t_f, E_i, B_i, N, result_array, printflag):
    ...  # do some stuff
```

This has a lot of parameters, making it hard to use / easy to misuse. In Python,
you can pass parameters by name, which helps (you can even force it), which
helps. In C++, you can only pass positionally.

Some helpful hints:

- Try to make functions do one thing, and do it well (more on this below)
- Bundle data into composite data types when possible.

Here's an example of bundling. Let's take a simpler example:

```python
def get_rect_area(x1, y1, x2, y2):
    ...  # does stuff


get_rect_area(x1, y1, x2, y2)
```

Someone calling the function could easily make a mistake:
`get_rect_area(x1, x2, y1, y1)` for example. However, if you bundle this:

```python
def get_rect_area(point_1, point_2):
    ...  # does stuff


get_rect_area(Point(x1, y1), Point(x2, y2))
```

Now it's much harder to misuse. What is `Point`, though? It can be something
like a dataclass or a NamedTuple (or a struct or tuple in C++). We'll cover
these topics when we get to object oriented programming. It may even make sense
to create a `rectangle` object with the method `get_area` with no arguments.

Think about designing the _interface_ to code; how functions are called and
used.

## Think in terms of creating tools, not accomplishing tasks

Scientists and engineers untrained in coding tend to write code that looks like
a to-do list. It is very "pipeline-y": do this, then do this other thing, then
do that. That's natural, and normal, but it's a narrow view: you are the user,
and the code as a whole is providing you a service, namely repeating monotonous
tasks for you in a certain order.

With experience, you start to pick up a different view: pieces of code can be
users, too... of other pieces of code. In a given context, one code is providing
the service, while the other uses that service. And you as the human may only
request service from a couple of very "high-level" pieces of code, which in turn
execute the details of their tasks by making service requests of other pieces of
code, without you the top-level user needing to worry about the details.

This way of thinking becomes the driving force behind good code design, and we
can think of a several sub-ideas under this umbrella.

"pipeline-y" code does have its place; the final layer of code (driver code),
workflow automation scripts, utility scripts for your operating system, etc.

### DRY code is good. WET code is bad.

DRY = Don't Repeat Yourself

WET = Write Everything Twice (or more times)

Once you find yourself writing the same essential code more than one time in
more than one place, it's time to promote that chunk of code from the status of
a task to the status of a reusable tool. Make it a function, or its own data
type, something -- but don't just keep repeating the same task. Abstract away
the essentials.

If you don't bundle your code and keep it in one place, you can't reuse it.
Maintainability is a nightmare if the code lives in more than one place. You
will make a change in one place where those instructions live, but not in
another. It'll happen.

A rule I've seen is never, never write anything three times. Try to avoid twice
too, but don't panic if you have something twice. Very rarely, it's worth
duplicating something once just to avoid major shenanigans to have a single
source of truth.

As a side effect, DRY code promotes having smaller functions, which are easier
to understand, test and refactor. Everything has a single, tested source of
truth.

## Modularity

Break code into chunks, and have each chunk do one thing. Try not to mix tasks
within the same code unit that are logically orthogonal to one another.

Think more in terms of interfaces, less in terms of implementation.

A mechanic provides you with a service when your car breaks. To do her job, she
has to rely on a host of other services: parts vendors, her tools, the hydraulic
lift in her garage. You don't care about the details of how she does her job --
you just know car goes in, money goes in, car comes back in 3 days.

How you doing your job is the implementation -- code that _provides_ a service
knows how it's implemented, but code that _uses_ a service shouldn't know or
care.

What is the job you do and what do I need to give you so you can do it is the
interface. This is the only thing the users of code should care about. It is a
contract.

In this class, we will gradually learn to think and design in terms of reusable
tools and their interfaces, so that higher-level code can use lower-level code
via that interface without worrying about implementation details (which the
low-level code can change, without breaking high-level code --- you get easier
extensibility).

Key concept: To the extent possible, decouple code that provides a service from
code that uses the service. Don't rely on a specific implementation, as that
could change.

## Odds and ends

### Optimize code only late in the game

Prioritize making your code clean and correct. Only try to make it fast if you
think it is too slow. Why? Because you'll almost certainly guess wrong about
where (and why) your code is slow or inefficient, and complicate it needlessly.

Memory is cheap. Disk space is cheap. CPU cycles are cheap. Your time is
expensive. If you are being wasteful, but your code runs in 2 seconds, does what
you want, and it's not interfering with anyone else's work, then who cares? Let
the computer do the work.

"Premature optimization is the root of all evil." --popularized by Donald Knuth,
the creator of TeX

### Avoid global variables

Global variables are quantities that all the code in your system can see and
alter. As code becomes more complex, you'll eventually find that one code unit
did something to a variable that it shouldn't have, and now your other code
units are suffering.

These bugs are very hard to track down.

Make your variable local in scope (i.e. only the function in which they're
active can modify them). It simplifies testing and is less error prone. Local
variables are easier to understand since you don't have to jump to different
parts of a file or project to see what the variable is.

There are some exceptions to this, but it's a decent rule of thumb.

Global **constants** are generally ok. For instance, you probably want to define
`PI` once and let all your code reference it (that's more DRY).

You can take this one step further:

### Minimize capture

Python has automatic variable capture[^1] from outer scope. In C++ lambda
functions, you have to explicitly list variables you want to capture, but Python
hides this. This makes this a common source of errors and makes reading the code
much harder! There are a few rare cases where you do need this, but it should be
reserved for functions with short bodies and written in such a way to make it
obvious you need capture. And also consider `functools.partial`, which not only
advertises the intent to capture to the reader, but actually captures the value
when it is created, rather than when it is called later.

```python
# Bad
x = 2


def f():
    print(x)


x = 3
```

```python
# Better
x = 2


def f_needs_x(x_value):
    print(x_value)


f = functools.partial(f_needs_x, x)
x = 3
```

Remember, the signature of a function is not just for Python, it's telling the
reader what the function expects and what it returns. Capture causes the
function to lie to the reader.

<!-- prettier-ignore-start -->
[^1]: Actually does a lookup when calling, which can be surprising; not true
      capture. But we'll use the common term "capture" here.
<!-- prettier-ignore-end -->
