from logging import getLogger
from multiprocessing import JoinableQueue, Queue
from os import cpu_count
from pathlib import Path
from queue import Empty, Queue
from typing import Optional, Union

from hasher.algorithm import Algorithm
from hasher.filter import Filter, HashFilter
from hasher.worker import HashValidationWorker, HashingWorker, MissingFileWorker

NUMBER_OF_CPU = cpu_count()
if NUMBER_OF_CPU is not None and NUMBER_OF_CPU > 0:
    WORKER_COUNT = NUMBER_OF_CPU * 2
else:
    WORKER_COUNT = 1

DEFAULT_QUEUE_SIZE = 1000

__all__ = ["generate_hash", "validate_hash"]
logger = getLogger("hasher")


def generate_hash(path: Path,
                  path_filter: Filter,
                  algorithm: Algorithm,
                  dry_run: bool,
                  recursive: bool,
                  worker_count: int = WORKER_COUNT,
                  queue_size: Optional[int] = DEFAULT_QUEUE_SIZE):
    paths = JoinableQueue(queue_size)
    for _ in range(0, worker_count):
        HashingWorker(paths, algorithm, dry_run).start()
    find_paths(path, paths, path_filter, recursive, worker_count)


def find_paths(path: Path,
               queue: JoinableQueue,
               path_filter: Union[Filter, HashFilter],
               recursive: bool,
               worker_count: int):
    paths = Queue()
    # It needs to extract child first or else recursive will prevent it
    if path.is_dir():
        for child in path.iterdir():
            paths.put(child)
    else:
        paths.put(path)
    while True:
        try:
            new_path: Path = paths.get(timeout=1)
        except Empty:
            break
        if not path_filter.filter(new_path):
            continue
        if new_path.is_file():
            queue.put(new_path)
        elif new_path.is_dir():
            if recursive:
                for child in new_path.iterdir():
                    paths.put(child)
    for i in range(0, worker_count):
        queue.put(None)
    queue.join()


def validate_hash(path: Path,
                  path_filter: Filter,
                  recursive: bool,
                  worker_count: int = WORKER_COUNT,
                  queue_size: Optional[int] = DEFAULT_QUEUE_SIZE):
    paths = JoinableQueue(queue_size)
    for _ in range(0, worker_count):
        HashValidationWorker(paths).start()
    find_paths(path, paths, path_filter, recursive, worker_count)

    hash_paths = JoinableQueue(queue_size)
    hash_filter = HashFilter(symlink=path_filter.symlink)
    for _ in range(0, worker_count):
        MissingFileWorker(hash_paths).start()
    find_paths(path, hash_paths, hash_filter, recursive, worker_count)
