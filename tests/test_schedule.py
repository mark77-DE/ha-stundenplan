"""Tests for the Stundenplan schedule engine."""

import pytest

from datetime import date, datetime, time

from tests.fixtures import (
    create_complete_new_config,
    create_student_a_new_config,
    create_student_b_new_config,
)

from custom_components.stundenplan.parser import (
    parse_legacy_schedule,
    parse_schedule,
)

from custom_components.stundenplan.models import (
    Block,
    DaySchedule,
    Person,
    Schedule,
    ScheduleManager,
)


from custom_components.stundenplan.schedule import (
    get_current_lesson,
    get_next_lesson,
)

from custom_components.stundenplan.person import (
    get_current_lesson_for_person,
    get_next_lesson_for_person,
)

from custom_components.stundenplan.config import (
    create_schedule_manager,
    create_schedule_manager_from_config,
    load_schedule_manager_from_yaml,
)

def create_student_b_legacy_data() -> list[dict]:
    """Return Student B's complete legacy schedule."""
    return [
        {
            "block": 1,
            "start": {
                "monday": "07:40",
                "tuesday": "07:40",
                "wednesday": "07:40",
                "thursday": "07:40",
                "friday": "07:40",
            },
            "end": {
                "monday": "08:20",
                "tuesday": "08:20",
                "wednesday": "08:20",
                "thursday": "08:20",
                "friday": "08:20",
            },
            "class": {
                "monday": "Subject O",
                "tuesday": "",
                "wednesday": "Subject Z",
                "thursday": "Subject W",
                "friday": "Subject V",
            },
        },
        {
            "block": 2,
            "start": {
                "monday": "08:20",
                "tuesday": "08:20",
                "wednesday": "08:20",
                "thursday": "08:20",
                "friday": "08:20",
            },
            "end": {
                "monday": "09:00",
                "tuesday": "09:00",
                "wednesday": "09:00",
                "thursday": "09:00",
                "friday": "09:00",
            },
            "class": {
                "monday": "Subject A",
                "tuesday": "Subject V",
                "wednesday": "Subject P",
                "thursday": "Subject W",
                "friday": "Subject V",
            },
        },
        {
            "block": "Subject AA",
            "start": {
                "monday": "09:10",
                "tuesday": "09:10",
                "wednesday": "09:10",
                "thursday": "09:10",
                "friday": "09:10",
            },
            "end": {
                "monday": "09:50",
                "tuesday": "09:50",
                "wednesday": "09:50",
                "thursday": "09:50",
                "friday": "09:50",
            },
            "class": {
                "monday": "Subject N",
                "tuesday": "Subject AA",
                "wednesday": "Subject AA",
                "thursday": "Subject AA",
                "friday": "Subject AA",
            },
        },
        {
            "block": 3,
            "start": {
                "monday": "10:10",
                "tuesday": "10:10",
                "wednesday": "10:10",
                "thursday": "10:10",
                "friday": "10:10",
            },
            "end": {
                "monday": "10:50",
                "tuesday": "10:50",
                "wednesday": "10:50",
                "thursday": "10:50",
                "friday": "10:50",
            },
            "class": {
                "monday": "Subject H",
                "tuesday": "Subject X",
                "wednesday": "Subject Q",
                "thursday": "Subject I",
                "friday": "Subject O",
            },
        },
        {
            "block": 4,
            "start": {
                "monday": "10:50",
                "tuesday": "10:50",
                "wednesday": "10:50",
                "thursday": "10:50",
                "friday": "10:50",
            },
            "end": {
                "monday": "11:30",
                "tuesday": "11:30",
                "wednesday": "11:30",
                "thursday": "11:30",
                "friday": "11:30",
            },
            "class": {
                "monday": "Subject H",
                "tuesday": "Subject X",
                "wednesday": "Subject Q",
                "thursday": "Subject I",
                "friday": "Subject O",
            },
        },
        {
            "block": 5,
            "start": {
                "monday": "11:50",
                "tuesday": "11:50",
                "wednesday": "11:50",
                "thursday": "11:50",
                "friday": "11:50",
            },
            "end": {
                "monday": "12:30",
                "tuesday": "12:30",
                "wednesday": "12:30",
                "thursday": "12:30",
                "friday": "12:30",
            },
            "class": {
                "monday": "Subject Y",
                "tuesday": "Subject O",
                "wednesday": "Subject R",
                "thursday": "",
                "friday": "Subject S",
            },
        },
        {
            "block": 6,
            "start": {
                "monday": "12:30",
                "tuesday": "12:30",
                "wednesday": "12:30",
                "thursday": "12:30",
                "friday": "12:30",
            },
            "end": {
                "monday": "13:10",
                "tuesday": "13:10",
                "wednesday": "13:10",
                "thursday": "13:10",
                "friday": "13:10",
            },
            "class": {
                "monday": "Subject Y",
                "tuesday": "Subject Z/Subject L",
                "wednesday": "Subject U",
                "thursday": "Subject X",
                "friday": "Subject T",
            },
        },
        {
            "block": 7,
            "start": {
                "monday": "13:20",
                "tuesday": "13:40",
                "wednesday": "",
                "thursday": "13:20",
                "friday": "",
            },
            "end": {
                "monday": "14:00",
                "tuesday": "14:20",
                "wednesday": "",
                "thursday": "14:00",
                "friday": "",
            },
            "class": {
                "monday": "Subject Q",
                "tuesday": "Subject W",
                "wednesday": "",
                "thursday": "Subject A",
                "friday": "",
            },
        },
        {
            "block": 8,
            "start": {
                "monday": "14:00",
                "tuesday": "",
                "wednesday": "",
                "thursday": "14:00",
                "friday": "",
            },
            "end": {
                "monday": "14:40",
                "tuesday": "",
                "wednesday": "",
                "thursday": "14:40",
                "friday": "",
            },
            "class": {
                "monday": "Subject Q",
                "tuesday": "",
                "wednesday": "",
                "thursday": "Subject A",
                "friday": "",
            },
        },
    ]


