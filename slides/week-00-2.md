---
marp: true
theme: gaia
_class: lead
paginate: false
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# SE4Sci

## Code cleanup

---

## Comments

Not all comments are _helpful_!

```python
# Multiply x by two and store it in y
y = 2 * x

# Then we do this
z = 3 * x
```

- Comments should explain something not evident from the code
- Can depend on the audience

```python
# The following workaround is required because ...

# Here we are going to compute ...
# (followed by a block of complex code)
```

---

## More bad comments

- Comments can lie, while code cannot.
- Comments are easy to forget when updating.
- Never comment out code.

---

## Alternatives to comments

Most (all?) languages have

---

## Variable names

Compare:

```python
# Compute the volume using width x depth x height
v = w * d * h
```

with:

```python
volume = width * depth * height
```

---

## Variable name conventions (Python)

Follow the conventions for the language you are using!

For example, variable names:

- Variable: `snake_case`
- Global constant: `ALL_CAPS`
- Function: `snake_case`
- Class: `CamelCase`
- Hidden / Not Public: `_underscore`
- Built-in (Python only): `__dunder__`

---

## Conventions: loops in C & C++

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

Python:

```python
for i in range(10):
    ...  # i goes from 0 to 9
```
