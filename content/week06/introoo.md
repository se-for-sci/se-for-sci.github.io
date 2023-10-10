---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python [conda env:se-for-sci] *
  language: python
  name: conda-env-se-for-sci-py
---

# Intro to Object Oriented Programming (OOP)

[Slides](https://henryiii.github.io/se-for-sci/slides/week-06-1)

## Objects as collections of data and functions

An object is simply a collection of data and functions that operate on that
data.

For example, let’s say we wanted to represent our home directory as an object.
It might look something like this:

```{mermaid}
graph TD
    A{home_directory} -->|string_location| B["'/home/me'"]
    A -->|exists| C("def exists(...): ...")
```

This object holds a single data "member" (named `string_location`), and has a
function, called a "method", to see if the directory exists.

We could produce lots of these, each with different `string_location` values,
and we could use them in our code to track directories and see if they exist.
All of these objects are interchangeable, and all of them have identical
functions - only the contents of the data are different. This suggests we could
make a further improvement to the model. (Unless we were in JavaScript, by the
way, where this really is how objects were implemented!)

To ensure we make exactly the same structure of object, we could make a
templating function that "constructs" the same sort of object. Classic
JavaScript (before ES6 in 2015) does exactly this. We will quickly upgrade this
idea to something much nicer and more native to Python! But let's just try it
out to illustrate the point:

```{code-cell} python3
import os
from types import SimpleNamespace

def make_path(string_location):
    self = SimpleNamespace()
    self.string_location = string_location
    self.exists = lambda: os.path.exists(string_location)
    return self

my_dir = make_path("my/dir")
print(f"{my_dir.string_location = }")
print(f"{my_dir.exists() = }")
```

Again, don't do this in Python! There's a better way. But you'll see it's not
_so_ different. The key feature is is we are "templating" new object creation to
ensure they all have the attributes we require. As you'll see, languages
formalize this in something called "constructors".

There's one other issue above. We make a brand new function `exists` every
single object we create. If `exists` simply had access to the object it was
being called from, you could make it completely generic and just share it
between all objects that are "similar". But first, let's formalize "similar"!

## Classes

People like to categorize things; it helps us think. If I asked you what Bluey
was, you would say she's a dog (at least if you are around small children and
have seen the show). We would say Bluey is an object, an instance of a dog, a
class (we capitalize instances and classes backwards from English).

In our example, we want a concept for the type of thing that `make_path`
produced, and `my_dir` was an instance of - we'll call it `Path` - that's the
class.

Here's what making such a class looks like in several languages:

`````{tab-set}
````{tab-item} Python
```python
import os


class Path:
    def __init__(self, string_location):
        self.string_location = string_location

    def exists(self):
        return os.path.exists(self.string_location)
```
````

````{tab-item} Python dataclasses
```python
import os
import dataclasses


@dataclasses.dataclass
class Path:
    string_location: str

    def exists(self):
        return os.path.exists(self.string_location)
```
````


````{tab-item} C++
```cpp
#include <filesystem>
#include <string>

class Path {
  public:
    std::string string_location;

    Path(std::string string_location) : string_location(string_location) {}

    bool exists() const {
        const std::filesystem::path path_location{string_location};
        return std::filesystem::exists(path_location);
    }
};
```
````
````{tab-item} Matlab
```matlab
classdef Path
    properties
        string_location
    end
    methods
        function obj = Path(string_location)
            obj.string_location = string_location;
        end

        function res = exists()
            res = isfile(filename)
        end
    end
end
```
````
````{tab-item} Ruby
```ruby
class Path
    attr_accessor :string_location

    def initialize(string_location)
        @string_location = string_location
    end

    def exists?
        Path.exists? @string_location
    end
end
```
````
````{tab-item} NodeJS
```js
const fs = require("fs");

class Path {
    constructor(string_location) {
        this.string_location = string_location;
    }

    exists() {
        return fs.existsSync(path);
    }
}
```
````
````{tab-item} Rust
```rust
use std::fs;

struct Path {
    string_location: &'static str
}

impl Path {
    fn new(value: &'static str) -> Self {
        Path { string_location: value }
    }

    fn exists(&self) -> bool {
        fs::metadata(self.string_location).is_ok()
    }
}
```
````
`````

This gives us several benefits: If we get a Path, we know it has
`string_location` and `exists()`. We no longer need an `exists` function on
every instance, we can define it on the class, and Python's syntax will help us
use it. Python provides a handy shortcut for calling `Path.exists(instance)`;
you can just call `instance.exists()` instead, and it passes the instance in as
the first value to the function (traditionally called `self`).