def create_student_a_legacy_data() -> list[dict]:
    """Return Student A's complete legacy schedule."""
    return [
        {
            "block": 1,
            "start": {
                "monday": "07:40",
                "tuesday": "07:40",
                "wednesday": "07:40",
                "thursday": "07:40",
                "friday": "07:40",
            },
            "end": {
                "monday": "08:20",
                "tuesday": "08:20",
                "wednesday": "08:20",
                "thursday": "08:20",
                "friday": "08:20",
            },
            "class": {
                "monday": "Subject J",
                "tuesday": "Subject A",
                "wednesday": "Subject A",
                "thursday": "Subject B",
                "friday": "Subject C",
            },
        },
        {
            "block": 2,
            "start": {
                "monday": "08:20",
                "tuesday": "08:20",
                "wednesday": "08:20",
                "thursday": "08:20",
                "friday": "08:20",
            },
            "end": {
                "monday": "09:00",
                "tuesday": "09:00",
                "wednesday": "09:00",
                "thursday": "09:00",
                "friday": "09:00",
            },
            "class": {
                "monday": "Subject J",
                "tuesday": "Subject A",
                "wednesday": "Subject A",
                "thursday": "Subject B",
                "friday": "Subject C",
            },
        },
        {
            "block": "Subject AA",
            "start": {
                "monday": "09:10",
                "tuesday": "09:10",
                "wednesday": "09:10",
                "thursday": "09:10",
                "friday": "09:10",
            },
            "end": {
                "monday": "09:50",
                "tuesday": "09:50",
                "wednesday": "09:50",
                "thursday": "09:50",
                "friday": "09:50",
            },
            "class": {
                "monday": "Subject AA",
                "tuesday": "Subject AA",
                "wednesday": "KR",
                "thursday": "Subject AA",
                "friday": "Subject AA",
            },
        },
        {
            "block": 3,
            "start": {
                "monday": "10:10",
                "tuesday": "10:10",
                "wednesday": "10:10",
                "thursday": "10:10",
                "friday": "10:10",
            },
            "end": {
                "monday": "10:50",
                "tuesday": "10:50",
                "wednesday": "10:50",
                "thursday": "10:50",
                "friday": "10:50",
            },
            "class": {
                "monday": "Subject D",
                "tuesday": "Subject E",
                "wednesday": "Subject H",
                "thursday": "Subject V",
                "friday": "Subject J",
            },
        },
        {
            "block": 4,
            "start": {
                "monday": "10:50",
                "tuesday": "10:50",
                "wednesday": "10:50",
                "thursday": "10:50",
                "friday": "10:50",
            },
            "end": {
                "monday": "11:30",
                "tuesday": "11:30",
                "wednesday": "11:30",
                "thursday": "11:30",
                "friday": "11:30",
            },
            "class": {
                "monday": "Subject D",
                "tuesday": "Subject E",
                "wednesday": "Subject H",
                "thursday": "Subject V",
                "friday": "Subject J",
            },
        },
        {
            "block": 5,
            "start": {
                "monday": "11:50",
                "tuesday": "11:50",
                "wednesday": "11:50",
                "thursday": "11:50",
                "friday": "11:50",
            },
            "end": {
                "monday": "12:30",
                "tuesday": "12:30",
                "wednesday": "12:30",
                "thursday": "12:30",
                "friday": "12:30",
            },
            "class": {
                "monday": "Subject B",
                "tuesday": "Subject F",
                "wednesday": "Subject D",
                "thursday": "Subject K",
                "friday": "Subject G",
            },
        },
        {
            "block": 6,
            "start": {
                "monday": "12:30",
                "tuesday": "12:30",
                "wednesday": "12:30",
                "thursday": "12:30",
                "friday": "12:30",
            },
            "end": {
                "monday": "13:10",
                "tuesday": "13:10",
                "wednesday": "13:10",
                "thursday": "13:10",
                "friday": "13:10",
            },
            "class": {
                "monday": "Subject B",
                "tuesday": "Subject L",
                "wednesday": "Subject D",
                "thursday": "Subject K",
                "friday": "Subject G",
            },
        },
        {
            "block": 7,
            "start": {
                "monday": "",
                "tuesday": "13:40",
                "wednesday": "",
                "thursday": "",
                "friday": "13:20",
            },
            "end": {
                "monday": "",
                "tuesday": "14:20",
                "wednesday": "",
                "thursday": "",
                "friday": "14:00",
            },
            "class": {
                "monday": "",
                "tuesday": "Subject I",
                "wednesday": "",
                "thursday": "",
                "friday": "Subject K",
            },
        },
        {
            "block": 8,
            "start": {
                "monday": "",
                "tuesday": "14:20",
                "wednesday": "",
                "thursday": "",
                "friday": "",
            },
            "end": {
                "monday": "",
                "tuesday": "15:00",
                "wednesday": "",
                "thursday": "",
                "friday": "",
            },
            "class": {
                "monday": "",
                "tuesday": "Subject I",
                "wednesday": "",
                "thursday": "",
                "friday": "",
            },
        },
    ]





def create_student_a_schedule() -> Schedule:
    """Create Student A's current schedule for testing."""
    return Schedule(
        
        blocks=[
            Block(
                id="1",
                days={
                    "monday": DaySchedule(time(7, 40), time(8, 20), "Subject J"),
                    "tuesday": DaySchedule(time(7, 40), time(8, 20), "Subject A"),
                    "wednesday": DaySchedule(time(7, 40), time(8, 20), "Subject A"),
                    "thursday": DaySchedule(time(7, 40), time(8, 20), "Subject B"),
                    "friday": DaySchedule(time(7, 40), time(8, 20), "Subject C"),
                },
            ),
            Block(
                id="2",
                days={
                    "monday": DaySchedule(time(8, 20), time(9, 0), "Subject J"),
                    "tuesday": DaySchedule(time(8, 20), time(9, 0), "Subject A"),
                    "wednesday": DaySchedule(time(8, 20), time(9, 0), "Subject A"),
                    "thursday": DaySchedule(time(8, 20), time(9, 0), "Subject B"),
                    "friday": DaySchedule(time(8, 20), time(9, 0), "Subject C"),
                },
            ),
            Block(
                id="Subject AA",
                days={
                    "monday": DaySchedule(time(9, 10), time(9, 50), "Subject AA"),
                    "tuesday": DaySchedule(time(9, 10), time(9, 50), "Subject AA"),
                    "wednesday": DaySchedule(time(9, 10), time(9, 50), "KR"),
                    "thursday": DaySchedule(time(9, 10), time(9, 50), "Subject AA"),
                    "friday": DaySchedule(time(9, 10), time(9, 50), "Subject AA"),
                },
            ),
            Block(
                id="3",
                days={
                    "monday": DaySchedule(time(10, 10), time(10, 50), "Subject D"),
                    "tuesday": DaySchedule(time(10, 10), time(10, 50), "Subject E"),
                    "wednesday": DaySchedule(time(10, 10), time(10, 50), "Subject H"),
                    "thursday": DaySchedule(time(10, 10), time(10, 50), "Subject V"),
                    "friday": DaySchedule(time(10, 10), time(10, 50), "Subject J"),
                },
            ),
            Block(
                id="4",
                days={
                    "monday": DaySchedule(time(10, 50), time(11, 30), "Subject D"),
                    "tuesday": DaySchedule(time(10, 50), time(11, 30), "Subject E"),
                    "wednesday": DaySchedule(time(10, 50), time(11, 30), "Subject H"),
                    "thursday": DaySchedule(time(10, 50), time(11, 30), "Subject V"),
                    "friday": DaySchedule(time(10, 50), time(11, 30), "Subject J"),
                },
            ),
            Block(
                id="5",
                days={
                    "monday": DaySchedule(time(11, 50), time(12, 30), "Subject B"),
                    "tuesday": DaySchedule(time(11, 50), time(12, 30), "Subject F"),
                    "wednesday": DaySchedule(time(11, 50), time(12, 30), "Subject D"),
                    "thursday": DaySchedule(time(11, 50), time(12, 30), "Subject K"),
                    "friday": DaySchedule(time(11, 50), time(12, 30), "Subject G"),
                },
            ),
            Block(
                id="6",
                days={
                    "monday": DaySchedule(time(12, 30), time(13, 10), "Subject B"),
                    "tuesday": DaySchedule(time(12, 30), time(13, 10), "Subject L"),
                    "wednesday": DaySchedule(time(12, 30), time(13, 10), "Subject D"),
                    "thursday": DaySchedule(time(12, 30), time(13, 10), "Subject K"),
                    "friday": DaySchedule(time(12, 30), time(13, 10), "Subject G"),
                },
            ),
            Block(
                id="7",
                days={
                    "tuesday": DaySchedule(time(13, 40), time(14, 20), "Subject I"),
                    "friday": DaySchedule(time(13, 20), time(14, 0), "Subject K"),
                },
            ),
            Block(
                id="8",
                days={
                    "tuesday": DaySchedule(time(14, 20), time(15, 0), "Subject I"),
                },
            ),
        ],
    )


