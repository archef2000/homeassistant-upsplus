"""GitHub Custom Component."""
import asyncio
import logging
import os
import json
import voluptuous as vol
from homeassistant import config_entries, core
from homeassistant.core import HomeAssistant, ServiceResponse, ServiceCall, SupportsResponse
from homeassistant.components import persistent_notification
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client
from .const import DOMAIN, DEVICE_ADDR, UPDATE_URL
from .battery import UPSManager

_LOGGER = logging.getLogger(__name__)

UPSPLUS_UPDATE_SCHEMA = vol.Schema({
    vol.Required("ota_mode"): bool,
    vol.Required("shutdown"): bool,
    vol.Required("cut_power"): bool,
    vol.Required("remove_batteries"): bool,
    vol.Required("insert_batteries"): bool,
    vol.Required("connect_power"): bool,
    vol.Required("power_up_system"): bool,
    vol.Optional("version"): int,
})

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
    await hass.config_entries.async_forward_entry_setup(entry, ["sensor","button","switch"])
    return True

async def add_services(hass: HomeAssistant):
    """adds report service"""
    async def restart(call: ServiceCall):
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

    async def update(call: ServiceCall) -> ServiceResponse:
        preperation = all(call.data.values())
        return_json = { "success": False }
        if not preperation:
            return_json["error"] = "Please finish the preperation"
            return return_json
        client_session = aiohttp_client.async_get_clientsession(hass)
        ups_manager = UPSManager()
        request_data={"UID0": ups_manager.uid1, "UID1": ups_manager.uid2, "UID2": ups_manager.uid3}
        if call.data.get("version"):
            request_data["ver"] = call.data["version"]
        response = await client_session.post(UPDATE_URL, data=request_data)
        json_response =  await response.json()
        if json_response['code'] != 0:
            return_json["error"] = json_response['reason']
            return_json["step"] = "Getting download url"
            return return_json
        download_response = await client_session.get(json_response["url"])
        if download_response.status == 404:
            return_json["error"] = "Version not found"
            return_json["step"] = "Downloading firmware"
            return return_json
        firmware_data = download_response.content
        bus = ups_manager.bus
        while True:
            data = await firmware_data.read(16)
            for i in range(len(list(data))):
                bus.write_byte_data(0x18, i + 1, data[i])
            bus.write_byte_data(0x18, 50, 250)
            if len(list(data)) == 0:
                bus.write_byte_data(0X18, 50, 0)
                break
        return_json["success"] = True
        return_json["step"] = "Flashed successful, disconnect all power/batteries and reinstall to use new firmware"
        return return_json
    hass.services.async_register(
        DOMAIN,
        "update",
        update,
        supports_response=SupportsResponse.ONLY,
        )
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
