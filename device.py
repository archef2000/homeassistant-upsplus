from homeassistant.helpers.entity import Entity
from .const import DOMAIN, UPS_ID
from .battery import UPSManager

def device_info():
    return {
        "identifiers": {(DOMAIN, UPS_ID)},
        "name": "UPS",
        "manufacturer": "52PI",
        "model": "52Pi 18650 UPS",
        "sw_version": UPSManager().sw_version,
        #"entry_type": DeviceEntryType.SERVICE,
    }

class UPSDevice(Entity):
    """Base system entity."""
    def __init__(self) -> None:
        """Initialize."""

    #_attr_icon = "hacs:hacs"
    @property
    def device_info(self) -> dict[str, any]:
        """Return device information."""
        return device_info()