def test_current_lesson_tuesday_block_7() -> None:
    """Tuesday 14:00 should be Subject I in block 7."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 0),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_current_lesson_friday_block_7() -> None:
    """Friday 13:30 should be Subject K in block 7."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 14, 13, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "Subject K"
    assert lesson.start == time(13, 20)
    assert lesson.end == time(14, 0)


def test_no_block_7_on_monday() -> None:
    """Monday should have no block 7."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 10, 13, 30),
    )

    assert result is None


def test_wednesday_block_3() -> None:
    """Wednesday 10:20 should be Subject Hgraphy in block 3."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 12, 10, 20),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "3"
    assert lesson.subject == "Subject H"


def test_wednesday_special_block() -> None:
    """Wednesday 09:30 should be KR."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 12, 9, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "Subject AA"
    assert lesson.subject == "KR"


def test_before_school() -> None:
    """Before the first block there should be no current lesson."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 10, 7, 30),
    )

    assert result is None


def test_after_school() -> None:
    """After the last block there should be no current lesson."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 14, 14, 30),
    )

    assert result is None


def test_sunday() -> None:
    """Sunday should have no lessons."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 16, 10, 0),
    )

    assert result is None


def test_block_boundary() -> None:
    """At the exact end of a block the block should no longer be active."""
    schedule = create_student_a_schedule()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 14, 14, 0),
    )

    assert result is None
    
    
    
def test_next_lesson_tuesday_before_block_7() -> None:
    """Tuesday 13:30 should return block 7 as the next lesson."""
    schedule = create_student_a_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 13, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_next_lesson_tuesday_block_7() -> None:
    """During block 7, block 8 should be the next lesson."""
    schedule = create_student_a_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "8"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(14, 20)
    assert lesson.end == time(15, 0)


def test_next_lesson_friday_before_block_7() -> None:
    """Friday 13:00 should return block 7 as the next lesson."""
    schedule = create_student_a_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 14, 13, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 14).date()
    assert block_id == "7"
    assert lesson.subject == "Subject K"
    assert lesson.start == time(13, 20)
    assert lesson.end == time(14, 0)


def test_next_lesson_after_friday_school() -> None:
    """After Friday school, Monday block 1 should be next."""
    schedule = create_student_a_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 14, 15, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 17).date()
    assert block_id == "1"
    assert lesson.subject == "Subject J"
    assert lesson.start == time(7, 40)
    assert lesson.end == time(8, 20)


def test_next_lesson_saturday() -> None:
    """Saturday should return Monday block 1."""
    schedule = create_student_a_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 15, 12, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 17).date()
    assert block_id == "1"
    assert lesson.subject == "Subject J"


def test_next_lesson_sunday() -> None:
    """Sunday should return Monday block 1."""
    schedule = create_student_a_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 16, 12, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 17).date()
    assert block_id == "1"
    assert lesson.subject == "Subject J"


def test_next_lesson_at_block_start() -> None:
    """At the exact start of a block, the next lesson is that block."""
    schedule = create_student_a_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 13, 40),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "7"
    assert lesson.subject == "Subject I"


def test_next_lesson_at_block_end() -> None:
    """At the exact end of a block, the following block is next."""
    schedule = create_student_a_schedule()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 20),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "8"
    assert lesson.subject == "Subject I"

    
def test_next_lesson_works_with_unsorted_blocks() -> None:
    """The next lesson must not depend on block order."""
    schedule = create_student_a_schedule()

    # Deliberately scramble the block order.
    schedule.blocks.reverse()

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 13, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_current_lesson_works_with_unsorted_blocks() -> None:
    """The current lesson must not depend on block order."""
    schedule = create_student_a_schedule()

    # Deliberately scramble the block order.
    schedule.blocks.reverse()

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 0),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)    
    
    
def test_person_contains_schedule() -> None:
    """A person must contain an individual schedule."""
    schedule = create_student_a_schedule()

    person = Person(
        id="student_a",
        name="Student A",
        schedule=schedule,
    )

    assert person.id == "student_a"
    assert person.name == "Student A"
    assert person.schedule is schedule    
    
    
    
def test_multiple_persons_have_independent_schedules() -> None:
    """Different persons must be able to have independent schedules."""
    student_a_schedule = create_student_a_schedule()

    student_b_schedule = Schedule(
        blocks=[],
    )

    student_a = Person(
        id="student_a",
        name="Student A",
        schedule=student_a_schedule,
    )

    student_b = Person(
        id="student_b",
        name="Student B",
        schedule=student_b_schedule,
    )

    assert student_a.id != student_b.id
    assert student_a.name != student_b.name
    assert student_a.schedule is not student_b.schedule
    

def test_parse_schedule() -> None:
    """A schedule can be parsed from dictionary data."""
    data = {
        "blocks": [
            {
                "id": "1",
                "days": {
                    "monday": {
                        "start": "07:40",
                        "end": "08:20",
                        "subject": "Subject A",
                    },
                },
            },
            {
                "id": "Subject AA",
                "days": {
                    "monday": {
                        "start": "09:00",
                        "end": "09:40",
                        "subject": "Subject AA",
                    },
                },
            },
        ],
    }

    schedule = parse_schedule(data)

    assert len(schedule.blocks) == 2

    assert schedule.blocks[0].id == "1"
    assert schedule.blocks[0].days["monday"].subject == "Subject A"

    assert schedule.blocks[1].id == "Subject AA"
    assert schedule.blocks[1].days["monday"].subject == "Subject AA"    
    
    
    
