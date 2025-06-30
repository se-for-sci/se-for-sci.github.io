# Parallel computing

In programming, there are two ways to run code in parallel. One is to use
threads, which are an operating system construct allowing a single process to
run code at the same time. The other is to use processes, where you simply
create several processes, and manage the communication between them yourself
(including using tools like MPI); this is the only mechanism that also works
between separate machines. The cost of starting a thread is smaller than a
process, but still non-negligible in some situations. Note that both models work
even on a single core; the operating system context-switches between active
processes and threads.

There's also async, which is more of a control scheme than a multithreading
model; async code might not even use threads at all. In threaded code, the
running context switches back and forth at any point when the operating system
decides to, while in async code, you place explicit points in your code that are
allowed to pause/resume, and the programming language/libraries handle the
context switching. This by itself is always single threaded, but you can tie
long running operations to threads and interact with them using async. If you
don't have threads (like in WebAssembly), async is your only option.

Multithreading in Python was historically split into two groups: multithreading
and multiprocessing, as you might expect, along with async. Compiled extensions
can be implemented with multithreading in the underlying language (like C++ or
Rust) as well.

There's a problem with multithreading in Python: the Python implementation has a
Global Interpreter Lock (GIL for short), which locks access to any Python
instructions to a single thread. This protects the Python internals, notably the
reference count, from potentially being corrupted and segfaulting. But this
means that threading _pure_ Python code is not any faster than running it in a
single thread, because each Python instruction runs one-at-a-time. If you use a
well-written C extension (like NumPy), those may release the GIL while running
their compiled routines if they are not touching the Python memory model, which
does allow you to do something else at the same time.

The other method is multiprocessing, but not always the best solution. This
involves creating two or more Python processes, with their own memory space,
then either transferring data (via Pickle) or by sharing selected portions of
memory. This is much heaver weight than threading, but can be used effectively
sometimes.

Recently, there have been two major attempts to improve access to multiple cores
in Python. Python 3.12 added subinterpeters each with their own GIL; two pure
Python ways to access these are being added in Python 3.14 (previously there was
only a C API and third-party wrappers). Compiled extensions have to opt-into
supporting multiple interpreters.

Python added free-threading (no GIL) as a special experimental version of Python
in 3.13 (called `python3.13t`); this is no longer an experimental build in 3.14,
but is still a separate, non-default build for now. Compiled extensions have to
have a separate compiled binary for free-threading Python builds.

The relevant built-in libraries supporting multithreaded code:

- **`threading`**: A basic interface to **`thread`**, still rather low-level by
  modern standards.
- **`multiprocessing`**: Similar to threading, but with processes. Shared memory
  tools added in Python 3.8.
- **`concurrent.futures`**: Higher-level interface to `threading`,
  `multiprocessing`, and subinterpreters (3.14+).
- **`concurrent.interpreters`**: A lower-level interface to subinterpreters
  (3.14+).
- **`ascynio`**: Explicit control over switching points, with tools to integrate
  with threads.

For all of these examples, we'll use these two examples. We'll also use this
simple timer:

```python
import contextlib
import time


@contextlib.contextmanager
def timer():
    start = time.monotonic()
    yield
    print(f"Took {time.monotonic() - start:.3}s to run")
```

## Pi Example

This example is written in pure Python, without using a compiled library like
NumPy. We can compute π like this:

```{literalinclude} piexample/single.py
:linenos:
:lineno-match: true
:lines: 14-
```

This looks something like this:

```console
Took 4.92s to run
pi(10_000_000)=3.1414332
```

## Fractal example

This example does use NumPy, a compiled library that releases the GIL. The
simple single-threaded code is this:

```python
import numpy as np


def prepare(height, width):
    c = np.sum(
        np.broadcast_arrays(*np.ogrid[-1j : 0j : height * 1j, -1.5 : 0 : width * 1j]),
        axis=0,
    )
    fractal = np.zeros_like(c, dtype=np.int32)
    return c, fractal


def run(c, fractal, maxiterations=20):
    z = c

    for i in range(1, maxiterations + 1):
        z = z**2 + c  # Compute z
        diverge = abs(z) > 2  # Divergence criteria

        z[diverge] = 2  # Keep number size small
        fractal[~diverge] = i  # Fill in non-diverged iteration number
```

Using it without threading looks like this:

```python
size = 4000, 3000

c, fractal = prepare(*size)
fractal = run(c, fractal)
```

For me, I see:

```
Took 2.677322351024486s to run
```

## Threaded programming in Python

### Threading library

The most general form of threading can be achieved with the `threading` library.
You can start a thread by using `worker.thread.Thread(target=func, args=(...))`.
Or you can use the OO interface, and subclass `Thread`, replacing the `run`
method.

Once you a ready to start, call `worker.start()`. The code in the Thread will
now start executing; Python will switch back and forth between the main thread
and the worker thread(s). When you are ready to wait until the worker thread is
done, you can call `worker.join()`.

#### Pi example

For the PI example, it would look like this:

```{literalinclude} piexample/thread.py
:linenos:
:lineno-match: true
:lines: 16-
:emphasize-lines: 1,12,17-26
```

