from dataclasses import dataclass


@dataclass(frozen=True)
class Instance:
    title: str
    pid: int