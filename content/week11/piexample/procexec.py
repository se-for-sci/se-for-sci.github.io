import contextlib
import random
import statistics
import time
from concurrent.futures import ProcessPoolExecutor


@contextlib.contextmanager
def timer():
    start = time.monotonic()
    yield
    print(f"Took {time.monotonic() - start:.3}s to run")


def pi_each(trials: int) -> None:
    Ncirc = 0

    for _ in range(trials):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        if x * x + y * y <= 1:
            Ncirc += 1

    return 4.0 * (Ncirc / trials)


@timer()
def pi(trials: int, threads: int) -> float:
    with ProcessPoolExecutor() as pool:
        futures = pool.map(pi_each, [trials // threads] * threads)
        return statistics.mean(futures)


if __name__ == "__main__":
    print(f"{pi(10_000_000, 10)=}")