def test_parse_schedule_supports_arbitrary_block_ids() -> None:
    """Block IDs are arbitrary labels and have no special meaning."""
    data = {
        "blocks": [
            {
                "id": 3,
                "days": {
                    "monday": {
                        "start": "09:10",
                        "end": "09:50",
                        "subject": "Subject AA",
                    },
                    "tuesday": {
                        "start": "09:20",
                        "end": "10:00",
                        "subject": "Subject A",
                    },
                },
            },
            {
                "id": "Subject N",
                "days": {
                    "monday": {
                        "start": "10:10",
                        "end": "10:50",
                        "subject": "Berufsorientierung",
                    },
                },
            },
            {
                "id": "Subject AA",
                "days": {
                    "monday": {
                        "start": "11:50",
                        "end": "12:30",
                        "subject": "Subject F",
                    },
                },
            },
        ],
    }

    schedule = parse_schedule(data)

    assert len(schedule.blocks) == 3

    block_3 = schedule.blocks[0]
    assert block_3.id == "3"
    assert block_3.days["monday"].subject == "Subject AA"
    assert block_3.days["tuesday"].subject == "Subject A"
    assert block_3.days["tuesday"].start == time(9, 20)

    block_beor = schedule.blocks[1]
    assert block_beor.id == "Subject N"
    assert block_beor.days["monday"].subject == "Berufsorientierung"

    block_ht = schedule.blocks[2]
    assert block_ht.id == "Subject AA"
    assert block_ht.days["monday"].subject == "Subject F"    
    
def test_parse_legacy_schedule_with_student_a_data() -> None:
    """Student A's legacy schedule format is parsed correctly."""
    data = [
        {
            "block": 1,
            "start": {
                "monday": "07:40",
                "tuesday": "07:40",
                "wednesday": "07:40",
                "thursday": "07:40",
                "friday": "07:40",
            },
            "end": {
                "monday": "08:20",
                "tuesday": "08:20",
                "wednesday": "08:20",
                "thursday": "08:20",
                "friday": "08:20",
            },
            "class": {
                "monday": "Subject J",
                "tuesday": "Subject A",
                "wednesday": "Subject A",
                "thursday": "Subject B",
                "friday": "Subject C",
            },
        },
        {
            "block": "Subject AA",
            "start": {
                "monday": "09:10",
                "tuesday": "09:10",
                "wednesday": "09:10",
                "thursday": "09:10",
                "friday": "09:10",
            },
            "end": {
                "monday": "09:50",
                "tuesday": "09:50",
                "wednesday": "09:50",
                "thursday": "09:50",
                "friday": "09:50",
            },
            "class": {
                "monday": "Subject AA",
                "tuesday": "Subject AA",
                "wednesday": "KR",
                "thursday": "Subject AA",
                "friday": "Subject AA",
            },
        },
        {
            "block": 7,
            "start": {
                "monday": "",
                "tuesday": "13:40",
                "wednesday": "",
                "thursday": "",
                "friday": "13:20",
            },
            "end": {
                "monday": "",
                "tuesday": "14:20",
                "wednesday": "",
                "thursday": "",
                "friday": "14:00",
            },
            "class": {
                "monday": "",
                "tuesday": "Subject I",
                "wednesday": "",
                "thursday": "",
                "friday": "Subject K",
            },
        },
        {
            "block": 8,
            "start": {
                "monday": "",
                "tuesday": "14:20",
                "wednesday": "",
                "thursday": "",
                "friday": "",
            },
            "end": {
                "monday": "",
                "tuesday": "15:00",
                "wednesday": "",
                "thursday": "",
                "friday": "",
            },
            "class": {
                "monday": "",
                "tuesday": "Subject I",
                "wednesday": "",
                "thursday": "",
                "friday": "",
            },
        },
    ]

    schedule = parse_legacy_schedule(data)

    assert len(schedule.blocks) == 4

    block_1 = schedule.blocks[0]
    assert block_1.id == "1"
    assert block_1.days["monday"].subject == "Subject J"
    assert block_1.days["tuesday"].subject == "Subject A"

    ht = schedule.blocks[1]
    assert ht.id == "Subject AA"
    assert ht.days["monday"].subject == "Subject AA"
    assert ht.days["wednesday"].subject == "KR"

    block_7 = schedule.blocks[2]
    assert block_7.id == "7"
    assert "monday" not in block_7.days
    assert block_7.days["tuesday"].subject == "Subject I"
    assert block_7.days["tuesday"].start == time(13, 40)
    assert block_7.days["friday"].subject == "Subject K"
    assert block_7.days["friday"].start == time(13, 20)

    block_8 = schedule.blocks[3]
    assert block_8.id == "8"
    assert "monday" not in block_8.days
    assert "friday" not in block_8.days
    assert block_8.days["tuesday"].subject == "Subject I"    
    
    
def test_parse_complete_student_a_schedule() -> None:
    """Student A's complete schedule is represented correctly."""
    schedule = parse_legacy_schedule(create_student_a_legacy_data())

    assert len(schedule.blocks) == 9

    # Monday has six regular lessons plus Subject AA.
    monday_lessons = [
        block
        for block in schedule.blocks
        if "monday" in block.days
    ]
    assert len(monday_lessons) == 7

    # Tuesday has all blocks including 7 and 8.
    tuesday_lessons = [
        block
        for block in schedule.blocks
        if "tuesday" in block.days
    ]
    assert len(tuesday_lessons) == 9

    # Wednesday has no block 7 or 8.
    wednesday_lessons = [
        block
        for block in schedule.blocks
        if "wednesday" in block.days
    ]
    assert len(wednesday_lessons) == 7

    # Friday has block 7 but no block 8.
    friday_lessons = [
        block
        for block in schedule.blocks
        if "friday" in block.days
    ]
    assert len(friday_lessons) == 8

    # Special block after the second lesson.
    ht = next(block for block in schedule.blocks if block.id == "Subject AA")

    assert ht.days["monday"].subject == "Subject AA"
    assert ht.days["tuesday"].subject == "Subject AA"
    assert ht.days["wednesday"].subject == "KR"
    assert ht.days["thursday"].subject == "Subject AA"
    assert ht.days["friday"].subject == "Subject AA"

    # Tuesday block 7.
    block_7 = next(block for block in schedule.blocks if block.id == "7")

    assert block_7.days["tuesday"].subject == "Subject I"
    assert block_7.days["tuesday"].start == time(13, 40)
    assert block_7.days["tuesday"].end == time(14, 20)

    # Friday block 7 has different times.
    assert block_7.days["friday"].subject == "Subject K"
    assert block_7.days["friday"].start == time(13, 20)
    assert block_7.days["friday"].end == time(14, 0)    
    
    
