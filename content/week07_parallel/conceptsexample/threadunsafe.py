from concurrent.futures import ThreadPoolExecutor

x = [0]


def add(num: int) -> None:
    for i in range(num):
        x[0] += 1


with ThreadPoolExecutor() as pool:
    for _ in range(8):
        pool.submit(add, 10_000)

print(x[0])
