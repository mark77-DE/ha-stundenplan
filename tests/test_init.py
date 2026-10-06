"""Tests for the Stundenplan Home Assistant integration."""


from homeassistant.core import HomeAssistant

from custom_components.stundenplan import async_setup
from custom_components.stundenplan.const import DOMAIN
from tests.fixtures import create_complete_new_config



async def test_async_setup_without_configuration(
    hass: HomeAssistant,
) -> None:
    """Integration setup succeeds without configuration."""
    result = await async_setup(hass, {})

    assert result is True
    assert DOMAIN not in hass.data



async def test_async_setup_with_configuration(
    hass: HomeAssistant,
) -> None:
    """Integration setup creates a schedule manager from configuration."""
    config = {
        DOMAIN: create_complete_new_config(),
    }

    result = await async_setup(hass, config)

    assert result is True
    assert DOMAIN in hass.data

    manager = hass.data[DOMAIN]

    assert manager.has_person("paulina")
    assert manager.has_person("johanna")
