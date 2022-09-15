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

## PDB

The simplest and always-available debugger for Python is `pdb`
[(docs)](https://docs.python.org/3/library/pdb.html). If you are debugging
compiled code, `gdb` (GNU compilers) or `lldb` (LLVM) work very similarly, so
once you learn one, you'll be able to adapt to a different one.

You can jump into the debugger by adding a `breakpoint()` call anywhere in your
code. The commands have one character shortcuts:

- `h`: help
- `p`: print
- `n`: next
- `s`: step
- `w`: where
- `u`: up
- `d`: down
- `c`: continue
- `q`: quit

You _can_ learn about how to set watch variables, breakpoints in existing code,
etc, but this basic set will get you quite far. You'll quickly interact with the
call stack - but that's honestly a good thing - you can see how Python (and most
other languages) work.

You can run your code in `pdb` by starting it with `python -m pdb`; you'll also
need to type `r` to start it up.

### IPDB

IPython slightly wraps pdb to make it interact nicely with IPython and Jupyter;
you'll get this version automatically using `breakpoint`. You can also enter the
debugger by typing `%debug` - this will enter the last thrown exception at the
point of the exception! Great for post-mortum investigation of an error.

### Jupyter Lab debugger

Jupyter Lab now has a visual debugger! You can activate it at the top right of
the Jupyter Lab window. Many other IDEs (like PyCharm, Spyder) have visual
debuggers as well.

### Pytest & PDB

You can enter a debugger very easily from Pytest. Just pass `--pdb` to start up
pdb if a test fails, or `--trace` to drop into a debugger at the start of each
test (probably pick a single test or use `--lf` to start on the last failure)
