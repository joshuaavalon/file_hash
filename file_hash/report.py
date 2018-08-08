from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from jinja2 import Environment, PackageLoader

from file_hash.hash import Hash

__all__ = ["Record", "Report"]

loader = PackageLoader("file_hash")
environment = Environment(loader=loader)
template = environment.get_template("report.html")


@dataclass
class Record:
    path: Path
    hash: Optional[Hash] = None
    error: Optional[str] = None


class Report:
    def __init__(self, records: List[Record]):
        self.records = records

    def append(self, record: Record):
        self.records.append(record)

    def generate(self):
        success = []
        error = []
        for record in self.records:
            if record.error is None:
                success.append(record)
            else:
                error.append(record)
        return template.render(success=success, error=error)