In real world classes, each instance will contain multiple attributes and
methods that use those attributes. By bundling the data and methods together,
you limit namespace pollution and lessen the mental load required to use those
methods. Think of a `FileSystem` class with several `Path` attributes for
documents, downloads, backups, etc. A method like `backup_home` in such a class
would require no arguments; in a non-OOP implementation, each path would need a
unique variable name to track what it contains.

The "template" function in this case was `__init__`. In this function, you get
the new, empty class and you have to add the members manually, just like in our
template example. This will always run when classes are constructed, and it gets
the arguments used to make the class, too.

You can access the class that an object belongs to with `.__class__`.
`self.__class__.__name__` is a common trick for getting the name of the class.

### Subclassing

We can take our analogy one step further. Bluey is a dog, and a dog is an
animal. We like to have sets of broader and broader labels. Only Bluey is an
instance, so dog is a subclass of animal (or animal is a parent class of dog).
You could have as many of these as you wanted - for example, maybe Bluey is
actually an instance of "blue healer", which is a subclass of dog.

When Python looks up something on a class, it goes through the "Method
Resolution Order". The procedure to look up an attribute access looks something
like this:

```{mermaid}
graph TD
    O[object] --> A
    A[Path] --> B(home_directory)
```

First, is it in contained in `home_directory`? No, then is it contained in
`Path`? The final look up is in `object`, which is the implicit parent at the
top of all MRO's.

```{code-cell} python3
class Animal:
    def eat(self, food):
        print(f"{self.__class__.__name__} eating {food}")

class Dog(Animal):
    pass

bluey = Dog()
bluey.eat("fruit")
```

Notice that `self.__class__` inside `eat` was `Dog`, even though we defined the
method on `Animal`. That's because `self` was `bluey`, which is an instance of
`Dog`.

We can override a method if we want:

```{code-cell} python3
class Raccoon(Animal):
    def eat(self, food):
        print("Washing first")
        super().eat(food)

rascal = Raccoon()
rascal.eat("berries")
```

In this case, all `Animal`s can eat - if you know you take an `Animal`, you know
it can eat. However, `Raccoon` has have a custom eat function. It has the same
signature (important!), but it does a bit more. This is also how Python calls a
method from the "class above", by using `super()`. You could have also said
`Animal.eat(self, food)` here, but `super()` is better.

An important feature of subclassing is instance checks. `rascal`, above, is both
an instance of Raccoon and of Animal.

```{code-cell} python3
print(f"{isinstance(rascal, Raccoon)}")
print(f"{isinstance(rascal, Animal)}")
```

You can look up the exact method resolution order by looking at `__mro__`:

```{code-cell} python3
print(f"{Raccoon.__mro__ = }")
```

This is how error catching works in Python. If you see custom errors, they often
have no members or methods at all; they are just utilizing this inheritance
concept!

```{code-cell} python3
print(f"{KeyError.__mro__ = }")
```

This means you'll catch a `KeyError` if you ask for a `KeyError`, `LookupError`,
or an `Exception`! (Or a `BaseException`, but don't ask for that, too general,
catches things like `MemoryError` too!)

Many novice object oriented programmers are tempted to use subclassing for every
object relationship. Often, it is more appropriate (and easier to read and
write) if objects are composed with one another, instead of inherit from one
another. Remember, inheritance indicates an "is a" relationship. Subclasses can
specialize, but if you are overriding every method of a superclass with distinct
implementations you aren't really inheriting anything.

### Multiple inheritance

If one parent is good, why not allow more? Some languages allow you to combine
multiple classes into one child - this is called multiple inheritance. It is
quite tricky to get right, and there are a host of potential issues (Which
method do you call if both parents have it? What happens if you get a diamond
pattern by having both parents share a common parent? Etc.). However, if you
restrict multiple inheritance to a specific subset of uses, it can be very
powerful. Python, Matlab, and C++ allow multiple inheritance. Ruby doesn't, but
it has an alternative more limited mechanism that covers the usage we cover in
the next chapters.

One suggestion to make sure you are as ready as possible: always use `super()`
to call a parent method; don't just manually name the parent. There are special
mechanisms in super that kick in if you have multiple parents. In short, always
check the `__mro__`; that's always linear and super will always go up the
`__mro__`.

### Abstract base classes and interfaces

