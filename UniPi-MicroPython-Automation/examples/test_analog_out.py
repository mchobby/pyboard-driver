""" Test the Analog Output of the UniPi

	see project https://github.com/mchobby/pyboard-driver/tree/master/UniPi-MicroPython-Automation

	See PybStick-UniPi interface @ MCHobby
	https://shop.mchobby.be/fr/nouveaute/1891-carte-interface-unipi-pro-et-lite-pour-pybstick-3232100018914.html

	See project https://github.com/mchobby/pyboard-driver/tree/master/UniPi-MicroPython-Automation

	domeu, 08 june 2020, Initial Writing (shop.mchobby.be)
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

# AOUT (AO): analog output is a percentage of the AOUT_VOLTAGE (AOV) provided
# To the UniPi
print( "--- Set voltage to 33% of Max AO ---")
unipi.analog_out =33 # 33%
