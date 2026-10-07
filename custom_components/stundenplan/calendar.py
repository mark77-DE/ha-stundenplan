"""Calendar platform for individual school schedules."""

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .models import Person


class StundenplanCalendar(CalendarEntity):
    """A read-only calendar containing a person's recurring lessons."""

    _attr_should_poll = False

    def __init__(self, person: Person) -> None:
        """Initialize the calendar for one person."""
        self._person = person
        self._attr_unique_id = f"stundenplan_{person.id}"
        self._attr_name = f"Stundenplan {person.name}"

    @property
    def event(self) -> CalendarEvent | None:
        """Return the currently active or next upcoming lesson."""
        now = dt_util.now()
        events = self._events_between(
            now,
            now + timedelta(days=8),
        )
        return next(
            (event for event in events if event.end > now),
            None,
        )

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return all lessons that overlap the requested time range."""
        return self._events_between(start_date, end_date)

    async def async_added_to_hass(self) -> None:
        """Refresh the calendar state as lessons start and finish."""
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

    async def _handle_time_change(self, now: datetime) -> None:
        """Recompute the active event when the minute changes."""
        self.async_write_ha_state()

    def _events_between(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Build lesson events in a half-open datetime range."""
        if end_date <= start_date:
            return []

        first_day = start_date.date()
        last_day = end_date.date()
        timezone = start_date.tzinfo or dt_util.DEFAULT_TIME_ZONE
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=timezone)
        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=timezone)
        events: list[CalendarEvent] = []
        current_day = first_day

        while current_day <= last_day:
            weekday = current_day.strftime("%A").lower()
            for block in self._person.schedule.blocks:
                day_schedule = block.days.get(weekday)
                if day_schedule is None:
                    continue

                event_start = datetime.combine(
                    current_day,
                    day_schedule.start,
                    tzinfo=timezone,
                )
                event_end = datetime.combine(
                    current_day,
                    day_schedule.end,
                    tzinfo=timezone,
                )

                if event_start < end_date and event_end > start_date:
                    events.append(
                        CalendarEvent(
                            start=event_start,
                            end=event_end,
                            summary=day_schedule.subject,
                            description=f"Stundenplan-Block {block.id}",
                            uid=(
                                f"{self._person.id}-"
                                f"{current_day.isoformat()}-{block.id}"
                            ),
                        )
                    )

            current_day += timedelta(days=1)

        return sorted(events, key=lambda event: event.start)
