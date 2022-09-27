# Logging & Debugging

## Logging

Something broke. Add a print statement! Fixed. Take it out! We’ve all been here.
A steady stream of adding and (hopefully) removing print statements. But there
is a better way, if you are willing to pay the (rather ugly) cost of setting it
up: Logging. Here’s what it looks like (yes, it looks like it was designed in
the 80's, even though Python only dates back to '91):

```python
import logging
```

Next we get a logger, these are usually given globally unique names that match
their package name. If the name doesn't match an existing logger, a new one is
created.

```python
log = logging.getLogger("unique")
```

You'll often see this shortcut used in modules:

```python
log = logging.getLogger(__module__)
```

Here are a couple of logging statements:

```python
log.warning("Very important")
log.info("Logging this here")
log.debug("Logging this here")
```

To get the logger to show anything, you'll need to set the severity level to
display:

```python
# Global setting
logging.basicConfig(level="INFO")
```

This is a global setting that affects all loggers, including the ones in the
libraries you are using (hopefully they utilize logging). You can also change
this setting for an individual logger.

You can set fancier handlers, too, which can add timestamps and other
information.

This is very powerful for adding printouts that only show up if you ask for info
or debug printouts (the normal setting is "WARN"). Sadly the design is very old,
relying on the classic `%` style formatting. You _can_ use f-strings in the
logging messages, though; that works well unless you want to avoid evaluating
the string formatting, global logger pool, and such. See Rich for a much more
beautiful setting (for use in applications, not libraries).

The hardest part of logging is generally setting up the infrastructure for
controlling the logger, usually; it’s best if you have a flag or environment
variable that can control this, and you have to decide or allow a choice on
whether you want all loggers or just yours to change level. And you have might
want to log to a file, rotate logs, etc; everything is doable but not all that
pretty.

### Combining with pytest

You can have pytest add your logs whenever tests fail! This can save a lot of
time debugging failures.

This configuration causes logging to be reported for test failures:

```toml
[tool.pytest.ini_options]
log_cli_level = "info"
```

### Pretty logging with Rich

You can use the `rich` third party library to produce beautiful logs. Here's how
you do it:

```python
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich_example")
log.info("Hello, World!")
```

Notice that the _logging code is exactly the same_; the only thing that changes
is the configuration setting, which is done by the application running the
library, not the library itself.

Also look up [structlog](https://www.structlog.org/) if you'd like nicer, more
modern logging.

### What to log

Tell a story with your logging. If you are wrapping a command line tool, print
out every interaction with the command line tool as INFO messages. Then you can
turn on INFO logging and observe what is happening behind the scenes. You can
put DEBUG messages in for things you needed for debugging, instead of using
print and then deleting it when you are done. Logging has almost no cost if it's
not activated (especially if you use `%` formatting or go through hoops to make
`format` formatting work, which you can do via custom classes).

## Debugging

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
