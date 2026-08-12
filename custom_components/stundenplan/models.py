"""Data models for the Stundenplan integration."""

from dataclasses import dataclass, field
from datetime import time


@dataclass
class DaySchedule:
    """Schedule information for one day."""

    start: time
    end: time
    subject: str


@dataclass
class Block:
    """A single schedule block."""

    id: str
    days: dict[str, DaySchedule] = field(default_factory=dict)


@dataclass
class Schedule:
    """Complete school schedule."""

    name: str
    blocks: list[Block] = field(default_factory=list)
    