When designing with inheritance in mind, you might want to require a method be
implemented in all subclasses. For example, if you had a Vector class with
Vector2D and Vector3D subclasses, you might want to require all subclasses
define `mag2` (the squared magnitude). You can do this with the `abc` module:

```python
import abc


class Vector(abc.ABC):
    @abc.abstractmethod
    def mag2(self):
        pass

    def mag(self):
        return self.mag2() ** 0.5
```

The `abc.ABC`` class is a convenience class; you can also use `class
Vector(metaclass=abc.ABCMeta)`instead to avoid inheritance on this convenience class. We won't be discussing metaclasses, so just briefly they customize _class_ creation rather than _instance_ creation (everything is an object, even classes!). ABCs inject checks to all the child classes so that when you create an instance, they see if any abstract components are missing from the class. If you never make an instance, you can have abstract methods. Above,`Vector`
is called an abstract class, since you can't make instances of it. However, you
can make a concrete class from it:

```python
@dataclasses.dataclass
class Vector2D(Vector):
    x: float
    y: float

    def mag2(self):
        return self.x**2 + self.y**2
```

Since we have provided concrete definitions for all abstract methods in
`Vector2D`, we can instantiated it at use it:

```python
assert Vector2D(3, 4).mag() == 5
```

Notice that we can provide concrete methods in an abstract class, and we can
even provide helper code in the abstract methods that can be accessed via
`super()`. The only rule is no abstract methods can be exposed directly in a
class that gets instantiated.

Notice what this means for a user. If a user knows they have a `Vector`, they
can now use `.mag()` and `.mag2()` without worrying _which_ Vector they have. We
call this an _Interface_. When we get to static typing, we will discuss a way to
formalize this in Python without ABCs (hint: it will be called `Protocol`s).
Python actually has dozens of Interfaces, many of which are in
`collections.abc`. For example, the `Sized` Interface is basically this:

```python
class Sized(abc.ABC):
    @abc.abstractmethod
    def __len__(self):
        pass
