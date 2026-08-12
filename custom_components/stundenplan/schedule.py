"""Schedule calculation logic."""

from datetime import datetime

from .models import DaySchedule, Schedule


def get_current_lesson(
    schedule: Schedule,
    current: datetime,
) -> tuple[str, DaySchedule] | None:
    """Return the currently active block and lesson."""
    day = current.strftime("%A").lower()
    current_time = current.time()

    for block in schedule.blocks:
        day_schedule = block.days.get(day)

        if day_schedule is None:
            continue

        if day_schedule.start <= current_time < day_schedule.end:
            return block.id, day_schedule

    return None