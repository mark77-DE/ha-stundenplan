"""Tests for the Stundenplan sensor platform."""

from datetime import datetime

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import async_fire_time_changed


from custom_components.stundenplan import async_setup
from custom_components.stundenplan.const import DOMAIN
from tests.fixtures import create_complete_new_config


async def test_sensor_created_for_each_person(
    hass: HomeAssistant,
) -> None:
    """Create one sensor for each configured person."""
    config = {
        DOMAIN: create_complete_new_config(),
    }

    result = await async_setup(hass, config)

    assert result is True

    state = hass.states.get("sensor.stundenplan_paulina")

    assert state is not None
    assert state.attributes["person_id"] == "paulina"

    state = hass.states.get("sensor.stundenplan_johanna")

    assert state is not None
    assert state.attributes["person_id"] == "johanna"


async def test_sensor_shows_current_lesson(
    hass: HomeAssistant,
    freezer,
) -> None:
    """Sensor shows the currently active lesson."""
    freezer.move_to(
        datetime(2026, 8, 18, 9, 10)
    )

    config = {
        DOMAIN: create_complete_new_config(),
    }

    await async_setup(hass, config)

    async_fire_time_changed(
        hass,
        datetime(2026, 8, 18, 9, 10),
    )

    await hass.async_block_till_done()

    state = hass.states.get("sensor.stundenplan_paulina")

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

    config = {
        DOMAIN: create_complete_new_config(),
    }

    await async_setup(hass, config)

    state = hass.states.get("sensor.stundenplan_paulina")

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

    config = {
        DOMAIN: create_complete_new_config(),
    }

    await async_setup(hass, config)

    state = hass.states.get("sensor.stundenplan_paulina")

    assert state is not None

    assert state.attributes["next_subject"] == "Mathe"
    assert state.attributes["next_block"] == "1"
    assert state.attributes["next_date"] == "2026-08-18"
    assert state.attributes["next_start"] == "07:40:00"
    assert state.attributes["next_end"] == "08:20:00"
    
    
    

async def test_sensor_updates_when_lesson_changes(
    hass: HomeAssistant,
    freezer,
) -> None:
    """Sensor updates when the current lesson changes."""
    freezer.move_to(
        datetime(2026, 8, 18, 9, 5)
    )

    config = {
        DOMAIN: create_complete_new_config(),
    }

    await async_setup(hass, config)

    state = hass.states.get("sensor.stundenplan_paulina")

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

    state = hass.states.get("sensor.stundenplan_paulina")

    assert state is not None
    assert state.state == "HT"



    