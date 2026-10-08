"""Tests for the Stundenplan sensor platform."""

from datetime import datetime
from pathlib import Path

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import async_fire_time_changed


from custom_components.stundenplan import async_setup
from custom_components.stundenplan.const import DOMAIN


def _prepare_schedules_file(hass: HomeAssistant) -> None:
    """Copy the sample schedule into Home Assistant's config directory."""
    source = Path(__file__).parent / "data" / "schedules.yaml"
    target = Path(hass.config.path("schedules.yaml"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")



async def test_sensor_created_for_each_person(
    hass: HomeAssistant,
) -> None:
    """Create one sensor for each configured person."""
    _prepare_schedules_file(hass)
    config = {DOMAIN: {}}

    result = await async_setup(hass, config)

    assert result is True

    state = hass.states.get("sensor.stundenplan_student_a")

    assert state is not None
    assert state.attributes["person_id"] == "student_a"

    state = hass.states.get("sensor.stundenplan_student_b")

    assert state is not None
    assert state.attributes["person_id"] == "student_b"


async def test_sensor_shows_current_lesson(
    hass: HomeAssistant,
    freezer,
) -> None:
    """Sensor shows the currently active lesson."""
    freezer.move_to(
        datetime(2026, 8, 18, 9, 10)
    )

    _prepare_schedules_file(hass)
    config = {DOMAIN: {}}

    await async_setup(hass, config)

    async_fire_time_changed(
        hass,
        datetime(2026, 8, 18, 9, 10),
    )

    await hass.async_block_till_done()

    state = hass.states.get("sensor.stundenplan_student_a")

    assert state is not None
    assert state.state == "HT"

    assert state.attributes["current_block"] == "HT"
    assert state.attributes["current_start"] == "09:10:00"
    assert state.attributes["current_end"] == "09:50:00"


async def test_sensor_shows_free_outside_lessons(
    hass: HomeAssistant,
    freezer,
) -> None:
    """Sensor shows frei when there is no current lesson."""
    freezer.move_to(
        datetime(2026, 8, 18, 7, 30)
    )

    _prepare_schedules_file(hass)
    config = {DOMAIN: {}}

    await async_setup(hass, config)

    state = hass.states.get("sensor.stundenplan_student_a")

    assert state is not None
    assert state.state == "frei"


async def test_sensor_contains_next_lesson(
    hass: HomeAssistant,
    freezer,
) -> None:
    """Sensor contains information about the next lesson."""
    freezer.move_to(
        datetime(2026, 8, 18, 7, 30)
    )

    _prepare_schedules_file(hass)
    config = {DOMAIN: {}}

    await async_setup(hass, config)

    state = hass.states.get("sensor.stundenplan_student_a")

    assert state is not None

    assert state.attributes["next_subject"] == "Subject A"
    assert state.attributes["next_block"] == "1"
    assert state.attributes["next_date"] == "2026-08-18"
    assert state.attributes["next_start"] == "07:40:00"
    assert state.attributes["next_end"] == "08:20:00"


async def test_sensor_contains_all_lessons_today_and_tomorrow(
    hass: HomeAssistant,
    freezer,
) -> None:
    """Expose complete daily schedules for dashboard summaries."""
    freezer.move_to(datetime(2026, 8, 18, 7, 30))
    _prepare_schedules_file(hass)

    await async_setup(hass, {DOMAIN: {}})

    state = hass.states.get("sensor.stundenplan_student_a")

    assert state is not None
    assert state.attributes["today_date"] == "2026-08-18"
    assert [
        (lesson["start"], lesson["end"], lesson["subject"])
        for lesson in state.attributes["today_lessons"]
    ] == [
        ("07:40", "08:20", "Subject A"),
        ("08:20", "09:00", "Subject A"),
        ("09:10", "09:50", "HT"),
        ("10:10", "10:50", "Subject E"),
        ("10:50", "11:30", "Subject E"),
        ("11:50", "12:30", "Subject F"),
        ("12:30", "13:10", "Subject L"),
        ("13:40", "14:20", "Subject I"),
        ("14:20", "15:00", "Subject I"),
    ]
    assert state.attributes["tomorrow_date"] == "2026-08-19"
    assert [
        lesson["subject"] for lesson in state.attributes["tomorrow_lessons"]
    ] == ["Subject A", "Subject A", "Subject AB", "Subject H", "Subject H", "Subject D", "Subject D"]

    
    

async def test_sensor_updates_when_lesson_changes(
    hass: HomeAssistant,
    freezer,
) -> None:
    """Sensor updates when the current lesson changes."""
    freezer.move_to(
        datetime(2026, 8, 18, 9, 5)
    )

    _prepare_schedules_file(hass)
    config = {DOMAIN: {}}

    await async_setup(hass, config)

    state = hass.states.get("sensor.stundenplan_student_a")

    assert state is not None
    assert state.state == "frei"

    freezer.move_to(
        datetime(2026, 8, 18, 9, 10)
    )

    async_fire_time_changed(
        hass,
        datetime(2026, 8, 18, 9, 10),
    )

    await hass.async_block_till_done()

    state = hass.states.get("sensor.stundenplan_student_a")

    assert state is not None
    assert state.state == "HT"