def test_student_a_current_lesson_through_parser() -> None:
    """The parsed Student A schedule works with the schedule engine."""
    schedule = parse_legacy_schedule(create_student_a_legacy_data())

    # Tuesday, 13:45 -> block 7 / Subject I.
    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 13, 45),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_student_a_friday_block_7_through_parser() -> None:
    """Friday block 7 uses its own schedule times."""
    schedule = parse_legacy_schedule(create_student_a_legacy_data())

    # Friday, 13:30 -> block 7 / Subject K.
    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 14, 13, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "Subject K"
    assert lesson.start == time(13, 20)
    assert lesson.end == time(14, 0)
    
    
    
def test_student_a_next_lesson_through_parser() -> None:
    """The next lesson is correctly found from parsed data."""
    schedule = parse_legacy_schedule(create_student_a_legacy_data())

    # Tuesday, 13:30 -> block 7 is next.
    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 13, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)  


def test_student_a_next_lesson_friday_through_parser() -> None:
    """Friday block 7 is found as the next lesson."""
    schedule = parse_legacy_schedule(create_student_a_legacy_data())

    # Friday, 13:00 -> block 7 is next.
    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 14, 13, 0),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 14).date()
    assert block_id == "7"
    assert lesson.subject == "Subject K"
    assert lesson.start == time(13, 20)
    assert lesson.end == time(14, 0)   
    
    
def test_current_lesson_for_person() -> None:
    """Current lesson can be resolved through a Person."""
    person = Person(
        id="student_a",
        name="Student A",
        schedule=parse_legacy_schedule(create_student_a_legacy_data()),
    )

    result = get_current_lesson_for_person(
        person,
        datetime(2026, 8, 11, 13, 45),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_next_lesson_for_person() -> None:
    """Next lesson can be resolved through a Person."""
    person = Person(
        id="student_a",
        name="Student A",
        schedule=parse_legacy_schedule(create_student_a_legacy_data()),
    )

    result = get_next_lesson_for_person(
        person,
        datetime(2026, 8, 11, 13, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)    
    
    
    
def test_special_subjects_are_normal_lessons() -> None:
    """Special subjects such as Subject AA, KR and Subject N behave like normal lessons."""
    schedule = Schedule(
        
        blocks=[
            Block(
                id="Subject AA",
                days={
                    "monday": DaySchedule(
                        start=time(9, 10),
                        end=time(9, 50),
                        subject="Subject AA",
                    )
                },
            ),
            Block(
                id="KR",
                days={
                    "tuesday": DaySchedule(
                        start=time(9, 10),
                        end=time(9, 50),
                        subject="KR",
                    )
                },
            ),
            Block(
                id="Subject N",
                days={
                    "wednesday": DaySchedule(
                        start=time(9, 10),
                        end=time(9, 50),
                        subject="Subject N",
                    )
                },
            ),
        ],
    )

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 10, 9, 30),
    )

    assert result is not None
    block_id, lesson = result

    assert block_id == "Subject AA"
    assert lesson.subject == "Subject AA"

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    assert result is not None
    block_id, lesson = result

    assert block_id == "KR"
    assert lesson.subject == "KR"

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 12, 9, 30),
    )

    assert result is not None
    block_id, lesson = result

    assert block_id == "Subject N"
    assert lesson.subject == "Subject N"



def test_parse_legacy_schedule_with_student_b_data() -> None:
    """Student B's legacy schedule is parsed correctly."""
    schedule = parse_legacy_schedule(create_student_b_legacy_data())

    assert len(schedule.blocks) == 9

    blocks = {block.id: block for block in schedule.blocks}

    # Monday
    assert blocks["1"].days["monday"].subject == "Subject O"
    assert blocks["2"].days["monday"].subject == "Subject A"
    assert blocks["Subject AA"].days["monday"].subject == "Subject N"
    assert blocks["3"].days["monday"].subject == "Subject H"
    assert blocks["4"].days["monday"].subject == "Subject H"
    assert blocks["5"].days["monday"].subject == "Subject Y"
    assert blocks["6"].days["monday"].subject == "Subject Y"
    assert blocks["7"].days["monday"].subject == "Subject Q"
    assert blocks["8"].days["monday"].subject == "Subject Q"

    # Tuesday
    assert "tuesday" not in blocks["1"].days
    assert blocks["2"].days["tuesday"].subject == "Subject V"
    assert blocks["Subject AA"].days["tuesday"].subject == "Subject AA"
    assert blocks["3"].days["tuesday"].subject == "Subject X"
    assert blocks["4"].days["tuesday"].subject == "Subject X"
    assert blocks["5"].days["tuesday"].subject == "Subject O"
    assert blocks["6"].days["tuesday"].subject == "Subject Z/Subject L"
    assert blocks["7"].days["tuesday"].subject == "Subject W"
    assert "tuesday" not in blocks["8"].days
    
    
def test_student_b_current_lesson_monday_ht() -> None:
    """Student B has Subject N during Subject AA on Monday."""
    schedule = parse_legacy_schedule(create_student_b_legacy_data())

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 10, 9, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "Subject AA"
    assert lesson.subject == "Subject N"
    assert lesson.start == time(9, 10)
    assert lesson.end == time(9, 50)


def test_student_b_current_lesson_tuesday_ht() -> None:
    """Student B has Subject AA during the Subject AA block on Tuesday."""
    schedule = parse_legacy_schedule(create_student_b_legacy_data())

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "Subject AA"
    assert lesson.subject == "Subject AA"


def test_student_b_tuesday_first_block_is_free() -> None:
    """Student B has no lesson during block 1 on Tuesday."""
    schedule = parse_legacy_schedule(create_student_b_legacy_data())

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 8, 0),
    )

    assert result is None


def test_student_b_next_lesson_tuesday_before_school() -> None:
    """Student B's first Tuesday lesson is block 2."""
    schedule = parse_legacy_schedule(create_student_b_legacy_data())

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 7, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "2"
    assert lesson.subject == "Subject V"
    assert lesson.start == time(8, 20)
    assert lesson.end == time(9, 0)


def test_student_b_next_lesson_tuesday_after_school() -> None:
    """After Student B's Tuesday schedule, the next lesson is Wednesday."""
    schedule = parse_legacy_schedule(create_student_b_legacy_data())

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 12).date()
    assert block_id == "1"
    assert lesson.subject == "Subject Z"
    assert lesson.start == time(7, 40)
    assert lesson.end == time(8, 20)


