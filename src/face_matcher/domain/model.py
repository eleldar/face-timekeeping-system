from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    path: str


@dataclass
class Candidate:
    name: str | None
    found_path: str | None
