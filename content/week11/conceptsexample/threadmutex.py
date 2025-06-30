from concurrent.futures import ThreadPoolExecutor
import threading

x = [0]
lock = threading.Lock()


def add(num: int) -> None:
    for i in range(num):
        with lock:
            x[0] += 1


with ThreadPoolExecutor() as pool:
    for _ in range(8):
        pool.submit(add, 10_000)

print(x[0])
