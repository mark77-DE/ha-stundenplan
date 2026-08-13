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

    blocks: list[Block] = field(default_factory=list)
    
    
@dataclass
class Person:
    """A person with an individual school schedule."""

    id: str
    name: str
    schedule: Schedule    
    
@dataclass
class ScheduleManager:
    """Manage schedules for multiple persons."""

    persons: dict[str, Person] = field(default_factory=dict)

    def add_person(self, person: Person) -> None:
        """Add or replace a person."""
        self.persons[person.id] = person

    def get_person(self, person_id: str) -> Person | None:
        """Return a person by ID."""
        return self.persons.get(person_id)

    def all_persons(self) -> list[Person]:
        """Return all configured persons."""
        return list(self.persons.values())
        
    def has_person(self, person_id: str) -> bool:
        """Return whether a person is configured."""
        return person_id in self.persons

        