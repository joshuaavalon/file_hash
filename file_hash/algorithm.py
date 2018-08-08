import hashlib
from pathlib import Path

from file_hash.hash import Hash

__all__ = ["Algorithm"]


class Algorithm:
    name: str

    def __init__(self, name: str):
        self.name = name

    def hash(self, path: Path) -> Hash:
        if not path.is_file():
            raise ValueError(f"{path.absolute()} is not a file.")

        file_hash = hashlib.new(self.name)
        with open(path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                file_hash.update(chunk)
        return Hash(hex_digest=file_hash.hexdigest(), algorithm=self.name)

    @classmethod
    def new(cls, algorithm: str) -> "Algorithm":
        if algorithm in hashlib.algorithms_available:
            return cls(algorithm)
        raise ValueError(f"{algorithm} does not exists!")
