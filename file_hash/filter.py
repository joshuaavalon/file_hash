from dataclasses import dataclass, field
from hashlib import algorithms_available
from pathlib import Path
from re import search
from typing import List, Optional


def default_ignore_suffix() -> List[str]:
    return [f".{algorithm}" for algorithm in algorithms_available]


def default_ignore_prefix() -> List[str]:
    return ["."]


@dataclass
class Filter:
    ignore_suffix: List[str] = field(default_factory=default_ignore_suffix)
    ignore_prefix: List[str] = field(default_factory=default_ignore_prefix)
    min_size: int = -1
    max_size: int = -1
    regex: Optional[str] = None
    symlink: bool = False

    def filter(self, path: Path) -> bool:
        if not self.symlink and path.is_symlink():
            return False
        if self.min_size >= 0 and path.stat().st_size < self.min_size:
            return False
        if 0 <= self.max_size < path.stat().st_size:
            return False
        for prefix in self.ignore_prefix:
            if path.name.startswith(prefix):
                return False
        for suffix in self.ignore_suffix:
            if path.name.endswith(suffix):
                return False
        if self.regex is not None and search(self.regex, path.name) is None:
            return False
        return True


@dataclass
class HashFilter:
    suffix: List[str] = field(default_factory=default_ignore_suffix)
    symlink: bool = False

    def filter(self, path: Path) -> bool:
        if not self.symlink and path.is_symlink():
            return False
        for suffix in self.suffix:
            if path.name.endswith(suffix):
                return True
        return False
