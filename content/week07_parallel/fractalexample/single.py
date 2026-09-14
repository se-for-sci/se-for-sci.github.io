import contextlib
import time

import numpy as np


@contextlib.contextmanager
def timer():
    start = time.monotonic()
    yield
    print(f"Took {time.monotonic() - start}s to run")


def prepare(height, width):
    c = np.sum(
        np.broadcast_arrays(*np.ogrid[-1j : 0j : height * 1j, -1.5 : 0 : width * 1j]),
        axis=0,
    )
    fractal = np.zeros_like(c, dtype=np.int32)
    return c, fractal


@timer()
def run(c, fractal, maxiterations=20):
    z = c

    for i in range(1, maxiterations + 1):
        z = z**2 + c  # Compute z
        diverge = abs(z) > 2  # Divergence criteria

        z[diverge] = 2  # Keep number size small
        fractal[~diverge] = i  # Fill in non-diverged iteration number


size = 4000, 3000

c, fractal = prepare(*size)
fractal = run(c, fractal)
