from dataclasses import dataclass


@dataclass
class Candidate:
    name: str | None
    found_path: str | None
