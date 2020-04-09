"""
adc_all.py - read adc on PYBStick S26 and transform the value into 10 Bits
             as Arduino (value from 0 to 1024).
			 This may help a lot in code portage.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Fiche produit:
---> https://shop.mchobby.be/fr/micropython/1830-pybstick-lite-26-micropython-et-arduino-3232100018303-garatronic.html

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  09 april 2020 - Dominique - initial code
"""

from pyb import ADC
from time import sleep

adc = ADC("S26")

def arduino_map(valeur, in_min, in_max, out_min, out_max):
	return (valeur - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
	val = adc.read()
	# degrade in 10 bits (like Arduino)
	val_10bits = arduino_map( val, 0, 4095, 0, 1024 )
	# in volts, with Arduino precision (so lower resolution)
	volt = arduino_map( val_10bits, 0, 1024, 0, 3.3 )
	print( "ADC %s : %4i, %3.2f v" %("S26", val_10bits, volt) )
	sleep( 1 )
