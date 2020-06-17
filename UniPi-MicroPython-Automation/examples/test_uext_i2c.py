""" Test the I2C port on UEXT connector

	use the Olimex MOD-TC-MK2-31855 sensor from Olimex - https://shop.mchobby.be/fr/uext/1624-mod-tc-mk2-31855-interface-thermocouple-type-k-avec-max31855-bus-i2c-gpio-3232100016248-olimex.html
	See the modtc-mk2 micropython driver - https://github.com/mchobby/esp8266-upy/tree/master/modtc-mk2

	See PybStick-UniPi interface @ MCHobby
	https://shop.mchobby.be/fr/nouveaute/1891-carte-interface-unipi-pro-et-lite-pour-pybstick-3232100018914.html

	See project https://github.com/mchobby/pyboard-driver/tree/master/UniPi-MicroPython-Automation

	domeu, 11 june 2020, Initial Writing (shop.mchobby.be)
	----------------------------------------------------------------------------

	MCHobby invest time and ressource in developping project and libraries.
	It is a long and tedious work developed with Open-Source mind and freely available.
	IF you like our work THEN help us by buying your product at MCHobby (shop.mchobby.be).

	----------------------------------------------------------------------------
	Copyright (C) 2020  - Meurisse D. (shop.mchobby.be)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
from unipi import unipi
from modtc_mk2 import MODTC_MK2

# Obtain the instance of machine.I2C bus on the UEXT connector
i2c = unipi.uext.i2c( freq=10000 ) # Other parameters can be provided when creating I2C
mk2 = MODTC_MK2( i2c )

temp_in, temp_ext = mk2.temperatures
print( "Internal Temp = %s" % temp_in )
print( "External Temp = %s" % temp_ext )