```

However, the implementation doesn't really matter for an Interface; you don't
have to inherit from an Interface to implement it. In fact, Python will even
report any instance of a class that defined `__len__` as
`isinstance(..., collections.abc.Sized)`, regardless of whether it actually
inherits from this ABC! This is called structural subtyping, and it solves one
of the big drawbacks we've been seeing with subclassing, the loss of modularity.

Users of a Interface simply use ducktyping and access the methods that they
support. In the case of `Sized`, `len(x)` works on `Sized`, which just simply
calls `x.__len__()`. There are
[lots of other](https://docs.python.org/3/library/collections.abc.html), more
complex Interfaces, such as `Iterable` (for loops and such). Most of the ones in
Python use dunder names. This is because Python reserves all dunder names for
it's own use, but some libraries (especially large, older libraries!) do define
new ones, almost always for Interfaces.

At this point, an ABC is well defined (we have seen how to make one in code),
but an Interface is a concept, an agreement between implementer and caller. We
fill formalize this later when we get to static typing with `Protocol`s.

### Special methods

We've already seen a special method in Python: `__init__`. You can customize
almost every aspect of the behavior with special methods; it's easier to go over
what you can't do than what you can. You can't change assignment, `and`/`or`
behavior (due to short-circuiting logic and some limitations that might be
removed in the future). That's about it, almost every other behavior can be
changed.

One point to note about special behavior: Python shortcuts the object lookup
check for special operations, meaning the operation must be defined in the class
or immediate super class.

Here are a few to give you a taste of what is available

- `__add__`/`__sub__`/`__mul__`/`__truediv__`: The standard math operators.
- `__iadd__`/`__isub__`/`__imul__`/`__itruediv__`: Inplace versions of math
  operators.
- `__radd__`/`__rsub__`/`__rmul__`/`__rtruediv__`: Reversed versions of math
  operators. These are called if the first operator is not a member of this
  class.
- `__eq__`/`__neq__`/`__lt__`/...: The comparison operators. You can just
  specify two and then let `@functools.totalordering` generate the rest for you.
- `__repr__`/`__str__`: Controls hows the object is printed. Unlike some other
  languages, Python allows customizing the repr ("programmer view") and the str
  ("user view").

Want more? There are many, many more, handling other operators, conversion to
various things, indexing, attribute access, you name it. The
[Python Data Model](https://docs.python.org/3/reference/datamodel.html)
describes all of them.

Other languages have equivalents. C++ uses `operator +` as the function name,
for example. Matlab uses normal names like `plus` (AFAIK, it's the only one not
to call this `add`) Ruby allows almost anything as a function name, so it uses
the operator by itself as the function name. JavaScript is the only one with no
operator overloading at all (and ironically, the defaults are horrible, with
`"1" - 2` producing 3). It still has some special named methods, though.

## Dataclasses

If you look at other languages, you'll notice that some other languages
(especially compiled ones) have a nice way of declaring exactly what members the
classes are allowed to have. While there is a trick to force the attributes to
be limited to a pre-defined collection in Python (look up `__slots__` and
`__dict__`, but it's a bit involved), what we'd like is that nice syntax -
**init** is very repetitive to write, especially for the common use case of
classes as "data + functions". Python has a trick to write this very nicely
these days:

`````{tab-set}
````{tab-item} Dataclass
```python
from dataclasses import dataclass


@dataclasses.dataclass
class Vector:
    x: float
    y: float
```
````
````{tab-item} Classic class
```python
from typing import Any


class Vector:
    __match_args__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

    __hash__ = None
```
````
`````

You can use the toggle to see what dataclasses automatically generates for you.
I've included type annotations, because dataclasses include them for free -
we'll cover those later. You get a free `__init__`, `__repr__`, and `__eq__`. If
you add options to the decorator, you can generate even more useful things.
`order=True` will generate all the ordering methods. `frozen=True` will make the
members unsettable by wrapping every member with a property (a non-trivial
amount of code!) and will generate a `__hash__` as well. Python 3.10 added two
more fantastic options, `slots=True` and `kw_only=True`, too. Notice the
`__match_args__` that got added for free in Python 3.10; you get free improved
support for Python 3.10 pattern matching just by using dataclasses!

You can use [undataclasses](https://www.pythonmorsels.com/undataclass/) to see
exactly what dataclasses is supposed to be doing for you. (It's recomputed, so
could be _slightly_ off. `__hash__ = None` is missing at time of writing.)

The `dataclasses` module has other useful tools in it, as well. You have tools
to control each field when you define them. You also have a way to iterate over
all the fields. There's a tool to convert to a `dict` or a `tuple`; dicts can be
then combined with other libraries like the `json` library. And there's a
`replace` function that will make a new dataclass but with a subset of fields
replaced, which can help you "modify" a frozen instance by making a new one.

Dataclasses are a really great way to use OOP as data + actions (which is a
really important usage) without having to learn or write a lot of boilerplate.
But you also get one more feature: dataclasses are a standard. Other third-party
tools can detect them using `dataclasses.is_dataclass(...)`, and work with them.
The `rich` library can pretty-print their reprs. The `cattrs` library has tools
to convert - you can get modularity and separation of concerns by building a
`cattrs` converter separate from your dataclass.

### Example of using dataclasses

Let's just look at how dataclasses can transform the way you think. We have an
example of reading an JSON file, but we'll try a bit of a fancier one:

#### Input JSON

```{code-cell} python3
:tags: [remove-input]

from pathlib import Path
import tempfile
import rich
import json


json_contents = {
  "size": 100,
  "name": "Test",
  "simulation": True,
  "details": {
    "info": "Something or other",
  },
  "duration": 10.0,
}

rich.print(json.dumps(json_contents, indent=2))
```

#### Dataclass schema

If you'd like to read that into a structure, you could manually implement all
that code imperatively. But wouldn't it be nice if you could just declare the
data structure as it is, something like this:

```{code-cell} python3
import dataclasses

@dataclasses.dataclass
class Details:
    info: str


@dataclasses.dataclass
class Run:
    size: int
    name: str
    simulation: bool
    details: Details
    duration: float
```

#### Conversion from JSON

And then implement it's conversion separately (modular design!)? Well, this is a
standard, introspectable structure, so there's a third party library for
converting them called `cattrs`:

```{code-cell} python3
from cattrs.preconf.json import make_converter


converter = make_converter()

data = converter.structure(json_contents, Run)
print(data)
```

#### Pretty printing

We can also use another third party library, `rich`, to provide a rich, colorful
display of dataclasses:

```python3
from rich import print
```

```{code-cell} python3
:tags: [remove-cell]

from rich.console import Console

console = Console(width=80)
print = console.print
```

```{code-cell} python3
print(data)
```

#### Quick conversion to dicts/tuples

And we can use the built-in tools to quickly convert dataclasses to dicts &
tuples, recursively:

```{code-cell} python3
print(dataclasses.asdict(data))
```

```{code-cell} python3
print(dataclasses.astuple(data))
```
