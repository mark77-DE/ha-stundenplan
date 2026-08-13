"""Schedule calculation logic."""

from datetime import date, datetime, timedelta

from .models import DaySchedule, Schedule


def _get_day_blocks(
    schedule: Schedule,
    day: str,
) -> list[tuple[str, DaySchedule]]:
    """Return all blocks for a day, sorted by start time."""
    day_blocks = [
        (block.id, block.days[day])
        for block in schedule.blocks
        if day in block.days
    ]

    day_blocks.sort(key=lambda item: item[1].start)

    return day_blocks




def get_current_lesson(
    schedule: Schedule,
    current: datetime,
) -> tuple[str, DaySchedule] | None:
    """Return the currently active block and lesson."""
    day = current.strftime("%A").lower()
    current_time = current.time()

    for block_id, day_schedule in _get_day_blocks(schedule, day):
        if day_schedule.start <= current_time < day_schedule.end:
            return block_id, day_schedule

    return None


def get_next_lesson(
    schedule: Schedule,
    current: datetime,
) -> tuple[date, str, DaySchedule] | None:
    """Return the next upcoming lesson."""
    for day_offset in range(0, 8):
        target_date = current.date() + timedelta(days=day_offset)
        day = target_date.strftime("%A").lower()

        for block_id, day_schedule in _get_day_blocks(schedule, day):
            if day_offset == 0 and day_schedule.start < current.time():
                continue

            return target_date, block_id, day_schedule

    return None