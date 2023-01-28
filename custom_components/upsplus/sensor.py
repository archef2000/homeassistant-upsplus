"""GitHub sensor platform."""
from __future__ import annotations
from datetime import timedelta
import json
import logging
from .const import DOMAIN, SENSOR_LIST, DEVICE_ADDR, SENSOR_LIST_SMBUS
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import Entity, DeviceInfo, EntityDescription
from homeassistant.components.switch import SwitchEntity
from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from .battery import UPSManager, read_buff
from .device import UPSDevice
import asyncio

_LOGGER = logging.getLogger(__name__)

class SensorJSON(UPSDevice, Entity):
    def __init__(self, hass, json_entity, config):
        self._hass = hass
        self._entity = json_entity
        self._attr_name = json_entity["name"]
        self._entity_subfix = json_entity.get("subfix")
        self._entity_prefix = json_entity.get("prefix")
        self._multiplier = json_entity.get("multiplier", 0.001)
        self._variable_manager = UPSManager()
        self._state = None
        self._config = config
        self._attr_unit_of_measurement = json_entity.get("unit_of_measurement","")
        self._attr_unique_id = f"{DOMAIN}_{config.entry_id}_{self._entity_prefix}_{self._entity_subfix}"
        self._attr_device_class = json_entity.get("class",self._entity_subfix)
        self._funct_name = getattr(
                getattr(
                        self._variable_manager,
                        f"ina_{json_entity.get('prefix', 'battery')}"
                    ),
                json_entity.get("subfix", "voltage")
            )
        self._attr_device_info = DeviceInfo(identifiers={DOMAIN, self._attr_unique_id})

    async def async_update(self):
        self._state = "{:.2f}".format(self._funct_name()*self._multiplier)

    @property
    def state(self):
        return self._state

class SensorSMB(UPSDevice, SensorEntity):
    def __init__(self, hass, entity_id, json_entity, config):
        self._entity = json_entity
        self._config_id = config.entry_id
        self._name = json_entity["name"]
        self._attr_name = self._name
        self._attr_device_class = json_entity.get("class")
        self._bus = UPSManager().bus
        self._attr_unique_id = f"{DOMAIN}_{config.entry_id}_{entity_id}"
        self._state = None
        self._attr_device_info = DeviceInfo(identifiers={DOMAIN, self._attr_unique_id})

    @property
    def unit_of_measurement(self):
        return self._entity.get("unit_of_measurement","")

    async def async_update(self):
        state = read_buff(self._bus, *self._entity.get("index"))
        if self._entity.get("unit_of_measurement","") == "V":
            self._state = "{:.2f}".format(state/1000)
        else:
            self._state = "{:.2f}".format(state)

    @property
    def state(self):
        return self._state

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensors = []
    for _ , sensor_entity in SENSOR_LIST.items():
        sensors.append(SensorJSON(hass, sensor_entity, config))
    for entity_id , sensor_entity in SENSOR_LIST_SMBUS.items():
        sensors.append(SensorSMB(hass, entity_id, sensor_entity, config))
    async_add_entities(sensors, update_before_add=True)

async def async_setup_entry(hass, config, async_add_entities):
    sensors = []
    for _ , sensor_entity in SENSOR_LIST.items():
        sensors.append(SensorJSON(hass, sensor_entity, config))
    for entity_id , sensor_entity in SENSOR_LIST_SMBUS.items():
        sensors.append(SensorSMB(hass, entity_id, sensor_entity, config))
    async_add_entities(sensors, update_before_add=True)

SCAN_INTERVAL = timedelta(seconds=20)
