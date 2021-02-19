""" Scan and read DS18B20 temperature from OneWire master

	See PybStick-UniPi interface @ MCHobby
	https://shop.mchobby.be/fr/nouveaute/1891-carte-interface-unipi-pro-et-lite-pour-pybstick-3232100018914.html

	See project https://github.com/mchobby/pyboard-driver/tree/master/UniPi-MicroPython-Automation

	domeu, 5 july 2020, Initial Writing (shop.mchobby.be)
"""
#from unipi import unipi
import time
from machine import I2C
from ds2482 import OneWireFacade

i2c = I2C(2)
# OneWireFacade expose a OneWire API over the DS2482 driver (1Wire Master over I2C)
oneWire = OneWireFacade( i2c )

roms = oneWire.scan()
print( "found devices:", roms )

from ds18x20 import DS18X20
ds = DS18X20( oneWire )

for i in range(10):
	print('temperatures:')
	ds.convert_temp()
	time.sleep_ms(750)
	for rom in roms:
		print( ds.read_temp(rom) )
