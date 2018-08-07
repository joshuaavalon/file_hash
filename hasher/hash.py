from dataclasses import dataclass

__all__ = ["Hash"]


@dataclass
class Hash:
    hex_digest: str
    algorithm: str
