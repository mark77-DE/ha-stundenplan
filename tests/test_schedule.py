"""Tests for the Stundenplan schedule engine."""

from datetime import datetime, time

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

def create_johanna_legacy_data() -> list[dict]:
    """Return Johanna's complete legacy schedule."""
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
                "monday": "SpanA",
                "tuesday": "",
                "wednesday": "Che",
                "thursday": "Deu",
                "friday": "Bio",
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
                "monday": "Mathe",
                "tuesday": "Bio",
                "wednesday": "Inform",
                "thursday": "Deu",
                "friday": "Bio",
            },
        },
        {
            "block": "HT",
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
                "monday": "BeOr",
                "tuesday": "HT",
                "wednesday": "HT",
                "thursday": "HT",
                "friday": "HT",
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
                "monday": "Geo",
                "tuesday": "Eng",
                "wednesday": "SpoP",
                "thursday": "WiPo",
                "friday": "SpanA",
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
                "monday": "Geo",
                "tuesday": "Eng",
                "wednesday": "SpoP",
                "thursday": "WiPo",
                "friday": "SpanA",
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
                "monday": "Ges",
                "tuesday": "SpanA",
                "wednesday": "Reli",
                "thursday": "",
                "friday": "Musik/Kunst",
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
                "monday": "Ges",
                "tuesday": "Che/Hosp.",
                "wednesday": "Philo",
                "thursday": "Eng",
                "friday": "Kunst/DSp.",
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
                "monday": "SpoP",
                "tuesday": "Deu",
                "wednesday": "",
                "thursday": "Mathe",
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
                "monday": "SpoP",
                "tuesday": "",
                "wednesday": "",
                "thursday": "Mathe",
                "friday": "",
            },
        },
    ]


def create_paulina_legacy_data() -> list[dict]:
    """Return Paulina's complete legacy schedule."""
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
                "monday": "WP1",
                "tuesday": "Mathe",
                "wednesday": "Mathe",
                "thursday": "Deutsch",
                "friday": "Physik",
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
                "monday": "WP1",
                "tuesday": "Mathe",
                "wednesday": "Mathe",
                "thursday": "Deutsch",
                "friday": "Physik",
            },
        },
        {
            "block": "HT",
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
                "monday": "HT",
                "tuesday": "HT",
                "wednesday": "KR",
                "thursday": "HT",
                "friday": "HT",
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
                "monday": "Englisch",
                "tuesday": "Chemie",
                "wednesday": "Geo",
                "thursday": "Bio",
                "friday": "WP1",
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
                "monday": "Englisch",
                "tuesday": "Chemie",
                "wednesday": "Geo",
                "thursday": "Bio",
                "friday": "WP1",
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
                "monday": "Deutsch",
                "tuesday": "Sport",
                "wednesday": "Englisch",
                "thursday": "WP2",
                "friday": "Geschichte",
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
                "monday": "Deutsch",
                "tuesday": "Hosp.",
                "wednesday": "Englisch",
                "thursday": "WP2",
                "friday": "Geschichte",
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
                "tuesday": "WiPo",
                "wednesday": "",
                "thursday": "",
                "friday": "WP2",
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
                "tuesday": "WiPo",
                "wednesday": "",
                "thursday": "",
                "friday": "",
            },
        },
    ]





