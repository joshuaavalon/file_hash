from logging import getLogger
from multiprocessing import JoinableQueue, Process
from pathlib import Path
from typing import Optional

from file_hash.algorithm import Algorithm
from file_hash.report import Record, Report
from file_hash.serialize import HashFileHandler

__all__ = ["HashingWorker", "HashValidationWorker", "MissingFileWorker"]
logger = getLogger("hasher")


class PathWorker(Process):
    def __init__(self, queue: JoinableQueue, report: Optional[Report]):
        super().__init__()
        self.queue = queue
        self.report = report
        self.handler = HashFileHandler()

    def run(self):
        while True:
            path = self.queue.get()
            if path is None:
                self.queue.task_done()
                break
            try:
                self._run(path)
            except IOError as e:
                logger.error(f"I/O error: {e}")
                self.report.append(Record(path=path, error=str(e)))
            except Exception as e:
                logger.exception(f"Unexpected error: {e}")
                raise e
            finally:
                self.queue.task_done()

    def _run(self, path: Path):
        raise NotImplementedError()


class HashingWorker(PathWorker):
    def __init__(self, queue: JoinableQueue,
                 algorithm: Algorithm,
                 dry_run: bool,
                 report: Optional[Report]):
        super().__init__(queue, report)
        self.algorithm = algorithm
        self.dry_run = dry_run

    def _run(self, path: Path):
        file_hash = self.algorithm.hash(path)
        self.handler.save(file_hash, path, self.dry_run)
        self.report.append(Record(path=path, hash=file_hash))


class HashValidationWorker(PathWorker):
    def _run(self, path: Path):
        hashes = self.handler.load(path)
        for file_hash in hashes:
            algorithm = Algorithm.new(file_hash.algorithm)
            full_path = path.absolute()
            name = algorithm.name
            if algorithm.hash(path) == file_hash:
                logger.info(f"{name} hash of {full_path} is valid")
                self.report.append(Record(path=path, hash=file_hash))
            else:
                message = f"{name} hash of {full_path} is invalid"
                logger.warning(message)
                record = Record(path=path, hash=file_hash, error=message)
                self.report.append(record)


class MissingFileWorker(PathWorker):
    def _run(self, path: Path):
        file_path: Path = path.parent.joinpath(path.stem)
        if file_path.exists():
            return
        file_hash = self.handler.load(path, exact=True)[0]
        message = f"{path.absolute()} exists " \
                  f"but {file_path.absolute()} does not exist!"
        logger.warning(message)
        self.report.append(Record(path=path, hash=file_hash, error=message))
