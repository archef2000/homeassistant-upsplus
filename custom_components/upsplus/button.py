"""Button entites"""
from homeassistant.components.button import ButtonEntity
from .battery import UPSManager
from .device import UPSDevice
from .const import DOMAIN, DEVICE_ADDR, BUTTONS

class BusButton(UPSDevice, ButtonEntity):
    """Create the Button structure for all entities"""
    def __init__(self, hass, button_entity, config_entry_id) -> None:
        """Read all data from button_entity to get config"""
        self._hass = hass
        self._bus = UPSManager().bus
        self._entity_id = button_entity.get("entry_id")
        self._attr_name = button_entity.get("name", self._entity_id)
        self._address = button_entity.get("address", 0)
        self._value = button_entity.get("value", 0)
        self._attr_unique_id = f"{DOMAIN}_{config_entry_id}_{self._entity_id}"

    async def async_press(self) -> None:
        """Handle the button press."""
        self._bus.write_byte_data(DEVICE_ADDR, self._address, self._value)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup all buttons"""
    sensors = [BusButton(hass, button_entity, config.entry_id) for button_entity in BUTTONS]
    async_add_entities(sensors, update_before_add=True)

async def async_setup_entry(hass, config, async_add_entities):
    """Setup all buttons"""
    sensors = [BusButton(hass, button_entity, config.entry_id) for button_entity in BUTTONS]
    async_add_entities(sensors, update_before_add=True)