def create_paulina_schedule() -> Schedule:
    """Create Paulina's current schedule for testing."""
    return Schedule(
        
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

    
def test_next_lesson_works_with_unsorted_blocks() -> None:
    """The next lesson must not depend on block order."""
    schedule = create_paulina_schedule()

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
    assert lesson.subject == "WiPo"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_current_lesson_works_with_unsorted_blocks() -> None:
    """The current lesson must not depend on block order."""
    schedule = create_paulina_schedule()

    # Deliberately scramble the block order.
    schedule.blocks.reverse()

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
    
    
def test_person_contains_schedule() -> None:
    """A person must contain an individual schedule."""
    schedule = create_paulina_schedule()

    person = Person(
        id="paulina",
        name="Paulina",
        schedule=schedule,
    )

    assert person.id == "paulina"
    assert person.name == "Paulina"
    assert person.schedule is schedule    
    
    
    
def test_multiple_persons_have_independent_schedules() -> None:
    """Different persons must be able to have independent schedules."""
    paulina_schedule = create_paulina_schedule()

    johanna_schedule = Schedule(
        blocks=[],
    )

    paulina = Person(
        id="paulina",
        name="Paulina",
        schedule=paulina_schedule,
    )

    johanna = Person(
        id="johanna",
        name="Johanna",
        schedule=johanna_schedule,
    )

    assert paulina.id != johanna.id
    assert paulina.name != johanna.name
    assert paulina.schedule is not johanna.schedule
    

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
                        "subject": "Mathe",
                    },
                },
            },
            {
                "id": "HT",
                "days": {
                    "monday": {
                        "start": "09:00",
                        "end": "09:40",
                        "subject": "HT",
                    },
                },
            },
        ],
    }

    schedule = parse_schedule(data)

    assert len(schedule.blocks) == 2

    assert schedule.blocks[0].id == "1"
    assert schedule.blocks[0].days["monday"].subject == "Mathe"

    assert schedule.blocks[1].id == "HT"
    assert schedule.blocks[1].days["monday"].subject == "HT"    
    
    
    
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
                        "subject": "HT",
                    },
                    "tuesday": {
                        "start": "09:20",
                        "end": "10:00",
                        "subject": "Mathe",
                    },
                },
            },
            {
                "id": "BeOr",
                "days": {
                    "monday": {
                        "start": "10:10",
                        "end": "10:50",
                        "subject": "Berufsorientierung",
                    },
                },
            },
            {
                "id": "HT",
                "days": {
                    "monday": {
                        "start": "11:50",
                        "end": "12:30",
                        "subject": "Sport",
                    },
                },
            },
        ],
    }

    schedule = parse_schedule(data)

    assert len(schedule.blocks) == 3

    block_3 = schedule.blocks[0]
    assert block_3.id == "3"
    assert block_3.days["monday"].subject == "HT"
    assert block_3.days["tuesday"].subject == "Mathe"
    assert block_3.days["tuesday"].start == time(9, 20)

    block_beor = schedule.blocks[1]
    assert block_beor.id == "BeOr"
    assert block_beor.days["monday"].subject == "Berufsorientierung"

    block_ht = schedule.blocks[2]
    assert block_ht.id == "HT"
    assert block_ht.days["monday"].subject == "Sport"    
    
def test_parse_legacy_schedule_with_paulina_data() -> None:
    """Paulina's legacy schedule format is parsed correctly."""
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
                "monday": "WP1",
                "tuesday": "Mathe",
                "wednesday": "Mathe",
                "thursday": "Deutsch",
                "friday": "Physik",
            },
        },
        {
            "block": "HT",
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
                "monday": "HT",
                "tuesday": "HT",
                "wednesday": "KR",
                "thursday": "HT",
                "friday": "HT",
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
                "tuesday": "WiPo",
                "wednesday": "",
                "thursday": "",
                "friday": "WP2",
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
                "tuesday": "WiPo",
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
    assert block_1.days["monday"].subject == "WP1"
    assert block_1.days["tuesday"].subject == "Mathe"

    ht = schedule.blocks[1]
    assert ht.id == "HT"
    assert ht.days["monday"].subject == "HT"
    assert ht.days["wednesday"].subject == "KR"

    block_7 = schedule.blocks[2]
    assert block_7.id == "7"
    assert "monday" not in block_7.days
    assert block_7.days["tuesday"].subject == "WiPo"
    assert block_7.days["tuesday"].start == time(13, 40)
    assert block_7.days["friday"].subject == "WP2"
    assert block_7.days["friday"].start == time(13, 20)

    block_8 = schedule.blocks[3]
    assert block_8.id == "8"
    assert "monday" not in block_8.days
    assert "friday" not in block_8.days
    assert block_8.days["tuesday"].subject == "WiPo"    
    
    
def test_parse_complete_paulina_schedule() -> None:
    """Paulina's complete schedule is represented correctly."""
    schedule = parse_legacy_schedule(create_paulina_legacy_data())

    assert len(schedule.blocks) == 9

    # Monday has six regular lessons plus HT.
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
    ht = next(block for block in schedule.blocks if block.id == "HT")

    assert ht.days["monday"].subject == "HT"
    assert ht.days["tuesday"].subject == "HT"
    assert ht.days["wednesday"].subject == "KR"
    assert ht.days["thursday"].subject == "HT"
    assert ht.days["friday"].subject == "HT"

    # Tuesday block 7.
    block_7 = next(block for block in schedule.blocks if block.id == "7")

    assert block_7.days["tuesday"].subject == "WiPo"
    assert block_7.days["tuesday"].start == time(13, 40)
    assert block_7.days["tuesday"].end == time(14, 20)

    # Friday block 7 has different times.
    assert block_7.days["friday"].subject == "WP2"
    assert block_7.days["friday"].start == time(13, 20)
    assert block_7.days["friday"].end == time(14, 0)    
    
    
def test_paulina_current_lesson_through_parser() -> None:
    """The parsed Paulina schedule works with the schedule engine."""
    schedule = parse_legacy_schedule(create_paulina_legacy_data())

    # Tuesday, 13:45 -> block 7 / WiPo.
    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 13, 45),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "WiPo"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_paulina_friday_block_7_through_parser() -> None:
    """Friday block 7 uses its own schedule times."""
    schedule = parse_legacy_schedule(create_paulina_legacy_data())

    # Friday, 13:30 -> block 7 / WP2.
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
    
    
    
