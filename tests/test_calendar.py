"""Tests for the Stundenplan calendar platform."""

from datetime import datetime, timedelta

from homeassistant.util import dt as dt_util

from custom_components.stundenplan.calendar import StundenplanCalendar
from custom_components.stundenplan.config import (
    load_schedule_manager_from_yaml,
)


async def test_calendar_returns_lessons_in_requested_range(hass) -> None:
    """Return all configured lessons in chronological order."""
    manager = load_schedule_manager_from_yaml("tests/data/schedules.yaml")
    person = manager.get_person("paulina")
    assert person is not None

    calendar = StundenplanCalendar(person)
    timezone = dt_util.DEFAULT_TIME_ZONE
    start = datetime(2026, 10, 7, 7, 0, tzinfo=timezone)
    end = start + timedelta(hours=3)

    events = await calendar.async_get_events(hass, start, end)

    assert [event.summary for event in events] == [
        "Mathe",
        "Mathe",
        "KR",
    ]
    assert events[0].start == datetime(
        2026, 10, 7, 7, 40, tzinfo=timezone
    )
    assert events[0].end == datetime(
        2026, 10, 7, 8, 20, tzinfo=timezone
    )
    assert events[0].uid == "paulina-2026-10-07-1"


async def test_calendar_event_is_next_upcoming_lesson(hass, freezer) -> None:
    """Expose the next lesson as the calendar entity's current event."""
    manager = load_schedule_manager_from_yaml("tests/data/schedules.yaml")
    person = manager.get_person("paulina")
    assert person is not None

    timezone = dt_util.DEFAULT_TIME_ZONE
    now = datetime(2026, 10, 7, 7, 30, tzinfo=timezone)
    freezer.move_to(now)
    calendar = StundenplanCalendar(person)

    event = calendar.event

    assert event is not None
    assert event.summary == "Mathe"
    assert event.start == datetime(
        2026, 10, 7, 7, 40, tzinfo=timezone
    )
