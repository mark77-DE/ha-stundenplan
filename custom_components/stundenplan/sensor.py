"""Sensor platform for the Stundenplan integration."""

from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change

from .models import Person
from .person import (
    get_current_lesson_for_person,
    get_next_lesson_for_person,
)


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

    @property
    def native_value(self) -> str:
        """Return the current subject."""
        current = datetime.now()

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
        current = datetime.now()

        attributes = {
            "person_id": self._person.id,
            "person_name": self._person.name,
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
        self.async_write_ha_state()