Above, I am now using a separate `Random` instance in each thread; for GIL
Python, this doesn't make a difference, but it's important for free-threaded
Python, where accessing a global random generator is threadsafe, and will end up
being a point of contention. The parts of the code that are interacting with the
threading are highlighted.

Now let's try running this on 3.13 with and without the GIL:

```console
$ uv run --python=3.13 python single.py
Took 4.98s to run
pi(10_000_000)=3.141544
$ uv run --python 3.13 thread.py
Took 4.96s to run
pi(10_000_000, 10)=3.1417908
$ uv run --python 3.13t thread.py
Took 1.29s to run
pi(10_000_000, 10)=3.1411228
```

(On 3.14t (beta), the single threaded run is about 25% faster and the
multithreaded run is about 40% faster.)

#### Fractal

Our fractal example above could look like this:

```python
import threading

c, fractal = prepare(*size)


def piece(i):
    ci = c[10 * i : 10 * (i + 1), :]
    fi = fractal[10 * i : 10 * (i + 1), :]
    run(ci, fi)


workers = []
for i in range(size[0] // 10):
    workers.append(threading.Thread(target=piece, args=(i,)))
```

Or this:

```python
class Worker(threading.Thread):
    def __init__(self, c, fractal, i):
        super(Worker, self).__init__()
        self.c = c
        self.fractal = fractal
        self.i = i

    def run(self):
        run(
            self.c[10 * self.i : 10 * (self.i + 1), :],
            self.fractal[10 * self.i : 10 * (self.i + 1), :],
        )


workers = []
for i in range(size[0] // 10):
    workers.append(Worker(c, fractal, i))
```

Regardless of interface, we can run all of our threads:

```python
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()
```

Similar interfaces exist for other languages, like `Boost::Thread` for C++ or
`std::thread` for Rust.

For these, you have to handle concurrency yourself. There's no guarantee about
how things run. We won't go into all of them here, but the standard concepts
are:

- Lock (aka mutex): A way to acquire/release something that blocks other threads
  while held.
- RLock: A re-entrant lock, which only blocks between threads, it can be entered
  multiple times in a single thread.
- Conditions/Events: Ways to signal/communicate between threads.
- Semaphore/BoundedSemaphore: Limited counter, often used to keep connections
  below some value.
- Barrier: A way to wait till N threads are ready for a next step.
- Queue (`queue.Queue`): A collection you can add work items to or read them out
  from in threads.

There's also a Timer, which is just a `Thread` that waits a certain amount of
time to start. Another important concept is a "Thread Pool", which is a
collection of threads that you feed work to. If you need a Thread Pool you
usually make your own or you can use the `concurrent.futures` module.

An important concept is the idea of "thread safe"; something that is threadsafe
can be used in multiple threads without running into race conditions.

### Executors

For a lot of cases, this is extra boiler plate that can be avoided by using a
higher level library, and Python provides one: `concurrent.futures`.

Python provides a higher-level abstraction that is especially useful in data
processing: Executors (threading, multiprocessing, and interpreter (3.14+)
versions are available). These are build around a thread pool and context
managers:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as executor:
    future = executor.submit(function, *args)
```

This adds a new concept: a Future, which is a placeholder that will contain a
result eventually. When you exit the block or call `.result()`, then Python will
block until the result is ready.

A handy shortcut is provided with `.map`, as well; this will make a iterable of
futures from an iterable of data. We can use it for our example:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = executor.map(piece, range(size[0] // 10))

    # Optional, exiting the context manager does this too
    for _ in futures:  # iterating over them waits for the results
        pass
```

Here's the new version of our pi example:

```{literalinclude} piexample/threadexec.py
:linenos:
:lineno-match: true
:lines: 15-
:emphasize-lines: 17-20
```

Notice how the thread handling code is now just three lines, and we were able to
use the same sort of structure as the single threaded example, without having to
worry about thread-safe queues. For the most part, times should be similar to
the threading example, with the minor change that we could control the maximum
number of allowed threads in the pool when we create it, while before we tied it
to the number of divisions of our task.

There are two ways to submit something to be run; `.submit` adds a job to run,
and `.map` creates an iterator that applies a function to an iterator. This is
really handy for splitting work over a large dataset, for example. With
`.submit`, you do have access to the return, but it's wrapped in `Future`.

## Multiple interpreters in Python

Another option, mostly unique to Python, is you can have multiple interpreters
running in the same process. While this has been possible for a long time, each
interpreter can now have it's own GIL starting in 3.12, and a Python API to run
this didn't get added until 3.14 (there are experimental packages on PyPI that
enable this on 3.12 and 3.13 if you really need it; we'll just look at 3.14
though).

We won't go into to much detail (and in current betas there are a few quirks),
but here's the basic idea: The high level interface looks like this:

```python
import concurrent.futures
import random
import statistics


def pi(trials: int) -> float:
    Ncirc = 0

    for _ in range(trials):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        if x * x + y * y <= 1:
            Ncirc += 1

    return 4.0 * (Ncirc / trials)


def pi_in_threads(threads: int, trials: int) -> float:
    with InterpreterPoolExecutor(max_workers=threads) as executor:
        return statistics.mean(executor.map(pi, [trials // threads] * threads))
```

