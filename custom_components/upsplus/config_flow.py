"""All functions for the config flow"""
import logging
from typing import Any, Dict, Optional
import os
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .battery import UPSManager, read_buff
from .const import DOMAIN,DEVICE_ADDR

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = {
    vol.Required("enable_automatic_shutdown", default=True): bool,
    vol.Required("automatic_shutdown_voltage", default=3700): int,
    vol.Optional("advanced", default=False): bool,
}

class CustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Custom config flow."""

    data: Optional[Dict[str, Any]]
    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if not os.path.exists("/dev/i2c-1"):
            return self.async_abort(reason="no_ups")
        if user_input is not None:
            self.data = {
                    "enable_automatic_shutdown": user_input.get("enable_automatic_shutdown",True),
                    "automatic_shutdown_voltage": user_input.get("automatic_shutdown_voltage",3700)
                }
            if user_input.get("advanced", False):
                return await self.async_step_advanced()
            return self.async_create_entry(title="UPS I2C", data={"upsplus":self.data})
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(CONFIG_SCHEMA), errors=errors
        )

    async def async_step_advanced(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        bus = UPSManager().bus
        if user_input is not None:
            error = config_ups(bus, user_input)
            if not error:
                return self.async_create_entry(title="UPS I2C", data={"upsplus":self.data})
            else:
                errors["base"] = error
        data_schema = {
            vol.Required("sampling_time", default=read_buff(bus,21,22)): int,
            vol.Required("protection_voltage", default=read_buff(bus,17,18)): int
        }
        return self.async_show_form(
            step_id="advanced", data_schema=vol.Schema(data_schema), errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handles options flow for the component."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Manage the options for the custom component."""
        errors: Dict[str, str] = {}
        bus = UPSManager().bus
        if user_input is not None:
            error = config_ups(bus, user_input)
            if not error:
                data = {
                    "enable_automatic_shutdown": user_input.get("enable_automatic_shutdown",True),
                    "automatic_shutdown_voltage": user_input.get("automatic_shutdown_voltage",3700)
                }
                return self.async_create_entry(title="UPS I2C", data={"upsplus":data})
            else:
                errors["base"] = error
        data = self.config_entry.options.get("upsplus")
        if not data:
            entries = self.hass.config_entries.async_entries()
            entry_data = [entry.data for entry in entries if entry.data.get("upsplus",False)]
            data = entry_data[0].get("upsplus")
        curr_enable_automatic_shutdown = data.get("enable_automatic_shutdown",True)
        curr_automatic_shutdown = data.get("automatic_shutdown_voltage",3700)
        data_schema = {
            vol.Required("enable_automatic_shutdown", default=curr_enable_automatic_shutdown): bool,
            vol.Required("automatic_shutdown_voltage", default=curr_automatic_shutdown): int,
            vol.Required("sampling_time", default=read_buff(bus,21,22)): int,
            vol.Required("protection_voltage", default=read_buff(bus,17,18)): int
        }
        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(data_schema), errors=errors
        )

def config_ups(bus, user_input: Dict[str, Any] = None) -> str:
    """Set current options from userinput"""
    sampling_time = user_input.get("sampling_time",2)
    if 1 <= sampling_time <= 10:
        bus.write_byte_data(DEVICE_ADDR, 21, sampling_time & 0xFF)
        bus.write_byte_data(DEVICE_ADDR, 22, (sampling_time >> 8)& 0xFF)
    else:
        return "invalid_sampling_time"
    protection_voltage = user_input.get("protection_voltage",3700)
    if 3700 <= protection_voltage <= 4100:
        bus.write_byte_data(DEVICE_ADDR, 17, protection_voltage & 0xFF)
        bus.write_byte_data(DEVICE_ADDR, 18, (protection_voltage >> 8)& 0xFF)
    else:
        return "invalid_protection_voltage"
    return ""
