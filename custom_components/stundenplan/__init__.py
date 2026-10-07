"""Home Assistant integration for school schedules."""

from typing import Any

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_component import EntityComponent

from .config import load_schedule_manager_from_yaml
from .const import DOMAIN
from .sensor import StundenplanSensor


async def async_setup(
    hass: HomeAssistant,
    config: dict[str, Any],
) -> bool:
    """Set up the Stundenplan integration."""
    if DOMAIN not in config:
        return True

    manager = load_schedule_manager_from_yaml(
        hass.config.path("schedules.yaml")
    )
    hass.data[DOMAIN] = manager

    component = EntityComponent(
        None,
        SENSOR_DOMAIN,
        hass,
    )

    hass.data[f"{DOMAIN}_component"] = component

    sensors = [
        StundenplanSensor(person)
        for person in manager.all_persons()
    ]

    await component.async_add_entities(sensors)

    return True
