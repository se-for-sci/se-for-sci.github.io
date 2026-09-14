import contextlib
import random
import statistics
import threading
import time
import asyncio


@contextlib.asynccontextmanager
async def timer():
    start = time.monotonic()
    yield
    print(f"Took {time.monotonic() - start:.3}s to run")


async def pi_async(trials: int) -> float:
    Ncirc = 0
    rand = random.Random()

    for trial in range(trials):
        x = rand.uniform(-1, 1)
        y = rand.uniform(-1, 1)

        if x * x + y * y <= 1:
            Ncirc += 1

        # yield to event loop every 1000 iterations
        # This allows other asyncs to do their job
        if trial % 1000 == 0:
            await asyncio.sleep(0)

    return 4.0 * (Ncirc / trials)


@timer()
async def pi_all(trials: int, threads: int) -> float:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(pi_async(trials // threads)) for _ in range(threads)]
    return statistics.mean(t.result() for t in tasks)


def pi(trials: int, threads: int) -> float:
    return asyncio.run(pi_all(trials, threads))


print(f"{pi(10_000_000, 10)=}")
