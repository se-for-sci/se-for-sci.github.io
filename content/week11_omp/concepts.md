# Parallel concepts

These are general concepts, with some examples primarily in Python.

Note when playing with these examples: errors can get swallowed in threads we
create, so static checks are really useful. The mechanism used to show an error
varies based on several factors. `concurrent.futures` rethrows the exception
when you get the result. `threading` prints out errors as strings (customizable
in 3.8+, though). Etc.

Quite a few of these work across threading, interpreters, and multiprocessing in
Python, and are generally found in other languages too, sometimes with different
names.

## Thread safety

Is it safe to use a variable from multiple threads? Generally, read-only
variables are fine; if you don't modify something, there's no problem. But if
you modify a variable, there's a potential problem. Here's an example:

```{literalinclude} conceptsexample/threadunsafe.py

```

First, I set up a mutable variable, which is simply a list containing an item. I
did this so I can avoid writing the word `gllobal`, to show that the problem is
about mutating variables shared between threads, not unique to global variables.
I use `+=` to add 1. Remember, `x+=1` really does `x = x + 1`: the processor
reads the value, then adds one, then writes the value. If another thread reads
the value in the middle of that process, then the final result will be one less
than you expected!

If you run this with traditional Python, you'll probably get the trivial result:
80,000. That's due to Python's context switching; it's not context switching
within this operation. However, if you run it with free-threaded Python, you'll
get the normal multithreading result; some smaller number (around 17,000 for
me). (Don't rely on this in traditional Python either; this is a highly
simplified example and we are relying completely on the context switching points
helping us out here!).

This variable is not thread safe, which means we can't safely set it across
threads. We'll look at several ways to make or use thread safe variables.

## Mutex

One of the most general tools for thread safely is a mutex. In Python, it's
called a `Lock` or `RLock`, depending on if you can re-enter it in the same
thread. Let's take a look:

```{literalinclude} conceptsexample/threadmutex.py

```

Here, we create an instance of a `threading.Lock`. Now we protect the part of
our code that is mutating a variable by taking a lock with our mutex (using the
with block, which releases automatically when exiting the block).

Note this works because the variable itself (Lock instances) are threadsafe,
meaning taking a lock is guaranteed to work from any thread.

If you were going for performance, remember, now you have some extra overhead
_and_ only one thread at a time can make it through this portion of the code.
Free-threaded Python now gives the correct result, but is not really any faster
than traditional Python, because it's basically doing the same thing. If you
were doing a lot of work then locking around just a small portion of the code
doing some sort of synchronized update, that would be much better.

One common issue is called a "deadlock"; this is when you end up trying to
acquire a lock that is already acquired and won't be released. Sometimes if it
happens, it's from the same thread; such as if you have a recursive function
call. Since you usually don't need the lock from the same thread anyway, `RLock`
only blocks for a different thread trying to take the lock, solving this issue
at least in that one case.

## Semaphore

This is like a Lock, but instead of having an on/off state, it keeps track of a
number with a pre-set limit. For example, you can use a semaphore with a value 4
to create something that never runs more than 4 at a time. This is useful if you
have lots of threads, but a resource that you don't want to hit with all threads
at once.

## Atomic (not in Python)

Often, you need to lock because you are updating a single value. Modern
processors have specialized instructions to allow a value (like an integer) to
be updated in a way that is threadsafe without all the overhead of a lock (and
also they don't need a separate lock object).

Python doesn't have this, since modifying a Python object far more than a single
integer operation, and it's just a performance benefit over a mutex. You can use
`Event`, which is basically an atomic bool that you can wait on to be set
(True).

## Queue

Another common use case is adding and removing items, usually so one thread can
communicate work with another. A common use case will be creating a threadpool
of workers, then feeding work to them, with each thread picking up and
processing available work. This requires a threadsafe container, and it's
usually optimized for input and output, versus iteration for example.

Python has a `Queue` class, which is very powerful first-in, first-out (FIFO)
queue. A trimmed down version, `SimpleQueue`, is available, which doesn't have
the added task-related additions. There's also last-in, first out (LIFO) and
priority queues, depending on how you want to process tasks.

Here's an example:

```{literalinclude} conceptsexample/threadqueue.py

```

Here, we set up two queues. The first one has "jobs", and we tell the queue when
we've completed each task so that it knows when it's done (for clean shutdowns
of the worker threads, this also uses the `shutdown` mechanism introduced in
Python 3.13; you can set clean shutdown yourself if you want to support older
versions).

You might notice, if you look at the API for Queue, that there `block` and
`timeout` arguments on the get and put methods. You can decide if you want to
wait (`block` the current thread) till something is available, and also set a
timeout for how long to wait. Queue's can also have a maximum size, which is why
these exist for `put` as well. And, like locks, you can end up with deadlocks if
you are not careful.

```{admonition} Error checking
This example will swallow errors if you play with it and make a mistake. To fix that, you need to save the returned values from the `.submit(...)`'s, and then call `.result()` on them; that will reraise the exception in the current thread.
```

## Barrier

You can set a barrier, which pause threads until all of them reach that point.
For example, if you have 4 threads all computing something, you could use a
barrier to ensure all threads are done with that computation before you move on
to the next step.

## Local / shared memory

Sometimes you need memory just for a single thread. This differs a bit depending
on what you are using, so feel free to look it up. Threading, for example, has
`threading.local`. Async programming uses `contextvars`, since it actually runs
in one thread, it needs a different mechanism to track "context" instead. For
multiprocessing and interpereters, along with variables defined inside function
bodies and such, this is the default.

Then you may need "shared" memory. This might be the default for
threading/async, but is required for multiprocessing and subinterpreters. This
is not an option if you are running on multiple machines; then you must transfer
serialized objects instead. See the examples in the distributed section.

## Event loop

One common design for a reactive program is an event loop, where the program is
designed around a central loop, and it reacts to input. This is common with
async programming, but is also used by things like older GUI toolkits without
async, as well. Let's try creating our own from scratch using generators:

```{literalinclude} conceptsexample/eventloop.py

```

In this example, we start with tasks, and loop over them. Each task returns an
estimate of how long it will take. If you were to use one task within another
task, you would need `yield from` for the inner task. The loop waits for the
shortest task to be ready, then tries again. It's basic, but the idea is there.

We are using the generator system in Python (asyncio was built originally using
it), but we could have implemented it with the async special methods instead; it
would have been more verbose (since those weren't really designed to be hand
implemented simply), but is quite doable.

Let's try the same thing with asyncio:

```{literalinclude} conceptsexample/asyncloop.py

```

We don't sort the output here, but otherwise, it runs about the same, and takes
the same total amount of time. The difference here is we using a pre-existing
awaitable (sleep), so we have to use `await`, which is really just `yield from`
but using the async-named special methods.
