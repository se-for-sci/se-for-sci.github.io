# Parallel computing

Multithreading in Python is split into two groups: multithreading and
multiprocessing. Async could be seen as a third group, and extensions can be
implemented with multithreading as well. Python 3.12 added a subinterpeters each
with their own GIL. Python 3.13 is also adding no-gil threading.

Multithreading means you have one Python process. Due to the way that Python is
implemented with Global Interpreter Lock (GIL), you can only run one Python
instruction at a time, even from multiple threads. This is very limiting, but
not the end of the world for multithreading. One loophole is that this only is
valid for Python instructions; as long as they don't change Python's internal
memory model (like changing refcounts), compiled code is allowed to escape the
GIL. This includes NumPy code and JIT code like Numba!

The other method is multiprocessing. This involves creating two or more Python
processes, with their own memory space, then either transferring data (via
Pickle) or by sharing selected portions of memory. This is much heaver-weight
than threading, but can be used effectively.

A third category is async code; this is not actually multithreaded, but provides
very similar mechanism for control flow, and can be combined with real
multithreading. If Python was built without threads (such as for WebAssembly),
then this is the only option.

The relevant built-in libraries supporting multithreaded code:

- **Threading**: A basic interface to **thread**, still rather low-level by
  modern standards.
- **Multiprocessing**: Similar to threading, but with processes. Shared memory
  tools added in Python 3.8.
- **Concurrent.futures**: Higher-level interface to both threading and
  multiprocessing.
- **Ascynio**: Explicit control over switching points.

For all of these examples, we'll use this fractal example:

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

Our example above could look like this:

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

Python provides a higher-level abstraction that is especially useful in data
processing: Executors (both a threading version and a multiprocessing version).
These are build around a thread pool and context managers:

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

This is shared across processes and can enen outlive the owning process, so make
sure you close (per process) and unlink (once) the memory you take! Having a
fixed name (like above) can be safer.

When using multiprocessing (including `concurrent.futures.ProcessPoolExecutor`),
you usually need source code to be importable, since the new process will have
to get it's instructions too. That can make it a bit harder to use from
something like a notebook.

## Async code in Python

Here's an example of an async function:

```python
async def compute_async():
    await asyncio.gather(*(asyncio.to_thread(piece, x) for x in range(size[0] // 10)))
```
