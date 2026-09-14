import time


class NotReady(float):
    pass


def event_loop(tasks):
    while tasks:  # Stops when all tasks are done
        waits = []
        for task in tasks:
            try:
                res = task.send(None)  # async function runs here
                if isinstance(res, NotReady):
                    waits.append(res)  # Build up all the requested waits
                else:
                    yield res  # Produce result
            except StopIteration:
                tasks.remove(task)  # Task done, remove from tasks
        if waits:
            time.sleep(min(waits))  # Wait for the shortest requested wait


def sleep(t):
    endtime = time.time() + t
    while time.time() < endtime:
        yield NotReady(endtime - time.time())
    yield f"Sleep {t} over"


print(*event_loop([sleep(3), sleep(2), sleep(1), sleep(4)]), sep="\n")
