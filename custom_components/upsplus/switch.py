from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo
from .battery import UPSManager
from .device import UPSDevice
from .const import DOMAIN, SENSOR_LIST, DEVICE_ADDR, SENSOR_LIST_SMBUS
from datetime import timedelta
import logging
import asyncio
_LOGGER = logging.getLogger(__name__)

from .device import UPSDevice

class PowerON(UPSDevice, SwitchEntity):
    def __init__(self, config_entry_id) -> None:
        self._bus = UPSManager().bus
        self._entity_id = "turn_on_after_power_on"
        self._attr_name = "UPS turn on after power on"
        self._attr_unique_id = f"{DOMAIN}_{config_entry_id}_{self._entity_id}"
        self._attr_device_info = DeviceInfo(identifiers={DOMAIN, self._attr_unique_id})
        self._state = None

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs) -> None:
        self._bus.write_byte_data(DEVICE_ADDR, 25, 1)
        self._state = True

    async def async_turn_off(self, **kwargs) -> None:
        self._bus.write_byte_data(DEVICE_ADDR, 25, 0)
        self._state = False

    async def async_update(self) -> None:
        self._state = self._bus.read_byte_data(DEVICE_ADDR, 25) == 1

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([PowerON(config.entry_id)], update_before_add=True)

async def async_setup_entry(hass, config, async_add_entities):
    async_add_entities([PowerON(config.entry_id)], update_before_add=True)

SCAN_INTERVAL = timedelta(seconds=20)
