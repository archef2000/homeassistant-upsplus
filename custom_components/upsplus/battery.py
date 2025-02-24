"""All functions for reading data from the UPS"""
import smbus2
from ina219 import INA219
from .const import DEVICE_BUS, DEVICE_ADDR

class UPSManager:
    """Setup UPS for all sensors"""
    _instance = None

    def __new__(cls):
        """Only create instance if it doesn't already exist"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """initiate UPS operation"""
        self._initialize_sensors()
        #self.ina_supply = INA219(0.00725, busnum=DEVICE_BUS, address=0x40)
        #self.ina_supply.configure()
        #self.ina_battery = INA219(0.005, busnum=DEVICE_BUS, address=0x45)
        #self.ina_battery.configure()
        self.bus = smbus2.SMBus(DEVICE_BUS)
        self.sw_version = read_buff(self.bus,40,41)
        self.serial_number = ("%08X" % read_buff(self.bus,240,241,242,243)) + "-" + ("%08X" % read_buff(self.bus,244,245,246,247)) + "-" + ("%08X" % read_buff(self.bus,248,249,250,251))
        self.uid1 = "%08X" % read_buff(self.bus,0,1,2,3)
        self.uid2 = "%08X" % read_buff(self.bus,4,5,6,7)
        self.uid3 = "%08X" % read_buff(self.bus,8,9,10,11)
    
    def _initialize_sensors(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_supply = executor.submit(self._init_ina_supply)
            future_battery = executor.submit(self._init_ina_battery)
            self.ina_supply = future_supply.result()
            self.ina_battery = future_battery.result()

    def _init_ina_supply(self):
        ina = INA219(0.00725, busnum=DEVICE_BUS, address=0x40)
        ina.configure()
        return ina

    def _init_ina_battery(self):
        ina = INA219(0.005, busnum=DEVICE_BUS, address=0x45)
        ina.configure()
        return ina

def read_buff(bus, index1, *args):
    """Function to read the SMBus and add all specified indexes"""
    result = bus.read_byte_data(DEVICE_ADDR, index1)
    i = 0
    for index in args:
        i += 1
        result = result | bus.read_byte_data(DEVICE_ADDR, index) << (8 * i)
    return result
