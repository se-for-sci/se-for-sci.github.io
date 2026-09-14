from concurrent.futures import ThreadPoolExecutor
import contextlib
import queue
import time

task_queue = queue.Queue()
result_queue = queue.SimpleQueue()


def worker(q: queue.Queue, r: queue.SimpleQueue) -> None:
    with contextlib.suppress(queue.ShutDown):
        while True:
            task = q.get()
            time.sleep(0.1)
            r.put(task * 10)
            q.task_done()


with ThreadPoolExecutor() as pool:
    # Start up 8 workers
    for _ in range(8):
        pool.submit(worker, task_queue, result_queue)

    # Load work for the workers to do
    for i in range(50):
        task_queue.put(i)

    # Wait until task_done() is called the same number of times as items in the queue
    task_queue.shutdown()
    task_queue.join()


print(sum(result_queue.get() for _ in range(result_queue.qsize())))
