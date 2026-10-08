"""Sensor platform for the Stundenplan integration."""

from datetime import date, datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .models import Person
from .person import (
    get_current_lesson_for_person,
    get_next_lesson_for_person,
)


def _lessons_for_day(person: Person, day: date) -> list[dict[str, str]]:
    """Return all lessons for a day, ordered by start time."""
    weekday = day.strftime("%A").lower()
    lessons = []

    for block in person.schedule.blocks:
        lesson = block.days.get(weekday)
        if lesson is None:
            continue

        lessons.append(
            {
                "block": block.id,
                "subject": lesson.subject,
                "start": lesson.start.isoformat(timespec="minutes"),
                "end": lesson.end.isoformat(timespec="minutes"),
            }
        )

    return sorted(lessons, key=lambda lesson: lesson["start"])


def _week_schedule(
    person: Person,
    day: date,
) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    """Return weekday lessons and a shared time grid for the current week."""
    monday = day - timedelta(days=day.weekday())
    days = [
        {
            "date": (monday + timedelta(days=offset)).isoformat(),
            "weekday": (monday + timedelta(days=offset)).strftime("%A").lower(),
            "lessons": _lessons_for_day(person, monday + timedelta(days=offset)),
        }
        for offset in range(5)
    ]

    boundaries = sorted(
        {
            boundary
            for week_day in days
            for lesson in week_day["lessons"]
            for boundary in (lesson["start"], lesson["end"])
        }
    )
    slots = [
        {"start": start, "end": end}
        for start, end in zip(boundaries, boundaries[1:])
        if any(
            lesson["start"] <= start and end <= lesson["end"]
            for week_day in days
            for lesson in week_day["lessons"]
        )
    ]

    for week_day in days:
        subjects = [
            next(
                (
                    lesson["subject"]
                    for lesson in week_day["lessons"]
                    if lesson["start"] <= slot["start"]
                    and slot["end"] <= lesson["end"]
                ),
                None,
            )
            for slot in slots
        ]
        cells = []
        slot_index = 0
        while slot_index < len(slots):
            subject = subjects[slot_index]
            if subject is None:
                cells.append({"subject": "", "rowspan": 1})
                slot_index += 1
                continue

            group_end = slot_index + 1
            while (
                group_end < len(slots)
                and subjects[group_end] == subject
                and slots[group_end - 1]["end"] == slots[group_end]["start"]
            ):
                group_end += 1

            cells.append({"subject": subject, "rowspan": group_end - slot_index})
            cells.extend([None] * (group_end - slot_index - 1))
            slot_index = group_end

        week_day["grid_cells"] = cells

    return days, slots


def _week_focus_date(current: datetime) -> date:
    """Return today until 17:00, then the next weekday (Monday-Friday)."""
    focus = current.date()
    if focus.weekday() >= 5:
        return focus + timedelta(days=7 - focus.weekday())
    if current.hour >= 17:
        focus += timedelta(days=1)
        if focus.weekday() >= 5:
            focus += timedelta(days=7 - focus.weekday())
    return focus




class StundenplanSensor(SensorEntity):
    """Representation of a person's school schedule."""

    _attr_should_poll = False

    def __init__(
        self,
        person: Person,
    ) -> None:
        """Initialize the sensor."""
        self._person = person

        self._attr_unique_id = f"stundenplan_{person.id}"
        self._attr_name = f"Stundenplan {person.name}"
        self._current_time = dt_util.now()

    @property
    def native_value(self) -> str:
        """Return the current subject."""
        current = self._current_time

        lesson = get_current_lesson_for_person(
            self._person,
            current,
        )

        if lesson is None:
            return "frei"

        _, day_schedule = lesson

        return day_schedule.subject

    @property
    def extra_state_attributes(self) -> dict:
        """Return schedule information as attributes."""
        current = self._current_time
        focus_date = _week_focus_date(current)
        week_lessons, week_time_slots = _week_schedule(
            self._person,
            focus_date,
        )

        attributes = {
            "person_id": self._person.id,
            "person_name": self._person.name,
            "week_focus_date": focus_date.isoformat(),
            "week_start": (
                focus_date - timedelta(days=focus_date.weekday())
            ).isoformat(),
            "week_lessons": week_lessons,
            "week_time_slots": week_time_slots,
            "today_date": current.date().isoformat(),
            "today_lessons": _lessons_for_day(self._person, current.date()),
            "tomorrow_date": (current.date() + timedelta(days=1)).isoformat(),
            "tomorrow_lessons": _lessons_for_day(
                self._person,
                current.date() + timedelta(days=1),
            ),
        }

        current_lesson = get_current_lesson_for_person(
            self._person,
            current,
        )

        if current_lesson is not None:
            block_id, day_schedule = current_lesson

            attributes.update(
                {
                    "current_block": block_id,
                    "current_start": day_schedule.start.isoformat(),
                    "current_end": day_schedule.end.isoformat(),
                }
            )

        next_lesson = get_next_lesson_for_person(
            self._person,
            current,
        )

        if next_lesson is not None:
            next_date, block_id, day_schedule = next_lesson

            attributes.update(
                {
                    "next_subject": day_schedule.subject,
                    "next_block": block_id,
                    "next_date": next_date.isoformat(),
                    "next_start": day_schedule.start.isoformat(),
                    "next_end": day_schedule.end.isoformat(),
                }
            )

        return attributes

    async def async_added_to_hass(self) -> None:
        """Set up time-based updates."""
        await super().async_added_to_hass()

        remove_listener = async_track_time_change(
            self.hass,
            self._handle_time_change,
            second=0,
        )

        self.async_on_remove(remove_listener)

        self.hass.bus.async_listen_once(
            "homeassistant_stop",
            lambda event: remove_listener(),
        )

    async def _handle_time_change(
        self,
        now: datetime,
    ) -> None:
        """Update the sensor when the time changes."""
        self._current_time = now
        self.async_write_ha_state()
