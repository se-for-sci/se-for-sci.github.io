import contextlib
import random
import statistics
import time


@contextlib.contextmanager
def timer():
    start = time.monotonic()
    yield
    print(f"Took {time.monotonic() - start:.3}s to run")


@timer()
def pi(trials: int) -> float:
    Ncirc = 0

    for _ in range(trials):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        if x * x + y * y <= 1:
            Ncirc += 1

    return 4.0 * (Ncirc / trials)


print(f"{pi(10_000_000)=}")
