"""Tests for the Stundenplan schedule engine."""

from datetime import datetime, time

from custom_components.stundenplan.models import Block, DaySchedule, Schedule
from custom_components.stundenplan.schedule import (
    get_current_lesson,
    get_next_lesson,
)


def create_paulina_schedule() -> Schedule:
    """Create Paulina's current schedule for testing."""
    return Schedule(
        name="Paulina",
        blocks=[
            Block(
                id="1",
                days={
                    "monday": DaySchedule(time(7, 40), time(8, 20), "WP1"),
                    "tuesday": DaySchedule(time(7, 40), time(8, 20), "Mathe"),
                    "wednesday": DaySchedule(time(7, 40), time(8, 20), "Mathe"),
                    "thursday": DaySchedule(time(7, 40), time(8, 20), "Deutsch"),
                    "friday": DaySchedule(time(7, 40), time(8, 20), "Physik"),
                },
            ),
            Block(
                id="2",
                days={
                    "monday": DaySchedule(time(8, 20), time(9, 0), "WP1"),
                    "tuesday": DaySchedule(time(8, 20), time(9, 0), "Mathe"),
                    "wednesday": DaySchedule(time(8, 20), time(9, 0), "Mathe"),
                    "thursday": DaySchedule(time(8, 20), time(9, 0), "Deutsch"),
                    "friday": DaySchedule(time(8, 20), time(9, 0), "Physik"),
                },
            ),
            Block(
                id="HT",
                days={
                    "monday": DaySchedule(time(9, 10), time(9, 50), "HT"),
                    "tuesday": DaySchedule(time(9, 10), time(9, 50), "HT"),
                    "wednesday": DaySchedule(time(9, 10), time(9, 50), "KR"),
                    "thursday": DaySchedule(time(9, 10), time(9, 50), "HT"),
                    "friday": DaySchedule(time(9, 10), time(9, 50), "HT"),
                },
            ),
            Block(
                id="3",
                days={
                    "monday": DaySchedule(time(10, 10), time(10, 50), "Englisch"),
                    "tuesday": DaySchedule(time(10, 10), time(10, 50), "Chemie"),
                    "wednesday": DaySchedule(time(10, 10), time(10, 50), "Geo"),
                    "thursday": DaySchedule(time(10, 10), time(10, 50), "Bio"),
                    "friday": DaySchedule(time(10, 10), time(10, 50), "WP1"),
                },
            ),
            Block(
                id="4",
                days={
                    "monday": DaySchedule(time(10, 50), time(11, 30), "Englisch"),
                    "tuesday": DaySchedule(time(10, 50), time(11, 30), "Chemie"),
                    "wednesday": DaySchedule(time(10, 50), time(11, 30), "Geo"),
                    "thursday": DaySchedule(time(10, 50), time(11, 30), "Bio"),
                    "friday": DaySchedule(time(10, 50), time(11, 30), "WP1"),
                },
            ),
            Block(
                id="5",
                days={
                    "monday": DaySchedule(time(11, 50), time(12, 30), "Deutsch"),
                    "tuesday": DaySchedule(time(11, 50), time(12, 30), "Sport"),
                    "wednesday": DaySchedule(time(11, 50), time(12, 30), "Englisch"),
                    "thursday": DaySchedule(time(11, 50), time(12, 30), "WP2"),
                    "friday": DaySchedule(time(11, 50), time(12, 30), "Geschichte"),
                },
            ),
            Block(
                id="6",
                days={
                    "monday": DaySchedule(time(12, 30), time(13, 10), "Deutsch"),
                    "tuesday": DaySchedule(time(12, 30), time(13, 10), "Hosp."),
                    "wednesday": DaySchedule(time(12, 30), time(13, 10), "Englisch"),
                    "thursday": DaySchedule(time(12, 30), time(13, 10), "WP2"),
                    "friday": DaySchedule(time(12, 30), time(13, 10), "Geschichte"),
                },
            ),
            Block(
                id="7",
                days={
                    "tuesday": DaySchedule(time(13, 40), time(14, 20), "WiPo"),
                    "friday": DaySchedule(time(13, 20), time(14, 0), "WP2"),
                },
            ),
            Block(
                id="8",
                days={
                    "tuesday": DaySchedule(time(14, 20), time(15, 0), "WiPo"),
                },
            ),
        ],
    )


def test_current_lesson_tuesday_block_7() -> None:
    """Tuesday 14:00 should be WiPo in block 7."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 0),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "WiPo"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_current_lesson_friday_block_7() -> None:
    """Friday 13:30 should be WP2 in block 7."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 14, 13, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "WP2"
    assert lesson.start == time(13, 20)
    assert lesson.end == time(14, 0)


def test_no_block_7_on_monday() -> None:
    """Monday should have no block 7."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 10, 13, 30),
    )

    assert result is None


def test_wednesday_block_3() -> None:
    """Wednesday 10:20 should be Geography in block 3."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 12, 10, 20),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "3"
    assert lesson.subject == "Geo"


def test_wednesday_special_block() -> None:
    """Wednesday 09:30 should be KR."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 12, 9, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "HT"
    assert lesson.subject == "KR"


def test_before_school() -> None:
    """Before the first block there should be no current lesson."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 10, 7, 30),
    )

    assert result is None


def test_after_school() -> None:
    """After the last block there should be no current lesson."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 14, 14, 30),
    )

    assert result is None


def test_sunday() -> None:
    """Sunday should have no lessons."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 16, 10, 0),
    )

    assert result is None


def test_block_boundary() -> None:
    """At the exact end of a block the block should no longer be active."""
    schedule = create_paulina_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 14, 14, 0),
    )

    assert result is None
    
    
    
def test_next_lesson_tuesday_before_block_7() -> None:
    """Tuesday 13:30 should return block 7 as the next lesson."""
    schedule = create_paulina_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 13, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "7"
    assert lesson.subject == "WiPo"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_next_lesson_tuesday_block_7() -> None:
    """During block 7, block 8 should be the next lesson."""
    schedule = create_paulina_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "8"
    assert lesson.subject == "WiPo"
    assert lesson.start == time(14, 20)
    assert lesson.end == time(15, 0)


def test_next_lesson_friday_before_block_7() -> None:
    """Friday 13:00 should return block 7 as the next lesson."""
    schedule = create_paulina_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 14, 13, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 14).date()
    assert block_id == "7"
    assert lesson.subject == "WP2"
    assert lesson.start == time(13, 20)
    assert lesson.end == time(14, 0)


def test_next_lesson_after_friday_school() -> None:
    """After Friday school, Monday block 1 should be next."""
    schedule = create_paulina_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 14, 15, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 17).date()
    assert block_id == "1"
    assert lesson.subject == "WP1"
    assert lesson.start == time(7, 40)
    assert lesson.end == time(8, 20)


def test_next_lesson_saturday() -> None:
    """Saturday should return Monday block 1."""
    schedule = create_paulina_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 15, 12, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 17).date()
    assert block_id == "1"
    assert lesson.subject == "WP1"


def test_next_lesson_sunday() -> None:
    """Sunday should return Monday block 1."""
    schedule = create_paulina_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 16, 12, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 17).date()
    assert block_id == "1"
    assert lesson.subject == "WP1"


def test_next_lesson_at_block_start() -> None:
    """At the exact start of a block, the next lesson is that block."""
    schedule = create_paulina_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 13, 40),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "7"
    assert lesson.subject == "WiPo"


def test_next_lesson_at_block_end() -> None:
    """At the exact end of a block, the following block is next."""
    schedule = create_paulina_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 20),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "8"
    assert lesson.subject == "WiPo"    