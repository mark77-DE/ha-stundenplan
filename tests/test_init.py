"""Tests for the Stundenplan Home Assistant integration."""

from pathlib import Path

from homeassistant.core import HomeAssistant

from custom_components.stundenplan import async_setup
from custom_components.stundenplan.const import DOMAIN

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
    """Integration setup loads the local schedules.yaml file."""
    source = Path(__file__).parent / "data" / "schedules.yaml"
    target = Path(hass.config.path("schedules.yaml"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        source.read_text(encoding="utf-8"), encoding="utf-8"
    )
    config = {DOMAIN: {}}

    result = await async_setup(hass, config)

    assert result is True
    assert DOMAIN in hass.data

    manager = hass.data[DOMAIN]

    assert manager.has_person("paulina")
    assert manager.has_person("johanna")
