"""GitHub Custom Component."""
import asyncio
import logging
import os
from homeassistant.core import HomeAssistant
from homeassistant import config_entries, core
from homeassistant.components import persistent_notification
from homeassistant.exceptions import ConfigEntryNotReady
from .const import DOMAIN, DEVICE_ADDR
from .battery import UPSManager

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Setup integration."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    if not os.path.exists("/dev/i2c-1"):
        raise ConfigEntryNotReady("UPS was not found")
    await add_services(hass)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "button")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )
    return True

async def add_services(hass: HomeAssistant):
    """adds report service"""
    async def restart(call):
        restart_timer = int(call.data.get("seconds", 0))
        if restart_timer == 0:
            UPSManager().bus.write_byte_data(DEVICE_ADDR, 26, 0)
            UPSManager().bus.write_byte_data(DEVICE_ADDR, 24, 0)
            return True
        await async_notification(
                hass,
                "Warning Restart",
                f"System restart in `{restart_timer}` seconds"
            )
        UPSManager().bus.write_byte_data(DEVICE_ADDR, 24, restart_timer+55)
        await asyncio.sleep(restart_timer)
        left_time = UPSManager().bus.read_byte_data(DEVICE_ADDR, 24)
        if left_time != 0:
            hass.services.call('hassio', 'host_shutdown',{})
    hass.services.async_register(DOMAIN, "restart", restart)
    return True

async def async_notification(hass, title, message, n_id=DOMAIN):
    """Show a persistent notification"""
    persistent_notification.async_create(
        hass,
        message,
        title=title,
        notification_id=n_id,
    )

async def async_unload_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Unload all config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(entry, "sensor"),
              hass.config_entries.async_forward_entry_unload(entry, "button"),
              hass.config_entries.async_forward_entry_unload(entry, "switch"),
            ]
        )
    )
    return unload_ok
