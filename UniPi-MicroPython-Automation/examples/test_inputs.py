""" Test the INPUTs of the UniPi

	See PybStick-UniPi interface @ MCHobby
	https://shop.mchobby.be/fr/nouveaute/1891-carte-interface-unipi-pro-et-lite-pour-pybstick-3232100018914.html

	See project https://github.com/mchobby/pyboard-driver/tree/master/UniPi-MicroPython-Automation

	domeu, 06 june 2020, Initial Writing (shop.mchobby.be)
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

# Collect all inputs state
print( "--- collect entries ---")
unipi.inputs.read()

# get the state of Input 1 & input 3
print( "--- Read inputs ---")
print( "IN1 = %s" % unipi.inputs[1] )
print( "IN3 = %s" % unipi.inputs[3] )

# Display state of all inputs
print( "--- Iterate all inputs ---" )
unipi.inputs.read()
for i in range(1, 14): # 1 to 13
	print( "IN%s = %s" % (i, unipi.inputs[i]) )

# Value of inputs as dictionnary (displays last known state)
print( "--- Input values as dict ---" )
print( unipi.inputs.read_all() )

# Same as previous but force the inputs reads to refresh the state
print( "--- Input values as dict (read) ---")
print( unipi.inputs.read_all( read=True ) )
