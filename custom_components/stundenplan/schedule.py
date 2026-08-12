"""Schedule calculation logic."""

from datetime import date, datetime, timedelta

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


def get_next_lesson(
    schedule: Schedule,
    current: datetime,
) -> tuple[date, str, DaySchedule] | None:
    """Return the next upcoming lesson."""
    for day_offset in range(0, 8):
        target_date = current.date() + timedelta(days=day_offset)
        day = target_date.strftime("%A").lower()

        for block in schedule.blocks:
            day_schedule = block.days.get(day)

            if day_schedule is None:
                continue

            if day_offset == 0 and day_schedule.start < current.time():
                continue

            return target_date, block.id, day_schedule

    return None
    