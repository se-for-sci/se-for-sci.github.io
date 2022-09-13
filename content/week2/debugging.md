# Debugging

Code always eventually breaks. Let’s look at some broken code:

```python
def broken() -> None:
    1 / 0
```

Okay, that's pretty obviously broken. But what about this:

```python
def my_broken_function():
    x = 6
    y = 4
    x += 2
    y *= 2
    x -= y
    y /= x
    return x, y
```

A debugger allows us to investigate the values in the function.
