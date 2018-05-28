import logging
from queue import Queue
import sched
import time
from threading import Thread
from news.config import config
from news.feed import fetch
from news.persist import persist

logging.basicConfig(level=logging.INFO)
queue = Queue()


def persist_wrapper(queue):
    thread = Thread(target=persist, args=(queue, ))
    thread.daemon = True
    thread.start()


def fetch_wrapper(source, queue):
    thread = Thread(
        target=fetch, args=(
            source,
            queue,
        ))
    thread.daemon = True
    thread.start()


def enter_interval(scheduler, delay, action, argument=(), kwargs={}):
    scheduler.enter(delay, 1, enter_interval,
                    (scheduler, delay, action, argument, kwargs))
    action(*argument, **kwargs)


if __name__ == '__main__':
    # Start persistence worker
    persist_wrapper(queue)

    # Schedule feed polling
    scheduler = sched.scheduler(time.time, time.sleep)
    for source in config['sources']:
        enter_interval(
            scheduler,
            config['fetch_interval'],
            fetch_wrapper,
            argument=(
                source,
                queue,
            ))

    scheduler.run()
