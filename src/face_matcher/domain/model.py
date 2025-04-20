from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    path: str


@dataclass
class Candidate:
    name: str | None
    found_path: str | None


@dataclass
class MatchOutput:
    fake: bool
    access: bool
