"""Switch for UPS power on"""
from datetime import timedelta
import logging
from homeassistant.components.switch import SwitchEntity
from .battery import UPSManager
from .device import UPSDevice
from .const import DOMAIN, DEVICE_ADDR

_LOGGER = logging.getLogger(__name__)

class PowerON(UPSDevice, SwitchEntity):
    """Switch class"""
    def __init__(self, config_entry_id) -> None:
        self._bus = UPSManager().bus
        self._entity_id = "turn_on_after_power_on"
        self._attr_name = "UPS turn on after power on"
        self._attr_unique_id = f"{DOMAIN}_{config_entry_id}_{self._entity_id}"
        self._state = None

    @property
    def is_on(self):
        """Return state of the switch."""
        return self._state

    async def async_turn_on(self, **kwargs) -> None:
        """Write state to UPS"""
        self._bus.write_byte_data(DEVICE_ADDR, 25, 1)
        self._state = True

    async def async_turn_off(self, **kwargs) -> None:
        """Write state to UPS"""
        self._bus.write_byte_data(DEVICE_ADDR, 25, 0)
        self._state = False

    async def async_update(self) -> None:
        """Update state from UPS"""
        self._state = self._bus.read_byte_data(DEVICE_ADDR, 25) == 1

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the switch"""
    async_add_entities([PowerON(config.entry_id)], update_before_add=True)

async def async_setup_entry(hass, config, async_add_entities):
    """Setup the switch"""
    async_add_entities([PowerON(config.entry_id)], update_before_add=True)

SCAN_INTERVAL = timedelta(seconds=20)
