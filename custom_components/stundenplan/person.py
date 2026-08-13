"""Person-related schedule helpers."""

from datetime import date, datetime

from .models import DaySchedule, Person
from .schedule import get_current_lesson, get_next_lesson


def get_current_lesson_for_person(
    person: Person,
    current: datetime,
) -> tuple[str, DaySchedule] | None:
    """Return the current lesson for a person."""
    return get_current_lesson(person.schedule, current)


def get_next_lesson_for_person(
    person: Person,
    current: datetime,
) -> tuple[date, str, DaySchedule] | None:
    """Return the next lesson for a person."""
    return get_next_lesson(person.schedule, current)