def test_paulina_next_lesson_through_parser() -> None:
    """The next lesson is correctly found from parsed data."""
    schedule = parse_legacy_schedule(create_paulina_legacy_data())

    # Tuesday, 13:30 -> block 7 is next.
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


def test_paulina_next_lesson_friday_through_parser() -> None:
    """Friday block 7 is found as the next lesson."""
    schedule = parse_legacy_schedule(create_paulina_legacy_data())

    # Friday, 13:00 -> block 7 is next.
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
    
    
def test_current_lesson_for_person() -> None:
    """Current lesson can be resolved through a Person."""
    person = Person(
        id="paulina",
        name="Paulina",
        schedule=parse_legacy_schedule(create_paulina_legacy_data()),
    )

    result = get_current_lesson_for_person(
        person,
        datetime(2026, 8, 11, 13, 45),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "7"
    assert lesson.subject == "WiPo"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)


def test_next_lesson_for_person() -> None:
    """Next lesson can be resolved through a Person."""
    person = Person(
        id="paulina",
        name="Paulina",
        schedule=parse_legacy_schedule(create_paulina_legacy_data()),
    )

    result = get_next_lesson_for_person(
        person,
        datetime(2026, 8, 11, 13, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "7"
    assert lesson.subject == "WiPo"
    assert lesson.start == time(13, 40)
    assert lesson.end == time(14, 20)    
    
    
    
def test_special_subjects_are_normal_lessons() -> None:
    """Special subjects such as HT, KR and BeOr behave like normal lessons."""
    schedule = Schedule(
        
        blocks=[
            Block(
                id="HT",
                days={
                    "monday": DaySchedule(
                        start=time(9, 10),
                        end=time(9, 50),
                        subject="HT",
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
                id="BeOr",
                days={
                    "wednesday": DaySchedule(
                        start=time(9, 10),
                        end=time(9, 50),
                        subject="BeOr",
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

    assert block_id == "HT"
    assert lesson.subject == "HT"

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

    assert block_id == "BeOr"
    assert lesson.subject == "BeOr"



def test_parse_legacy_schedule_with_johanna_data() -> None:
    """Johanna's legacy schedule is parsed correctly."""
    schedule = parse_legacy_schedule(create_johanna_legacy_data())

    assert len(schedule.blocks) == 9

    blocks = {block.id: block for block in schedule.blocks}

    # Monday
    assert blocks["1"].days["monday"].subject == "SpanA"
    assert blocks["2"].days["monday"].subject == "Mathe"
    assert blocks["HT"].days["monday"].subject == "BeOr"
    assert blocks["3"].days["monday"].subject == "Geo"
    assert blocks["4"].days["monday"].subject == "Geo"
    assert blocks["5"].days["monday"].subject == "Ges"
    assert blocks["6"].days["monday"].subject == "Ges"
    assert blocks["7"].days["monday"].subject == "SpoP"
    assert blocks["8"].days["monday"].subject == "SpoP"

    # Tuesday
    assert "tuesday" not in blocks["1"].days
    assert blocks["2"].days["tuesday"].subject == "Bio"
    assert blocks["HT"].days["tuesday"].subject == "HT"
    assert blocks["3"].days["tuesday"].subject == "Eng"
    assert blocks["4"].days["tuesday"].subject == "Eng"
    assert blocks["5"].days["tuesday"].subject == "SpanA"
    assert blocks["6"].days["tuesday"].subject == "Che/Hosp."
    assert blocks["7"].days["tuesday"].subject == "Deu"
    assert "tuesday" not in blocks["8"].days
    
    
def test_johanna_current_lesson_monday_ht() -> None:
    """Johanna has BeOr during HT on Monday."""
    schedule = parse_legacy_schedule(create_johanna_legacy_data())

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 10, 9, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "HT"
    assert lesson.subject == "BeOr"
    assert lesson.start == time(9, 10)
    assert lesson.end == time(9, 50)


def test_johanna_current_lesson_tuesday_ht() -> None:
    """Johanna has HT during the HT block on Tuesday."""
    schedule = parse_legacy_schedule(create_johanna_legacy_data())

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    assert result is not None

    block_id, lesson = result

    assert block_id == "HT"
    assert lesson.subject == "HT"


def test_johanna_tuesday_first_block_is_free() -> None:
    """Johanna has no lesson during block 1 on Tuesday."""
    schedule = parse_legacy_schedule(create_johanna_legacy_data())

    result = get_current_lesson(
        schedule,
        datetime(2026, 8, 11, 8, 0),
    )

    assert result is None


def test_johanna_next_lesson_tuesday_before_school() -> None:
    """Johanna's first Tuesday lesson is block 2."""
    schedule = parse_legacy_schedule(create_johanna_legacy_data())

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 7, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 11).date()
    assert block_id == "2"
    assert lesson.subject == "Bio"
    assert lesson.start == time(8, 20)
    assert lesson.end == time(9, 0)


def test_johanna_next_lesson_tuesday_after_school() -> None:
    """After Johanna's Tuesday schedule, the next lesson is Wednesday."""
    schedule = parse_legacy_schedule(create_johanna_legacy_data())

    result = get_next_lesson(
        schedule,
        datetime(2026, 8, 11, 14, 30),
    )

    assert result is not None

    lesson_date, block_id, lesson = result

    assert lesson_date == datetime(2026, 8, 12).date()
    assert block_id == "1"
    assert lesson.subject == "Che"
    assert lesson.start == time(7, 40)
    assert lesson.end == time(8, 20)


def test_paulina_and_johanna_have_independent_schedules() -> None:
    """Paulina and Johanna can use different schedules independently."""
    paulina = Person(
        id="paulina",
        name="Paulina",
        schedule=parse_legacy_schedule(create_paulina_legacy_data()),
    )

    johanna = Person(
        id="johanna",
        name="Johanna",
        schedule=parse_legacy_schedule(create_johanna_legacy_data()),
    )

    paulina_result = get_current_lesson(
        paulina.schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    johanna_result = get_current_lesson(
        johanna.schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    assert paulina_result is not None
    assert johanna_result is not None

    paulina_block, paulina_lesson = paulina_result
    johanna_block, johanna_lesson = johanna_result

    assert paulina_block == "HT"
    assert paulina_lesson.subject == "HT"

    assert johanna_block == "HT"
    assert johanna_lesson.subject == "HT"


def test_person_schedule_is_accessible() -> None:
    """A person's schedule is directly accessible."""
    schedule = parse_legacy_schedule(create_paulina_legacy_data())

    person = Person(
        id="paulina",
        name="Paulina",
        schedule=schedule,
    )

    assert person.id == "paulina"
    assert person.name == "Paulina"
    assert person.schedule is schedule
    assert len(person.schedule.blocks) == 9

def test_person_schedule_can_differ_between_persons() -> None:
    """Different persons can have completely different schedules."""
    paulina = Person(
        id="paulina",
        name="Paulina",
        schedule=parse_legacy_schedule(create_paulina_legacy_data()),
    )

    johanna = Person(
        id="johanna",
        name="Johanna",
        schedule=parse_legacy_schedule(create_johanna_legacy_data()),
    )

    assert paulina.schedule is not johanna.schedule

    paulina_lesson = get_current_lesson(
        paulina.schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    johanna_lesson = get_current_lesson(
        johanna.schedule,
        datetime(2026, 8, 11, 9, 30),
    )

    assert paulina_lesson is not None
    assert johanna_lesson is not None

    assert paulina_lesson[1].subject == "HT"
    assert johanna_lesson[1].subject == "HT"

def test_schedule_manager_stores_multiple_persons() -> None:
    """The schedule manager stores multiple independent persons."""
    manager = ScheduleManager()

    paulina = Person(
        id="paulina",
        name="Paulina",
        schedule=parse_legacy_schedule(create_paulina_legacy_data()),
    )

    johanna = Person(
        id="johanna",
        name="Johanna",
        schedule=parse_legacy_schedule(create_johanna_legacy_data()),
    )

    manager.add_person(paulina)
    manager.add_person(johanna)

    assert manager.get_person("paulina") is paulina
    assert manager.get_person("johanna") is johanna
    assert manager.get_person("unknown") is None

    assert len(manager.all_persons()) == 2

def test_schedule_manager_replaces_person_with_same_id() -> None:
    """Adding a person with an existing ID replaces the previous person."""
    manager = ScheduleManager()

    first = Person(
        id="paulina",
        name="Paulina",
        schedule=parse_legacy_schedule(create_paulina_legacy_data()),
    )

    replacement = Person(
        id="paulina",
        name="Paulina",
        schedule=parse_legacy_schedule(create_johanna_legacy_data()),
    )

    manager.add_person(first)
    manager.add_person(replacement)

    assert manager.get_person("paulina") is replacement
    assert len(manager.all_persons()) == 1



def test_schedule_manager_can_check_person_existence() -> None:
    """The schedule manager can check whether a person exists."""
    manager = ScheduleManager()

    person = Person(
        id="paulina",
        name="Paulina",
        schedule=parse_legacy_schedule(create_paulina_legacy_data()),
    )

    manager.add_person(person)

    assert manager.has_person("paulina")
    assert not manager.has_person("johanna")    