def test_student_a_and_student_b_have_independent_schedules() -> None:
    """Student A and Student B can use different schedules independently."""
    student_a = Person(
        id="student_a",
        name="Student A",
        schedule=parse_legacy_schedule(create_student_a_legacy_data()),
    )

    student_b = Person(
        id="student_b",
        name="Student B",
        schedule=parse_legacy_schedule(create_student_b_legacy_data()),
    )

    student_a_result = get_current_lesson(
        student_a.schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    student_b_result = get_current_lesson(
        student_b.schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    assert student_a_result is not None
    assert student_b_result is not None

    student_a_block, student_a_lesson = student_a_result
    student_b_block, student_b_lesson = student_b_result

    assert student_a_block == "Subject AA"
    assert student_a_lesson.subject == "Subject AA"

    assert student_b_block == "Subject AA"
    assert student_b_lesson.subject == "Subject AA"


def test_person_schedule_is_accessible() -> None:
    """A person's schedule is directly accessible."""
    schedule = parse_legacy_schedule(create_student_a_legacy_data())

    person = Person(
        id="student_a",
        name="Student A",
        schedule=schedule,
    )

    assert person.id == "student_a"
    assert person.name == "Student A"
    assert person.schedule is schedule
    assert len(person.schedule.blocks) == 9

def test_person_schedule_can_differ_between_persons() -> None:
    """Different persons can have completely different schedules."""
    student_a = Person(
        id="student_a",
        name="Student A",
        schedule=parse_legacy_schedule(create_student_a_legacy_data()),
    )

    student_b = Person(
        id="student_b",
        name="Student B",
        schedule=parse_legacy_schedule(create_student_b_legacy_data()),
    )

    assert student_a.schedule is not student_b.schedule

    student_a_lesson = get_current_lesson(
        student_a.schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    student_b_lesson = get_current_lesson(
        student_b.schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    assert student_a_lesson is not None
    assert student_b_lesson is not None

    assert student_a_lesson[1].subject == "Subject AA"
    assert student_b_lesson[1].subject == "Subject AA"

def test_schedule_manager_stores_multiple_persons() -> None:
    """The schedule manager stores multiple independent persons."""
    manager = ScheduleManager()

    student_a = Person(
        id="student_a",
        name="Student A",
        schedule=parse_legacy_schedule(create_student_a_legacy_data()),
    )

    student_b = Person(
        id="student_b",
        name="Student B",
        schedule=parse_legacy_schedule(create_student_b_legacy_data()),
    )

    manager.add_person(student_a)
    manager.add_person(student_b)

    assert manager.get_person("student_a") is student_a
    assert manager.get_person("student_b") is student_b
    assert manager.get_person("unknown") is None

    assert len(manager.all_persons()) == 2

def test_schedule_manager_replaces_person_with_same_id() -> None:
    """Adding a person with an existing ID replaces the previous person."""
    manager = ScheduleManager()

    first = Person(
        id="student_a",
        name="Student A",
        schedule=parse_legacy_schedule(create_student_a_legacy_data()),
    )

    replacement = Person(
        id="student_a",
        name="Student A",
        schedule=parse_legacy_schedule(create_student_b_legacy_data()),
    )

    manager.add_person(first)
    manager.add_person(replacement)

    assert manager.get_person("student_a") is replacement
    assert len(manager.all_persons()) == 1



def test_schedule_manager_can_check_person_existence() -> None:
    """The schedule manager can check whether a person exists."""
    manager = ScheduleManager()

    person = Person(
        id="student_a",
        name="Student A",
        schedule=parse_legacy_schedule(create_student_a_legacy_data()),
    )

    manager.add_person(person)

    assert manager.has_person("student_a")
    assert not manager.has_person("student_b")    
    
    
def test_create_schedule_manager_from_configuration() -> None:
    """A schedule manager can be created from configuration data."""
    manager = create_schedule_manager(
        [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": create_student_a_legacy_data(),
            },
            {
                "id": "student_b",
                "name": "Student B",
                "schedule": create_student_b_legacy_data(),
            },
        ]
    )

    assert manager.has_person("student_a")
    assert manager.has_person("student_b")

    student_a = manager.get_person("student_a")
    student_b = manager.get_person("student_b")

    assert student_a is not None
    assert student_b is not None

    assert student_a.name == "Student A"
    assert student_b.name == "Student B"

    assert len(student_a.schedule.blocks) == 9
    assert len(student_b.schedule.blocks) == 9    
    
    
def test_create_schedule_manager_from_new_configuration() -> None:
    """A schedule manager can be created from the new configuration format."""
    config = {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject J",
                        },
                        "tuesday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                    },
                },
            }
        ]
    }

    manager = create_schedule_manager_from_config(config)

    assert manager.has_person("student_a")

    person = manager.get_person("student_a")

    assert person is not None
    assert person.name == "Student A"

    monday = person.schedule.blocks[0].days["monday"]

    assert monday.start == time(7, 40)
    assert monday.end == time(8, 20)
    assert monday.subject == "Subject J"    
    
    
def test_new_configuration_supports_days_without_lessons() -> None:
    """A block can exist only on selected days."""
    config = {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "7": {
                        "tuesday": {
                            "start": "13:40",
                            "end": "14:20",
                            "subject": "Subject I",
                        },
                        "friday": {
                            "start": "13:20",
                            "end": "14:00",
                            "subject": "Subject K",
                        },
                    },
                },
            }
        ]
    }

    manager = create_schedule_manager_from_config(config)

    person = manager.get_person("student_a")

    assert person is not None

    block = person.schedule.blocks[0]

    assert block.id == "7"
    assert "tuesday" in block.days
    assert "friday" in block.days
    assert "monday" not in block.days
    assert "wednesday" not in block.days
    assert "thursday" not in block.days

    assert block.days["tuesday"].subject == "Subject I"
    assert block.days["friday"].subject == "Subject K"    
    
    
def test_new_configuration_treats_special_block_as_normal_block() -> None:
    """Special blocks such as Subject AA are handled like normal schedule blocks."""
    config = {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "Subject AA": {
                        "monday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                        "wednesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "KR",
                        },
                    },
                },
            }
        ]
    }

    manager = create_schedule_manager_from_config(config)

    person = manager.get_person("student_a")

    assert person is not None

    block = person.schedule.blocks[0]

    assert block.id == "Subject AA"
    assert block.days["monday"].subject == "Subject AA"
    assert block.days["wednesday"].subject == "KR"    
    
def test_new_configuration_rejects_invalid_time() -> None:
    """Invalid time values are rejected."""
    config = {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "not-a-time",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                    },
                },
            }
        ]
    }

    with pytest.raises(ValueError):
        create_schedule_manager_from_config(config)    
        

