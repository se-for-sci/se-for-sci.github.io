---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Object Oriented Introduction

---

## Prelude

To keep the slides simple, I won't be showing the following imports:

```python
import abc
import dataclasses
import json
import os
```

I will be using the fully qualified names, though.

---

## A toolbox

We'll be providing lots of _ideas_ for design. Remember core concepts:

- Modular
- DRY (Don't Repeat Yourself)
- Single responsibility
- Limited public API
- Readability

Don't sacrifice too many of these just for another if you can help it!

---

## Structured data

Most languages provide a way to group data together. For example:

```python
from types import SimpleNamespace

vector = SimpleNamespace(x=1, y=2)
print(f"{vector.x=}, {vector.y=}")
```

```output
vector.x=1, vector.y=2
```

---

## Structured data + functions

```python
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

---

## Structured data + functions

```python
from types import SimpleNamespace


def make_path(string_location):  # Construction function
    self = SimpleNamespace()
    self.string_location = string_location  # Member
    self.exists = lambda: os.path.exists(string_location)  # Method
    return self  # Instance


my_dir = make_path("my/dir")
print(f"{my_dir.string_location = }")
print(f"{my_dir.exists() = }")
```

---

## Classes

Every instance gets "printed out" by the constructor with same structure. We need to depend on that structure to use the objects.

We can formalize this in most languages with classes.

```python
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

---

## More boilerplate

```python
class Vector2D:
    __match_args__ = ("x", "y")
    __hash__ = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y
```

---

## Dataclasses (more like other languages, too)

```python
@dataclasses.dataclass
class Vector2D:
    x: float
    y: float
```

Automatically generates the helper functions. See <https://www.pythonmorsels.com/undataclass>.

Don't worry about the type annotations above, they are only needed to make the syntax work (unless they use `typing.ClassVar`).

---

## Dataclasses options

Can add options:

- `frozen=True`: Make read-only (see `dataclasses.replace`)
- `order=True`: Define ordering (treats fields like tuple)
- (3.10+) `kw_only`: require keywords when setting
- (3.10+) `slots=True`: Generate `__slots__`

Helpful tools in `dataclasses`:

- `asdict` / `astuple`: convert any dataclass to dict/tuple
- `isdataclass`: see if something is a dataclass

---

## Python example

```python
class Path:
    def __init__(self, string_location):
        self.string_location = string_location

    def exists(self):
        return os.path.exists(self.string_location)
```

---

## Dataclasses (Python) example

```python
@dataclasses.dataclass
class Path:
    string_location: str

    def exists(self):
        return os.path.exists(self.string_location)
```

---

## C++ example

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

---

## Subclassing

```python
class Animal:
    def eat(self, food):
        print(f"{self.__class__.__name__} eating {food}")


class Dog(Animal):
    pass


bluey = Dog()
bluey.eat("fruit")
```

```output
Dog eating fruit
```

---

## Subclassing: using super

```python
class Raccoon(Animal):
    def eat(self, food):
        print("Washing first")
        super().eat(food)


rascal = Raccoon()
rascal.eat("berries")
```

```output
Washing first
Raccoon eating berries
```

---

## Subclassing: details

Subclasses are instances of the parents, too.

```python
print(f"{isinstance(rascal, Raccoon)}")  # True
print(f"{isinstance(rascal, Animal)}")  # True
```

You can print the subclass chain:

```python
print(f"{Raccoon.__mro__ = }")
```

```output
Raccoon.__mro__ = (<class '__main__.Raccoon'>, <class '__main__.Animal'>, <class 'object'>)
```

---

## You can't delete via subclasses!

```python
@dataclasses.dataclass
class Vector2D:
    x: float
    y: float

    def mag(self):
        return (self.x**2 + self.y**2) ** 0.5


class Vector3D(Vector2D):
    z: float
```

**`mag2` will be incorrect unless overridden!**

---

## Safer design

```python
@dataclasses.dataclass
class Vector:
    pass


@dataclasses.dataclass
class Vector2D(Vector):
    x: float
    y: float


class Vector3D(Vector):
    x: float
    y: float
    z: float
```

---

## Abstract base classes

What about `mag2`? We want to require that it be implemented in all subclasses of `Vector`.

```python
class Vector(abc.ABC):
    @abc.abstractmethod
    def mag2(self):
        pass

    def mag(self):
        return self.mag2() ** 0.5
```

`Vector` is called an abstract base class. Checked on instantiation.

---

## Interfaces (Protocol preview)

`Vector` can also be seen as a set of _allowed_ methods:

```python
def do_something(x):
    return x.mag() + x.mag2()
```

Any class that defined `mag` and `mag2` would work here (due to duck typing).

- **Interface**: A collection of expected methods/properties
- **Structural Subtyping**: Calling something a subclass using structure
- **Protocol**: Python's formalization, will see in a couple of weeks

---

## collections.abc

Lots of Interfaces are in `collections.abc`:

- `Sized`: Anything with `__len__`

```pycon
>>> isinstance(list(), collections.abc.Sized)
True
```

But `list` does not inherit from `Sized`! This is structural subtyping.

Most standard library interfaces use dunder names for methods.

---

## Exceptions

Exceptions build this structure almost entirely just for the structure itself!

```python
print(f"{KeyError.__mro__ = }")
```

```output
KeyError.__mro__ = (<class 'KeyError'>,
                    <class 'LookupError'>,
                    <class 'Exception'>,
                    <class 'BaseException'>,
                    <class 'object'>)
```

So you can catch `KeyError` by catching `LookupError`, for example.

---

## Multiple inheritance

You can also inherit from more than one at a time.

- `__mro__` builds linear history from tree

Just because you can, doesn't mean you should. ;)

---

## Special methods (dunder methods)

You can customize the syntax around objects, such as:

- `__init__`: Runs when an object is created
- `__repr__`: Display of object on REPL
- `__str__`: Conversion of object to string
- `__add__`/`__sub__`/`__mul__`/`__truediv__`: Math operators
- `__iadd__`/`__isub__`/`__imul__`/`__itruediv__`: Inplace math
- `__radd__`/`__rsub__`/`__rmul__`/`__rtruediv__`: Right acting math
- `__eq__`/`__neq__`/`__lt__`/`__gt__`/`__ge__`/`__le__`: Comparisons

---

## Design

Choice: imperative vs. declarative

- Imperative design: make function that do each step.
  - Have to repeat this process every new data structure.
  - Not modular: the structure is mangled up with the conversions.
- Declarative design: Declare the structure, then define conversions, etc. independent of the structure details.
  - Can be reused with new data structures.
  - Modular: can use libraries like `cattrs`.

---

## Example: using dataclasses

See code example in `content/week3/config_example`.

Input:

```json
{
  "size": 100,
  "name": "Test",
  "simulation": true,
  "details": {
    "info": "Something or other"
  },
  "duration": 10.0
}
```

---

## Example: using dataclasses (2)

```python
@dataclasses.dataclass
class Configuration:
    size: int
    name: str
    simulation: bool
    path: str
    duration: float
```

---

## Conversion from JSON

```python
def new_configuration_from_json(filename):
    """Read a JSON file and return the contents as a Configuration object."""

    with open(filename, encoding="utf-8") as f:
        json_dict = json.load(f)

    # Optional, but protects against extra keys in the JSON file
    config_dict = {f.name: json_dict[f.name] for f in dataclasses.fields(Configuration)}

    return Configuration(**config_dict)
```

---

## No custom code needed to convert to JSON

```python
json.dumps(dataclasses.asdict(data), indent=2)
```

```json
{
  "size": 100,
  "name": "Test",
  "simulation": true,
  "details": {
    "info": "Something or other"
  },
  "duration": 10.0
}
```

---

## Can put conversion functions in class:

```python
@dataclasses.dataclass
class Configuration:
    size: int
    name: str
    simulation: bool
    path: str
    duration: float

    @classmethod
    def from_json(cls, filename):
        ...
        return cls(**config_dict)

    def to_dict(self):
        return dataclasses.asdict(self)
```
