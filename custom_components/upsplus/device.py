"""The UPS Device for HA UI"""
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, UPS_ID
from .battery import UPSManager

def device_info():
    """Generate all device information"""
    return {
        "identifiers": {(DOMAIN, UPS_ID)},
        "name": "UPS",
        "manufacturer": "52PI",
        "model": "52Pi 18650 UPS",
        "sw_version": UPSManager().sw_version,
    }

class UPSDevice(Entity):
    """Base system entity."""
    def __init__(self) -> None:
        """Initialize."""

    @property
    def device_info(self) -> dict[str, any]:
        """Return device information."""
        return device_info()