def test_new_configuration_rejects_invalid_time_range() -> None:
    """A lesson must end after it starts."""
    config = {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "08:20",
                            "end": "07:40",
                            "subject": "Subject A",
                        },
                    },
                },
            }
        ]
    }

    with pytest.raises(ValueError):
        create_schedule_manager_from_config(config)


def test_new_configuration_rejects_zero_length_lesson() -> None:
    """A lesson cannot have identical start and end times."""
    config = {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "08:20",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                    },
                },
            }
        ]
    }

    with pytest.raises(ValueError):
        create_schedule_manager_from_config(config)

        
        
        
def test_new_configuration_rejects_duplicate_person_ids() -> None:
    """Duplicate person IDs are rejected."""
    config = {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                    },
                },
            },
            {
                "id": "student_a",
                "name": "Another Person",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject B",
                        },
                    },
                },
            },
        ]
    }

    with pytest.raises(ValueError):
        create_schedule_manager_from_config(config)        
        
        
def test_new_configuration_rejects_empty_person_id() -> None:
    """An empty person ID is rejected."""
    config = {
        "persons": [
            {
                "id": "",
                "name": "Student A",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                    },
                },
            }
        ]
    }

    with pytest.raises(ValueError):
        create_schedule_manager_from_config(config)


def test_new_configuration_rejects_empty_block_id() -> None:
    """An empty block ID is rejected."""
    config = {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                    },
                },
            }
        ]
    }

    with pytest.raises(ValueError):
        create_schedule_manager_from_config(config)        
        
 

   
    


def test_student_a_new_configuration_matches_schedule() -> None:
    """Student A's complete new configuration is parsed correctly."""
    manager = create_schedule_manager_from_config(
        create_student_a_new_config()
    )

    person = manager.get_person("student_a")

    assert person is not None
    assert person.name == "Student A"

    assert len(person.schedule.blocks) == 9

    tuesday = get_current_lesson(
        person.schedule,
        datetime(2026, 8, 11, 13, 50),
    )

    assert tuesday is not None

    block_id, lesson = tuesday

    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)

    friday = get_current_lesson(
        person.schedule,
        datetime(2026, 8, 14, 13, 30),
    )

    assert friday is not None

    block_id, lesson = friday

    assert block_id == "7"
    assert lesson.subject == "Subject K"
    assert lesson.start == time(13, 20)
    assert lesson.end == time(14, 0)    
    
    
def test_student_b_new_configuration_matches_schedule() -> None:
    """Student B's complete new configuration is parsed correctly."""
    manager = create_schedule_manager_from_config(
        create_student_b_new_config()
    )

    person = manager.get_person("student_b")

    assert person is not None
    assert person.name == "Student B"
    assert len(person.schedule.blocks) == 9

    monday = get_current_lesson(
        person.schedule,
        datetime(2026, 8, 10, 9, 20),
    )

    assert monday is not None

    block_id, lesson = monday

    assert block_id == "Subject AA"
    assert lesson.subject == "Subject N"
    assert lesson.start == time(9, 10)
    assert lesson.end == time(9, 50)

    tuesday = get_current_lesson(
        person.schedule,
        datetime(2026, 8, 11, 9, 20),
    )

    assert tuesday is not None

    block_id, lesson = tuesday

    assert block_id == "Subject AA"
    assert lesson.subject == "Subject AA"

    friday = get_current_lesson(
        person.schedule,
        datetime(2026, 8, 14, 12, 45),
    )

    assert friday is not None

    block_id, lesson = friday

    assert block_id == "6"
    assert lesson.subject == "Subject T"    
    
    
    
def test_complete_new_configuration_contains_all_persons() -> None:
    """The complete configuration contains all configured persons."""
    manager = create_schedule_manager_from_config(
        create_complete_new_config()
    )

    assert manager.has_person("student_a")
    assert manager.has_person("student_b")

    student_a = manager.get_person("student_a")
    student_b = manager.get_person("student_b")

    assert student_a is not None
    assert student_b is not None

    assert student_a.name == "Student A"
    assert student_b.name == "Student B"

    assert len(student_a.schedule.blocks) == 9
    assert len(student_b.schedule.blocks) == 9    
    
    
    
def test_load_complete_configuration_from_yaml() -> None:
    """The complete schedule configuration can be loaded from YAML."""
    manager = load_schedule_manager_from_yaml(
        "tests/data/schedules.yaml"
    )

    assert manager.has_person("student_a")
    assert manager.has_person("student_b")

    student_a = manager.get_person("student_a")
    student_b = manager.get_person("student_b")

    assert student_a is not None
    assert student_b is not None

    assert student_a.name == "Student A"
    assert student_b.name == "Student B"

    assert len(student_a.schedule.blocks) == 9
    assert len(student_b.schedule.blocks) == 9    
    
    
    
def test_yaml_configuration_matches_python_configuration() -> None:
    """YAML and Python configuration produce the same schedules."""
    yaml_manager = load_schedule_manager_from_yaml(
        "tests/data/schedules.yaml"
    )

    python_manager = create_schedule_manager_from_config(
        {
            "persons": [
                *create_student_a_new_config()["persons"],
                *create_student_b_new_config()["persons"],
            ]
        }
    )

    for person_id in ("student_a", "student_b"):
        yaml_person = yaml_manager.get_person(person_id)
        python_person = python_manager.get_person(person_id)

        assert yaml_person is not None
        assert python_person is not None

        assert yaml_person.id == python_person.id
        assert yaml_person.name == python_person.name

        assert yaml_person.schedule.blocks == python_person.schedule.blocks    
        
        
        
def test_yaml_configuration_rejects_empty_person_id() -> None:
    """YAML configuration must reject an empty person ID."""
    config = {
        "persons": [
            {
                "id": "",
                "name": "Student A",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                    },
                },
            }
        ]
    }

    with pytest.raises(ValueError):
        create_schedule_manager_from_config(config)        
        
        
        
def test_yaml_configuration_rejects_empty_person_id(
    tmp_path,
) -> None:
    """YAML configuration must reject an empty person ID."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  - id: ""
    name: Student A
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject A"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)

def test_yaml_configuration_rejects_invalid_time_range(
    tmp_path,
) -> None:
    """YAML configuration must reject a lesson ending before it starts."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  - id: student_a
    name: Student A
    schedule:
      "1":
        monday:
          start: "08:20"
          end: "07:40"
          subject: "Subject A"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)

