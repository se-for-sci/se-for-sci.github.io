import contextlib
import random
import statistics
import threading
import time
import queue


@contextlib.contextmanager
def timer():
    start = time.monotonic()
    yield
    print(f"Took {time.monotonic() - start:.3}s to run")


def pi_each(q: queue.Queue, trials: int) -> None:
    Ncirc = 0
    rand = random.Random()

    for _ in range(trials):
        x = rand.uniform(-1, 1)
        y = rand.uniform(-1, 1)

        if x * x + y * y <= 1:
            Ncirc += 1

    q.put(4.0 * (Ncirc / trials))


@timer()
def pi(trials: int, threads: int) -> float:
    q = queue.Queue()
    workers = [
        threading.Thread(target=pi_each, args=(q, trials // threads))
        for _ in range(threads)
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    return statistics.mean(q.get() for _ in range(q.qsize()))


print(f"{pi(10_000_000, 10)=}")
