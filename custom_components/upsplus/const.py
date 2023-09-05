"""All constants for the integration"""
DOMAIN = "upsplus"
DEVICE_ADDR = 0x17
DEVICE_BUS = 
UPDATE_URL = "https://api.52pi.com/update"

UPS_ID = "5t89t8th-7g45-jf93-c8534c97ejf9"

BUTTONS = [
    {
        "name": "Cancel shutdown",
        "entry_id": "cancel_shutdown",
        "address": 24,
        "value": 0
    },
    {
        "name": "Cancel restart",
        "entry_id": "cancel_restart",
        "address": 26,
        "value": 0
    },
    {
        "name": "Restore factory settings",
        "entry_id": "restore_factory_settings",
        "address": 27,
        "value": 1
    },
    {
        "name": "Enter OTA",
        "entry_id": "enter_ota",
        "address": 50,
        "value": 127
    },
]

SENSOR_LIST = {
    "supply_voltage": {
        "subfix": "voltage",
        "name": "UPS supply voltage",
        "unit_of_measurement": "V",
        "multiplier": 1,
        "class": "voltage",
        "prefix": "supply"
    },
    "supply_current": {
        "subfix": "current",
        "name": "UPS supply current",
        "unit_of_measurement": "A",
        "class": "current",
        "prefix": "supply"
    },
    "supply_power": {
        "subfix": "power",
        "name": "UPS supply power",
        "unit_of_measurement": "W",
        "class": "power",
        "prefix": "supply"
    },
    "battery_voltage": {
        "subfix": "voltage",
        "name": "UPS battery voltage",
        "unit_of_measurement": "V",
        "multiplier": 1,
        "class": "voltage",
        "prefix": "battery"
    },
    "battery_current": {
        "subfix": "current",
        "name": "UPS battery current input",
        "unit_of_measurement": "A",
        "multiplier": -0.001,
        "class": "current",
        "prefix": "battery"
    },
    "battery_power": {
        "subfix": "power",
        "name": "UPS battery power input",
        "unit_of_measurement": "W",
        "class": "power",
        "prefix": "battery"
    }
}

SENSOR_LIST_SMBUS = {
    "processor_voltage": {
        "name": "UPS processor voltage",
        "unit_of_measurement": "V",
        "class": "voltage",
        "index": [1,2]
    },
    "pi_report_voltage": {
        "name": "UPS pi report voltage",
        "unit_of_measurement": "V",
        "class": "voltage",
        "index": [3,4]
    },
    "input_report_voltage": {
        "name": "UPS input report voltage",
        "unit_of_measurement": "V",
        "class": "voltage",
        "index": [5,6]
    },
    "type_c_voltage": {
        "name": "UPS Type C voltage",
        "unit_of_measurement": "V",
        "class": "voltage",
        "index": [7,8]
    },
    "micro_usb_voltage": {
        "name": "UPS Micro USB voltage",
        "unit_of_measurement": "V",
        "class": "voltage",
        "index": [9,10]
    },
    "battery_temperature": {
        "name": "UPS battery temperature",
        "unit_of_measurement": "°C",
        "class": "temperature",
        "index": [11,12]
    },
    "battery_full_voltage": {
        "name": "UPS battery full voltage",
        "unit_of_measurement": "V",
        "class": "voltage",
        "index": [13,14]
    },
    "battery_empty_voltage": {
        "name": "UPS battery empty voltage",
        "unit_of_measurement": "V",
        "class": "voltage",
        "index": [15,16]
    },
    "battery_protection_voltage": {
        "name": "UPS battery protection voltage",
        "unit_of_measurement": "V",
        "class": "voltage",
        "index": [17,18]
    },
    "battery_capacity": {
        "name": "UPS battery capacity",
        "unit_of_measurement": "%",
        "class": "battery",
        "index": [19,20]
    },
    "sampling_period": {
        "name": "UPS sampling period",
        "unit_of_measurement": "min",
        "class": "duration",
        "index": [21,22]
    },
    "shutdown_timer": {
        "name": "UPS shutdown countdown",
        "unit_of_measurement": "s",
        "class": "duration",
        "index": [24]
    },
    "restart_timer": {
        "name": "UPS restart countdown",
        "unit_of_measurement": "s",
        "class": "duration",
        "index": [26]
    },
    "all_running_time": {
        "name": "UPS accumulated running time",
        "unit_of_measurement": "s",
        "class": "duration",
        "index": [28,29,30,31]
    },
    "all_charged_time": {
        "name": "UPS accumulated charged time",
        "unit_of_measurement": "s",
        "class": "duration",
        "index": [32,33,34,35]
    },
    "running_time": {
        "name": "UPS running time",
        "unit_of_measurement": "s",
        "class": "duration",
        "index": [36,37,38,39]
    }
}