def test_yaml_configuration_rejects_zero_length_lesson(
    tmp_path,
) -> None:
    """YAML configuration must reject identical start and end times."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  - id: student_a
    name: Student A
    schedule:
      "1":
        monday:
          start: "08:20"
          end: "08:20"
          subject: "Subject A"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)


def test_yaml_configuration_rejects_duplicate_person_ids(
    tmp_path,
) -> None:
    """YAML configuration must reject duplicate person IDs."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  - id: student_a
    name: Student A
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject A"

  - id: student_a
    name: Student A 2
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject B"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)


def test_yaml_configuration_rejects_empty_block_id(
    tmp_path,
) -> None:
    """YAML configuration must reject an empty block ID."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  - id: student_a
    name: Student A
    schedule:
      "":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject A"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)


def test_yaml_configuration_rejects_missing_persons(
    tmp_path,
) -> None:
    """YAML configuration must reject a missing persons section."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
something_else:
  - test
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)        
        
        
        
        
def test_yaml_configuration_rejects_invalid_persons_type(
    tmp_path,
) -> None:
    """YAML configuration must reject a non-list persons section."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  student_a:
    name: Student A
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)



def test_yaml_configuration_rejects_invalid_person_entry(
    tmp_path,
) -> None:
    """YAML configuration must reject a non-dictionary person entry."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  - student_a
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)


def test_yaml_configuration_rejects_missing_person_id(
    tmp_path,
) -> None:
    """YAML configuration must reject a person without an ID."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  - name: Student A
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject A"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)



def test_yaml_configuration_rejects_missing_person_name(
    tmp_path,
) -> None:
    """YAML configuration must reject a person without a name."""
    yaml_file = tmp_path / "invalid.yaml"

    yaml_file.write_text(
        """
persons:
  - id: student_a
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject A"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_schedule_manager_from_yaml(yaml_file)


def test_complete_yaml_configuration_preserves_schedule_structure(
    tmp_path,
) -> None:
    """The complete YAML configuration preserves all schedule details."""
    yaml_file = tmp_path / "stundenplan.yaml"

    yaml_file.write_text(
        """
persons:
  - id: student_a
    name: Student A
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject J"
        tuesday:
          start: "07:40"
          end: "08:20"
          subject: "Subject A"
      "Subject AA":
        monday:
          start: "09:10"
          end: "09:50"
          subject: "Subject AA"
        wednesday:
          start: "09:10"
          end: "09:50"
          subject: "KR"
      "7":
        tuesday:
          start: "13:40"
          end: "14:20"
          subject: "Subject I"

  - id: student_b
    name: Student B
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject O"
      "5":
        thursday:
          start: "11:50"
          end: "12:30"
          subject: "frei"
      "8":
        monday:
          start: "14:00"
          end: "14:40"
          subject: "Subject Q"
""",
        encoding="utf-8",
    )

    manager = load_schedule_manager_from_yaml(yaml_file)

    assert manager.has_person("student_a")
    assert manager.has_person("student_b")

    student_a = manager.get_person("student_a")
    student_b = manager.get_person("student_b")

    assert student_a.name == "Student A"
    assert student_b.name == "Student B"

    assert len(student_a.schedule.blocks) == 3
    assert len(student_b.schedule.blocks) == 3

    student_a_ht = next(
        block
        for block in student_a.schedule.blocks
        if block.id == "Subject AA"
    )

    assert student_a_ht.days["monday"].subject == "Subject AA"
    assert student_a_ht.days["wednesday"].subject == "KR"

    student_a_7 = next(
        block
        for block in student_a.schedule.blocks
        if block.id == "7"
    )

    assert set(student_a_7.days) == {"tuesday"}
    assert student_a_7.days["tuesday"].start == time(13, 40)

    student_b_5 = next(
        block
        for block in student_b.schedule.blocks
        if block.id == "5"
    )

    assert student_b_5.days["thursday"].subject == "frei"



def test_current_lesson_works_with_new_configuration() -> None:
    """Current lesson lookup works with the new configuration format."""
    manager = create_schedule_manager_from_config(
        create_student_a_new_config()
    )

    person = manager.get_person("student_a")

    assert person is not None

    result = get_current_lesson(
        person.schedule,
        datetime(2026, 8, 11, 13, 50),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_next_lesson_works_with_new_configuration() -> None:
    """Next lesson lookup works with the new configuration format."""
    manager = create_schedule_manager_from_config(
        create_student_a_new_config()
    )

    person = manager.get_person("student_a")

    assert person is not None

    result = get_next_lesson(
        person.schedule,
        datetime(2026, 8, 11, 13, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == date(2026, 8, 11)
    assert block_id == "7"
    assert lesson.subject == "Subject I"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)





def test_free_lesson_works_with_new_configuration() -> None:
    """A lesson with subject 'frei' is treated as a normal lesson."""
    manager = create_schedule_manager_from_config(
        create_student_b_new_config()
    )

    person = manager.get_person("student_b")

    assert person is not None

    result = get_current_lesson(
        person.schedule,
        datetime(2026, 8, 13, 12, 0),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "5"
    assert lesson.subject == "frei"
    assert lesson.start == time(11, 50)
    assert lesson.end == time(12, 30)



def test_next_free_lesson_works_with_new_configuration() -> None:
    """A free lesson is returned normally by next lesson lookup."""
    manager = create_schedule_manager_from_config(
        create_student_b_new_config()
    )

    person = manager.get_person("student_b")

    assert person is not None

    result = get_next_lesson(
        person.schedule,
        datetime(2026, 8, 13, 11, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == date(2026, 8, 13)
    assert block_id == "5"
    assert lesson.subject == "frei"
    assert lesson.start == time(11, 50)
    assert lesson.end == time(12, 30)


def test_yaml_configuration_loads_multiple_persons(
    tmp_path,
) -> None:
    """A YAML configuration can contain multiple persons."""
    yaml_file = tmp_path / "stundenplan.yaml"

    yaml_file.write_text(
        """
persons:
  - id: student_a
    name: Student A
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject J"
      "Subject AA":
        monday:
          start: "09:10"
          end: "09:50"
          subject: "Subject AA"

  - id: student_b
    name: Student B
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: "Subject O"
      "5":
        thursday:
          start: "11:50"
          end: "12:30"
          subject: "frei"
""",
        encoding="utf-8",
    )

    manager = load_schedule_manager_from_yaml(yaml_file)

    assert manager.has_person("student_a")
    assert manager.has_person("student_b")

    student_a = manager.get_person("student_a")
    student_b = manager.get_person("student_b")

    assert student_a is not None
    assert student_b is not None

    assert student_a.name == "Student A"
    assert student_b.name == "Student B"

    assert len(student_a.schedule.blocks) == 2
    assert len(student_b.schedule.blocks) == 2

    assert student_a.schedule.blocks[1].id == "Subject AA"
    assert student_b.schedule.blocks[1].id == "5"
    assert student_b.schedule.blocks[1].days["thursday"].subject == "frei"



    