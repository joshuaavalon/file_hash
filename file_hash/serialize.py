import hashlib
from logging import getLogger
from pathlib import Path
from typing import List

from file_hash.hash import Hash

__all__ = ["HashFileHandler"]

logger = getLogger("hasher")


class HashFileHandler:
    def save(self, file_hash: Hash, path: Path, dry_run: bool):
        hash_path = self.hash_path(path, file_hash).absolute()
        hex_digest = file_hash.hex_digest

        logger.info(f"Write {hex_digest} to {hash_path}")

        if not dry_run:
            with open(hash_path, "w", encoding="utf-8") as file:
                file.write(hex_digest)

    def load(self, path: Path, exact: bool = False) -> List[Hash]:
        if exact:
            hash_paths = [path]
        else:
            hash_paths = [self._hash_path(path, algorithm)
                          for algorithm in hashlib.algorithms_available]
        hash_paths = filter(lambda p: p.is_file(), hash_paths)
        hashes = []
        for hash_path in hash_paths:
            with open(hash_path, "r", encoding="utf-8") as file:
                hex_digest = file.read()
            hashes.append(Hash(hex_digest=hex_digest,
                               algorithm=hash_path.suffix[1:]))
        return hashes

    @staticmethod
    def hash_path(path: Path, file_hash: Hash) -> Path:
        return HashFileHandler._hash_path(path, file_hash.algorithm)

    @staticmethod
    def _hash_path(path: Path, algorithm: str) -> Path:
        return path.with_suffix(f"{path.suffix}.{algorithm}")