Notice that we don't have to worry about the global `random.uniform` usage;
every interpreter is independent, so no issues with threads fighting over a
thread safe lock on the random number generator. Otherwise, it looks just like
before. Like with multiprocessing, some magic is going on behind the scenes to
allow you to ignore that each interpreter needs to access the code in this file
(or, at least, it would, the magic is broken in 3.14.0b3).

We can see more of the differences if we dive into the lower level example that
just moves numbers around:

```python
import concurrent.interpreters
import concurrent.futures
import contextlib
import inspect

tasks = concurrent.interpreters.create_queue()

with (
    contextlib.closing(concurrent.interpreters.create()) as interp1,
    contextlib.closing(concurrent.interpreters.create()) as interp2,
):

    with concurrent.futures.ThreadPoolExecutor() as pool:
        for interp in [interp1, interp2]:
            interp.prepare_main(tasks=tasks)
            pool.submit(
                interp.exec,
                inspect.cleandoc(
                    """
                    import time

                    time.sleep(5)
                    tasks.put(1)
                    """
                ),
            )

    tasks.put(2)
    print(tasks.get_nowait(), tasks.get_nowait(), tasks.get_nowait())
    # Prints 1, 1, 2
```

Here, we create a queue, like before. Then we start up two (sub) interpreters.
These will be closed when we leave the with block. We set up a thread pool so we
can run the interpreters separately, but don't worry, the GIL is not held during
the `.exec` call, it just blocks until the call is done. Then, we send the
_string of code we want interpreted_ to each interpreter.

Finally, we read out the queue which should have two `1`'s (from each
subinterpreter) and a `2` from our interpreter. We have to do this before
closing the interpreters, as those values will be `UNBOUND` if they are not
still alive when you access the value from the parent interpreter.

## Multiprocessing in Python

Multiprocessing actually starts up a new process with a new Python. You have to
communicate objects either by serialization or by shared memory. Shared memory
looks like this:

```python
mem = multiprocessing.shared_memory.SharedMemory(
    name="perfdistnumpy", create=True, size=d_size
)
try:
    ...
finally:
    mem.close()
    mem.unlink()
```

This is shared across processes and can even outlive the owning process, so make
sure you close (per process) and unlink (once) the memory you take! Having a
fixed name (like above) can be safer.

When using multiprocessing (including `concurrent.futures.ProcessPoolExecutor`),
you usually need source code to be importable, since the new process will have
to get it's instructions too. That can make it a bit harder to use from
something like a notebook.

Here's our π example. Since we don't have to communicate anything other than a
integer, it's trivial and reasonably performant, minus the start up time:

```{literalinclude} piexample/procexec.py
:linenos:
:lineno-match: true
:lines: 15-
```

Notice we have to use the `if __name__ == "__main__":` idiom, because every
process will have to read this file to get `pi_each` out of it to run it. Also,
there are three different methods for starting new processes:

- `spawn`: Safe for multithreading, but slow. Default on Windows and macOS. Full
  startup process on each process.
- `fork`: Fast but risky, can't be mixed with threading. Duplicates the original
  process. Used to be the default before 3.14 on POSIX systems (like Linux).
  Some macOS system libraries create threads, so this was unsafe there.
- `forkserver`: A safer, more complex version of fork. Default on Python 3.14+
  on POSIX platforms.

## Async code in Python

Let's briefly show async code. Unlike before, I'll show everything, since I'm
also making the context manager async:

```{literalinclude} piexample/asyncpi.py
:linenos:
```

Every place you see `await`, that's where code pauses, gives up control and lets
the event loop (which is created by `asyncio.run`, there are third party ones
too) take control and "unpause" some other waiting `async` function if it's
ready.

You will notice no performance improvement over the single-threaded version of
the code, since the asyncio event loop runs on the main thread, and relies on
the async function to give up control so that other async functions can proceed,
like we've done using `asyncio.sleep()`.

Notice how we didn't need a special `queue` like in some of the other examples.
We could just create and loop over a normal list filled with tasks.

Also notice that these "async functions" are called and create the awaitable
object, so we didn't need any odd `(f, args)` syntax when making them, just the
normal `f(args)`. Every object you create that is awaitable should eventually be
awaited, Python will show a warning otherwise.

`async` is great for processing that takes time but shouldn't hog up all the
CPU. It is mostly used for "reactive" programs that do something based on
external input (GUIs, networking, etc).

It is also possible to run `async` code in a thread by awaiting on
`asyncio.to_thread(async_function, *args)`.

```{literalinclude} piexample/asyncpi_thread.py
:linenos:
```

Since the actual multithreading above comes from moving a function into threads,
it is identical to the threading examples when it comes to performance (same-ish
on normal Python, faster on free-threaded).

Outside of the `to_thread` part, we don't have to worry about normal thread
issues, like data races, thread safety, etc, as it's just oddly written single
threaded code.
